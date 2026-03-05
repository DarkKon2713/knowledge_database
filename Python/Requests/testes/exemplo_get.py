# Importa a biblioteca requests

import requests


# URL de teste usada no exemplo
# Essa API retorna o IP público da máquina que faz a requisição
# O parâmetro "?format=json" pede que a resposta venha no formato JSON
URL_TESTE = "https://api.ipify.org/?format=json"


def _exemplo_get():
    """
    Função que faz uma requisição HTTP GET para uma API
    e mostra diferentes informações que vêm na resposta.
    """

    # Faz uma requisição GET para a URL definida
    response = requests.get(URL_TESTE)

    # Outra forma de fazer exatamente a mesma coisa usando argumento nomeado
    response = requests.get(url=URL_TESTE)

    # Código de status HTTP da resposta
    # Exemplo: 200 (sucesso), 404 (não encontrado), 500 (erro no servidor)
    status = response.status_code

    # Conteúdo da resposta em formato texto (string)
    texto = response.text

    # Conteúdo da resposta em formato bruto (bytes)
    # Geralmente usado para arquivos ou dados binários
    content = response.content

    # Cabeçalhos HTTP da resposta
    # Contêm informações extras como tipo de conteúdo, servidor, cache etc.
    headers = response.headers

    # Cookies retornados pela resposta (se houver)
    # Alguns sites usam cookies para sessão ou autenticação
    cookies = response.cookies

    # URL final da requisição
    # Pode ser diferente da original caso tenha ocorrido redirecionamento
    url = response.url

    # Converte automaticamente o corpo da resposta para um dicionário Python
    # Isso funciona quando a resposta da API está em JSON
    json = response.json()

    # Exibe todas as informações coletadas
    # f-string permite inserir variáveis dentro da string
    # type() mostra o tipo da variável
    print(f"""
        Status:(Tipo: {type(status)}) {status} 
        URL:(Tipo: {type(url)}) {url} 
        Cookies:(Tipo: {type(cookies)}) {cookies} 
        Content:(Tipo: {type(content)}) {content} 
        Texto:(Tipo: {type(texto)}\n) {texto} 
        Headers:(Tipo: {type(headers)}) {headers} 
        JSON:(Tipo: {type(json)}) {json} 
    """)


# Esse bloco garante que o código abaixo só será executado
# se o arquivo for executado diretamente
# (e não quando ele for importado como módulo em outro script)
if __name__ == "__main__":
    _exemplo_get()