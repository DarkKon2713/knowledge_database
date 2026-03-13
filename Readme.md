# Knowledge Base — Python e Ferramentas de Desenvolvimento

Base de conhecimento para quem está começando a desenvolver em Python. O material foi pensado para quem já tem familiaridade com lógica de programação e APIs — o foco é mostrar como Python escreve o que você já conhece e como aplicar isso no dia a dia.

---

## Estrutura

```text
├── VSCode/
│   └── Readme.md                        — configuração do ambiente e extensões
├── git/
│   └── Readme.md                        — instalação, configuração e fluxo básico
├── python/
│   ├── basics/                          — fundamentos da linguagem
│   │   ├── dict_examples.py
│   │   ├── if_else.py
│   │   ├── input_examples.py
│   │   ├── list_examples.py
│   │   ├── loops_and_functions.py
│   │   ├── json_parsing.py
│   │   ├── string_methods.py
│   │   ├── error_handling.py
│   │   ├── files.py
│   │   └── type_hints.py
│   ├── _env/                            — variáveis de ambiente e credenciais
│   │   └── dotenv_example.py
│   ├── http/
│   │   ├── requests/                    — requisições HTTP com requests
│   │   │   └── examples/
│   │   │       ├── get_request.py
│   │   │       ├── post_form_data.py
│   │   │       └── post_json.py
│   │   └── curl_cffi/                   — requisições HTTP com curl_cffi
│   │       └── examples/
│   │           ├── get_request.py
│   │           ├── post_form_data.py
│   │           └── post_json.py
│   ├── oop/                             — orientação a objetos
│   │   ├── functions.py
│   │   └── classes.py
│   ├── database/                        — conexão e operações com PostgreSQL
│   │   ├── connection.py
│   │   ├── queries.py
│   │   └── postgres.py
│   ├── browser/                         — parsing de HTML e automação de navegadores
│   │   ├── beautifulsoup_example.py
│   │   ├── selenium_example.py
│   │   ├── playwright_example.py
│   │   ├── pyppeteer_example.py
│   │   ├── botasaurus_example.py
│   │   └── drissionpage_example.py
│   ├── utils/                           — utilitários do dia a dia
│   │   ├── datetime_examples.py
│   │   ├── regex_examples.py
│   │   └── logging_config.py
│   ├── async/                           — programação assíncrona
│   │   └── asyncio_basics.py
│   ├── patterns/                        — padrões de código reutilizáveis
│   │   ├── retry.py
│   │   ├── pagination.py
│   │   └── rate_limit.py
│   └── testing/                         — testes automatizados
│       └── pytest_basics.py
└── Readme.md
```

---

## Rota de estudos

### 🟢 Nível junior — comece aqui

Domine essa base antes de avançar. São os conceitos que aparecem em todo código Python.

```
1. git/
2. VSCode/
3. python/basics/
   ├── if_else.py
   ├── list_examples.py
   ├── dict_examples.py
   ├── loops_and_functions.py
   ├── string_methods.py
   ├── json_parsing.py
   ├── error_handling.py
   ├── files.py
   └── input_examples.py
4. python/_env/
5. python/http/requests/
```

### 🟡 Pleno — após dominar o básico

```
6. python/basics/type_hints.py
7. python/oop/
   ├── functions.py       (lambdas, closures, decorators)
   └── classes.py         (herança, polimorfismo, @classmethod)
8. python/utils/
   ├── datetime_examples.py
   ├── regex_examples.py
   └── logging_config.py
9. python/http/curl_cffi/
10. python/database/
11. python/patterns/
    ├── pagination.py
    ├── retry.py
    └── rate_limit.py
12. python/testing/
```

### 🔴 Avançado — diferencial de sênior

```
13. python/async/
14. python/browser/
    ├── playwright_example.py   (mais moderno)
    └── drissionpage_example.py (modo híbrido)
```

---

## O que é júnior e o que vai além

| Conteúdo | Nível |
|---|---|
| `if/else`, listas, dicts, loops, funções | 🟢 Junior |
| Strings, JSON, arquivos, `input()` | 🟢 Junior |
| Variáveis de ambiente, `.env` | 🟢 Junior |
| GET/POST com `requests`, tratamento de erro HTTP | 🟢 Junior |
| Type hints básicos (`str`, `int`, `list`, `dict`) | 🟢 Junior |
| `try/except`, erros específicos, `logging` básico | 🟢 Junior |
| OOP — classes, herança, `__init__`, métodos | 🟡 Pleno |
| Decorators, closures, funções como objetos | 🟡 Pleno |
| `TypedDict`, `Optional`, `Union`, `Callable` | 🟡 Pleno |
| `datetime`, `timedelta`, timestamp, `dateutil` | 🟡 Pleno |
| Regex — `search`, `findall`, `sub`, grupos | 🟡 Pleno |
| `logging` com handlers, rotação, múltiplos destinos | 🟡 Pleno |
| `curl_cffi`, `impersonate`, `http_version` | 🟡 Pleno |
| PostgreSQL com `psycopg2`, queries parametrizadas | 🟡 Pleno |
| Padrões — retry, paginação, rate limit | 🟡 Pleno |
| Testes com `pytest`, fixtures, mocks, parametrize | 🟡 Pleno |
| `async/await`, `asyncio.gather`, `aiohttp` | 🔴 Avançado |
| Automação de navegadores (Playwright, DrissionPage) | 🔴 Avançado |
| `Semaphore`, rate limit assíncrono | 🔴 Avançado |

---

## Instalação rápida

```bash
# Dependências principais
pip install requests curl_cffi python-dotenv psycopg2-binary

# Utils
pip install python-dateutil

# Patterns
pip install tenacity

# Testes
pip install pytest pytest-mock

# Async
pip install aiohttp

# Browser
pip install selenium webdriver-manager playwright botasaurus DrissionPage
playwright install chromium
```

---

## Resumo por pasta

| Pasta | Conteúdo |
|---|---|
| `git/` | Instalação, configuração, SSH, clone, add, commit, push, pull, branch |
| `VSCode/` | Configuração do ambiente Python, extensões, debug, boas práticas |
| `python/basics/` | if/else, listas, dicts, loops, funções, strings, JSON, arquivos, type hints |
| `python/_env/` | Variáveis de ambiente com `python-dotenv`, `.env`, `.gitignore` |
| `python/http/requests/` | GET, POST, PATCH, DELETE, paginação, OAuth2, Session |
| `python/http/curl_cffi/` | Igual ao requests + `impersonate` e `http_version` para APIs com proteção |
| `python/oop/` | Type hints, lambdas, decorators, classes, herança, polimorfismo |
| `python/database/` | Conexão com PostgreSQL, SELECT, INSERT, UPDATE, DELETE, classe reutilizável |
| `python/browser/` | BeautifulSoup, Selenium, Playwright, Pyppeteer, Botasaurus, DrissionPage |
| `python/utils/` | Datas, timestamps, expressões regulares, logging com handlers e rotação |
| `python/async/` | async/await, asyncio.gather, aiohttp, Semaphore |
| `python/patterns/` | Retry com tenacity, paginação (offset/cursor/link), rate limit |
| `python/testing/` | pytest, fixtures, parametrize, mock de API |