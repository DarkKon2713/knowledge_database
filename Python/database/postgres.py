# =============================================================================
# Classe de conexão reutilizável com PostgreSQL
# =============================================================================
# Encapsula a lógica de conexão, cursor e tratamento de erros em uma classe —
# evita repetir o bloco with psycopg2.connect()... em todo lugar do código.
#
# Baseada no padrão usado em produção neste repositório.
#
# Instalação:
#   pip install psycopg2-binary python-dotenv
# =============================================================================

import psycopg2
from psycopg2 import extras
from typing import Optional, Any
from dotenv import load_dotenv
import os

load_dotenv()


class PostgreSQLConnection:
    """Classe de conexão reutilizável com o PostgreSQL."""

    def __init__(self, db_credentials: dict, store_id: int = None):
        """
        Parâmetros:
            db_credentials  — dict com host, port, dbname, user, password
            store_id        — ID da loja/tenant, usado como filtro padrão nas queries
        """
        self.db_credentials = db_credentials
        self.store_id       = str(store_id) if store_id else None
        self.conn           = None

    # -------------------------------------------------------------------------
    # Conexão
    # -------------------------------------------------------------------------

    def _get_connection(self) -> psycopg2.extensions.connection:
        """Cria e retorna uma nova conexão com o banco."""
        return psycopg2.connect(**self.db_credentials)

    # -------------------------------------------------------------------------
    # Executor central — todas as queries passam por aqui
    # -------------------------------------------------------------------------

    def execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetchone: bool = False,
        fetchall: bool = False,
    ) -> Optional[Any]:
        """
        Executa uma query e retorna os resultados, se houver.

        Parâmetros:
            query    — string SQL com %s nos lugares dos parâmetros
            params   — tupla com os valores dos parâmetros
            fetchone — retorna apenas a primeira linha (dict)
            fetchall — retorna todas as linhas (lista de dicts)

        Para INSERT/UPDATE/DELETE: não passe fetchone nem fetchall.
        O commit é feito automaticamente pelo context manager do psycopg2.
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetchone:
                        return cur.fetchone()
                    elif fetchall:
                        return cur.fetchall()
                    conn.commit()

        except psycopg2.OperationalError as e:
            print(f"Erro de conexão: {e}")
        except psycopg2.Error as e:
            print(f"Erro no banco: {e}")

        return None

    # -------------------------------------------------------------------------
    # SELECT — sempre filtra por store_id
    # -------------------------------------------------------------------------

    def _select(self, query: str, param: Any = None) -> Optional[list]:
        """
        Executa um SELECT filtrando pelo store_id da instância.

        O store_id é sempre o primeiro parâmetro da query.
        Parâmetros adicionais são passados via `param`.

        Exemplos de query:
            SELECT * FROM tickets WHERE store_id = %s
            SELECT * FROM tickets WHERE store_id = %s AND id = %s
            SELECT * FROM tickets WHERE store_id = %s AND id = ANY(%s)

        Parâmetros:
            param=None           → só store_id
            param=123            → store_id + valor único
            param=(123, 456)     → store_id + múltiplos valores
            param=([1,2,3],)     → store_id + lista (para ANY(%s))
        """
        if param is None:
            params = (self.store_id,)
        elif isinstance(param, (tuple, list)):
            params = (self.store_id, *param)
        else:
            params = (self.store_id, param)

        return self.execute_query(query, params=params, fetchall=True)

    # -------------------------------------------------------------------------
    # INSERT / UPDATE / DELETE
    # -------------------------------------------------------------------------

    def _insert(self, query: str, param: Any = None) -> None:
        """
        Executa INSERT, UPDATE ou DELETE.

        Parâmetros:
            param=None           → sem parâmetros extras
            param=123            → valor único
            param=(123, 'texto') → múltiplos valores como tupla
        """
        if param is None:
            params = ()
        elif isinstance(param, (tuple, list)):
            params = tuple(param)
        else:
            params = (param,)

        self.execute_query(query, params=params)

    # -------------------------------------------------------------------------
    # Representação
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        host = self.db_credentials.get("host", "?")
        db   = self.db_credentials.get("dbname", "?")
        return f"PostgreSQLConnection(host={host}, dbname={db}, store_id={self.store_id})"


# -----------------------------------------------------------------------------
# Exemplo de uso
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Credenciais via .env
    credentials = {
        "host":     os.getenv("DB_HOST",  "localhost"),
        "port":     os.getenv("DB_PORT",  "5432"),
        "dbname":   os.getenv("DB_NAME"),
        "user":     os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    store_id  = 5540
    ticket_id = 101
    ids       = [101, 102, 103]

    conn = PostgreSQLConnection(db_credentials=credentials, store_id=store_id)
    print(conn)

    # SELECT simples — só store_id
    resultado = conn._select(
        "SELECT * FROM tickets WHERE store_id = %s LIMIT 5;"
    )
    print(resultado)

    # SELECT com parâmetro único
    resultado = conn._select(
        "SELECT * FROM tickets WHERE store_id = %s AND id = %s;",
        param=ticket_id
    )
    print(resultado)

    # SELECT com lista de IDs usando ANY
    resultado = conn._select(
        "SELECT * FROM tickets WHERE store_id = %s AND id = ANY(%s);",
        param=(ids,)     # lista dentro de tupla — ANY espera um único argumento
    )
    print(resultado)

    # INSERT
    conn._insert(
        "INSERT INTO tickets (store_id, titulo, status) VALUES (%s, %s, %s);",
        param=(store_id, "Erro ao logar", "aberto")
    )

    # UPDATE
    conn._insert(
        "UPDATE tickets SET status = %s WHERE id = %s AND store_id = %s;",
        param=("fechado", ticket_id, store_id)
    )