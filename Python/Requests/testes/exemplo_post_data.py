# Importa a biblioteca requests
# Usada para fazer requisições HTTP (GET, POST, PUT, DELETE, etc)
import requests


# API de teste que aceita requisições POST
# e devolve os dados que foram enviados
URL_POST = "https://httpbin.org/post"


def _exemplo_post_data():
    """
    Exemplo de requisição POST usando o parâmetro 'data'.

    No Python enviamos um dicionário (dict), porém a biblioteca requests
    converte automaticamente esse dicionário para o formato:

    Esse formato é o mesmo utilizado por formulários HTML.
    """

    # Payload enviado na requisição
    # Aqui usamos um dict Python
    payload = {
        "usuario": "leonardo",
        "senha": "123456"
    }

    # Quando usamos data=payload o requests converte o dict para:
    # usuario=leonardo&senha=123456
    response = requests.post(URL_POST, data=payload)

    # Converte a resposta da API para um dicionário Python
    resultado = response.json()

    print("\n====== EXEMPLO - POST COM DATA ======\n")

    print(f"Status HTTP: {response.status_code}")

    print("\nPayload enviado (dict Python):")
    print(payload)

    print("\nComo o servidor recebeu os dados (form-data):")
    print(resultado["form"])

    print("\nResposta completa da API:")
    print(resultado)


# Executa apenas se o arquivo for rodado diretamente
if __name__ == "__main__":
    _exemplo_post_data()