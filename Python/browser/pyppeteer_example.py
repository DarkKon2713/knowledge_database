# =============================================================================
# Manipulação de navegador com Pyppeteer
# =============================================================================
# Pyppeteer é um port Python do Puppeteer (Node.js) — controla o Chrome
# via DevTools Protocol. Usa async/await por padrão.
#
# Instalação:
#   pip install pyppeteer
#   (o Chromium é baixado automaticamente na primeira execução)
# =============================================================================

import asyncio
from pyppeteer import launch
import time


# -----------------------------------------------------------------------------
# Abrir página e capturar informações
# -----------------------------------------------------------------------------

async def capturar_pagina(url: str):
    """Abre uma URL e captura headers, HTML e cookies."""

    browser = await launch(headless=True, args=["--no-sandbox"])
    page    = await browser.newPage()

    # Intercepta responses para capturar headers HTTP
    headers_resposta = {}

    async def capturar_headers(response):
        if response.url == url:
            headers_resposta.update(response.headers)

    page.on("response", lambda res: asyncio.ensure_future(capturar_headers(res)))

    await page.goto(url, {"waitUntil": "domcontentloaded"})

    print(f"URL atual : {page.url}")
    titulo = await page.title()
    print(f"Título    : {titulo}")

    # HTML completo
    html = await page.content()
    print(f"HTML (primeiros 200 chars): {html[:200]}")

    # Headers da resposta
    print(f"\nHeaders da resposta:")
    for chave, valor in headers_resposta.items():
        print(f"  {chave}: {valor}")

    # Cookies
    cookies = await page.cookies()
    print(f"\nCookies ({len(cookies)} encontrados):")
    for cookie in cookies:
        print(f"  {cookie['name']} = {cookie['value']}")

    await browser.close()


# -----------------------------------------------------------------------------
# Navegar por uma lista de páginas
# -----------------------------------------------------------------------------

async def navegar_lista(urls: list[str], espera: float = 1.5):
    """
    Abre cada URL da lista em sequência, reutilizando o mesmo browser.
    """
    browser     = await launch(headless=True, args=["--no-sandbox"])
    page        = await browser.newPage()
    resultados  = []

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Acessando: {url}")

        try:
            await page.goto(url, {"waitUntil": "domcontentloaded", "timeout": 10000})

            titulo  = await page.title()
            html    = await page.content()
            cookies = await page.cookies()

            resultados.append({
                "url":     page.url,
                "titulo":  titulo,
                "html":    html[:500],
                "cookies": cookies,
            })

            await asyncio.sleep(espera)

        except Exception as e:
            print(f"  Erro em {url}: {e}")
            resultados.append({"url": url, "erro": str(e)})

    await browser.close()
    return resultados


# -----------------------------------------------------------------------------
# Executar JavaScript na página
# -----------------------------------------------------------------------------

async def capturar_com_js(url: str):
    """
    Executa JavaScript diretamente no contexto da página.
    evaluate() é o equivalente ao execute_script() do Selenium.
    """
    browser = await launch(headless=True, args=["--no-sandbox"])
    page    = await browser.newPage()

    await page.goto(url, {"waitUntil": "domcontentloaded"})

    titulo     = await page.evaluate("document.title")
    user_agent = await page.evaluate("navigator.userAgent")
    cookies_js = await page.evaluate("document.cookie")

    print(f"Título     : {titulo}")
    print(f"User-Agent : {user_agent}")
    print(f"Cookies JS : {cookies_js}")

    await browser.close()


# -----------------------------------------------------------------------------
# Exemplo de uso
# -----------------------------------------------------------------------------

# Pyppeteer é async — use asyncio.run() para executar
if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://httpbin.org/cookies",
    ]

    asyncio.run(navegar_lista(urls))