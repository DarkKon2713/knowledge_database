# =============================================================================
# Requisição GET com requests
# =============================================================================
# GET é usado para buscar dados — sem modificar nada no servidor.
# É o tipo de requisição mais comum ao consumir APIs.
#
# Instalação:
#   pip install requests
# =============================================================================

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL   = os.getenv("API_URL", "https://api.ipify.org")
API_TOKEN = os.getenv("API_TOKEN")

# -----------------------------------------------------------------------------
# Anatomia da resposta — o que vem em todo requests.get()
# -----------------------------------------------------------------------------

def inspecionar_resposta():
    """
    Mostra os principais campos disponíveis em qualquer objeto de resposta.
    Útil como referência rápida.
    """
    response = requests.get(f"{API_URL}?format=json", timeout=5)

    print(f"status_code : ({type(response.status_code)}) {response.status_code}")
    # 200 = sucesso, 404 = não encontrado, 500 = erro no servidor

    print(f"url         : ({type(response.url)}) {response.url}")
    # URL final — pode ser diferente da original se houve redirecionamento

    print(f"headers     : ({type(response.headers)}) {dict(response.headers)}")
    # Cabeçalhos da resposta — tipo de conteúdo, cache, servidor etc.

    print(f"cookies     : ({type(response.cookies)}) {dict(response.cookies)}")
    # Cookies retornados pela API (se houver)

    print(f"text        : ({type(response.text)}) {response.text}")
    # Corpo da resposta como string

    print(f"content     : ({type(response.content)}) {response.content}")
    # Corpo da resposta como bytes — use para arquivos ou dados binários

    print(f"json()      : ({type(response.json())}) {response.json()}")
    # Converte o corpo JSON em dict Python — equivale a json.loads(response.text)


# -----------------------------------------------------------------------------
# GET simples com tratamento de erro
# -----------------------------------------------------------------------------

def buscar_ip_publico():
    """
    Busca o IP público da máquina.
    Exemplo mínimo com tratamento de erro.
    """
    try:
        response = requests.get(f"{API_URL}?format=json", timeout=5)
        response.raise_for_status()     # lança exceção para status 4xx e 5xx
        return response.json()

    except requests.exceptions.Timeout:
        print("Erro: timeout — a API demorou mais de 5 segundos para responder.")
    except requests.exceptions.ConnectionError:
        print("Erro: não foi possível conectar à API.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e}")

    return None


# -----------------------------------------------------------------------------
# GET com headers de autenticação
# -----------------------------------------------------------------------------

def buscar_tickets():
    """
    Busca lista de tickets passando token de autenticação no header.
    Padrão mais comum em APIs REST.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type":  "application/json",
    }

    try:
        response = requests.get(
            f"{API_URL}/tickets",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
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
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return None


# -----------------------------------------------------------------------------
# GET com query params — filtros e paginação
# -----------------------------------------------------------------------------

def buscar_tickets_filtrados(status="aberto", pagina=1, limite=20):
    """
    Busca tickets com filtros via query params.

    Equivale a chamar:
        GET /tickets?status=aberto&page=1&limit=20
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    params = {
        "status": status,
        "page":   pagina,
        "limit":  limite,
    }
    # requests monta a query string automaticamente a partir do dict

    try:
        response = requests.get(
            f"{API_URL}/tickets",
            headers=headers,
            params=params,
            timeout=5
        )
        response.raise_for_status()

        dados = response.json()
        tickets = dados.get("tickets", [])
        total   = dados.get("total", 0)

        print(f"Página {pagina}: {len(tickets)} tickets (total: {total})")
        return tickets

    except requests.exceptions.Timeout:
        print(f"Timeout ao buscar tickets (página {pagina}).")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code} ao buscar tickets.")
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado: {e}")

    return []


# -----------------------------------------------------------------------------
# GET com paginação automática
# -----------------------------------------------------------------------------

def buscar_todos_os_tickets(status="aberto"):
    """
    Percorre todas as páginas e retorna todos os tickets de uma vez.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    todos   = []
    pagina  = 1

    while True:
        params = {"status": status, "page": pagina, "limit": 50}

        try:
            response = requests.get(
                f"{API_URL}/tickets",
                headers=headers,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            dados = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erro na página {pagina}: {e}")
            break

        tickets = dados.get("tickets", [])
        todos.extend(tickets)

        # Para quando não houver mais páginas
        if not dados.get("has_next_page"):
            break

        pagina += 1

    print(f"Total de tickets carregados: {len(todos)}")
    return todos


# -----------------------------------------------------------------------------
# GET com Session — reutiliza a conexão e os headers entre requisições
# -----------------------------------------------------------------------------

def buscar_com_session():
    """
    Session reutiliza a conexão TCP e permite definir headers globais.
    Mais eficiente quando você faz várias requisições seguidas.
    """
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type":  "application/json",
        })

        try:
            tickets   = session.get(f"{API_URL}/tickets",  timeout=5)
            usuarios  = session.get(f"{API_URL}/usuarios", timeout=5)

            tickets.raise_for_status()
            usuarios.raise_for_status()

            return {
                "tickets":  tickets.json(),
                "usuarios": usuarios.json(),
            }

        except requests.exceptions.RequestException as e:
            print(f"Erro na sessão: {e}")
            return None


if __name__ == "__main__":
    inspecionar_resposta()