# =============================================================================
# Datas e horários em Python
# =============================================================================
# Python tem suporte nativo via módulo `datetime`.
# Para manipulações mais avançadas, use `dateutil` (pip install python-dateutil).
#
# Instalação do extra:
#   pip install python-dateutil
# =============================================================================

from datetime import datetime, date, timedelta, timezone
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta


# -----------------------------------------------------------------------------
# Criando objetos de data e hora
# -----------------------------------------------------------------------------

# Data e hora atual
agora = datetime.now()
print(agora)                    # 2024-01-15 10:32:01.123456

# Só a data atual
hoje = date.today()
print(hoje)                     # 2024-01-15

# Data e hora específica
abertura = datetime(2024, 1, 15, 8, 30, 0)
print(abertura)                 # 2024-01-15 08:30:00

# Data e hora com timezone UTC — use em sistemas que precisam de precisão
agora_utc = datetime.now(tz=timezone.utc)
print(agora_utc)                # 2024-01-15 13:32:01.123456+00:00


# -----------------------------------------------------------------------------
# Formatação — datetime para string
# -----------------------------------------------------------------------------

# strftime() converte datetime → string com o formato desejado
agora = datetime(2024, 1, 15, 10, 32, 1)

print(agora.strftime("%Y-%m-%d"))               # 2024-01-15
print(agora.strftime("%d/%m/%Y"))               # 15/01/2024
print(agora.strftime("%d/%m/%Y %H:%M:%S"))      # 15/01/2024 10:32:01
print(agora.strftime("%Y-%m-%dT%H:%M:%S"))      # 2024-01-15T10:32:01  (ISO 8601)

# Códigos mais usados:
#   %Y — ano com 4 dígitos    %m — mês (01-12)    %d — dia (01-31)
#   %H — hora (00-23)         %M — minutos        %S — segundos


# -----------------------------------------------------------------------------
# Parsing — string para datetime
# -----------------------------------------------------------------------------

# strptime() converte string → datetime (você informa o formato)
data_str = "15/01/2024 10:32:01"
dt = datetime.strptime(data_str, "%d/%m/%Y %H:%M:%S")
print(dt)                       # 2024-01-15 10:32:01

# dateutil.parser.parse() — detecta o formato automaticamente
# útil quando você não controla o formato que a API retorna
datas_variaveis = [
    "2024-01-15",
    "15/01/2024",
    "January 15, 2024",
    "2024-01-15T10:32:01Z",
    "Mon, 15 Jan 2024 10:32:01 GMT",
]

for d in datas_variaveis:
    parsed = dateutil_parser.parse(d)
    print(f"{d:40} → {parsed}")


# -----------------------------------------------------------------------------
# Aritmética de datas — timedelta
# -----------------------------------------------------------------------------

agora = datetime(2024, 1, 15, 10, 0, 0)

# timedelta representa uma duração
mais_3_dias  = agora + timedelta(days=3)
menos_1_hora = agora - timedelta(hours=1)
mais_30_min  = agora + timedelta(minutes=30)

print(mais_3_dias)              # 2024-01-18 10:00:00
print(menos_1_hora)             # 2024-01-15 09:00:00

