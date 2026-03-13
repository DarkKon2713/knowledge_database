# =============================================================================
# Padrão Paginação — consumir APIs com múltiplas páginas
# =============================================================================
# APIs raramente retornam todos os registros de uma vez.
# Existem três formatos principais de paginação:
#
#   1. Offset/Limit   — ?page=2&limit=20
#   2. Cursor         — ?cursor=eyJpZCI6MTAwfQ==
#   3. Link Header    — Link: <url>; rel="next"
# =============================================================================

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL   = os.getenv("API_URL", "https://api.exemplo.com")
API_TOKEN = os.getenv("API_TOKEN")
HEADERS   = {"Authorization": f"Bearer {API_TOKEN}"}


# -----------------------------------------------------------------------------
# 1. Paginação por offset/limit — a mais comum
# -----------------------------------------------------------------------------

# A API retorna algo como:
# {
#   "tickets": [...],
#   "total": 150,
#   "page": 1,
#   "total_pages": 8
# }

def buscar_pagina(status: str, pagina: int, limite: int = 20) -> dict | None:
    """Busca uma página específica de tickets."""
    try:
        response = requests.get(
            f"{API_URL}/tickets",
            headers=HEADERS,
            params={"status": status, "page": pagina, "limit": limite},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na página {pagina}: {e}")
        return None


def buscar_todos_offset(status: str = "aberto") -> list[dict]:
    """
    Percorre todas as páginas usando offset/limit.
    Para quando não há mais páginas ou ocorre erro.
    """
    todos   = []
    pagina  = 1

    while True:
        dados = buscar_pagina(status, pagina)
        if not dados:
            break

        tickets = dados.get("tickets", [])
        todos.extend(tickets)

        print(f"Página {pagina}/{dados.get('total_pages', '?')} — {len(tickets)} tickets")

        # Para quando não há mais páginas
        if pagina >= dados.get("total_pages", 1):
            break

        # Alternativa: verificar has_next_page
        # if not dados.get("has_next_page"):
        #     break

        pagina += 1

    print(f"Total carregado: {len(todos)}")
    return todos


# -----------------------------------------------------------------------------
# 2. Paginação por cursor — comum em APIs modernas
# -----------------------------------------------------------------------------

# A API retorna algo como:
# {
#   "tickets": [...],
#   "next_cursor": "eyJpZCI6MTAwfQ==",   ← None quando não há mais páginas
# }

def buscar_todos_cursor(status: str = "aberto") -> list[dict]:
    """
    Percorre todas as páginas usando cursor.
    O cursor é opaco — não tente decodificá-lo, só passe de volta.
    """
    todos  = []
    cursor = None      # primeira página não tem cursor

    while True:
        params = {"status": status, "limit": 50}
        if cursor:
            params["cursor"] = cursor

        try:
            response = requests.get(
                f"{API_URL}/tickets",
                headers=HEADERS,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            dados = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar com cursor '{cursor}': {e}")
            break

        tickets = dados.get("tickets", [])
        todos.extend(tickets)

        cursor = dados.get("next_cursor")
        print(f"Carregados: {len(todos)} | Próximo cursor: {cursor or 'nenhum'}")

        if not cursor:      # None = última página
            break

    return todos


# -----------------------------------------------------------------------------
# 3. Paginação por Link Header — padrão RFC 5988
# -----------------------------------------------------------------------------

# O header Link da resposta contém a URL da próxima página:
# Link: <https://api.exemplo.com/tickets?page=3>; rel="next",
#       <https://api.exemplo.com/tickets?page=8>; rel="last"

def extrair_url_proxima(link_header: str) -> str | None:
    """Extrai a URL com rel='next' do header Link."""
    if not link_header:
        return None
    for parte in link_header.split(","):
        url, _, rel = parte.strip().partition(";")
        if 'rel="next"' in rel:
            return url.strip().strip("<>")
    return None


def buscar_todos_link_header(status: str = "aberto") -> list[dict]:
    """
    Percorre páginas seguindo o Link header.
    Não precisa saber o total de páginas antecipadamente.
    """
    todos = []
    url   = f"{API_URL}/tickets"
    params = {"status": status, "limit": 50}

    while url:
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=5)
            response.raise_for_status()

            tickets = response.json()
            todos.extend(tickets if isinstance(tickets, list) else tickets.get("tickets", []))

            # Pega próxima URL do header e limpa os params (já estão na URL)
            url    = extrair_url_proxima(response.headers.get("Link", ""))
            params = {}

            print(f"Carregados: {len(todos)}")

        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            break

    return todos


# -----------------------------------------------------------------------------
# Paginação com limite máximo — evitar buscar dados demais
# -----------------------------------------------------------------------------

def buscar_com_limite_maximo(
    status: str = "aberto",
    max_registros: int = 500,
    por_pagina: int = 50,
) -> list[dict]:
    """
    Igual ao offset/limit, mas para quando atinge max_registros.
    Útil para não travar o script em bases grandes.
    """
    todos  = []
    pagina = 1

    while len(todos) < max_registros:
        dados = buscar_pagina(status, pagina, por_pagina)
        if not dados:
            break

        tickets = dados.get("tickets", [])
        todos.extend(tickets)

        if pagina >= dados.get("total_pages", 1) or not tickets:
            break

        pagina += 1

    return todos[:max_registros]    # garante não ultrapassar o limite


if __name__ == "__main__":
    tickets = buscar_todos_offset("aberto")
    print(f"{len(tickets)} tickets carregados")