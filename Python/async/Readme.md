# Python — Async

## O que é programação assíncrona?

Imagine um atendente de suporte que, ao invés de esperar o cliente responder um e-mail para só então abrir o próximo, abre todos os tickets ao mesmo tempo e vai respondendo conforme as respostas chegam. Isso é async.

Em código síncrono normal, Python faz uma coisa por vez — envia uma requisição e fica parado esperando a resposta antes de enviar a próxima. Com async, Python envia todas as requisições e vai processando as respostas conforme chegam.

**Resultado prático:** buscar 20 tickets em paralelo leva o mesmo tempo que buscar 1, em vez de 20x mais.

---Programação assíncrona com `asyncio` e `aiohttp` — para executar múltiplas tarefas de I/O em paralelo sem travar o programa.

```bash
pip install aiohttp
```

---

## Estrutura

```text
async/
├── asyncio_basics.py   — async/await, gather, semaphore, aiohttp
└── Readme.md
```

---

## Quando usar async

| Situação | Usar async? |
|---|---|
| Fazer 1 requisição HTTP | Não — `requests` é suficiente |
| Fazer 20 requisições HTTP | Sim — `asyncio.gather()` + `aiohttp` |
| Processar lista de tickets em paralelo | Sim |
| Operações de CPU (cálculos pesados) | Não — async não ajuda, use `multiprocessing` |
| Banco de dados | Sim — com driver async (`asyncpg`, `databases`) |

---

## O que o arquivo cobre

| Conceito | Descrição |
|---|---|
| `async def` / `await` | Definir e pausar corrotinas |
| `asyncio.run()` | Ponto de entrada para rodar código async |
| `asyncio.gather()` | Rodar múltiplas corrotinas em paralelo |
| `return_exceptions=True` | Não cancelar tudo quando uma tarefa falha |
| `aiohttp.ClientSession` | Sessão HTTP assíncrona reutilizável |
| `asyncio.Semaphore` | Limitar número de tarefas simultâneas |

---

## Referência rápida

### Rodar uma corrotina

```python
resultado = asyncio.run(minha_funcao())
```

### Rodar várias em paralelo

```python
resultados = await asyncio.gather(tarefa1(), tarefa2(), tarefa3())
```

### Requisição HTTP assíncrona

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
        dados = await r.json()
```

### Limitar simultâneas (rate limit)

```python
sem = asyncio.Semaphore(5)      # máximo 5 ao mesmo tempo

async def buscar(url):
    async with sem:
        ...
```

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `RuntimeError: no running event loop` | Chamou `await` fora de função `async` | Envolver com `asyncio.run()` |
| `RuntimeError: This event loop is already running` | Tentou usar `asyncio.run()` dentro de outro loop (ex: Jupyter) | Usar `await` diretamente ou `nest_asyncio` |
| `TypeError: object is not awaitable` | Esqueceu o `await` antes da corrotina | Adicionar `await` |
| Todas as tarefas canceladas por um erro | `gather()` sem `return_exceptions=True` | Adicionar `return_exceptions=True` |