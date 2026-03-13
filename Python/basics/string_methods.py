# =============================================================================
# Strings em Python
# =============================================================================
# String é qualquer texto entre aspas — simples, duplas ou triplas.
# Python tem dezenas de métodos nativos pra manipular strings,
# muito úteis ao processar respostas de API, logs e inputs de usuário.
# =============================================================================


# -----------------------------------------------------------------------------
# Criando strings
# -----------------------------------------------------------------------------

simples  = 'texto com aspas simples'
duplas   = "texto com aspas duplas"
multiline = """
    texto em
    múltiplas linhas
"""

# f-string — a forma mais comum de montar strings com variáveis:
nome = "Ana"
ticket_id = 101
mensagem = f"Olá {nome}, seu ticket #{ticket_id} foi recebido."
print(mensagem)
# Saída: Olá Ana, seu ticket #101 foi recebido.

# Expressões dentro de f-strings:
preco = 9.5
print(f"Total: R$ {preco * 2:.2f}")     # Total: R$ 19.00
print(f"ID formatado: TKT-{ticket_id:03d}")  # ID formatado: TKT-101


# -----------------------------------------------------------------------------
# Maiúsculas e minúsculas
# -----------------------------------------------------------------------------

status = "  ABERTO  "

print(status.lower())       # '  aberto  '   — tudo minúsculo
print(status.upper())       # '  ABERTO  '   — tudo maiúsculo
print(status.strip())       # 'ABERTO'        — remove espaços das bordas
print(status.strip().lower())   # 'aberto'   — encadeando métodos

# capitalize() — primeira letra maiúscula, resto minúsculo:
print("email inválido".capitalize())   # Email inválido

# title() — primeira letra de cada palavra maiúscula:
print("erro de autenticação".title())  # Erro De Autenticação

# Na prática — normalizar status que vem de origens diferentes:
def normalizar_status(s):
    return s.strip().lower()

print(normalizar_status("  Aberto "))   # aberto
print(normalizar_status("FECHADO"))     # fechado


# -----------------------------------------------------------------------------
# Verificações — retornam True ou False
# -----------------------------------------------------------------------------

print("aberto".startswith("ab"))    # True
print("aberto".endswith("to"))      # True
print("erro 404".isdigit())         # False  — contém letras
print("12345".isdigit())            # True   — só dígitos

# Verificar se contém um trecho:
log = "ConnectionError: timeout ao acessar api.exemplo.com"

if "timeout" in log:
    print("Erro de timeout detectado")

if log.startswith("Connection"):
    print("Erro de conexão")


# -----------------------------------------------------------------------------
# Busca e substituição
# -----------------------------------------------------------------------------

url = "https://api.exemplo.com/tickets/101"

# find() — retorna o índice da primeira ocorrência, -1 se não encontrar:
print(url.find("tickets"))      # 30
print(url.find("usuarios"))     # -1

# count() — quantas vezes um trecho aparece:
texto = "erro erro erro"
print(texto.count("erro"))      # 3

# replace() — substitui todas as ocorrências:
print(url.replace("101", "202"))
# https://api.exemplo.com/tickets/202

# Útil pra mascarar dados sensíveis em logs:
token = "Bearer eyJhbGciOiJIUzI1NiJ9.payload.signature"
log_seguro = token.replace(token.split(".")[1], "***")
print(log_seguro)
# Bearer eyJhbGciOiJIUzI1NiJ9.***.signature


# -----------------------------------------------------------------------------
# Split e join — dividir e unir strings
# -----------------------------------------------------------------------------

# split() — divide a string em lista pelo separador:
csv_linha = "101,aberto,Ana,alta"
campos = csv_linha.split(",")
print(campos)
# ['101', 'aberto', 'Ana', 'alta']

# Com maxsplit — limita quantas divisões fazer:
print(csv_linha.split(",", 2))
# ['101', 'aberto', 'Ana,alta']

# splitlines() — divide por quebras de linha:
log_multiplo = "linha 1\nlinha 2\nlinha 3"
linhas = log_multiplo.splitlines()
print(linhas)
# ['linha 1', 'linha 2', 'linha 3']

# join() — une uma lista de strings com um separador:
tags = ["urgente", "bug", "cliente-vip"]
print(", ".join(tags))          # urgente, bug, cliente-vip
print(" | ".join(tags))         # urgente | bug | cliente-vip
print("\n".join(tags))          # cada tag em uma linha


# -----------------------------------------------------------------------------
# Fatiamento — igual em listas, funciona em strings também
# -----------------------------------------------------------------------------

codigo = "TKT-00123-PROD"

print(codigo[:3])       # TKT
print(codigo[4:9])      # 00123
print(codigo[-4:])      # PROD
print(codigo[::-1])     # DORP-32100-TKT  — string invertida


# -----------------------------------------------------------------------------
# strip, lstrip, rstrip — remover caracteres das bordas
# -----------------------------------------------------------------------------

entrada = "   \t texto sujo \n  "

print(entrada.strip())      # 'texto sujo'    — remove dos dois lados
print(entrada.lstrip())     # 'texto sujo \n  '  — só da esquerda
print(entrada.rstrip())     # '   \t texto sujo'  — só da direita

# strip() também aceita caracteres específicos:
print("###título###".strip("#"))    # título


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def parsear_log(linha_log):
    """
    Recebe uma linha de log no formato:
        '[2024-01-15 10:32:01] ERROR | ticket=101 | mensagem=Timeout ao buscar dados'
    Retorna um dict com os campos extraídos.
    """
    linha = linha_log.strip()

    # Extrai o timestamp entre colchetes
    timestamp = linha[1:linha.find("]")]

    # Divide pelo separador " | "
    partes = linha[linha.find("]") + 2:].split(" | ")

    nivel = partes[0].strip()

    # Extrai campos chave=valor
    campos = {}
    for parte in partes[1:]:
        if "=" in parte:
            chave, valor = parte.split("=", 1)
            campos[chave.strip()] = valor.strip()

    return {
        "timestamp": timestamp,
        "nivel":     nivel.lower(),
        "campos":    campos,
    }


log = "[2024-01-15 10:32:01] ERROR | ticket=101 | mensagem=Timeout ao buscar dados"
resultado = parsear_log(log)

print(resultado)
# {
#   'timestamp': '2024-01-15 10:32:01',
#   'nivel': 'error',
#   'campos': {'ticket': '101', 'mensagem': 'Timeout ao buscar dados'}
# }

print(f"Ticket {resultado['campos']['ticket']} com erro às {resultado['timestamp']}")
# Ticket 101 com erro às 2024-01-15 10:32:01