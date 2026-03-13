# =============================================================================
# Manipulação de navegador com Playwright
# =============================================================================
# Playwright é a alternativa moderna ao Selenium — mais rápido, mais estável
# e com suporte nativo a interceptação de requests e responses.
#
# Instalação:
#   pip install playwright
#   playwright install chromium
# =============================================================================

from playwright.sync_api import sync_playwright, Page, Response
import time


# -----------------------------------------------------------------------------
# Abrir página e capturar informações
# -----------------------------------------------------------------------------

def capturar_pagina(url: str):
    """Abre uma URL e captura headers, HTML e cookies."""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page    = context.new_page()

        # Intercepta a resposta da página principal para capturar headers HTTP
        headers_resposta = {}

        def capturar_headers(response: Response):
            if response.url == url:
                headers_resposta.update(dict(response.headers))

        page.on("response", capturar_headers)

        page.goto(url, wait_until="domcontentloaded")

        print(f"URL atual : {page.url}")
        print(f"Título    : {page.title()}")

        # HTML completo
        html = page.content()
        print(f"HTML (primeiros 200 chars): {html[:200]}")

        # Headers da resposta HTTP — exclusivo do Playwright
        print(f"\nHeaders da resposta:")
        for chave, valor in headers_resposta.items():
            print(f"  {chave}: {valor}")

        # Cookies
        cookies = context.cookies()
        print(f"\nCookies ({len(cookies)} encontrados):")
        for cookie in cookies:
            print(f"  {cookie['name']} = {cookie['value']}")

        browser.close()


# -----------------------------------------------------------------------------
# Navegar por uma lista de páginas
# -----------------------------------------------------------------------------

def navegar_lista(urls: list[str], espera: float = 1.5):
    """
    Abre cada URL da lista em sequência, reutilizando o mesmo contexto.
    Mantém cookies e sessão entre as páginas.
    """
    resultados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page    = context.new_page()

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Acessando: {url}")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)

                resultados.append({
                    "url":     page.url,
                    "titulo":  page.title(),
                    "html":    page.content()[:500],
                    "cookies": context.cookies(),
                })

                time.sleep(espera)

            except Exception as e:
                print(f"  Erro em {url}: {e}")
                resultados.append({"url": url, "erro": str(e)})

        browser.close()

    return resultados


# -----------------------------------------------------------------------------
# Interceptar requests e responses — exclusivo do Playwright
# -----------------------------------------------------------------------------

def interceptar_requests(url: str):
    """
    Captura todos os requests e responses feitos pela página —
    incluindo chamadas XHR/fetch para APIs internas.
    Útil para mapear quais endpoints uma página consome.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_page()

        page.on("request",  lambda req:  print(f"→ {req.method} {req.url}"))
        page.on("response", lambda res:  print(f"← {res.status} {res.url}"))

        page.goto(url, wait_until="networkidle")
        browser.close()


# -----------------------------------------------------------------------------
# Exemplo de uso
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://httpbin.org/cookies",
    ]

    resultados = navegar_lista(urls)
    for r in resultados:
        print(r.get("titulo", r.get("erro")))