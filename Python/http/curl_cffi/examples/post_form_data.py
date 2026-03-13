# =============================================================================
# Requisição POST com form data usando curl_cffi
# =============================================================================
# Funciona igual ao requests — data= envia como form-data.
# O diferencial do curl_cffi aqui é o impersonate, que torna a requisição
# indistinguível de um formulário enviado por um navegador real.
#
# Instalação:
#   pip install curl_cffi python-dotenv
# =============================================================================

from curl_cffi import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL   = os.getenv("API_URL", "https://httpbin.org")
API_TOKEN = os.getenv("API_TOKEN")


# -----------------------------------------------------------------------------
# POST form data — exemplo base
# -----------------------------------------------------------------------------

def exemplo_post_form_data():
    """
    Envia dados como form-data com TLS fingerprint de navegador real.
    Útil quando o endpoint detecta automação via TLS mesmo com data= correto.
    """
    payload = {
        "usuario": "leonardo",
        "senha":   "123456",
    }

    try:
        response = requests.post(
            f"{API_URL}/post",
            data=payload,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()
        resultado = response.json()

        print(f"Status: {response.status_code}")
        print(f"Protocolo: HTTP/{response.http_version}")
        print(f"Content-Type enviado: {response.request.headers.get('Content-Type')}")
        print(f"Como o servidor recebeu: {resultado['form']}")

    except requests.exceptions.Timeout:
        print("Timeout — servidor demorou mais de 5 segundos.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# -----------------------------------------------------------------------------
# OAuth2 com impersonate — útil quando o servidor de token verifica o TLS
# -----------------------------------------------------------------------------

def obter_token_oauth():
    """
    Fluxo OAuth2 client_credentials via form-data.
    Alguns servidores de autenticação verificam TLS fingerprint —
    impersonate="chrome" contorna essa verificação.
    """
    client_id     = os.getenv("OAUTH_CLIENT_ID")
    client_secret = os.getenv("OAUTH_CLIENT_SECRET")
    token_url     = os.getenv("OAUTH_TOKEN_URL")

    payload = {
        "grant_type":    "client_credentials",
        "client_id":     client_id,
        "client_secret": client_secret,
        "scope":         "tickets:read tickets:write",
    }

    try:
        response = requests.post(
            token_url,
            data=payload,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()

        dados        = response.json()
        access_token = dados.get("access_token")
        expires_in   = dados.get("expires_in")

        print(f"Token obtido. Expira em {expires_in}s.")
        return access_token

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Credenciais inválidas — verifique CLIENT_ID e CLIENT_SECRET no .env.")
        else:
            print(f"Erro HTTP {e.response.status_code} ao obter token.")
    except Exception as e:
        print(f"Erro ao conectar ao servidor de autenticação: {e}")

    return None


# -----------------------------------------------------------------------------
# Upload de arquivo com impersonate
# -----------------------------------------------------------------------------

def enviar_anexo(ticket_id, caminho_arquivo):
    """
    Envia arquivo via multipart/form-data simulando navegador real.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        with open(caminho_arquivo, "rb") as f:
            files   = {"arquivo": (os.path.basename(caminho_arquivo), f)}
            payload = {"ticket_id": str(ticket_id), "descricao": "Log de erro"}

            response = requests.post(
                f"{API_URL}/tickets/{ticket_id}/anexos",
                headers=headers,
                data=payload,
                files=files,
                impersonate="chrome",
                timeout=10
            )
            response.raise_for_status()
            print(f"Anexo enviado: {response.json()}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code} ao enviar anexo.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    exemplo_post_form_data()