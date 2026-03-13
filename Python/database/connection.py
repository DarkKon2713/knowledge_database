# =============================================================================
# Conexão com PostgreSQL usando psycopg2
# =============================================================================
# psycopg2 é o driver mais usado para conectar Python ao PostgreSQL.
#
# Instalação:
#   pip install psycopg2-binary python-dotenv
#
# psycopg2-binary inclui as dependências C compiladas — mais fácil de instalar.
# Em produção, prefira psycopg2 (sem -binary) para melhor performance.
# =============================================================================

import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
import os

load_dotenv()


# -----------------------------------------------------------------------------
# Credenciais — sempre via variáveis de ambiente, nunca no código
# -----------------------------------------------------------------------------

# Formato que o psycopg2.connect() aceita como **kwargs:
DB_CREDENTIALS = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# .env correspondente:
#   DB_HOST=localhost
#   DB_PORT=5432
#   DB_NAME=meu_banco
#   DB_USER=meu_usuario
#   DB_PASSWORD=minha_senha


# -----------------------------------------------------------------------------
# Conexão básica — abrindo e fechando manualmente
# -----------------------------------------------------------------------------

def conexao_basica():
    """
    Forma manual de conectar — útil para entender o fluxo,
    mas prefira o context manager abaixo para uso real.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CREDENTIALS)
        print(f"Conectado ao banco: {conn.dsn}")
        print(f"Versão do servidor: {conn.server_version}")

    except psycopg2.OperationalError as e:
        print(f"Falha na conexão: {e}")

    finally:
        if conn:
            conn.close()        # sempre fechar — evita conexões abertas no banco
            print("Conexão encerrada.")


# -----------------------------------------------------------------------------
# Conexão com context manager — forma recomendada
# -----------------------------------------------------------------------------

def conexao_com_context_manager():
    """
    O `with` garante que a conexão será fechada mesmo se ocorrer erro.
    Também faz commit automático ao sair do bloco sem erro,
    e rollback automático se ocorrer exceção.
    """
    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                versao = cur.fetchone()
                print(f"PostgreSQL: {versao[0]}")

    except psycopg2.OperationalError as e:
        print(f"Falha na conexão: {e}")


# -----------------------------------------------------------------------------
# RealDictCursor — retorna resultados como dicts em vez de tuplas
# -----------------------------------------------------------------------------

def conexao_com_dict_cursor():
    """
    Por padrão, psycopg2 retorna cada linha como tupla: (1, 'Ana', 'aberto')
    Com RealDictCursor, retorna como dict: {'id': 1, 'nome': 'Ana', 'status': 'aberto'}

    Use RealDictCursor sempre que for trabalhar com os dados por nome de campo.
    """
    try:
        with psycopg2.connect(**DB_CREDENTIALS) as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute("SELECT 1 AS id, 'Ana' AS nome, 'aberto' AS status;")
                linha = cur.fetchone()
                print(linha)
                # {'id': 1, 'nome': 'Ana', 'status': 'aberto'}
                print(linha["nome"])    # Ana — acesso por nome de campo

    except psycopg2.OperationalError as e:
        print(f"Falha na conexão: {e}")


# -----------------------------------------------------------------------------
# Erros comuns de conexão
# -----------------------------------------------------------------------------

# psycopg2.OperationalError  — banco não encontrado, credenciais erradas, porta errada
# psycopg2.InterfaceError    — tentou usar conexão já fechada
# psycopg2.DatabaseError     — erro genérico do banco (pai de vários erros)

# Dica: se `DB_NAME`, `DB_USER` ou `DB_PASSWORD` vier None do .env,
# o connect() vai tentar usar o usuário do sistema operacional — confuso.
# Valide as variáveis antes de conectar:

def validar_credenciais():
    obrigatorias = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    ausentes = [k for k in obrigatorias if not os.getenv(k)]
    if ausentes:
        raise EnvironmentError(
            f"Variáveis de banco não definidas: {', '.join(ausentes)}\n"
            f"Verifique o .env."
        )


if __name__ == "__main__":
    validar_credenciais()
    conexao_com_context_manager()
    conexao_com_dict_cursor()