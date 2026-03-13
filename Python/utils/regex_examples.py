# =============================================================================
# Expressões Regulares (Regex) em Python
# =============================================================================
# Regex é uma linguagem para encontrar padrões em strings.
# Módulo nativo `re` — sem precisar instalar nada.
#
# Funções principais:
#   re.search()   — encontra a primeira ocorrência
#   re.findall()  — encontra todas as ocorrências
#   re.sub()      — substitui ocorrências
#   re.match()    — verifica se a string começa com o padrão
#   re.fullmatch()— verifica se a string inteira bate com o padrão
# =============================================================================

import re


# -----------------------------------------------------------------------------
# Padrões básicos
# -----------------------------------------------------------------------------

# .      — qualquer caractere (exceto \n)
# \d     — dígito (0-9)
# \w     — letra, dígito ou _ (word character)
# \s     — espaço, tab, newline
# \D     — NÃO é dígito
# \W     — NÃO é word character
# ^      — início da string
# $      — fim da string
# +      — 1 ou mais
# *      — 0 ou mais
# ?      — 0 ou 1 (opcional)
# {n}    — exatamente n vezes
# {n,m}  — entre n e m vezes
# [abc]  — a, b ou c
# [^abc] — nenhum de a, b, c
# (...)  — grupo de captura


# -----------------------------------------------------------------------------
# re.search() — primeira ocorrência
# -----------------------------------------------------------------------------

texto = "Ticket TKT-00123 aberto por Ana em 15/01/2024"

# Busca um padrão no texto — retorna Match ou None
match = re.search(r"TKT-\d+", texto)
if match:
    print(match.group())        # TKT-00123
    print(match.start())        # 7  (índice onde começa)
    print(match.end())          # 16 (índice onde termina)


# -----------------------------------------------------------------------------
# re.findall() — todas as ocorrências
# -----------------------------------------------------------------------------

log = "Erros: 404 em /tickets, 500 em /usuarios, 404 em /produtos"

# Retorna lista de strings encontradas
codigos = re.findall(r"\d+", log)
print(codigos)      # ['404', '500', '404']

# Com grupos de captura — retorna lista de tuplas
pares = re.findall(r"(\d+) em (/\w+)", log)
print(pares)        # [('404', '/tickets'), ('500', '/usuarios'), ('404', '/produtos')]


# -----------------------------------------------------------------------------
# re.sub() — substituição
# -----------------------------------------------------------------------------

# Mascarar dados sensíveis em logs
log_com_token = "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig"
log_seguro    = re.sub(r"Bearer \S+", "Bearer ***", log_com_token)
print(log_seguro)   # Authorization: Bearer ***

# Normalizar espaços
texto_sujo = "erro   na   conexão    com   o  banco"
texto_limpo = re.sub(r"\s+", " ", texto_sujo).strip()
print(texto_limpo)  # erro na conexão com o banco

# Remover caracteres especiais de um campo
nome_usuario = "Ana @Silva!! (teste)"
nome_limpo   = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", nome_usuario).strip()
print(nome_limpo)   # Ana Silva  teste


# -----------------------------------------------------------------------------
# re.match() e re.fullmatch() — validação de formato
# -----------------------------------------------------------------------------

# match() verifica só o início da string
# fullmatch() verifica a string inteira

def validar_email(email: str) -> bool:
    padrao = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(padrao, email))

print(validar_email("ana@empresa.com"))     # True
print(validar_email("ana@"))               # False
print(validar_email("nao-é-email"))        # False


def validar_ticket_id(ticket_id: str) -> bool:
    """Valida formato TKT-XXXXX (3 letras, hífen, 5 dígitos)."""
    return bool(re.fullmatch(r"TKT-\d{5}", ticket_id))

print(validar_ticket_id("TKT-00123"))      # True
print(validar_ticket_id("TKT-123"))        # False
print(validar_ticket_id("tkt-00123"))      # False


# -----------------------------------------------------------------------------
# Grupos de captura — extrair partes específicas
# -----------------------------------------------------------------------------

# Grupos com () capturam partes do padrão
linha_log = "[2024-01-15 10:32:01] ERROR | ticket=101 | mensagem=Timeout"

match = re.search(r"\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\] (\w+)", linha_log)
if match:
    data      = match.group(1)  # 2024-01-15
    hora      = match.group(2)  # 10:32:01
    nivel     = match.group(3)  # ERROR
    print(f"Data: {data}, Hora: {hora}, Nível: {nivel}")

# Grupos nomeados — mais legível
match = re.search(
    r"\[(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2})\] (?P<nivel>\w+)",
    linha_log
)
if match:
    print(match.group("data"))   # 2024-01-15
    print(match.group("nivel"))  # ERROR
    print(match.groupdict())     # {'data': '2024-01-15', 'hora': '10:32:01', 'nivel': 'ERROR'}


# -----------------------------------------------------------------------------
# re.compile() — reutilizar padrões
# -----------------------------------------------------------------------------

# Quando o mesmo padrão é usado muitas vezes, compile() é mais eficiente
PADRAO_TICKET = re.compile(r"TKT-\d+")
PADRAO_DATA   = re.compile(r"\d{4}-\d{2}-\d{2}")

textos = [
    "Ticket TKT-00123 aberto em 2024-01-15",
    "Ticket TKT-00456 fechado em 2024-01-16",
    "Sem ticket aqui",
]

for texto in textos:
    ticket = PADRAO_TICKET.search(texto)
    data   = PADRAO_DATA.search(texto)
    print(f"Ticket: {ticket.group() if ticket else '—'} | Data: {data.group() if data else '—'}")


# -----------------------------------------------------------------------------
# Flags — modificar o comportamento do padrão
# -----------------------------------------------------------------------------

# re.IGNORECASE (re.I) — ignorar maiúsculas/minúsculas
print(bool(re.search(r"erro", "ERRO CRÍTICO", re.I)))   # True

# re.MULTILINE (re.M) — ^ e $ batem com início/fim de cada linha
texto = "linha 1\nlinha 2\nlinha 3"
linhas = re.findall(r"^linha \d", texto, re.M)
print(linhas)   # ['linha 1', 'linha 2', 'linha 3']


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def parsear_log(linha: str) -> dict | None:
    """
    Extrai campos de uma linha de log no formato:
    [2024-01-15 10:32:01] ERROR | ticket=101 | mensagem=Timeout
    """
    padrao = re.compile(
        r"\[(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2})\]\s+"
        r"(?P<nivel>\w+)\s+\|"
        r"(?P<campos>.+)"
    )

    match = padrao.search(linha)
    if not match:
        return None

    # Extrai campos chave=valor do restante da linha
    campos = {}
    for par in re.findall(r"(\w+)=([^|]+)", match.group("campos")):
        campos[par[0].strip()] = par[1].strip()

    return {
        "timestamp": f"{match.group('data')} {match.group('hora')}",
        "nivel":     match.group("nivel").lower(),
        **campos
    }


logs = [
    "[2024-01-15 10:32:01] ERROR | ticket=101 | mensagem=Timeout ao buscar dados",
    "[2024-01-15 10:33:15] INFO  | ticket=102 | mensagem=Ticket fechado com sucesso",
    "linha inválida sem formato",
]

for log in logs:
    resultado = parsear_log(log)
    print(resultado)

# {'timestamp': '2024-01-15 10:32:01', 'nivel': 'error', 'ticket': '101', 'mensagem': 'Timeout ao buscar dados'}
# {'timestamp': '2024-01-15 10:33:15', 'nivel': 'info',  'ticket': '102', 'mensagem': 'Ticket fechado com sucesso'}
# None