# Diferença entre duas datas → retorna timedelta
fechamento = datetime(2024, 1, 15, 14, 45, 0)
duracao    = fechamento - agora
print(duracao)                  # 4:45:00
print(duracao.total_seconds())  # 17100.0
print(duracao.seconds // 3600)  # 4  (horas inteiras)


# -----------------------------------------------------------------------------
# relativedelta — meses e anos (timedelta não suporta)
# -----------------------------------------------------------------------------

# timedelta não sabe lidar com "1 mês" porque meses têm tamanhos diferentes
agora = datetime(2024, 1, 31)

mais_1_mes  = agora + relativedelta(months=1)
mais_1_ano  = agora + relativedelta(years=1)
print(mais_1_mes)               # 2024-02-29  (ajusta para o último dia do mês)
print(mais_1_ano)               # 2025-01-31


# -----------------------------------------------------------------------------
# Comparação de datas
# -----------------------------------------------------------------------------

abertura  = datetime(2024, 1, 15, 8, 0, 0)
limite    = datetime(2024, 1, 15, 16, 0, 0)
agora     = datetime(2024, 1, 15, 10, 30, 0)

if abertura < agora < limite:
    print("Ticket dentro do prazo")

tempo_restante = limite - agora
print(f"Tempo restante: {tempo_restante}")  # 5:30:00


# -----------------------------------------------------------------------------
# Timestamp Unix — comum em APIs
# -----------------------------------------------------------------------------

# O que é um timestamp?
# É um número que representa um momento no tempo.
# Especificamente: quantos SEGUNDOS se passaram desde 01/01/1970 às 00:00:00 UTC.
# Essa data de referência é chamada de "Unix Epoch".
#
# Por que 1970? É uma convenção histórica dos sistemas Unix.
# Por que útil? Um número inteiro é mais fácil de armazenar, comparar
# e transmitir entre sistemas do que uma string de data formatada.
#
# Exemplos reais:
#   0           → 01/01/1970 00:00:00 UTC  (o início)
#   1705315921  → 15/01/2024 10:32:01 UTC
#   9999999999  → 20/11/2286 (muito no futuro)
#
# Você vai encontrar timestamps em:
#   - respostas de APIs ("created_at": 1705315921)
#   - logs de sistemas
#   - bancos de dados (coluna criada_em como inteiro)
#   - cookies e tokens JWT (campo "exp" de expiração)

# datetime → timestamp (segundos desde 1970)
agora     = datetime.now()
timestamp = agora.timestamp()
print(timestamp)                # 1705315921.123456  ← número de segundos

# timestamp → datetime (converter de volta para data legível)
dt = datetime.fromtimestamp(timestamp)
print(dt)                       # 2024-01-15 10:32:01.123456

# Timestamp em milissegundos — algumas APIs usam ms em vez de segundos
# Você reconhece porque o número é ~1000x maior: 1705315921000
timestamp_ms = int(agora.timestamp() * 1000)    # segundos → milissegundos
dt_ms        = datetime.fromtimestamp(timestamp_ms / 1000)  # milissegundos → segundos → datetime
print(dt_ms)

# Como saber se é segundos ou milissegundos?
#   segundos:      10 dígitos  ex: 1705315921
#   milissegundos: 13 dígitos  ex: 1705315921000
ts_recebido = 1705315921000
if len(str(ts_recebido)) == 13:
    dt = datetime.fromtimestamp(ts_recebido / 1000)
else:
    dt = datetime.fromtimestamp(ts_recebido)
print(dt)


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def calcular_sla(abertura_str: str, limite_horas: int = 8) -> dict:
    """
    Recebe a data de abertura de um ticket (string, qualquer formato)
    e calcula se o SLA foi respeitado.
    """
    abertura  = dateutil_parser.parse(abertura_str)
    limite    = abertura + timedelta(hours=limite_horas)
    agora     = datetime.now(tz=abertura.tzinfo)    # respeita timezone da abertura
    duracao   = agora - abertura
    excedido  = agora > limite

    horas_usadas   = duracao.total_seconds() / 3600
    horas_restantes = max(0, (limite - agora).total_seconds() / 3600)

    return {
        "abertura":        abertura.strftime("%d/%m/%Y %H:%M"),
        "limite":          limite.strftime("%d/%m/%Y %H:%M"),
        "horas_usadas":    round(horas_usadas, 1),
        "horas_restantes": round(horas_restantes, 1),
        "excedido":        excedido,
        "status_sla":      "ESTOURADO" if excedido else "OK",
    }


resultado = calcular_sla("2024-01-15T08:00:00", limite_horas=8)
for chave, valor in resultado.items():
    print(f"{chave:20}: {valor}")