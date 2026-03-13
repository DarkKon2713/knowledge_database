# =============================================================================
# Requisição POST com JSON usando requests
# =============================================================================
# Use json= quando a API espera o formato JSON:
#   Content-Type: application/json
#
# É o padrão da grande maioria das APIs REST modernas.
# requests.post(url, json=payload) serializa o dict automaticamente
# e define o Content-Type correto — você não precisa chamar json.dumps().
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
# POST JSON — exemplo base
# -----------------------------------------------------------------------------

def exemplo_post_json():
    """
    Envia dados no formato JSON (application/json).

    requests.post(url, json=payload):
      - serializa o dict para string JSON automaticamente
      - define Content-Type: application/json no header
    """
    payload = {
        "titulo":     "Erro ao fazer login",
        "prioridade": "alta",
        "usuario_id": 42,
    }

    try:
        response = requests.post(
            f"{API_URL}/post",
            json=payload,       # json= cuida da serialização e do header
            timeout=5
        )
        response.raise_for_status()
        resultado = response.json()

        print(f"Status: {response.status_code}")
        print(f"Como o servidor recebeu: {resultado['json']}")
        # {'titulo': 'Erro ao fazer login', 'prioridade': 'alta', 'usuario_id': 42}

    except requests.exceptions.Timeout:
        print("Timeout — servidor demorou mais de 5 segundos.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")


# -----------------------------------------------------------------------------
# Caso de uso real — criar ticket
# -----------------------------------------------------------------------------

def criar_ticket(titulo, descricao, prioridade="normal", usuario_id=None):
    """
    Cria um novo ticket via POST JSON.
    Retorna o dict do ticket criado ou None em caso de erro.
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

    # Adiciona usuario_id só se foi informado — evita mandar campo null
    if usuario_id:
        payload["usuario_id"] = usuario_id

    try:
        response = requests.post(
            f"{API_URL}/tickets",
            headers=headers,
            json=payload,
            timeout=5
        )
        response.raise_for_status()

        ticket = response.json()
        print(f"Ticket criado: #{ticket.get('id')} — {ticket.get('titulo')}")
        return ticket

    except requests.exceptions.Timeout:
        print("Timeout ao criar ticket.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            # A API geralmente devolve detalhes do erro no corpo
            erros = e.response.json().get("erros", [])
            print(f"Dados inválidos: {erros}")
        elif e.response.status_code == 401:
            print("Não autorizado — verifique o API_TOKEN no .env.")
        elif e.response.status_code == 422:
            print(f"Erro de validação: {e.response.json()}")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# POST JSON com payload aninhado
# -----------------------------------------------------------------------------

def criar_ticket_completo():
    """
    Exemplo com payload mais complexo — objetos aninhados e listas.
    Comum em APIs que aceitam criar recursos com relacionamentos em uma
    única requisição.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    payload = {
        "titulo":     "Falha na integração de pagamento",
        "prioridade": "alta",
        "responsavel": {
            "id":    7,
            "nome":  "Ana",
        },
        "tags":       ["bug", "pagamento", "urgente"],
        "metadados":  {
            "origem":  "webhook",
            "versao":  "2.1.0",
            "retry":   True,
        },
    }

    try:
        response = requests.post(
            f"{API_URL}/tickets",
            headers=headers,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# PUT e PATCH — atualizar recursos existentes
# -----------------------------------------------------------------------------

def atualizar_ticket(ticket_id, campos):
    """
    PATCH atualiza apenas os campos enviados — não sobrescreve o resto.
    PUT substitui o recurso inteiro.

    Na prática, prefira PATCH para atualizações parciais.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.patch(
            f"{API_URL}/tickets/{ticket_id}",
            headers=headers,
            json=campos,        # só os campos que você quer alterar
            timeout=5
        )
        response.raise_for_status()

        ticket = response.json()
        print(f"Ticket #{ticket_id} atualizado: status={ticket.get('status')}")
        return ticket

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Ticket #{ticket_id} não encontrado.")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# DELETE — remover um recurso
# -----------------------------------------------------------------------------

def fechar_ticket(ticket_id):
    """
    DELETE remove o recurso. Algumas APIs retornam 204 (No Content)
    em vez de 200 — por isso não chamamos .json() direto.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.delete(
            f"{API_URL}/tickets/{ticket_id}",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()

        # 204 = sucesso sem corpo — não tente chamar .json()
        if response.status_code == 204:
            print(f"Ticket #{ticket_id} removido.")
            return True

        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Ticket #{ticket_id} não encontrado.")
        else:
            print(f"Erro HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return False


if __name__ == "__main__":
    exemplo_post_json()