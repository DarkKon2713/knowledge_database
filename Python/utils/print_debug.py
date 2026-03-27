# =============================================================================
# print() — quando usar e como usar bem
# =============================================================================
# print() tem seu lugar. Saber quando preferir print vs logging evita
# código desnecessariamente complexo e facilita o debugging rápido.
# =============================================================================

import pprint
import sys


# -----------------------------------------------------------------------------
# Quando usar print
# -----------------------------------------------------------------------------

# USE print quando:
#   - script de linha de comando com saída para o usuário
#   - debugging rápido durante desenvolvimento (remover depois)
#   - Jupyter Notebook / exploração interativa
#   - scripts simples de automação pessoal (< 50 linhas)
#   - output formatado que é o produto do script (relatório, CSV)

# USE logging quando:
#   - código vai para produção / servidor
#   - precisa de timestamp, nível, origem do log
#   - múltiplos módulos ou workers
#   - precisa filtrar por nível ou redirecionar para arquivo
#   - bibliotecas (nunca use print em libs — use logging)


# -----------------------------------------------------------------------------
# print básico — parâmetros úteis
# -----------------------------------------------------------------------------

# Padrão
print("Olá, mundo")

# sep — separador entre múltiplos valores (padrão: " ")
print("nome", "idade", "cidade", sep=" | ")
# Saída: nome | idade | cidade

print("2024", "01", "15", sep="-")
# Saída: 2024-01-15

# end — o que colocar no final (padrão: "\n")
print("Carregando", end="")
print(".", end="")
print(".", end="")
print(".", end="\n")
# Saída: Carregando...

# file — redirecionar para outro destino
print("Erro grave!", file=sys.stderr)   # envia para stderr em vez de stdout

# flush — força a escrita imediata (útil em loops com saída lenta)
for i in range(5):
    print(f"Passo {i}", flush=True)


# -----------------------------------------------------------------------------
# f-strings para debug rápido
# -----------------------------------------------------------------------------

nome = "Ana"
idade = 30
dados = {"cargo": "dev", "nivel": "senior"}

# f-string básico
print(f"Nome: {nome}, Idade: {idade}")

# f-string com expressão
print(f"Próximo ano: {idade + 1}")

# f-string com formatação de número
preco = 1234.5678
print(f"Preço: R$ {preco:.2f}")         # R$ 1234.57
print(f"Inteiro: {preco:,.0f}")          # 1,235

# f-string com = (Python 3.8+) — mostra nome e valor automaticamente
# Muito útil para debug
print(f"{nome=}")        # nome='Ana'
print(f"{idade=}")       # idade=30
print(f"{dados=}")       # dados={'cargo': 'dev', 'nivel': 'senior'}

x = [1, 2, 3]
y = sum(x)
print(f"{x=}, {y=}")    # x=[1, 2, 3], y=6


# -----------------------------------------------------------------------------
# pprint — print para estruturas complexas
# -----------------------------------------------------------------------------

# print() em dicts/listas grandes fica ilegível
# pprint formata automaticamente com indentação

dados_complexos = {
    "usuarios": [
        {"id": 1, "nome": "Ana", "permissoes": ["leitura", "escrita", "admin"]},
        {"id": 2, "nome": "Bob", "permissoes": ["leitura"]},
    ],
    "total": 2,
    "config": {"timeout": 30, "retries": 3, "base_url": "https://api.exemplo.com"},
}

print(dados_complexos)      # tudo em uma linha — difícil de ler

pprint.pprint(dados_complexos)
# Saída formatada:
# {'config': {'base_url': 'https://api.exemplo.com',
#             'retries': 3,
#             'timeout': 30},
#  'total': 2,
#  'usuarios': [{'id': 1,
#                'nome': 'Ana',
#                'permissoes': ['leitura', 'escrita', 'admin']},
#               {'id': 2, 'nome': 'Bob', 'permissoes': ['leitura']}]}

pprint.pprint(dados_complexos, indent=2, width=60)   # controla indentação e largura

# pprint.pformat() — retorna string em vez de imprimir (útil para logging)
import logging
logger = logging.getLogger(__name__)
texto_formatado = pprint.pformat(dados_complexos)
logger.debug("Dados recebidos:\n%s", texto_formatado)


# -----------------------------------------------------------------------------
# print para saída de progresso (sem logging)
# -----------------------------------------------------------------------------

# Barra de progresso simples com \r (sobrescreve a linha)
import time

total = 50
for i in range(1, total + 1):
    percent = i / total * 100
    print(f"\rProcessando: {i}/{total} ({percent:.0f}%)", end="", flush=True)
    # time.sleep(0.05)   # simula trabalho
print()  # nova linha ao terminar


# -----------------------------------------------------------------------------
# Separadores visuais para debug rápido
# -----------------------------------------------------------------------------

# Úteis durante desenvolvimento para separar blocos de output

def debug_separator(titulo: str = ""):
    linha = "=" * 60
    if titulo:
        print(f"\n{linha}")
        print(f"  {titulo}")
        print(linha)
    else:
        print(linha)

debug_separator("Dados do usuário")
print(f"Nome: {nome}")
print(f"Idade: {idade}")

debug_separator("Dados de configuração")
pprint.pprint(dados_complexos["config"])


# -----------------------------------------------------------------------------
# Substituir print por logging ao evoluir o código
# -----------------------------------------------------------------------------

# ANTES (script rápido):
# print(f"Erro: {e}")
# print("Conectado ao banco")

# DEPOIS (produção):
# logger.exception("Erro: %s", e)
# logger.info("Conectado ao banco")

# O passo é mecânico — a diferença está no resultado:
# print → saída imediata sem contexto
# logging → timestamp, nível, módulo, destino configurável
