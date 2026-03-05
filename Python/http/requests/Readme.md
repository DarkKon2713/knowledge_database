# Biblioteca Python Requests --- Guia Didático

### O que é uma requisição HTTP

Quando você acessa um site no navegador, seu computador envia uma
requisição para um servidor na internet.

Fluxo simplificado:

    Seu computador ---- HTTP Request ----> Servidor
    Seu computador <---- HTTP Response ---- Servidor

### O que é HTTP

HTTP significa **HyperText Transfer Protocol**.\
É o protocolo usado para comunicação entre clientes (navegadores,
scripts, aplicativos) e servidores web.

### O que significa GET

GET é um método HTTP usado para **buscar informações**.

Exemplos:

    GET /users
    GET /posts
    GET /repos

### O que é uma API

API significa **Application Programming Interface**.

É uma interface que permite que programas conversem entre si.

Exemplo:

    https://api.github.com/users/octocat

Isso retorna dados estruturados que um programa pode usar.

### O que significa código 200

Servidores retornam códigos de status HTTP.

|Código |   Significado      |
| ----- | -------------------|
| 200   |   Sucesso          |
| 201   |   Criado           |
| 400   |   Erro do cliente  |
| 401   |   Não autorizado   |
| 403   |   Proibido         |
| 404   |   Não encontrado   |
| 500   |   Erro no servidor |


## 1. Instalação e Primeiro Passo

A biblioteca `requests` não vem instalada por padrão no Python.

Instalação:

``` bash
pip install requests
```

Primeiro teste:

``` python
import requests

# Faz uma requisição GET para a API do GitHub
r = requests.get('https://api.github.com')

# Imprime o código da resposta
print(r.status_code)
```

# 2. O Objeto Response

Quando fazemos:

``` python
r = requests.get(url)
```

`r` é um objeto **Response** que contém todos os dados da resposta.

### status_code

``` python
import requests

r = requests.get("https://api.github.com")
print(r.status_code)
```

### text

Retorna o conteúdo da resposta como texto.

``` python
print(r.text)
```

### json()

Converte automaticamente JSON em um dicionário Python.

``` python
dados = r.json()

print(dados)
print(dados["current_user_url"])
```

### headers

Headers são metadados da resposta.

``` python
print(r.headers)
print(r.headers["Content-Type"])
```

------------------------------------------------------------------------

# 3. Parâmetros de Query (GET)

Algumas URLs possuem parâmetros para filtrar dados.

Exemplo:

    https://api.github.com/search/repositories?q=python&sort=stars

Uso com requests:

``` python
import requests

payload = {
    'q': 'python',
    'sort': 'stars'
}

r = requests.get(
    'https://api.github.com/search/repositories',
    params=payload
)

print(r.url)
```

Saída:

    https://api.github.com/search/repositories?q=python&sort=stars

### Por que usar params

Errado:

``` python
url = "https://api.github.com/search?q=python&sort=stars"
```

Certo:

``` python
params = {"q": "python", "sort": "stars"}
```

`requests` monta a URL automaticamente e evita erros.

------------------------------------------------------------------------

# 4. Enviando Dados (POST)

GET busca dados.\
POST envia dados.

### Form Data

``` python
import requests

r = requests.post(
    'https://httpbin.org/post',
    data={'chave': 'valor'}
)

print(r.json())
```

### JSON (APIs modernas)

``` python
dados = {
    "nome": "Nemo",
    "tipo": "Peixe"
}

r = requests.post(
    'https://httpbin.org/post',
    json=dados
)

print(r.json())
```

### O que é JSON

JSON significa **JavaScript Object Notation**.

Exemplo:

``` json
{
 "nome": "João",
 "idade": 30
}
```

No Python:

``` python
{
 "nome": "João",
 "idade": 30
}
```

### Header Content-Type

Quando enviamos JSON:

    Content-Type: application/json

