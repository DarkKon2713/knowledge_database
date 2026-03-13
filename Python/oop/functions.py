# =============================================================================
# Funções em Python — conceitos avançados
# =============================================================================
# Se você ainda não viu o básico de funções (def, return, *args, **kwargs),
# comece por python/basics/loops_and_functions.py antes deste arquivo.
#
# Aqui o foco é em padrões mais usados no dia a dia de quem escreve código
# de verdade: funções como objetos, closures, decorators e type hints.
# =============================================================================


# -----------------------------------------------------------------------------
# Revisão rápida — def, return, parâmetros
# -----------------------------------------------------------------------------

def saudar(nome: str, formal: bool = False) -> str:
    if formal:
        return f"Bom dia, {nome}."
    return f"Oi, {nome}!"

print(saudar("Ana"))            # Oi, Ana!
print(saudar("Ana", formal=True))  # Bom dia, Ana.


# -----------------------------------------------------------------------------
# Type hints — documentar os tipos esperados
# -----------------------------------------------------------------------------

# Type hints não são obrigatórios e não validam em tempo de execução —
# são uma forma de documentar e ajudar o editor a detectar erros.

def calcular_sla(horas_abertas: int, limite_horas: int = 8) -> dict:
    excedido   = horas_abertas > limite_horas
    percentual = round((horas_abertas / limite_horas) * 100, 1)
    return {
        "horas":      horas_abertas,
        "limite":     limite_horas,
        "percentual": percentual,
        "excedido":   excedido,
    }

print(calcular_sla(6))    # {'horas': 6, 'limite': 8, 'percentual': 75.0, 'excedido': False}
print(calcular_sla(10))   # {'horas': 10, 'limite': 8, 'percentual': 125.0, 'excedido': True}


# -----------------------------------------------------------------------------
# Funções como objetos — passar funções como argumento
# -----------------------------------------------------------------------------

# Em Python, funções são objetos como qualquer outro — podem ser passadas
# como argumento, armazenadas em variáveis e retornadas de outras funções.

def aplicar(valor: int, funcao) -> int:
    return funcao(valor)

def dobrar(x: int) -> int:
    return x * 2

def triplicar(x: int) -> int:
    return x * 3

print(aplicar(5, dobrar))       # 10
print(aplicar(5, triplicar))    # 15

# Útil para aplicar transformações diferentes sobre os mesmos dados:
tickets = [
    {"id": 1, "prioridade": "alta"},
    {"id": 2, "prioridade": "normal"},
    {"id": 3, "prioridade": "critica"},
]

def é_critico(ticket: dict) -> bool:
    return ticket["prioridade"] == "critica"

criticos = list(filter(é_critico, tickets))
print(criticos)     # [{'id': 3, 'prioridade': 'critica'}]


# -----------------------------------------------------------------------------
# Lambda — funções anônimas de uma linha
# -----------------------------------------------------------------------------

# Sintaxe: lambda argumentos: expressão
# Use quando a função é simples e usada uma única vez.

dobrar    = lambda x: x * 2
somar     = lambda x, y: x + y

print(dobrar(4))    # 8
print(somar(3, 5))  # 8

# Muito comum com sorted(), filter() e map():
tickets_ordenados = sorted(tickets, key=lambda t: t["id"], reverse=True)

prioridades = {"critica": 0, "alta": 1, "normal": 2}
tickets_por_prioridade = sorted(tickets, key=lambda t: prioridades.get(t["prioridade"], 99))


# -----------------------------------------------------------------------------
# Closures — funções que "lembram" o contexto onde foram criadas
# -----------------------------------------------------------------------------

def criar_prefixador(prefixo: str):
    """
    Retorna uma função que adiciona o prefixo informado a qualquer string.
    A função interna "lembra" do valor de prefixo mesmo após criar_prefixador() terminar.
    """
    def prefixar(texto: str) -> str:
        return f"{prefixo} {texto}"
    return prefixar

avisar  = criar_prefixador("[AVISO]")
errar   = criar_prefixador("[ERRO]")

print(avisar("SLA próximo do limite"))   # [AVISO] SLA próximo do limite
print(errar("Falha na requisição"))      # [ERRO] Falha na requisição


# -----------------------------------------------------------------------------
# Decorators — modificar o comportamento de uma função sem alterar seu código
# -----------------------------------------------------------------------------

# Um decorator é uma função que recebe outra função e retorna uma versão
# modificada dela. A sintaxe @nome_decorator é um atalho para:
#   função = nome_decorator(função)

import time
import functools

def medir_tempo(func):
    """Decorator que mede quanto tempo a função levou para executar."""
    @functools.wraps(func)      # preserva nome e docstring da função original
    def wrapper(*args, **kwargs):
        inicio    = time.time()
        resultado = func(*args, **kwargs)
        fim       = time.time()
        print(f"{func.__name__} executou em {fim - inicio:.3f}s")
        return resultado
    return wrapper

def logar_chamada(func):
    """Decorator que registra quando a função foi chamada."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Chamando {func.__name__}({args}, {kwargs})")
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} retornou: {resultado}")
        return resultado
    return wrapper


# Aplicando decorators com @:
@medir_tempo
@logar_chamada
def buscar_tickets(status: str = "aberto") -> list:
    """Simula uma busca de tickets."""
    time.sleep(0.1)     # simula latência
    return [{"id": 1, "status": status}]

buscar_tickets("critico")
# Chamando buscar_tickets(('critico',), {})
# buscar_tickets retornou: [{'id': 1, 'status': 'critico'}]
# buscar_tickets executou em 0.101s


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def retry(tentativas: int = 3, espera: float = 1.0):
    """
    Decorator parametrizado — tenta executar a função N vezes antes de desistir.
    Útil para requisições HTTP que podem falhar por instabilidade.
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for tentativa in range(1, tentativas + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"{func.__name__} falhou (tentativa {tentativa}/{tentativas}): {e}")
                    if tentativa < tentativas:
                        time.sleep(espera)
            logging.error(f"{func.__name__} falhou após {tentativas} tentativas.")
            return None
        return wrapper
    return decorador


@retry(tentativas=3, espera=0.5)
def buscar_dados_externos(url: str) -> dict:
    """Simula uma requisição que pode falhar."""
    import random
    if random.random() < 0.7:       # 70% de chance de falhar
        raise ConnectionError("Falha de conexão simulada")
    return {"url": url, "dados": "ok"}

resultado = buscar_dados_externos("https://api.exemplo.com/tickets")
print(resultado)