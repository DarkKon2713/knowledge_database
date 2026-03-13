# Python — Conceitos Fundamentais

Esta pasta cobre os conceitos base da linguagem Python. Se você já tem familiaridade com lógica de programação e APIs, o objetivo aqui é mostrar **como Python escreve o que você já conhece**.

---

## Antes de começar — ambiente virtual

Sempre crie um ambiente virtual antes de instalar qualquer biblioteca. Sem ele, tudo é instalado globalmente no seu Python — e projetos diferentes com versões diferentes de bibliotecas vão conflitar entre si.

```bash
# Criar o ambiente virtual (uma vez por projeto)
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Mac/Linux)
source .venv/bin/activate

# Instalar bibliotecas (sempre com o ambiente ativado)
pip install requests

# Quando o terminal mostrar (.venv) na frente, está ativado
```

> O VS Code detecta o `.venv` automaticamente e pergunta se quer usá-lo. Clique em **Yes**.

---

```text
basics/
├── dict_examples.py       — dicionários e acesso a dados
├── if_else.py             — condicionais e operadores lógicos
├── input_examples.py      — leitura de entrada do usuário
├── list_examples.py       — listas, ordenação e filtros
├── loops_and_functions.py — for, while, def, *args, **kwargs
├── json_parsing.py        — leitura e escrita de JSON
├── string_methods.py      — manipulação de strings
└── error_handling.py      — try/except e tratamento de erros
```

---

## Ordem de leitura sugerida

Se você está começando, siga essa ordem:

1. `if_else.py` — condicionais e operadores lógicos
2. `list_examples.py` — listas e iteração
3. `dict_examples.py` — dicionários (estrutura base do JSON)
4. `loops_and_functions.py` — loops e funções
5. `string_methods.py` — manipulação de texto
6. `json_parsing.py` — leitura e escrita de JSON
7. `error_handling.py` — como lidar com erros sem derrubar o script
8. `files.py` — leitura e escrita de arquivos
9. `type_hints.py` — tipagem estática e documentação de código
10. `input_examples.py` — leitura de entrada do usuário (scripts interativos)

> Antes de partir para `python/http/`, garanta que está confortável com dicionários, loops e JSON — esses três aparecem em todo código que consome APIs.

---

## O que cada arquivo cobre

### `dict_examples.py`
Criação, acesso com `[]` e `.get()`, adição, remoção, iteração com `.items()`, dicts aninhados, `.update()` e dict comprehension.

### `if_else.py`
Estrutura `if / elif / else`, operadores de comparação, `and / or / not`, valores truthy/falsy, operador `in` e condicional ternário.

### `input_examples.py`
Função `input()`, `.strip()` para limpar entradas, conversão de tipos e validação básica.

### `list_examples.py`
Criação, acesso por índice, slicing, `append / insert / extend`, `remove / pop / del`, `sorted()` e `sort()`, ordenação de listas de dicts e list comprehension.

### `loops_and_functions.py`
`for` com `enumerate`, iteração sobre listas de dicts, `range`, `while` com paginação, `break / continue`, list comprehension, `def`, parâmetros com valor padrão, retorno múltiplo, `*args` e `**kwargs`.

### `string_methods.py`
f-strings, `lower / upper / strip`, `startswith / endswith`, `find / replace / count`, `split / join / splitlines`, fatiamento de strings.

### `json_parsing.py`
`json.loads()` e `json.dumps()`, acesso a campos aninhados, `.get()` para campos opcionais, iteração sobre listas de objetos, `indent` e `ensure_ascii`.

### `error_handling.py`
`try / except / else / finally`, captura de erros específicos, erros comuns do `requests` (Timeout, ConnectionError, HTTPError), `raise_for_status()`, verificação manual de `status_code` e logging com `logging`.

### `files.py`
`open` com context manager, modos de abertura (`r`, `w`, `a`), leitura de texto/linhas, `json.load/dump`, `csv.DictReader/DictWriter`, `os.path` para verificações e listagem de arquivos.

### `type_hints.py`
Tipos básicos, `list[]`/`dict[]`, `Optional`, `Union`, `Any`, `TypedDict` com campos obrigatórios e opcionais, `Callable`, type alias, sintaxe moderna com `|`.

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `KeyError` | Acessar chave inexistente com `[]` | Usar `.get()` ou verificar com `in` |
| `TypeError` | Operar tipos incompatíveis (ex: `int + str`) | Converter com `int()`, `str()`, `float()` |
| `IndexError` | Acessar índice fora do range da lista | Verificar `len()` antes ou usar slicing |
| `JSONDecodeError` | String não é um JSON válido | Envolver `json.loads()` em `try/except` |
| `FileNotFoundError` | Arquivo não existe no caminho informado | Verificar com `os.path.exists()` antes de abrir |

---

## Documentação oficial

- Python: https://docs.python.org/3/tutorial/
- Biblioteca `json`: https://docs.python.org/3/library/json.html
- Biblioteca `logging`: https://docs.python.org/3/library/logging.html