# =============================================================================
# Manipulação de navegador com DrissionPage
# =============================================================================
# DrissionPage combina controle de navegador (como Selenium) com requisições
# HTTP (como requests) em uma única interface.
# Pode alternar entre os dois modos sem perder cookies ou sessão.
#
# Instalação:
#   pip install DrissionPage
#   (Chromium é gerenciado automaticamente)
# =============================================================================

from DrissionPage import ChromiumPage, SessionPage, WebPage
import time


# -----------------------------------------------------------------------------
# Modo browser — controla o Chrome diretamente
# -----------------------------------------------------------------------------

def capturar_pagina_browser(url: str):
    """
    ChromiumPage controla o Chrome — renderiza JS, mantém cookies,
    comportamento idêntico a um usuário real.
    """
    page = ChromiumPage()           # abre o Chrome (headful por padrão)
    # Para headless: ChromiumPage(ChromiumOptions().headless())

    page.get(url)

    print(f"URL atual : {page.url}")
    print(f"Título    : {page.title}")

    # HTML completo da página (após JS renderizado)
    html = page.html
    print(f"HTML (primeiros 200 chars): {html[:200]}")

    # Cookies
    cookies = page.cookies()
    print(f"\nCookies ({len(cookies)} encontrados):")
    for cookie in cookies.as_dict().items():
        print(f"  {cookie[0]} = {cookie[1]}")

    page.quit()


# -----------------------------------------------------------------------------
# Modo session — requisição HTTP direta, sem abrir browser
# -----------------------------------------------------------------------------

def capturar_headers_session(url: str):
    """
    SessionPage faz requisições HTTP como o requests — mais rápido,
    mas não renderiza JavaScript.
    Útil quando a página não precisa de JS para ter o conteúdo.
    """
    page = SessionPage()

    page.get(url)

    print(f"Status  : {page.response.status_code}")
    print(f"URL     : {page.url}")

    # Headers da resposta HTTP — disponível no modo session
    print(f"\nHeaders:")
    for chave, valor in page.response.headers.items():
        print(f"  {chave}: {valor}")

    # HTML cru (sem JS)
    print(f"\nHTML (primeiros 200 chars): {page.html[:200]}")


# -----------------------------------------------------------------------------
# WebPage — alterna entre browser e session sem perder cookies
# -----------------------------------------------------------------------------

def capturar_com_alternancia(url: str):
    """
    WebPage é o modo híbrido — começa como browser para logar/pegar cookies,
    depois troca para session para fazer requisições mais rápidas.
    Cookies e headers são mantidos automaticamente entre os modos.
    """
    page = WebPage()

    # Modo browser — carrega a página com JS
    page.change_mode("d")       # "d" = driver (browser)
    page.get(url)
    print(f"[browser] Título: {page.title}")

    # Alterna para session — usa os cookies capturados pelo browser
    page.change_mode("s")       # "s" = session (HTTP)
    page.get(url)
    print(f"[session] Status: {page.response.status_code}")
    print(f"[session] Headers: {dict(page.response.headers)}")

    page.quit()


# -----------------------------------------------------------------------------
# Navegar por uma lista de páginas
# -----------------------------------------------------------------------------

def navegar_lista(urls: list[str], espera: float = 1.5):
    """
    Abre cada URL da lista reutilizando a mesma instância do Chrome.
    Mantém cookies e sessão entre as páginas.
    """
    page       = ChromiumPage()
    resultados = []

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Acessando: {url}")

        try:
            page.get(url)

            resultados.append({
                "url":     page.url,
                "titulo":  page.title,
                "html":    page.html[:500],
                "cookies": page.cookies().as_dict(),
            })

            time.sleep(espera)

        except Exception as e:
            print(f"  Erro em {url}: {e}")
            resultados.append({"url": url, "erro": str(e)})

    page.quit()
    return resultados


# -----------------------------------------------------------------------------
# Exemplo de uso
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://httpbin.org/cookies",
    ]

    # Navegar em modo browser
    resultados = navegar_lista(urls)
    for r in resultados:
        print(r.get("titulo", r.get("erro")))

    # Capturar headers sem abrir browser
    capturar_headers_session("https://httpbin.org/headers")