# =============================================================================
# Tratamento de Erros em Python
# =============================================================================
# Erros são inevitáveis — APIs ficam fora do ar, campos chegam vazios,
# timeouts acontecem. Sem tratamento, qualquer erro derruba o script inteiro.
#
# try/except permite capturar o erro, tomar uma ação e continuar rodando.
# =============================================================================

import json
import requests


# -----------------------------------------------------------------------------
# Estrutura básica — try / except
# -----------------------------------------------------------------------------

# Sem tratamento — se "status" não existir, o script quebra aqui:
# ticket = {}
# print(ticket["status"])  →  KeyError: 'status'

# Com tratamento:
ticket = {}

try:
    print(ticket["status"])
except KeyError:
    print("Campo 'status' não encontrado no ticket.")

# O script continua rodando normalmente após o except.


# -----------------------------------------------------------------------------
# Capturando o erro para inspecionar a mensagem
# -----------------------------------------------------------------------------

try:
    valor = int("abc")          # tenta converter string inválida pra int
except ValueError as e:
    print(f"Erro de conversão: {e}")

# Saída: Erro de conversão: invalid literal for int() with base 10: 'abc'

# O `as e` captura o objeto de erro — útil pra logar a mensagem original.


# -----------------------------------------------------------------------------
# Múltiplos excepts — tratando erros diferentes de formas diferentes
# -----------------------------------------------------------------------------

def buscar_campo(dados, campo):
    try:
        valor = dados[campo]
        return int(valor)           # pode lançar ValueError se não for número
    except KeyError:
        print(f"Campo '{campo}' não existe nos dados.")
    except ValueError:
        print(f"Campo '{campo}' existe mas não é um número válido.")
    return None                     # retorna None em caso de erro


print(buscar_campo({"id": "42"},  "id"))        # 42
print(buscar_campo({"id": "abc"}, "id"))        # ValueError
print(buscar_campo({},            "id"))        # KeyError


# -----------------------------------------------------------------------------
# else — executado só se nenhum erro ocorreu
# -----------------------------------------------------------------------------

try:
    dados = json.loads('{"id": 1, "status": "aberto"}')
except json.JSONDecodeError as e:
    print(f"JSON inválido: {e}")
else:
    # só chega aqui se o json.loads() funcionou sem erro
    print(f"JSON lido com sucesso. Status: {dados['status']}")


# -----------------------------------------------------------------------------
# finally — executado sempre, com ou sem erro
# -----------------------------------------------------------------------------

# Útil para fechar conexões, arquivos ou logar que o bloco terminou.

try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Divisão por zero.")
finally:
    print("Bloco finalizado.")     # sempre executa

# Saída:
# Divisão por zero.
# Bloco finalizado.


# -----------------------------------------------------------------------------
# Erros comuns com requisições HTTP
# -----------------------------------------------------------------------------

def fazer_requisicao(url):
    try:
        resposta = requests.get(url, timeout=5)

        # status_code fora do range 2xx não lança exceção por padrão —
        # raise_for_status() faz isso por você
        resposta.raise_for_status()

        return resposta.json()

    except requests.exceptions.Timeout:
        print(f"Timeout: a requisição para {url} demorou mais de 5 segundos.")

    except requests.exceptions.ConnectionError:
        print(f"Erro de conexão: não foi possível alcançar {url}.")

    except requests.exceptions.HTTPError as e:
        # capturado pelo raise_for_status() — ex: 404, 500, 403
        print(f"Erro HTTP {e.response.status_code}: {e}")

    except requests.exceptions.RequestException as e:
        # captura qualquer outro erro do requests não tratado acima
        print(f"Erro inesperado na requisição: {e}")

    return None


# -----------------------------------------------------------------------------
# Verificando status_code manualmente — mais controle que raise_for_status()
# -----------------------------------------------------------------------------

def buscar_ticket(ticket_id):
    url = f"https://api.exemplo.com/tickets/{ticket_id}"

    try:
        resposta = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Falha na requisição: {e}")
        return None

    if resposta.status_code == 200:
        return resposta.json()
    elif resposta.status_code == 404:
        print(f"Ticket {ticket_id} não encontrado.")
    elif resposta.status_code == 401:
        print("Não autorizado. Verifique o token de autenticação.")
    elif resposta.status_code == 429:
        print("Rate limit atingido. Aguarde antes de tentar novamente.")
    else:
        print(f"Erro inesperado: status {resposta.status_code}")

    return None


# -----------------------------------------------------------------------------
# Logar erros em vez de só printar — bom para scripts em produção
# -----------------------------------------------------------------------------

import logging

# Configuração básica: exibe timestamp, nível e mensagem
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def processar_ticket(ticket_id):
    url = f"https://api.exemplo.com/tickets/{ticket_id}"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        logging.info(f"Ticket {ticket_id} carregado com sucesso.")
        return dados

    except requests.exceptions.Timeout:
        logging.warning(f"Timeout ao buscar ticket {ticket_id}.")

    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro HTTP ao buscar ticket {ticket_id}: {e}")

    except Exception as e:
        # Exception genérica como último recurso — nunca deixe cair sem log
        logging.exception(f"Erro inesperado ao processar ticket {ticket_id}: {e}")

    return None

# Níveis de log (do menos pro mais grave):
#   logging.debug()     → detalhes internos, só em desenvolvimento
#   logging.info()      → fluxo normal, confirmações
#   logging.warning()   → algo errado mas o script continua
#   logging.error()     → erro que impediu uma ação
#   logging.exception() → igual error, mas inclui o traceback completo


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def processar_lista_tickets(ids):
    """
    Recebe uma lista de IDs de tickets.
    Tenta processar cada um — erros em um ticket não param os outros.
    Retorna um resumo com sucessos e falhas.
    """
    sucesso = []
    falha   = []

    for ticket_id in ids:
        url = f"https://api.exemplo.com/tickets/{ticket_id}"
        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()

            dados = resposta.json()
            sucesso.append(ticket_id)
            logging.info(f"Ticket {ticket_id} processado: status={dados.get('status')}")

        except requests.exceptions.Timeout:
            falha.append(ticket_id)
            logging.warning(f"Timeout no ticket {ticket_id}.")

        except requests.exceptions.HTTPError as e:
            falha.append(ticket_id)
            logging.error(f"HTTP {e.response.status_code} no ticket {ticket_id}.")

        except Exception as e:
            falha.append(ticket_id)
            logging.exception(f"Erro inesperado no ticket {ticket_id}.")

    print(f"\nResumo: {len(sucesso)} processados, {len(falha)} com falha.")
    if falha:
        print(f"IDs com falha: {falha}")

    return sucesso, falha