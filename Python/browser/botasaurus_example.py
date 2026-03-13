# =============================================================================
# Manipulação de navegador com Botasaurus
# =============================================================================
# Botasaurus é um framework de scraping construído sobre Selenium.
# Foco em simplicidade, bypass de bot detection e paralelismo fácil.
#
# Instalação:
#   pip install botasaurus
# =============================================================================

from botasaurus.browser import browser, Driver
from botasaurus.request import request, HttpRequest
import time


# -----------------------------------------------------------------------------
# Abrir página e capturar informações — @browser decorator
# -----------------------------------------------------------------------------

@browser(headless=True)
def capturar_pagina(driver: Driver, url: str):
    """
    O decorator @browser cria e gerencia o driver automaticamente.
    Botasaurus já aplica stealth e anti-detecção por padrão.
    """
    driver.get(url)
    driver.wait_for_element("body")

    print(f"URL atual : {driver.current_url}")
    print(f"Título    : {driver.title}")

    # HTML completo
    html = driver.page_html
    print(f"HTML (primeiros 200 chars): {html[:200]}")

    # Cookies — retorna lista de dicts
    cookies = driver.get_cookies()
    print(f"\nCookies ({len(cookies)} encontrados):")
    for cookie in cookies:
        print(f"  {cookie['name']} = {cookie['value']}")

    # Botasaurus não expõe headers HTTP diretamente via @browser —
    # use @request (abaixo) para capturar headers de resposta.

    return {
        "url":     driver.current_url,
        "titulo":  driver.title,
        "html":    html[:500],
        "cookies": cookies,
    }


# -----------------------------------------------------------------------------
# Capturar headers com @request — mais leve que abrir o browser
# -----------------------------------------------------------------------------

@request(headless=True)
def capturar_headers(request: HttpRequest, url: str):
    """
    @request usa um browser leve para obter cookies/headers
    e depois faz as requisições HTTP diretamente — mais rápido que @browser.
    """
    response = request.get(url)

    print(f"Status  : {response.status_code}")
    print(f"Headers :")
    for chave, valor in response.headers.items():
        print(f"  {chave}: {valor}")

    return {
        "status":  response.status_code,
        "headers": dict(response.headers),
        "html":    response.text[:500],
    }


# -----------------------------------------------------------------------------
# Navegar por uma lista de páginas
# -----------------------------------------------------------------------------

@browser(headless=True)
def navegar_lista(driver: Driver, urls: list[str]):
    """
    Recebe a lista inteira — Botasaurus passa como primeiro argumento
    quando você passa uma lista para a função decorada.
    """
    resultados = []

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Acessando: {url}")

        try:
            driver.get(url)
            driver.wait_for_element("body")

            resultados.append({
                "url":     driver.current_url,
                "titulo":  driver.title,
                "html":    driver.page_html[:500],
                "cookies": driver.get_cookies(),
            })

            time.sleep(1.5)

        except Exception as e:
            print(f"  Erro em {url}: {e}")
            resultados.append({"url": url, "erro": str(e)})

    return resultados


# -----------------------------------------------------------------------------
# Paralelismo — exclusivo do Botasaurus
# -----------------------------------------------------------------------------

@browser(headless=True, parallel=3)     # abre 3 browsers ao mesmo tempo
def capturar_em_paralelo(driver: Driver, url: str):
    """
    Quando você passa uma lista de URLs e parallel=N,
    Botasaurus distribui automaticamente entre N browsers.
    """
    driver.get(url)
    driver.wait_for_element("body")

    return {
        "url":    driver.current_url,
        "titulo": driver.title,
    }


# -----------------------------------------------------------------------------
# Exemplo de uso
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://httpbin.org/cookies",
    ]

    # Navegar em sequência
    resultados = navegar_lista(urls)
    for r in resultados:
        print(r.get("titulo", r.get("erro")))

    # Capturar headers via @request
    info = capturar_headers("https://httpbin.org/headers")
    print(info["headers"])