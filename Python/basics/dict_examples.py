# =============================================================================
# Dicionários (dict) em Python
# =============================================================================
# Um dict armazena dados no formato chave: valor — estrutura idêntica ao JSON.
# É o tipo mais usado no dia a dia de quem trabalha com APIs.
# =============================================================================


# -----------------------------------------------------------------------------
# Criando um dicionário
# -----------------------------------------------------------------------------

usuario = {
    "nome": "Leonardo",
    "idade": 30,
    "ativo": True
}


# -----------------------------------------------------------------------------
# Acessando valores
# -----------------------------------------------------------------------------

# Com colchetes — lança KeyError se a chave não existir:
print(usuario["nome"])          # Leonardo

# Com .get() — retorna None se a chave não existir (sem erro):
print(usuario.get("email"))     # None

# Com .get() e valor padrão — retorna o padrão se a chave não existir:
print(usuario.get("email", "sem email"))    # sem email

# Use colchetes quando a chave é obrigatória (ausência = bug).
# Use .get() quando o campo é opcional na resposta da API.


# -----------------------------------------------------------------------------
# Adicionando e atualizando campos
# -----------------------------------------------------------------------------

# Adicionar nova chave:
usuario["email"] = "leo@email.com"

# Atualizar valor existente — mesma sintaxe:
usuario["ativo"] = False

print(usuario)
# {'nome': 'Leonardo', 'idade': 30, 'ativo': False, 'email': 'leo@email.com'}


# -----------------------------------------------------------------------------
# Removendo campos
# -----------------------------------------------------------------------------

# pop() remove e retorna o valor — útil se você precisar do valor removido:
email = usuario.pop("email")
print(email)        # leo@email.com
print(usuario)      # sem o campo "email"

# del remove sem retornar:
del usuario["idade"]


# -----------------------------------------------------------------------------
# Verificando se uma chave existe
# -----------------------------------------------------------------------------

if "nome" in usuario:
    print("Campo nome presente")

if "telefone" not in usuario:
    print("Campo telefone ausente")


# -----------------------------------------------------------------------------
# Iterando sobre um dicionário
# -----------------------------------------------------------------------------

ticket = {
    "id": 101,
    "status": "aberto",
    "prioridade": "alta",
    "usuario": "Ana"
}

# Iterar sobre as chaves:
for chave in ticket:
    print(chave)

# Iterar sobre os valores:
for valor in ticket.values():
    print(valor)

# Iterar sobre chave e valor ao mesmo tempo — o mais comum:
for chave, valor in ticket.items():
    print(f"{chave}: {valor}")

# Saída:
# id: 101
# status: aberto
# prioridade: alta
# usuario: Ana


# -----------------------------------------------------------------------------
# Dicionários aninhados — JSON dentro de JSON
# -----------------------------------------------------------------------------

resposta = {
    "ticket": {
        "id": 101,
        "status": "aberto"
    },
    "responsavel": {
        "nome": "Bruno",
        "email": "bruno@empresa.com"
    }
}

# Acesse descendo com colchetes:
print(resposta["ticket"]["status"])         # aberto
print(resposta["responsavel"]["email"])     # bruno@empresa.com

# Com .get() em múltiplos níveis — evita quebrar se algum nível não existir:
responsavel = resposta.get("responsavel", {})
email = responsavel.get("email", "sem email")
print(email)    # bruno@empresa.com


# -----------------------------------------------------------------------------
# Métodos úteis
# -----------------------------------------------------------------------------

# .keys() — lista de chaves
print(list(ticket.keys()))
# ['id', 'status', 'prioridade', 'usuario']

# .values() — lista de valores
print(list(ticket.values()))
# [101, 'aberto', 'alta', 'Ana']

# .update() — mescla outro dict (sobrescreve chaves existentes)
ticket.update({"status": "fechado", "resolucao": "problema corrigido"})
print(ticket)
# {'id': 101, 'status': 'fechado', 'prioridade': 'alta', 'usuario': 'Ana', 'resolucao': 'problema corrigido'}


# -----------------------------------------------------------------------------
# Construindo um dict dinamicamente — comum ao montar payloads de API
# -----------------------------------------------------------------------------

campos = ["id", "status", "usuario"]
valores = [101, "aberto", "Ana"]

payload = dict(zip(campos, valores))
print(payload)
# {'id': 101, 'status': 'aberto', 'usuario': 'Ana'}

# Ou com dict comprehension — equivale a uma list comprehension mas pra dicts:
tickets_por_id = {t["id"]: t for t in [
    {"id": 1, "status": "aberto"},
    {"id": 2, "status": "fechado"},
    {"id": 3, "status": "aberto"},
]}

print(tickets_por_id[2])
# {'id': 2, 'status': 'fechado'}

# Dict comprehension com filtro — só tickets abertos:
abertos = {k: v for k, v in tickets_por_id.items() if v["status"] == "aberto"}
print(abertos)
# {1: {'id': 1, 'status': 'aberto'}, 3: {'id': 3, 'status': 'aberto'}}


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def normalizar_ticket(dados_brutos):
    """
    Recebe um dict com dados de um ticket (formato variável da API).
    Retorna um dict padronizado com os campos que o sistema espera.
    """
    return {
        "id":         dados_brutos.get("id") or dados_brutos.get("ticket_id"),
        "status":     dados_brutos.get("status", "desconhecido").lower(),
        "prioridade": dados_brutos.get("prioridade", "normal"),
        "usuario":    dados_brutos.get("usuario", {}).get("nome", "não informado"),
    }


ticket_v1 = {"id": 10, "status": "Aberto", "usuario": {"nome": "Ana"}}
ticket_v2 = {"ticket_id": 11, "status": "FECHADO"}

print(normalizar_ticket(ticket_v1))
# {'id': 10, 'status': 'aberto', 'prioridade': 'normal', 'usuario': 'Ana'}

print(normalizar_ticket(ticket_v2))
# {'id': 11, 'status': 'fechado', 'prioridade': 'normal', 'usuario': 'não informado'}