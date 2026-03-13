# =============================================================================
# JSON em Python
# =============================================================================
# JSON é o formato mais comum em respostas de API. Python tem suporte nativo
# via módulo `json` — sem precisar instalar nada.
#
# Os dois movimentos principais:
#   json.loads()  →  string JSON  →  dict Python  (você recebeu da API)
#   json.dumps()  →  dict Python  →  string JSON  (você vai enviar pra API)
# =============================================================================

import json


# -----------------------------------------------------------------------------
# json.loads() — converte string JSON em dict Python
# -----------------------------------------------------------------------------

# Simula o corpo de uma resposta de API (chega como string)
resposta_api = '{"id": 101, "status": "aberto", "usuario": "Ana", "prioridade": "alta"}'

ticket = json.loads(resposta_api)

print(ticket)
# Saída: {'id': 101, 'status': 'aberto', 'usuario': 'Ana', 'prioridade': 'alta'}

print(type(ticket))
# Saída: <class 'dict'>

# Agora é um dict normal — acesse os campos com colchetes:
print(ticket["status"])     # aberto
print(ticket["usuario"])    # Ana


# -----------------------------------------------------------------------------
# Acessando campos aninhados — JSON dentro de JSON
# -----------------------------------------------------------------------------

resposta_aninhada = '''
{
    "ticket": {
        "id": 101,
        "status": "aberto"
    },
    "responsavel": {
        "nome": "Bruno",
        "email": "bruno@empresa.com"
    },
    "tags": ["urgente", "cliente-vip", "bug"]
}
'''

dados = json.loads(resposta_aninhada)

# Acessando campos aninhados — vai descendo com colchetes
print(dados["ticket"]["status"])        # aberto
print(dados["responsavel"]["email"])    # bruno@empresa.com

# Acessando lista
print(dados["tags"])                    # ['urgente', 'cliente-vip', 'bug']
print(dados["tags"][0])                 # urgente

# Iterando sobre a lista de tags
for tag in dados["tags"]:
    print(f"Tag: {tag}")


# -----------------------------------------------------------------------------
# Campos que podem não existir — .get() evita KeyError
# -----------------------------------------------------------------------------

# Se você tentar acessar uma chave que não existe com colchetes, o Python
# lança um KeyError e o script quebra.

# PERIGOSO — quebra se "sla" não existir:
# print(ticket["sla"])  →  KeyError: 'sla'

# SEGURO — retorna None se a chave não existir:
sla = ticket.get("sla")
print(sla)
# Saída: None

# Melhor ainda — define um valor padrão se a chave não existir:
sla = ticket.get("sla", "não definido")
print(sla)
# Saída: não definido

# Use .get() sempre que o campo for opcional na resposta da API.


# -----------------------------------------------------------------------------
# Lidando com listas de objetos — formato comum em APIs
# -----------------------------------------------------------------------------

resposta_lista = '''
[
    {"id": 1, "status": "aberto",   "usuario": "Ana"},
    {"id": 2, "status": "fechado",  "usuario": "Bruno"},
    {"id": 3, "status": "aberto",   "usuario": "Carlos"}
]
'''

tickets = json.loads(resposta_lista)

# tickets agora é uma lista de dicts — itere normalmente
for t in tickets:
    print(f"Ticket {t['id']} — {t['status']} ({t['usuario']})")

# Saída:
# Ticket 1 — aberto (Ana)
# Ticket 2 — fechado (Bruno)
# Ticket 3 — aberto (Carlos)

# Filtrar só os abertos:
abertos = [t for t in tickets if t["status"] == "aberto"]
print(f"{len(abertos)} tickets abertos")
# Saída: 2 tickets abertos


# -----------------------------------------------------------------------------
# json.dumps() — converte dict Python em string JSON
# -----------------------------------------------------------------------------

# Útil quando você precisa montar o corpo de uma requisição POST
payload = {
    "titulo": "Erro ao fazer login",
    "prioridade": "alta",
    "usuario_id": 42
}

payload_json = json.dumps(payload)
print(payload_json)
# Saída: {"titulo": "Erro ao fazer login", "prioridade": "alta", "usuario_id": 42}

print(type(payload_json))
# Saída: <class 'str'>

# indent= deixa o JSON formatado e legível (bom pra debug)
print(json.dumps(payload, indent=4))
# Saída:
# {
#     "titulo": "Erro ao fazer login",
#     "prioridade": "alta",
#     "usuario_id": 42
# }

# ensure_ascii=False preserva caracteres especiais como acentos
payload_com_acento = {"mensagem": "Solicitação recebida"}
print(json.dumps(payload_com_acento, ensure_ascii=False))
# Saída: {"mensagem": "Solicitação recebida"}


# -----------------------------------------------------------------------------
# Na prática com requests — você raramente usa json.loads() diretamente
# -----------------------------------------------------------------------------

# A biblioteca requests já converte o JSON da resposta pra você:
#
#   import requests
#   resposta = requests.get("https://api.exemplo.com/tickets/101")
#   ticket = resposta.json()   ← equivale a json.loads(resposta.text)
#
# Mas entender json.loads() é importante pra quando você precisar
# processar strings JSON que não vieram direto de um requests.


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def extrair_tickets_abertos(json_str):
    """
    Recebe uma string JSON com lista de tickets.
    Retorna uma lista de dicts apenas com os tickets abertos,
    incluindo somente os campos relevantes.
    """
    tickets = json.loads(json_str)

    resultado = []
    for t in tickets:
        if t.get("status") == "aberto":
            resultado.append({
                "id":       t["id"],
                "usuario":  t.get("usuario", "desconhecido"),
                "sla":      t.get("sla", "não definido"),   # campo opcional
            })

    return resultado


dados_brutos = '''
[
    {"id": 1, "status": "aberto",  "usuario": "Ana",    "sla": "4h"},
    {"id": 2, "status": "fechado", "usuario": "Bruno"},
    {"id": 3, "status": "aberto",  "usuario": "Carlos"}
]
'''

abertos = extrair_tickets_abertos(dados_brutos)
print(json.dumps(abertos, indent=4, ensure_ascii=False))

# Saída:
# [
#     {
#         "id": 1,
#         "usuario": "Ana",
#         "sla": "4h"
#     },
#     {
#         "id": 3,
#         "usuario": "Carlos",
#         "sla": "não definido"
#     }
# ]