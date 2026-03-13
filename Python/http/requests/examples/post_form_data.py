# =============================================================================
# Requisição POST com form data usando requests
# =============================================================================
# Use form data (data=) quando a API espera o formato de formulário HTML:
#   Content-Type: application/x-www-form-urlencoded
#
# Os dados chegam no servidor como: campo=valor&campo2=valor2
# Comum em: autenticação OAuth, login de sistemas legados, alguns webhooks.
#
# Se a API espera JSON, use post_json.py.
#
# Instalação:
#   pip install requests python-dotenv
# =============================================================================

import requests
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
    Envia dados no formato form-data (application/x-www-form-urlencoded).

    requests.post(url, data=payload) converte o dict automaticamente para:
        usuario=leonardo&senha=123456
    """
    payload = {
        "usuario": "leonardo",
        "senha":   "123456",
    }

    try:
        response = requests.post(
            f"{API_URL}/post",
            data=payload,       # data= envia como form-data
            timeout=5
        )
        response.raise_for_status()
        resultado = response.json()

        print(f"Status: {response.status_code}")
        print(f"Como o servidor recebeu: {resultado['form']}")
        # {'usuario': 'leonardo', 'senha': '123456'}

    except requests.exceptions.Timeout:
        print("Timeout — servidor demorou mais de 5 segundos.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")


# -----------------------------------------------------------------------------
# Caso de uso real — autenticação OAuth2 (client_credentials)
# -----------------------------------------------------------------------------

def obter_token_oauth():
    """
    Fluxo OAuth2 client_credentials — muito comum em integrações B2B.
    A maioria das APIs OAuth espera form-data, não JSON, nesta etapa.
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
        response = requests.post(token_url, data=payload, timeout=5)
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
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao servidor de autenticação: {e}")

    return None


# -----------------------------------------------------------------------------
# POST form data com arquivo (multipart/form-data)
# -----------------------------------------------------------------------------

def enviar_anexo(ticket_id, caminho_arquivo):
    """
    Envia um arquivo junto com campos de formulário.
    Quando files= está presente, requests usa multipart/form-data
    em vez de application/x-www-form-urlencoded.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        with open(caminho_arquivo, "rb") as f:
            files   = {"arquivo": (os.path.basename(caminho_arquivo), f)}
            payload = {"ticket_id": str(ticket_id), "descricao": "Log de erro"}

            response = requests.post(
                f"{API_URL}/tickets/{ticket_id}/anexos",
                headers=headers,
                data=files,
                files=payload,
                timeout=10
            )
            response.raise_for_status()
            print(f"Anexo enviado: {response.json()}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code} ao enviar anexo.")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")


# -----------------------------------------------------------------------------
# data= vs json= — qual usar?
# -----------------------------------------------------------------------------

# data=payload   →  Content-Type: application/x-www-form-urlencoded
#                   corpo: usuario=leonardo&senha=123456
#                   use quando: OAuth, formulários, sistemas legados

# json=payload   →  Content-Type: application/json
#                   corpo: {"usuario": "leonardo", "senha": "123456"}
#                   use quando: APIs REST modernas (a maioria)

# Se não souber qual usar, verifique o Content-Type que a API espera
# na documentação — ou inspecione uma requisição real no DevTools/Postman.


if __name__ == "__main__":
    exemplo_post_form_data()