# =============================================================================
# Manipulação de navegador com Selenium
# =============================================================================
# Selenium é a biblioteca mais antiga e conhecida para automação de navegadores.
# Funciona com Chrome, Firefox, Edge e Safari via WebDriver.
#
# Instalação:
#   pip install selenium webdriver-manager
# =============================================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


# -----------------------------------------------------------------------------
# Configuração do driver
# -----------------------------------------------------------------------------

def criar_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Cria e retorna uma instância do Chrome WebDriver.

    headless=True  — roda sem abrir janela (bom para produção)
    headless=False — abre o navegador visível (bom para debug)
    """
    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # webdriver-manager baixa e gerencia o chromedriver automaticamente
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


# -----------------------------------------------------------------------------
# Abrir página e capturar informações
# -----------------------------------------------------------------------------

def capturar_pagina(url: str):
    """Abre uma URL e captura headers, HTML e cookies."""
    driver = criar_driver(headless=True)

    try:
        driver.get(url)

        # Aguarda a página carregar completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print(f"URL atual : {driver.current_url}")
        print(f"Título    : {driver.title}")

        # HTML completo da página
        html = driver.page_source
        print(f"HTML (primeiros 200 chars): {html[:200]}")

        # Cookies — retorna lista de dicts
        cookies = driver.get_cookies()
        print(f"\nCookies ({len(cookies)} encontrados):")
        for cookie in cookies:
            print(f"  {cookie['name']} = {cookie['value']}")

        # Selenium não expõe headers de resposta diretamente —
        # use requests ou curl_cffi se precisar dos headers HTTP.
        # Com Selenium você acessa o DOM, não o protocolo HTTP.

    finally:
        driver.quit()   # sempre fechar o driver


# -----------------------------------------------------------------------------
# Navegar por uma lista de páginas
# -----------------------------------------------------------------------------

def navegar_lista(urls: list[str], espera: float = 1.5):
    """
    Abre cada URL da lista, captura o título e o HTML.
    espera= define quantos segundos aguardar entre páginas.
    """
    driver = criar_driver(headless=True)
    resultados = []

    try:
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Acessando: {url}")

            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                resultados.append({
                    "url":    driver.current_url,
                    "titulo": driver.title,
                    "html":   driver.page_source[:500],
                })

                time.sleep(espera)  # respeita o servidor entre requisições

            except Exception as e:
                print(f"  Erro em {url}: {e}")
                resultados.append({"url": url, "erro": str(e)})

    finally:
        driver.quit()

    return resultados


# -----------------------------------------------------------------------------
# Executar JavaScript na página
# -----------------------------------------------------------------------------

def capturar_com_js(url: str):
    """
    Executa JavaScript diretamente no contexto da página.
    Útil para acessar dados que só existem após execução de JS.
    """
    driver = criar_driver(headless=True)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # execute_script roda JS e retorna o resultado para Python
        titulo    = driver.execute_script("return document.title;")
        user_agent = driver.execute_script("return navigator.userAgent;")
        cookies_js = driver.execute_script("return document.cookie;")

        print(f"Título (JS)     : {titulo}")
        print(f"User-Agent      : {user_agent}")
        print(f"Cookies (JS)    : {cookies_js}")

    finally:
        driver.quit()


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