# Biblioteca Python curl_cffi

## Introdução

`curl_cffi` é uma biblioteca Python que permite fazer requisições HTTP
utilizando o **libcurl** através de **CFFI (C Foreign Function
Interface)**.

Ela foi criada para oferecer:

-   alta performance
-   suporte a protocolos modernos
-   melhor compatibilidade com sites que bloqueiam bots

Uma das principais vantagens é que ela consegue **imitar navegadores
reais**, algo que bibliotecas como `requests` nem sempre conseguem.

Isso torna `curl_cffi` muito útil para:

-   scraping avançado
-   bypass de bloqueios simples
-   automação web
-   requisições HTTP de alta performance

------------------------------------------------------------------------

# Instalação

A instalação é feita via pip.

``` bash
pip install curl_cffi
```

Depois disso a biblioteca pode ser importada no Python.

``` python
from curl_cffi import requests
```

A API foi projetada para ser **muito parecida com a biblioteca
requests**.

------------------------------------------------------------------------

# Primeiro Exemplo

``` python
from curl_cffi import requests

r = requests.get("https://httpbin.org/get")

print(r.status_code)
print(r.text)
```

Explicação:

-   `requests.get()` faz uma requisição HTTP GET
-   `status_code` mostra o código de resposta
-   `text` contém o conteúdo retornado pelo servidor

------------------------------------------------------------------------

# Diferença entre curl_cffi e requests

  Biblioteca   Base          Objetivo
  ------------ ------------- -------------------------------
  requests     Python puro   simplicidade
  curl_cffi    libcurl (C)   performance e compatibilidade

`curl_cffi` usa internamente o **libcurl**, que é a mesma tecnologia
usada por:

-   curl (linha de comando)
-   navegadores
-   ferramentas de rede

------------------------------------------------------------------------

# Fazendo Requisições GET

``` python
from curl_cffi import requests

response = requests.get(
    "https://api.github.com/repos/python/cpython"
)

print(response.status_code)
print(response.json())
```

A função `json()` converte automaticamente a resposta JSON para um
dicionário Python.

------------------------------------------------------------------------

# Enviando Parâmetros (Query Params)

``` python
from curl_cffi import requests

params = {
    "q": "python",
    "sort": "stars"
}

r = requests.get(
    "https://api.github.com/search/repositories",
    params=params
)

print(r.url)
```

A URL final será:

    https://api.github.com/search/repositories?q=python&sort=stars

------------------------------------------------------------------------

# Enviando Dados com POST

``` python
from curl_cffi import requests

data = {
    "username": "admin",
    "password": "123"
}

r = requests.post(
    "https://httpbin.org/post",
    data=data
)

print(r.json())
```

POST é usado quando precisamos **enviar dados para o servidor**.

------------------------------------------------------------------------

# Enviando JSON

``` python
from curl_cffi import requests

payload = {
    "nome": "Nemo",
    "tipo": "Peixe"
}

r = requests.post(
    "https://httpbin.org/post",
    json=payload
)

print(r.json())
```

Quando usamos `json=`:

-   o dicionário é convertido automaticamente
-   o header `Content-Type: application/json` é enviado

------------------------------------------------------------------------

# Headers HTTP

Headers permitem enviar informações adicionais na requisição.

Exemplo:

``` python
from curl_cffi import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

r = requests.get(
    "https://httpbin.org/headers",
    headers=headers
)

print(r.json())
```

Headers comuns:

  Header          Uso
  --------------- ---------------------------
  User-Agent      identificar cliente
  Accept          tipo de resposta esperado
  Authorization   autenticação

------------------------------------------------------------------------

# Simulando Navegadores

Uma das funcionalidades mais poderosas do `curl_cffi` é **impersonar
navegadores**.

Isso ajuda a evitar bloqueios de scraping.

Exemplo:

``` python
from curl_cffi import requests

r = requests.get(
    "https://example.com",
    impersonate="chrome110"
)

print(r.status_code)
```

Isso faz a requisição parecer que veio do **Chrome versão 110**.

Outros exemplos:

    chrome110
    chrome120
    safari15
    edge101

------------------------------------------------------------------------

# Sessões

Sessões permitem reutilizar conexão e manter cookies.

``` python
from curl_cffi import requests

session = requests.Session()

session.get("https://httpbin.org/cookies/set/test/123")

r = session.get("https://httpbin.org/cookies")

print(r.text)
```

Benefícios:

-   reutilização de conexão
-   persistência de cookies
-   melhor performance

------------------------------------------------------------------------

# Timeout

Sempre defina timeout para evitar travamentos.

``` python
from curl_cffi import requests

r = requests.get(
    "https://httpbin.org/delay/2",
    timeout=5
)

print(r.status_code)
```

------------------------------------------------------------------------

# Tratamento de Erros

``` python
from curl_cffi import requests

try:

    r = requests.get("https://api.github.com", timeout=5)

    r.raise_for_status()

    print(r.json())

except Exception as e:

    print("Erro:", e)
```

------------------------------------------------------------------------

# Upload de Arquivos

``` python
from curl_cffi import requests

files = {
    "file": open("arquivo.txt", "rb")
}

r = requests.post(
    "https://httpbin.org/post",
    files=files
)

print(r.status_code)
```

`rb` significa **read binary**.

------------------------------------------------------------------------

# Vantagens do curl_cffi

Principais vantagens:

-   usa libcurl (muito estável)
-   consegue imitar navegadores
-   maior compatibilidade com sites protegidos
-   suporte melhor a HTTP2
-   mais rápido em algumas situações

------------------------------------------------------------------------

# Quando usar curl_cffi

Use quando:

-   sites bloqueiam `requests`
-   precisa imitar navegador
-   scraping avançado
-   alta performance em requisições

Para automação simples, `requests` ainda é suficiente.

------------------------------------------------------------------------

# Mini Exemplo Real

Buscar informações de um repositório do GitHub.

``` python
from curl_cffi import requests

url = "https://api.github.com/repos/python/cpython"

r = requests.get(url)

data = r.json()

print("Nome:", data["name"])
print("Stars:", data["stargazers_count"])
print("URL:", data["html_url"])
```

Saída exemplo:

    Nome: cpython
    Stars: 60000
    URL: https://github.com/python/cpython
