# Importa a versão requests da biblioteca curl_cffi
# Ela é compatível com a API do requests tradicional
from curl_cffi import requests


# URL usada no teste
URL_TESTE = "https://api.ipify.org/?format=json"


def exemplo_get_http_version_impersonate():
    """
    Exemplo de requisição GET usando curl_cffi
    demonstrando:

    - impersonate (simular navegador)
    - http_version (forçar versão do protocolo HTTP)
    """

    # Faz a requisição GET
    response = requests.get(
        url=URL_TESTE,

        # Simula uma requisição vinda de um navegador real
        # Isso altera headers, TLS fingerprint e comportamento
        impersonate="chrome",

        # Define qual versão do protocolo HTTP usar
        # Opções comuns:
        # "v1"   -> HTTP/1.1
        # "v2"   -> HTTP/2
        # "v3"   -> HTTP/3 (quando suportado)
        http_version="v2"
    )

    # Informações da resposta
    status = response.status_code
    texto = response.text
    headers = response.headers
    url = response.url
    json_data = response.json()

    print("\n====== EXEMPLO GET COM curl_cffi ======\n")

    print(f"Status HTTP: {status}")

    print("\nURL final:")
    print(url)

    print("\nVersão HTTP utilizada:")
    print(response.http_version)

    print("\nHeaders da resposta:")
    print(headers)

    print("\nResposta em texto:")
    print(texto)

    print("\nResposta convertida para JSON:")
    print(json_data)


if __name__ == "__main__":
    exemplo_get_http_version_impersonate()