# curl_cffi

## O que é TLS fingerprint?

Quando seu navegador se conecta a um site via HTTPS, ele faz um "aperto de mão" (handshake) com o servidor. Durante esse handshake, o cliente envia informações técnicas sobre si mesmo — algoritmos suportados, versão do protocolo, ordem das opções. Esse conjunto de informações forma uma "impressão digital" (fingerprint) única.

Sites com proteção anti-bot analisam esse fingerprint e conseguem identificar que a requisição veio de um script Python (requests) e não de um Chrome real — e bloqueiam.

O `curl_cffi` resolve isso simulando exatamente o fingerprint de um navegador real, tornando a requisição indistinguível de um usuário abrindo o site no Chrome.

---Biblioteca HTTP que usa libcurl internamente. A API é quase idêntica ao `requests` — a diferença está em dois parâmetros extras: `impersonate` e `http_version`.

```bash
pip install curl_cffi python-dotenv
```

---

## Quando usar curl_cffi em vez de requests

| Situação | requests | curl_cffi |
|---|---|---|
| API REST simples sem proteção | ✓ | ✓ |
| API que bloqueia por TLS fingerprint | ✗ | ✓ |
| Precisa de HTTP/2 ou HTTP/3 | ✗ | ✓ |
| Scraping com detecção de bot | ✗ | ✓ |
| WAF ou Cloudflare bloqueando | ✗ | ✓ |

Se `requests` funciona, não há motivo para trocar.

---

## Estrutura

```text
curl_cffi/
├── Readme.md
└── examples/
    ├── get_request.py       — GET, params, paginação, Session
    ├── post_form_data.py    — POST form-data, OAuth2, upload de arquivo
    └── post_json.py         — POST/PATCH/DELETE com JSON
```

---

## Referência rápida

### GET

```python
from curl_cffi import requests

response = requests.get(
    "https://api.exemplo.com/tickets",
    headers={"Authorization": "Bearer TOKEN"},
    params={"status": "aberto"},
    impersonate="chrome",
    http_version="v2",
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
    impersonate="chrome",
    timeout=5
)
```

---

## Parâmetros exclusivos do curl_cffi

### `impersonate`

Simula um navegador real — altera TLS fingerprint, headers e comportamento da conexão.

| Valor | Navegador simulado |
|---|---|
| `"chrome"` | Chrome (versão mais recente) |
| `"chrome110"` | Chrome versão 110 |
| `"safari"` | Safari (versão mais recente) |
| `"safari15_5"` | Safari versão 15.5 |
| `"edge"` | Edge (versão mais recente) |
| `"firefox"` | Firefox (versão mais recente) |

Use `"chrome"` na maioria dos casos — é o mais comum e bem mantido.

### `http_version`

| Valor | Protocolo |
|---|---|
| `"v1"` | HTTP/1.1 |
| `"v2"` | HTTP/2 |
| `"v3"` | HTTP/3 (quando suportado pelo servidor) |

### `response.http_version`

Campo exclusivo do curl_cffi — informa qual protocolo foi efetivamente usado na conexão.

```python
print(response.http_version)   # "2" ou "3"
```

---

## Tratamento de erros

Igual ao `requests`:

```python
try:
    response = requests.get(url, impersonate="chrome", timeout=5)
    response.raise_for_status()
    return response.json()

except requests.exceptions.Timeout:
    print("Timeout.")

except requests.exceptions.ConnectionError:
    print("Falha de conexão.")

except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP {e.response.status_code}: {e}")

except Exception as e:
    print(f"Erro inesperado: {e}")
```

> curl_cffi não tem subclasses tão específicas quanto o `requests`.
> Use `Exception` como fallback para erros não mapeados.

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `ImpersonateError` | Valor de `impersonate` inválido | Usar um dos valores da tabela acima |
| Ainda bloqueado com `impersonate` | Site usa detecção mais avançada (JS, comportamento) | curl_cffi resolve TLS — JS challenge precisa de Playwright/Selenium |
| `JSONDecodeError` | Resposta não é JSON | Verificar `response.text` antes de `.json()` |
| `204` quebrando em `.json()` | Resposta sem corpo | Checar `status_code` antes de chamar `.json()` |