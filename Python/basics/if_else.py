# =============================================================================
# Condicionais em Python — if, elif, else
# =============================================================================
# Condicionais controlam o fluxo do código: executam blocos diferentes
# dependendo se uma condição é verdadeira ou falsa.
# =============================================================================


# -----------------------------------------------------------------------------
# Estrutura básica — if / elif / else
# -----------------------------------------------------------------------------

numero = 10

if numero > 10:
    print("Maior que 10")
elif numero == 10:
    print("Igual a 10")
else:
    print("Menor que 10")

# elif = "senão, se..." — pode ter quantos quiser
# else = bloco padrão, executado se nenhuma condição anterior for verdadeira
# else é opcional — use só quando fizer sentido ter um comportamento padrão


# -----------------------------------------------------------------------------
# Operadores de comparação
# -----------------------------------------------------------------------------

# ==   igual a
# !=   diferente de
# >    maior que
# <    menor que
# >=   maior ou igual
# <=   menor ou igual

status_code = 404

if status_code == 200:
    print("OK")
elif status_code == 401:
    print("Não autorizado")
elif status_code == 404:
    print("Não encontrado")
elif status_code >= 500:
    print("Erro no servidor")
else:
    print(f"Status inesperado: {status_code}")


# -----------------------------------------------------------------------------
# Operadores lógicos — and, or, not
# -----------------------------------------------------------------------------

usuario_ativo = True
tem_permissao = False

# and — ambas as condições precisam ser verdadeiras
if usuario_ativo and tem_permissao:
    print("Acesso liberado")
else:
    print("Acesso negado")

# or — basta uma das condições ser verdadeira
prioridade = "alta"

if prioridade == "alta" or prioridade == "critica":
    print("Escalar imediatamente")

# not — inverte a condição
if not usuario_ativo:
    print("Usuário inativo")


# -----------------------------------------------------------------------------
# Verificando valores "vazios" — truthy e falsy
# -----------------------------------------------------------------------------

# Em Python, os seguintes valores são considerados False em condicionais:
#   False, None, 0, "", [], {}, ()

# Não precisa comparar com None ou "" explicitamente na maioria dos casos:

nome = ""
if nome:
    print(f"Nome: {nome}")
else:
    print("Nome não informado")      # cai aqui porque "" é falsy

lista_tickets = []
if lista_tickets:
    print(f"{len(lista_tickets)} tickets encontrados")
else:
    print("Nenhum ticket encontrado")   # cai aqui porque [] é falsy

# Quando comparar explicitamente com None:
# Use `is None` — não `== None`
valor = None
if valor is None:
    print("Valor não definido")


# -----------------------------------------------------------------------------
# in — verificar se um valor está em uma lista ou string
# -----------------------------------------------------------------------------

status = "aberto"
status_validos = ["aberto", "pendente", "em_andamento"]

if status in status_validos:
    print(f"Status '{status}' é válido")

# Funciona com strings também:
mensagem = "erro de autenticação"
if "autenticação" in mensagem:
    print("Problema de autenticação detectado")


# -----------------------------------------------------------------------------
# Condicional em uma linha — ternário
# -----------------------------------------------------------------------------

# Sintaxe: valor_se_true if condição else valor_se_false

ativo = True
label = "ativo" if ativo else "inativo"
print(label)    # ativo

# Útil para atribuições simples — evite para lógicas complexas
prioridade = "alta"
escalar = True if prioridade in ["alta", "critica"] else False


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def classificar_ticket(ticket):
    """
    Recebe um dict com dados de um ticket.
    Retorna uma string com a classificação e ação recomendada.
    """
    status    = ticket.get("status", "desconhecido")
    prioridade = ticket.get("prioridade", "normal")
    responsavel = ticket.get("responsavel")

    if status == "fechado":
        return "Ticket já encerrado — nenhuma ação necessária."

    if not responsavel:
        if prioridade in ["alta", "critica"]:
            return "Sem responsável e prioridade alta — escalar imediatamente."
        else:
            return "Sem responsável — atribuir na próxima triagem."

    if prioridade == "critica":
        return f"Crítico! Acionar {responsavel} agora."
    elif prioridade == "alta":
        return f"Alta prioridade. {responsavel} deve responder em até 1h."
    else:
        return f"Ticket normal. {responsavel} pode tratar no fluxo padrão."


tickets = [
    {"status": "aberto",  "prioridade": "critica",  "responsavel": "Ana"},
    {"status": "aberto",  "prioridade": "alta",     "responsavel": None},
    {"status": "fechado", "prioridade": "normal",   "responsavel": "Bruno"},
    {"status": "aberto",  "prioridade": "normal",   "responsavel": "Carlos"},
]

for t in tickets:
    print(classificar_ticket(t))

# Saída:
# Crítico! Acionar Ana agora.
# Sem responsável e prioridade alta — escalar imediatamente.
# Ticket já encerrado — nenhuma ação necessária.
# Ticket normal. Carlos pode tratar no fluxo padrão.