Ao usar `json=` o requests adiciona esse header automaticamente.

------------------------------------------------------------------------

# 5. Headers Personalizados

Headers são informações extras enviadas na requisição.

Exemplo:

    User-Agent
    Accept
    Authorization

Exemplo em código:

``` python
headers = {
    'User-Agent': 'MeuApp/1.0',
    'Accept': 'application/json'
}

r = requests.get(
    "https://api.github.com",
    headers=headers
)

print(r.status_code)
```

Alguns sites bloqueiam requisições sem User-Agent para evitar bots.

------------------------------------------------------------------------

# 6. Autenticação

### Basic Auth

``` python
from requests.auth import HTTPBasicAuth
import requests

r = requests.get(
    "https://httpbin.org/basic-auth/user/pass",
    auth=HTTPBasicAuth('user','pass')
)

print(r.status_code)
```

### Bearer Token

``` python
headers = {
    "Authorization": "Bearer SEU_TOKEN"
}

r = requests.get(url, headers=headers)
```

Uso comum:

  Tipo           Uso
  -------------- -----------------------------
  Basic Auth     Sistemas antigos
  Bearer Token   APIs modernas
  OAuth          Login com serviços externos

------------------------------------------------------------------------

# 7. Sessions

Sessões permitem manter informações entre requisições.

``` python
import requests

s = requests.Session()

# simula login
s.post(
    'https://httpbin.org/post',
    data={'user':'admin'}
)

# requisição após login
r = s.get('https://httpbin.org/get')

print(r.status_code)
```

Sessões mantêm:

-   cookies
-   headers
-   conexão

------------------------------------------------------------------------

# 8. Timeout e Tratamento de Erros

Sempre defina timeout.

``` python
import requests

try:

    r = requests.get("https://api.github.com", timeout=3)

    r.raise_for_status()

    print(r.json())

except requests.exceptions.Timeout:
    print("Timeout")

except requests.exceptions.HTTPError as e:
    print("Erro HTTP:", e)

except requests.exceptions.RequestException as e:
    print("Erro geral:", e)
```

Tipos de erro:

  Erro               Significado
  ------------------ ------------------
  Timeout            Servidor demorou
  ConnectionError    Falha de conexão
  HTTPError          Erro HTTP
  RequestException   Erro genérico

------------------------------------------------------------------------

# 9. Upload de Arquivos

``` python
import requests

files = {
    'file': open('relatorio.pdf', 'rb')
}

r = requests.post(
    "https://httpbin.org/post",
    files=files
)

print(r.status_code)
```

`rb` significa **read binary**, necessário para arquivos.

------------------------------------------------------------------------

# 10. Boas Práticas de Produção

### Sempre usar timeout

``` python
requests.get(url, timeout=5)
```

### Usar raise_for_status()

``` python
r.raise_for_status()
```

### Usar Session

``` python
session = requests.Session()
```

### Usar variáveis de ambiente para chaves

``` python
import os

API_KEY = os.getenv("API_KEY")
```

### Usar HTTPS

Sempre prefira:

    https://

### Respeitar Rate Limits

Algumas APIs limitam requisições.

Exemplo:

    429 Too Many Requests

------------------------------------------------------------------------

# Mini Projeto

Buscar repositórios populares de Python no GitHub e salvar em JSON.

``` python
import requests
import json

url = "https://api.github.com/search/repositories"

params = {
    "q": "python",
    "sort": "stars",
    "order": "desc"
}

r = requests.get(url, params=params, timeout=5)

r.raise_for_status()

dados = r.json()

repos = dados["items"]

lista = []

for repo in repos[:10]:

    info = {
        "nome": repo["name"],
        "estrelas": repo["stargazers_count"],
        "url": repo["html_url"]
    }

    lista.append(info)

with open("repos_python.json", "w") as f:
    json.dump(lista, f, indent=4)

print("Arquivo salvo")
```
