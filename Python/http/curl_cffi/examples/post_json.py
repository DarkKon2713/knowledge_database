# =============================================================================
# Requisição POST com JSON usando curl_cffi
# =============================================================================
# Funciona igual ao requests — json= serializa o dict e define o Content-Type.
# O diferencial é o impersonate e http_version, que tornam a requisição
# indistinguível de um navegador real para servidores com detecção de bots.
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
# POST JSON — exemplo base
# -----------------------------------------------------------------------------

def exemplo_post_json():
    """
    Envia JSON com TLS fingerprint de navegador real.
    """
    payload = {
        "titulo":     "Erro ao fazer login",
        "prioridade": "alta",
        "usuario_id": 42,
    }

    try:
        response = requests.post(
            f"{API_URL}/post",
            json=payload,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()
        resultado = response.json()

        print(f"Status: {response.status_code}")
        print(f"Protocolo: HTTP/{response.http_version}")
        print(f"Content-Type enviado: {response.request.headers.get('Content-Type')}")
        print(f"Como o servidor recebeu: {resultado['json']}")

    except requests.exceptions.Timeout:
        print("Timeout — servidor demorou mais de 5 segundos.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# -----------------------------------------------------------------------------
# Caso de uso real — criar ticket
# -----------------------------------------------------------------------------

def criar_ticket(titulo, descricao, prioridade="normal", usuario_id=None):
    """
    Cria ticket via POST JSON simulando navegador.
    Útil quando a API tem WAF ou proteção contra bots.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type":  "application/json",
    }

    payload = {
        "titulo":     titulo,
        "descricao":  descricao,
        "prioridade": prioridade,
        "status":     "aberto",
    }

    if usuario_id:
        payload["usuario_id"] = usuario_id

    try:
        response = requests.post(
            f"{API_URL}/tickets",
            headers=headers,
            json=payload,
            impersonate="chrome",
            http_version="v2",
            timeout=5
        )
        response.raise_for_status()

        ticket = response.json()
        print(f"Ticket criado: #{ticket.get('id')} — {ticket.get('titulo')}")
        return ticket

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            erros = e.response.json().get("erros", [])
            print(f"Dados inválidos: {erros}")
        elif e.response.status_code == 401:
            print("Não autorizado — verifique o API_TOKEN no .env.")
        elif e.response.status_code == 422:
            print(f"Erro de validação: {e.response.json()}")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# PATCH e DELETE — idênticos ao requests, com impersonate
# -----------------------------------------------------------------------------

def atualizar_ticket(ticket_id, campos):
    """PATCH — atualiza apenas os campos enviados."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.patch(
            f"{API_URL}/tickets/{ticket_id}",
            headers=headers,
            json=campos,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Ticket #{ticket_id} não encontrado.")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return None


def fechar_ticket(ticket_id):
    """DELETE — 204 = sucesso sem corpo, não chamar .json()."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.delete(
            f"{API_URL}/tickets/{ticket_id}",
            headers=headers,
            impersonate="chrome",
            timeout=5
        )
        response.raise_for_status()

        if response.status_code == 204:
            print(f"Ticket #{ticket_id} removido.")
            return True

        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Ticket #{ticket_id} não encontrado.")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return False


if __name__ == "__main__":
    exemplo_post_json()