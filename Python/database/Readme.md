# Python — Database (PostgreSQL)

## O que é um driver de banco de dados?

Python não sabe falar com bancos de dados por padrão — ele precisa de um intermediário que traduz comandos Python para o protocolo do banco. Esse intermediário é o driver.

`psycopg2` é o driver mais usado para PostgreSQL em Python. Sem ele, não é possível conectar ao banco. É como um tradutor entre o Python e o PostgreSQL.

Exemplos de conexão e operações com PostgreSQL usando `psycopg2`.

```bash
pip install psycopg2-binary python-dotenv
```

> `psycopg2-binary` inclui as dependências compiladas — mais fácil de instalar localmente. Em produção, prefira `psycopg2` (sem `-binary`).

---

## Estrutura

```text
database/
├── connection.py   — conexão básica, context manager, RealDictCursor
├── queries.py      — SELECT, INSERT, UPDATE, DELETE com parâmetros
├── postgres.py     — classe reutilizável PostgreSQLConnection
└── Readme.md
```

---

## Ordem de leitura sugerida

1. `connection.py` — entender como conectar e por que usar context manager
2. `queries.py` — operações CRUD com parâmetros seguros
3. `postgres.py` — classe que encapsula tudo acima

---

## Variáveis de ambiente necessárias

Adicione ao seu `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=meu_usuario
DB_PASSWORD=minha_senha
```

---

## Referência rápida

### Conectar

```python
import psycopg2
from psycopg2 import extras

with psycopg2.connect(**DB_CREDENTIALS) as conn:
    with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM tickets WHERE id = %s;", (ticket_id,))
        resultado = cur.fetchone()    # dict ou None
```

### SELECT com parâmetros

```python
cur.execute("SELECT * FROM tickets WHERE status = %s;", (status,))
linhas = cur.fetchall()     # lista de dicts
```

### SELECT com lista de IDs

```python
cur.execute("SELECT * FROM tickets WHERE id = ANY(%s);", (ids,))
```

### INSERT com RETURNING

```python
cur.execute(
    "INSERT INTO tickets (titulo, status) VALUES (%s, %s) RETURNING id;",
    (titulo, "aberto")
)
novo_id = cur.fetchone()[0]
conn.commit()
```

### UPDATE / DELETE

```python
cur.execute("UPDATE tickets SET status = %s WHERE id = %s;", (status, ticket_id))
conn.commit()
afetadas = cur.rowcount     # quantas linhas foram modificadas
```

### INSERT em lote

```python
from psycopg2 import extras

valores = [("Título A", "aberto"), ("Título B", "aberto")]
extras.execute_values(cur, "INSERT INTO tickets (titulo, status) VALUES %s;", valores)
conn.commit()
```

---

## O que é SQL injection?

É um ataque onde alguém manipula uma query SQL inserindo código malicioso como valor de um campo. Por exemplo, se você montar a query com f-string:

```python
# PERIGOSO
status = "aberto' OR '1'='1"
query = f"SELECT * FROM tickets WHERE status = '{status}'"
# Vira: SELECT * FROM tickets WHERE status = 'aberto' OR '1'='1'
# Resultado: retorna TODOS os tickets, ignorando o filtro
```

Usando parâmetros com `%s`, o psycopg2 trata o valor como dado puro — nunca como código SQL. O ataque não funciona.

---

| Situação | Errado | Certo |
|---|---|---|
| Passar variável na query | `f"WHERE id = {id}"` | `"WHERE id = %s", (id,)` |
| Passar lista na query | `f"WHERE id IN {ids}"` | `"WHERE id = ANY(%s)", (ids,)` |
| Credenciais no código | `password="abc123"` | `os.getenv("DB_PASSWORD")` |

**Nunca use f-string ou concatenação para montar queries com dados externos** — isso abre brecha para SQL injection.

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `OperationalError: could not connect` | Host, porta ou credenciais errados | Verificar `.env` |
| `ProgrammingError: column does not exist` | Nome de coluna errado na query | Verificar schema da tabela |
| `InterfaceError: connection already closed` | Usou conexão fora do `with` | Sempre operar dentro do context manager |
| `TypeError` ao passar parâmetro único | Passou `(id)` em vez de `(id,)` | Adicionar vírgula: `(id,)` para criar tupla |
| `fetchone()` retorna `None` | Nenhuma linha encontrada | Verificar se o registro existe antes de acessar campos |