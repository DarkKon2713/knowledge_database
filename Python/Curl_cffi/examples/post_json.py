# Importa a implementação de requests da biblioteca curl_cffi
# Ela funciona de forma parecida com a biblioteca requests tradicional,
# porém usa libcurl internamente (mais próximo do comportamento de navegadores).
from curl_cffi import requests


# API de teste que aceita POST e devolve os dados enviados
URL_POST = "https://httpbin.org/post"


def exemplo_post_json():
    """
    Exemplo de requisição POST enviando um payload JSON usando curl_cffi.

    Quando usamos o parâmetro json= :

    1) Um dict Python é convertido automaticamente para JSON
    2) O header "Content-Type: application/json" é adicionado automaticamente
    3) O corpo da requisição é enviado em formato JSON
    """

    # Payload que será enviado para a API
    payload = {
        "usuario": "leonardo",
        "senha": "123456",
        "ativo": True,
        "roles": ["admin", "dev"]
    }

    # Faz a requisição POST enviando JSON
    response = requests.post(
        url=URL_POST,

        # O dict Python será convertido automaticamente para JSON
        json=payload,

        # Simula requisição de um navegador real
        # Isso altera headers, TLS fingerprint e outros detalhes
        impersonate="chrome",

        # Define qual versão do HTTP será usada
        # v1 = HTTP/1.1
        # v2 = HTTP/2
        # v3 = HTTP/3 (quando suportado)
        http_version="v2"
    )

    # Converte a resposta da API para um dict Python
    resultado = response.json()

    print("\n====== EXEMPLO - POST COM JSON (curl_cffi) ======\n")

    # Código HTTP retornado pela API
    print(f"Status HTTP: {response.status_code}")

    # Mostra a versão HTTP usada
    print("\nVersão HTTP utilizada:")
    print(response.http_version)

    # Mostra o payload original em Python
    print("\nPayload enviado (dict Python):")
    print(payload)

    # Mostra o header Content-Type enviado na requisição
    print("\nHeader Content-Type enviado:")
    print(response.request.headers.get("Content-Type"))

    # httpbin retorna os dados recebidos dentro do campo "json"
    print("\nJSON recebido pela API:")
    print(resultado["json"])

    # Mostra a resposta completa da API
    print("\nResposta completa da API:")
    print(resultado)


# Executa apenas se o arquivo for rodado diretamente
if __name__ == "__main__":
    exemplo_post_json()