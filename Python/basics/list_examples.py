# =============================================================================
# Listas (list) em Python
# =============================================================================
# Lista é uma coleção ordenada e mutável de itens.
# É o tipo mais comum pra representar arrays de dados vindos de APIs —
# lista de tickets, usuários, eventos, etc.
# =============================================================================


# -----------------------------------------------------------------------------
# Criando listas
# -----------------------------------------------------------------------------

# Lista de strings
status_validos = ["aberto", "pendente", "fechado", "cancelado"]

# Lista de dicts — formato típico de resposta de API
tickets = [
    {"id": 1, "status": "aberto",   "prioridade": "alta"},
    {"id": 2, "status": "fechado",  "prioridade": "normal"},
    {"id": 3, "status": "aberto",   "prioridade": "critica"},
]

# Lista vazia — pra ir preenchendo depois
resultado = []


# -----------------------------------------------------------------------------
# Acessando itens por índice
# -----------------------------------------------------------------------------

frutas = ["maçã", "banana", "uva", "laranja"]

print(frutas[0])    # maçã    — primeiro item
print(frutas[-1])   # laranja — último item (índice negativo conta do fim)
print(frutas[-2])   # uva     — penúltimo

# Índices começam em 0, não em 1.


# -----------------------------------------------------------------------------
# Fatiamento (slicing) — pegar um pedaço da lista
# -----------------------------------------------------------------------------

# lista[inicio:fim]  — fim não é incluído
print(frutas[1:3])      # ['banana', 'uva']
print(frutas[:2])       # ['maçã', 'banana']     — do início até índice 2
print(frutas[2:])       # ['uva', 'laranja']     — do índice 2 até o fim

# Útil pra paginação manual ou limitar resultados:
todos = list(range(100))
primeira_pagina = todos[:10]    # primeiros 10 itens


# -----------------------------------------------------------------------------
# Adicionando itens
# -----------------------------------------------------------------------------

erros = []

erros.append("Timeout na requisição")           # adiciona no fim
erros.append("Status 500 recebido")

print(erros)
# ['Timeout na requisição', 'Status 500 recebido']

# insert() adiciona em uma posição específica:
erros.insert(0, "Falha de conexão")             # adiciona no início
print(erros)
# ['Falha de conexão', 'Timeout na requisição', 'Status 500 recebido']

# extend() adiciona todos os itens de outra lista:
novos_erros = ["Rate limit", "Token expirado"]
erros.extend(novos_erros)
print(len(erros))   # 5


# -----------------------------------------------------------------------------
# Removendo itens
# -----------------------------------------------------------------------------

tags = ["urgente", "bug", "cliente-vip", "bug"]

# remove() — remove a primeira ocorrência do valor:
tags.remove("bug")
print(tags)     # ['urgente', 'cliente-vip', 'bug']

# pop() — remove pelo índice e retorna o valor:
ultimo = tags.pop()         # remove o último
print(ultimo)               # bug

tags.pop(0)                 # remove o primeiro (índice 0)
print(tags)                 # ['cliente-vip']

# del — remove pelo índice sem retornar:
numeros = [10, 20, 30, 40]
del numeros[1]
print(numeros)  # [10, 30, 40]


# -----------------------------------------------------------------------------
# Verificando existência com in
# -----------------------------------------------------------------------------

status = "aberto"

if status in status_validos:
    print(f"'{status}' é um status válido")

if "bloqueado" not in status_validos:
    print("'bloqueado' não é reconhecido pelo sistema")


# -----------------------------------------------------------------------------
# Informações sobre a lista
# -----------------------------------------------------------------------------

ids = [5, 2, 8, 1, 9, 3]

print(len(ids))     # 6       — quantidade de itens
print(min(ids))     # 1       — menor valor
print(max(ids))     # 9       — maior valor
print(sum(ids))     # 28      — soma (só funciona com números)
print(sorted(ids))  # [1, 2, 3, 5, 8, 9]  — retorna nova lista ordenada

# sort() ordena a lista original (modifica ela):
ids.sort()
print(ids)          # [1, 2, 3, 5, 8, 9]

ids.sort(reverse=True)
print(ids)          # [9, 8, 5, 3, 2, 1]


# -----------------------------------------------------------------------------
# Ordenando lista de dicts — comum com respostas de API
# -----------------------------------------------------------------------------

# sorted() com key= — define o campo a usar na ordenação
tickets_ordenados = sorted(tickets, key=lambda t: t["id"])

# Ordenar por prioridade (critica > alta > normal):
ordem_prioridade = {"critica": 0, "alta": 1, "normal": 2}
tickets_por_prioridade = sorted(tickets, key=lambda t: ordem_prioridade.get(t["prioridade"], 99))

for t in tickets_por_prioridade:
    print(f"ID {t['id']} — {t['prioridade']}")

# Saída:
# ID 3 — critica
# ID 1 — alta
# ID 2 — normal


# -----------------------------------------------------------------------------
# List comprehension — criar lista nova a partir de outra
# -----------------------------------------------------------------------------

# Todos os IDs:
ids_tickets = [t["id"] for t in tickets]
print(ids_tickets)      # [1, 2, 3]

# Só os abertos:
abertos = [t for t in tickets if t["status"] == "aberto"]
print(len(abertos))     # 2

# Transformando valores:
ids_formatados = [f"TKT-{t['id']:03d}" for t in tickets]
print(ids_formatados)   # ['TKT-001', 'TKT-002', 'TKT-003']


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def resumir_tickets(tickets):
    """
    Recebe uma lista de tickets (dicts).
    Retorna um dict com contagens por status e lista dos críticos.
    """
    abertos   = [t for t in tickets if t["status"] == "aberto"]
    fechados  = [t for t in tickets if t["status"] == "fechado"]
    criticos  = [t for t in tickets if t["prioridade"] == "critica"]

    ids_criticos = [f"TKT-{t['id']:03d}" for t in criticos]

    return {
        "total":          len(tickets),
        "abertos":        len(abertos),
        "fechados":       len(fechados),
        "criticos":       len(criticos),
        "ids_criticos":   ids_criticos,
    }


resumo = resumir_tickets(tickets)

for chave, valor in resumo.items():
    print(f"{chave}: {valor}")

# Saída:
# total: 3
# abertos: 2
# fechados: 1
# criticos: 1
# ids_criticos: ['TKT-003']