# requests

## O que é uma API REST?

API REST é uma forma padronizada de sistemas se comunicarem pela internet via HTTP. Você envia uma requisição com um método (verbo) e uma URL, e recebe uma resposta — geralmente em JSON.

## O que significa cada método HTTP?

| Método | Significado | Exemplo |
|---|---|---|
| `GET` | Buscar dados — não modifica nada | Listar tickets, buscar um usuário |
| `POST` | Criar um novo recurso | Criar ticket, enviar formulário |
| `PATCH` | Atualizar parcialmente um recurso existente | Mudar só o status de um ticket |
| `PUT` | Substituir um recurso inteiro | Reescrever todos os dados de um ticket |
| `DELETE` | Remover um recurso | Deletar um ticket |

---

Biblioteca HTTP para Python. A mais usada para consumir APIs REST.

```bash
pip install requests python-dotenv
```

---

## Estrutura

```text
requests/
├── Readme.md
└── examples/
    ├── get_request.py       — GET, params, paginação, Session
    ├── post_form_data.py    — POST form-data, OAuth2, upload de arquivo
    └── post_json.py         — POST/PUT/PATCH/DELETE com JSON
```

---

## Referência rápida

### GET

```python
import requests

response = requests.get(
    "https://api.exemplo.com/tickets",
    headers={"Authorization": "Bearer TOKEN"},
    params={"status": "aberto", "page": 1},
    timeout=5
)
response.raise_for_status()
dados = response.json()
```

### POST JSON

```python
response = requests.post(
    "https://api.exemplo.com/tickets",
    headers={"Authorization": "Bearer TOKEN"},
    json={"titulo": "Erro ao logar", "prioridade": "alta"},
    timeout=5
)
```

### PATCH

```python
response = requests.patch(
    "https://api.exemplo.com/tickets/101",
    headers={"Authorization": "Bearer TOKEN"},
    json={"status": "fechado"},
    timeout=5
)
```

### DELETE

```python
response = requests.delete(
    "https://api.exemplo.com/tickets/101",
    headers={"Authorization": "Bearer TOKEN"},
    timeout=5
)
# 204 = sucesso sem corpo — não chame .json()
```

---

## Objeto Response — campos principais

| Campo | Tipo | Descrição |
|---|---|---|
| `response.status_code` | `int` | Código HTTP da resposta |
| `response.json()` | `dict` / `list` | Corpo da resposta convertido |
| `response.text` | `str` | Corpo da resposta como string |
| `response.content` | `bytes` | Corpo da resposta como bytes |
| `response.headers` | `dict` | Cabeçalhos da resposta |
| `response.url` | `str` | URL final (após redirecionamentos) |

---

## Tratamento de erros

```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

except requests.exceptions.Timeout:
    print("Timeout — servidor demorou mais de 5s.")

except requests.exceptions.ConnectionError:
    print("Falha de conexão.")

except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP {e.response.status_code}: {e}")

except requests.exceptions.RequestException as e:
    print(f"Erro inesperado: {e}")
```

> `raise_for_status()` lança `HTTPError` para qualquer status 4xx ou 5xx.
> Sem ele, o código continua mesmo com erro.

---

## Códigos de status mais comuns

| Código | Significado | O que fazer |
|---|---|---|
| `200` | OK | Processar normalmente |
| `201` | Criado | Recurso criado com sucesso |
| `204` | Sem conteúdo | Sucesso — não chamar `.json()` |
| `400` | Dados inválidos | Verificar o payload enviado |
| `401` | Não autorizado | Verificar token no `.env` |
| `403` | Sem permissão | Token válido mas sem acesso |
| `404` | Não encontrado | Verificar ID ou URL |
| `422` | Erro de validação | API rejeitou os dados — ver corpo do erro |
| `429` | Rate limit | Aguardar antes de tentar novamente |
| `500` | Erro no servidor | Problema na API — não é culpa do seu código |

---

## data= vs json=

| Parâmetro | Content-Type | Quando usar |
|---|---|---|
| `json=payload` | `application/json` | APIs REST modernas (maioria) |
| `data=payload` | `application/x-www-form-urlencoded` | OAuth2, formulários, sistemas legados |
| `files=payload` | `multipart/form-data` | Upload de arquivos |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `ConnectionError` | URL errada ou sem internet | Verificar `API_URL` no `.env` |
| `Timeout` | Sem `timeout=` ou servidor lento | Sempre passar `timeout=5` |
| `JSONDecodeError` | Resposta não é JSON válido | Verificar `response.text` antes de `.json()` |
| `KeyError` no `.json()` | Campo não existe na resposta | Usar `.get()` com valor padrão |
| `401` em toda requisição | Token inválido ou expirado | Verificar `API_TOKEN` no `.env` |
| `204` quebrando em `.json()` | Resposta sem corpo | Verificar `status_code` antes de chamar `.json()` |