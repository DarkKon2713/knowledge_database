# =============================================================================
# SELECT, INSERT, UPDATE, DELETE com psycopg2
# =============================================================================
# Regra mais importante: NUNCA use f-string ou concatenação para montar
# queries com dados do usuário — isso abre brecha para SQL injection.
#
# SEMPRE use parâmetros com %s e passe os valores separados:
#   cur.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
# =============================================================================

import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
import os

load_dotenv()

DB_CREDENTIALS = {
    "host":     os.getenv("DB_HOST",  "localhost"),
    "port":     os.getenv("DB_PORT",  "5432"),
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


# -----------------------------------------------------------------------------
# SELECT — buscar dados
# -----------------------------------------------------------------------------

def buscar_ticket(ticket_id: int) -> dict | None:
    """Busca um ticket pelo ID. Retorna dict ou None se não encontrado."""
    query = "SELECT id, titulo, status, prioridade FROM tickets WHERE id = %s;"

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, (ticket_id,))    # note a vírgula — precisa ser tupla
                return cur.fetchone()               # dict ou None

    except psycopg2.Error as e:
        print(f"Erro ao buscar ticket {ticket_id}: {e}")
        return None


def buscar_tickets_por_status(status: str) -> list:
    """Busca todos os tickets com um determinado status."""
    query = """
        SELECT id, titulo, status, prioridade
        FROM tickets
        WHERE status = %s
        ORDER BY id DESC;
    """

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, (status,))
                return cur.fetchall()               # lista de dicts

    except psycopg2.Error as e:
        print(f"Erro ao buscar tickets com status '{status}': {e}")
        return []


def buscar_tickets_por_ids(ids: list) -> list:
    """
    Busca múltiplos tickets por uma lista de IDs.
    extras.execute_values é mais eficiente que um loop de SELECTs.
    """
    query = "SELECT id, titulo, status FROM tickets WHERE id = ANY(%s);"

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, (ids,))          # passa a lista diretamente com ANY
                return cur.fetchall()

    except psycopg2.Error as e:
        print(f"Erro ao buscar tickets por IDs: {e}")
        return []


# -----------------------------------------------------------------------------
# INSERT — inserir dados
# -----------------------------------------------------------------------------

def criar_ticket(titulo: str, prioridade: str = "normal") -> int | None:
    """
    Insere um novo ticket e retorna o ID gerado.
    RETURNING id faz o banco devolver o ID sem precisar de outro SELECT.
    """
    query = """
        INSERT INTO tickets (titulo, status, prioridade)
        VALUES (%s, 'aberto', %s)
        RETURNING id;
    """

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (titulo, prioridade))
                resultado = cur.fetchone()
                conn.commit()                       # confirma a transação
                return resultado[0]                 # id gerado

    except psycopg2.Error as e:
        print(f"Erro ao criar ticket: {e}")
        return None


def inserir_multiplos_tickets(tickets: list[dict]) -> int:
    """
    Insere múltiplos tickets de uma vez com execute_values.
    Muito mais eficiente que um loop de INSERTs individuais.
    """
    query = "INSERT INTO tickets (titulo, status, prioridade) VALUES %s;"

    # execute_values espera lista de tuplas:
    valores = [(t["titulo"], t.get("status", "aberto"), t.get("prioridade", "normal"))
               for t in tickets]

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                extras.execute_values(cur, query, valores)
                conn.commit()
                return cur.rowcount                 # quantidade de linhas inseridas

    except psycopg2.Error as e:
        print(f"Erro ao inserir tickets em lote: {e}")
        return 0


# -----------------------------------------------------------------------------
# UPDATE — atualizar dados
# -----------------------------------------------------------------------------

def atualizar_status(ticket_id: int, novo_status: str) -> bool:
    """Atualiza o status de um ticket. Retorna True se atualizou."""
    query = "UPDATE tickets SET status = %s WHERE id = %s;"

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (novo_status, ticket_id))
                conn.commit()
                return cur.rowcount > 0             # rowcount = quantas linhas foram afetadas

    except psycopg2.Error as e:
        print(f"Erro ao atualizar ticket {ticket_id}: {e}")
        return False


def atualizar_campos(ticket_id: int, campos: dict) -> bool:
    """
    Atualiza campos dinâmicos de um ticket a partir de um dict.
    Útil quando você não sabe de antemão quais campos vão mudar.
    """
    if not campos:
        return False

    # Monta: "titulo = %s, prioridade = %s"
    set_clause = ", ".join(f"{campo} = %s" for campo in campos)
    query      = f"UPDATE tickets SET {set_clause} WHERE id = %s;"
    valores    = (*campos.values(), ticket_id)

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, valores)
                conn.commit()
                return cur.rowcount > 0

    except psycopg2.Error as e:
        print(f"Erro ao atualizar campos do ticket {ticket_id}: {e}")
        return False


# -----------------------------------------------------------------------------
# DELETE — remover dados
# -----------------------------------------------------------------------------

def deletar_ticket(ticket_id: int) -> bool:
    """Remove um ticket pelo ID. Retorna True se deletou."""
    query = "DELETE FROM tickets WHERE id = %s;"

    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (ticket_id,))
                conn.commit()
                return cur.rowcount > 0

    except psycopg2.Error as e:
        print(f"Erro ao deletar ticket {ticket_id}: {e}")
        return False


# -----------------------------------------------------------------------------
# SQL injection — nunca faça isso
# -----------------------------------------------------------------------------

# ERRADO — abre brecha para SQL injection:
# status = "aberto' OR '1'='1"
# cur.execute(f"SELECT * FROM tickets WHERE status = '{status}'")
# → vira: SELECT * FROM tickets WHERE status = 'aberto' OR '1'='1'
# → retorna TODOS os tickets, independente do status

# CERTO — psycopg2 sanitiza os valores automaticamente:
# cur.execute("SELECT * FROM tickets WHERE status = %s", (status,))


if __name__ == "__main__":
    ticket = buscar_ticket(1)
    print(ticket)

    tickets = buscar_tickets_por_status("aberto")
    for t in tickets:
        print(t)