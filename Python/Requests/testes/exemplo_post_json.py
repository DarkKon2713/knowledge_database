# Importa a biblioteca requests
# Usada para fazer requisições HTTP para APIs
import requests


# API de teste que aceita POST e devolve os dados enviados
URL_POST = "https://httpbin.org/post"


def exemplo_post_json():
    """
    Exemplo de requisição POST enviando um payload JSON.

    Quando usamos o parâmetro json= no requests:

    1) Um dict Python é convertido automaticamente para JSON
    2) O header "Content-Type: application/json" é adicionado automaticamente
    3) O corpo da requisição é enviado em formato JSON
    """

    # Payload que será enviado para a API
    # Em Python usamos um dict
    payload = {
        "usuario": "leonardo",
        "senha": "123456",
        "ativo": True,
        "roles": ["admin", "dev"]
    }

    # Faz a requisição POST enviando JSON
    # O requests converte automaticamente o dict para JSON
    response = requests.post(URL_POST, json=payload)

    # Converte a resposta da API para um dict Python
    resultado = response.json()

    print("\n====== EXEMPLO - POST COM JSON ======\n")

    # Código HTTP retornado pela API
    print(f"Status HTTP: {response.status_code}")

    # Mostra o payload original em Python
    print("\nPayload enviado (dict Python):")
    print(payload)

    # Mostra o header Content-Type que foi enviado
    print("\nHeader Content-Type enviado:")
    print(response.request.headers["Content-Type"])

    # httpbin retorna os dados recebidos dentro do campo "json"
    print("\nJSON recebido pela API:")
    print(resultado["json"])

    # Mostra a resposta completa da API
    print("\nResposta completa da API:")
    print(resultado)


# Executa apenas se o arquivo for rodado diretamente
if __name__ == "__main__":
    exemplo_post_json()