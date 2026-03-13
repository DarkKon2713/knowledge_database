# =============================================================================
# Requisição GET com curl_cffi
# =============================================================================
# curl_cffi usa libcurl internamente e consegue imitar navegadores reais —
# altera TLS fingerprint, headers e comportamento da conexão.
#
# A API é quase idêntica ao requests. A diferença principal está em dois
# parâmetros extras:
#   impersonate  — simula um navegador específico
#   http_version — força HTTP/1.1, HTTP/2 ou HTTP/3
#
# Use curl_cffi quando:
#   - a API bloqueia o requests por detectar automação
#   - precisa de HTTP/2 ou HTTP/3
#   - scraping de sites com proteções mais avançadas
#
# Para APIs REST simples sem proteção, requests é suficiente.
#
# Instalação:
#   pip install curl_cffi python-dotenv
# =============================================================================

from curl_cffi import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL   = os.getenv("API_URL", "https://api.ipify.org")
API_TOKEN = os.getenv("API_TOKEN")


# -----------------------------------------------------------------------------
# Anatomia da resposta — campos disponíveis
# -----------------------------------------------------------------------------

def inspecionar_resposta():
    """
    Mostra os principais campos do objeto Response do curl_cffi.
    Quase idêntico ao requests — o extra é response.http_version.
    """
    response = requests.get(
        f"{API_URL}?format=json",
        impersonate="chrome",
        timeout=5
    )

    print(f"status_code  : {response.status_code}")
    print(f"http_version : {response.http_version}")   # exclusivo curl_cffi
    print(f"url          : {response.url}")
    print(f"headers      : {dict(response.headers)}")
    print(f"text         : {response.text}")
    print(f"json()       : {response.json()}")


# -----------------------------------------------------------------------------
# GET simples com impersonate e tratamento de erro
# -----------------------------------------------------------------------------

def buscar_ip_publico():
    """
    Exemplo mínimo com impersonate e tratamento de erro.
    """
    try:
        response = requests.get(
            f"{API_URL}?format=json",
            impersonate="chrome",   # simula Chrome — altera TLS fingerprint
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("Timeout — servidor demorou mais de 5 segundos.")
    except requests.exceptions.ConnectionError:
        print("Falha de conexão.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")

    return None


# -----------------------------------------------------------------------------
# GET com impersonate e http_version
# -----------------------------------------------------------------------------

def buscar_tickets():
    """
    Requisição com navegador simulado e HTTP/2 forçado.
    Útil quando a API exige HTTP/2 ou detecta automação via TLS.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.get(
            f"{API_URL}/tickets",
            headers=headers,
            impersonate="chrome",   # opções: chrome, safari, edge, firefox
            http_version="v2",      # v1 = HTTP/1.1 | v2 = HTTP/2 | v3 = HTTP/3
            timeout=5
        )
        response.raise_for_status()

        print(f"Protocolo usado: HTTP/{response.http_version}")
        return response.json()

    except requests.exceptions.Timeout:
        print("Timeout ao buscar tickets.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Não autorizado — verifique o API_TOKEN no .env.")
        elif e.response.status_code == 403:
            print("Sem permissão para acessar este recurso.")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# GET com query params e paginação
# -----------------------------------------------------------------------------

def buscar_tickets_filtrados(status="aberto", pagina=1, limite=20):
    """
    Busca tickets com filtros. Idêntico ao requests — params= funciona igual.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params  = {"status": status, "page": pagina, "limit": limite}

    try:
        response = requests.get(
            f"{API_URL}/tickets",
            headers=headers,
            params=params,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()

        dados   = response.json()
        tickets = dados.get("tickets", [])
        print(f"Página {pagina}: {len(tickets)} tickets")
        return tickets

    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return []


# -----------------------------------------------------------------------------
# Session — reutiliza conexão, cookies e impersonate entre requisições
# -----------------------------------------------------------------------------

def buscar_com_session():
    """
    Session no curl_cffi mantém o mesmo TLS fingerprint e cookies
    em todas as requisições — importante pra sites que rastreiam sessão.
    """
    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {API_TOKEN}"})

        try:
            tickets  = session.get(
                f"{API_URL}/tickets",
                impersonate="chrome",
                timeout=5
            )
            usuarios = session.get(
                f"{API_URL}/usuarios",
                impersonate="chrome",
                timeout=5
            )

            tickets.raise_for_status()
            usuarios.raise_for_status()

            return {
                "tickets":  tickets.json(),
                "usuarios": usuarios.json(),
            }

        except Exception as e:
            print(f"Erro na sessão: {e}")
            return None


if __name__ == "__main__":
    inspecionar_resposta()