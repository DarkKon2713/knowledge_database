# Python — Patterns

Padrões de código que aparecem com frequência ao consumir APIs — retry, paginação e rate limit.

```bash
pip install tenacity
```

---

## Estrutura

```text
patterns/
├── retry.py        — tentar novamente em caso de falha
├── pagination.py   — consumir APIs com múltiplas páginas
├── rate_limit.py   — respeitar limites de requisições
└── Readme.md
```

---

## O que cada arquivo cobre

### `retry.py`

| Conceito | Descrição |
|---|---|
| Retry manual | Loop com `try/except` e `time.sleep()` |
| `@retry` (tenacity) | Decorator com `stop_after_attempt` e `wait_fixed` |
| Backoff exponencial | `wait_exponential` — aumenta o tempo a cada tentativa |
| Retry condicional | `retry_if_result` — tenta de novo baseado no retorno |
| Não fazer retry em 4xx | Erros do cliente não melhoram com retry — desistir imediatamente |

### `pagination.py`

| Tipo | Como funciona |
|---|---|
| Offset/limit | `?page=2&limit=20` — mais comum |
| Cursor | `?cursor=abc123` — sem saber o total de páginas |
| Link header | Header `Link: <url>; rel="next"` — padrão RFC 5988 |
| Limite máximo | Para antes de atingir N registros |

### `rate_limit.py`

| Conceito | Descrição |
|---|---|
| Espera simples | `time.sleep()` entre requisições |
| Retry-After | Lê o header `Retry-After` do 429 e aguarda |
| `RateLimiter` | Janela deslizante — controla o ritmo automaticamente |

---

## Quando usar cada padrão

| Situação | Padrão |
|---|---|
| API instável / timeout frequente | `retry.py` com backoff exponencial |
| API retorna dados paginados | `pagination.py` — escolha o tipo pelo formato da API |
| API retorna 429 com frequência | `rate_limit.py` com `RateLimiter` |
| Job assíncrono que demora para terminar | `retry.py` com `retry_if_result` |
| Scraping de muitas páginas | Combine `pagination.py` + `rate_limit.py` |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| Loop infinito na paginação | Condição de parada errada | Verificar `has_next_page` ou `total_pages` |
| 429 em todo request | Rate limit muito agressivo | Reduzir `max_por_segundo` no `RateLimiter` |
| Retry em erro 400/404 | Erro do cliente não melhora com retry | Não fazer retry em status < 500 |
| `tenacity.RetryError` | Todas as tentativas falharam | Capturar com `except RetryError` ou usar `reraise=True` |