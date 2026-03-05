# Importa a implementação de requests da biblioteca curl_cffi
# Ela possui API muito parecida com o requests tradicional,
# mas utiliza libcurl internamente.
from curl_cffi import requests


# API de teste que aceita requisições POST
# e devolve os dados que foram enviados
URL_POST = "https://httpbin.org/post"


def _exemplo_post_data():
    """
    Exemplo de requisição POST usando o parâmetro 'data'
    com curl_cffi.

    Assim como no requests tradicional, quando usamos:

        data=payload

    e payload é um dict Python, a biblioteca converte automaticamente
    para o formato:

        application/x-www-form-urlencoded

    Exemplo enviado na requisição HTTP:

        usuario=leonardo&senha=123456

    Esse é o mesmo formato usado por formulários HTML.
    """

    # Payload enviado na requisição
    payload = {
        "usuario": "leonardo",
        "senha": "123456"
    }

    # Faz a requisição POST
    response = requests.post(
        url=URL_POST,

        # Dados enviados como form-data
        data=payload,

        # Simula um navegador real (muda TLS fingerprint e headers)
        impersonate="chrome",

        # Define a versão do protocolo HTTP
        # v1 = HTTP/1.1
        # v2 = HTTP/2
        # v3 = HTTP/3 (quando suportado)
        http_version="v2"
    )

    # Converte a resposta da API para dict Python
    resultado = response.json()

    print("\n====== EXEMPLO - POST COM DATA (curl_cffi) ======\n")

    print(f"Status HTTP: {response.status_code}")

    print("\nVersão HTTP usada:")
    print(response.http_version)

    print("\nPayload enviado (dict Python):")
    print(payload)

    print("\nHeader Content-Type enviado:")
    print(response.request.headers.get("Content-Type"))

    # httpbin devolve os dados recebidos dentro de "form"
    print("\nComo o servidor recebeu os dados (form-data):")
    print(resultado["form"])

    print("\nResposta completa da API:")
    print(resultado)


# Executa apenas se o script for rodado diretamente
if __name__ == "__main__":
    _exemplo_post_data()