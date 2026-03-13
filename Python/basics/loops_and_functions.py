# =============================================================================
# Loops e Funções em Python
# =============================================================================
# Para quem já entende lógica: aqui você vai ver como Python escreve o que
# você já conhece — for, while, funções com parâmetros, retorno de valores.
# Os exemplos usam contexto de APIs e suporte pra facilitar o entendimento.
# =============================================================================


# -----------------------------------------------------------------------------
# FOR — iterando sobre listas
# -----------------------------------------------------------------------------

tickets = ["TKT-001", "TKT-002", "TKT-003"]

for ticket in tickets:
    print(f"Processando ticket: {ticket}")

# Saída:
# Processando ticket: TKT-001
# Processando ticket: TKT-002
# Processando ticket: TKT-003


# -----------------------------------------------------------------------------
# FOR com enumerate — quando você precisa do índice também
# -----------------------------------------------------------------------------

for i, ticket in enumerate(tickets):
    print(f"{i + 1}. {ticket}")

# Saída:
# 1. TKT-001
# 2. TKT-002
# 3. TKT-003


# -----------------------------------------------------------------------------
# FOR iterando sobre uma lista de dicts — comum em respostas de API
# -----------------------------------------------------------------------------

usuarios = [
    {"id": 1, "nome": "Ana", "ativo": True},
    {"id": 2, "nome": "Bruno", "ativo": False},
    {"id": 3, "nome": "Carlos", "ativo": True},
]

for usuario in usuarios:
    status = "ativo" if usuario["ativo"] else "inativo"
    print(f"{usuario['nome']} está {status}")

# Saída:
# Ana está ativo
# Bruno está inativo
# Carlos está ativo


# -----------------------------------------------------------------------------
# FOR com range — quando você precisa repetir N vezes
# -----------------------------------------------------------------------------

# Tentar uma requisição até 3 vezes antes de desistir
for tentativa in range(3):
    print(f"Tentativa {tentativa + 1} de 3")
    # aqui entraria a lógica de requisição

# range(3) gera: 0, 1, 2  →  por isso o +1 no print


# -----------------------------------------------------------------------------
# WHILE — repetir enquanto uma condição for verdadeira
# -----------------------------------------------------------------------------

# Útil para paginação: continuar buscando páginas enquanto houver mais dados
pagina = 1
tem_mais = True

while tem_mais:
    print(f"Buscando página {pagina}...")
    pagina += 1

    if pagina > 3:          # simulando fim dos dados
        tem_mais = False

# Saída:
# Buscando página 1...
# Buscando página 2...
# Buscando página 3...

# ATENÇÃO: sempre garanta que a condição do while vai ser falsa em algum momento,
# senão o código fica em loop infinito.


# -----------------------------------------------------------------------------
# BREAK e CONTINUE — controle de fluxo dentro de loops
# -----------------------------------------------------------------------------

# break → sai do loop imediatamente
for ticket in tickets:
    if ticket == "TKT-002":
        print("Ticket bloqueado encontrado, parando.")
        break
    print(f"Processando {ticket}")

# Saída:
# Processando TKT-001
# Ticket bloqueado encontrado, parando.


# continue → pula para a próxima iteração sem executar o resto do bloco
for usuario in usuarios:
    if not usuario["ativo"]:
        continue                # pula usuários inativos
    print(f"Enviando notificação para {usuario['nome']}")

# Saída:
# Enviando notificação para Ana
# Enviando notificação para Carlos


# -----------------------------------------------------------------------------
# LIST COMPREHENSION — criar uma lista nova a partir de outra, em uma linha
# -----------------------------------------------------------------------------

# Jeito tradicional (com for):
nomes = []
for usuario in usuarios:
    nomes.append(usuario["nome"])

# Jeito pythônico (list comprehension):
nomes = [usuario["nome"] for usuario in usuarios]

print(nomes)
# Saída: ['Ana', 'Bruno', 'Carlos']


# Com filtro — só usuários ativos:
nomes_ativos = [u["nome"] for u in usuarios if u["ativo"]]

print(nomes_ativos)
# Saída: ['Ana', 'Carlos']

# Use list comprehension quando a lógica for simples.
# Se precisar de if/else complexo ou múltiplas linhas, use o for tradicional.


# -----------------------------------------------------------------------------
# FUNÇÕES — def, parâmetros e return
# -----------------------------------------------------------------------------

# Função básica: recebe um argumento e retorna um valor
def formatar_ticket(ticket_id):
    return f"[TICKET] {ticket_id}"

print(formatar_ticket("TKT-001"))
# Saída: [TICKET] TKT-001


# Função com múltiplos parâmetros
def montar_mensagem(usuario, assunto):
    return f"Olá {usuario}, sua solicitação sobre '{assunto}' foi recebida."

print(montar_mensagem("Ana", "redefinição de senha"))
# Saída: Olá Ana, sua solicitação sobre 'redefinição de senha' foi recebida.


# -----------------------------------------------------------------------------
# PARÂMETROS COM VALOR PADRÃO (default)
# -----------------------------------------------------------------------------

# Se o argumento não for passado, usa o valor padrão
def buscar_tickets(status="aberto", limite=10):
    print(f"Buscando até {limite} tickets com status '{status}'")

buscar_tickets()                        # usa os dois padrões
buscar_tickets("fechado")               # sobrescreve só o status
buscar_tickets("pendente", limite=5)    # sobrescreve os dois


# -----------------------------------------------------------------------------
# RETORNANDO MÚLTIPLOS VALORES
# -----------------------------------------------------------------------------

# Python permite retornar mais de um valor de uma função
def processar_resposta(status_code):
    sucesso = status_code == 200
    mensagem = "OK" if sucesso else "Erro na requisição"
    return sucesso, mensagem           # retorna uma tupla

ok, msg = processar_resposta(200)
print(ok, msg)
# Saída: True OK

ok, msg = processar_resposta(500)
print(ok, msg)
# Saída: False Erro na requisição


# -----------------------------------------------------------------------------
# *args — aceitar quantidade variável de argumentos posicionais
# -----------------------------------------------------------------------------

def listar_ids(*ids):
    for id in ids:
        print(f"ID: {id}")

listar_ids("TKT-001", "TKT-002", "TKT-003")
# Pode passar quantos argumentos quiser.
# Dentro da função, `ids` vira uma tupla com todos os valores.


# -----------------------------------------------------------------------------
# **kwargs — aceitar quantidade variável de argumentos nomeados
# -----------------------------------------------------------------------------

def montar_payload(**campos):
    print(campos)

montar_payload(nome="Ana", status="ativo", prioridade="alta")
# Saída: {'nome': 'Ana', 'status': 'ativo', 'prioridade': 'alta'}

# Dentro da função, `campos` vira um dicionário.
# Útil quando você não sabe de antemão quais campos vão ser passados.


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def filtrar_e_notificar(usuarios, status_filtro="ativo"):
    """
    Recebe uma lista de usuários e um status de filtro.
    Retorna a lista de nomes que batem com o status.
    """
    filtrados = [u["nome"] for u in usuarios if (u["ativo"] if status_filtro == "ativo" else not u["ativo"])]

    for nome in filtrados:
        print(f"Notificando: {nome}")

    return filtrados


resultado = filtrar_e_notificar(usuarios)
print(resultado)
# Saída:
# Notificando: Ana
# Notificando: Carlos
# ['Ana', 'Carlos']