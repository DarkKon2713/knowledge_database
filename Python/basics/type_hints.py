# =============================================================================
# Type Hints em Python
# =============================================================================
# Type hints documentam os tipos esperados de variáveis, parâmetros e
# retornos de funções. Não são obrigatórios e não validam em tempo de
# execução — mas ajudam o editor a detectar erros e tornam o código
# muito mais legível.
#
# A partir do Python 3.10+, a sintaxe moderna (X | Y) é preferida.
# Para projetos em 3.9 ou menos, use Optional, Union etc. do módulo typing.
# =============================================================================

from typing import Optional, Union, Any, TypedDict
from __future__ import annotations   # habilita sintaxe moderna em Python < 3.10


# -----------------------------------------------------------------------------
# Tipos básicos
# -----------------------------------------------------------------------------

# Variáveis
nome: str       = "Ana"
idade: int      = 30
ativo: bool     = True
saldo: float    = 9.99

# Funções — parâmetros e retorno
def saudar(nome: str, formal: bool = False) -> str:
    if formal:
        return f"Bom dia, {nome}."
    return f"Oi, {nome}!"

# Sem retorno — use None
def registrar(mensagem: str) -> None:
    print(mensagem)


# -----------------------------------------------------------------------------
# Tipos compostos — listas, dicts, tuplas
# -----------------------------------------------------------------------------

# Python 3.9+: use list[], dict[], tuple[] diretamente
ids: list[int]              = [1, 2, 3]
config: dict[str, str]      = {"host": "localhost", "porta": "5432"}
coordenadas: tuple[float, float] = (23.5, 46.6)

# Dict com valor de tipo variado
dados: dict[str, Any]       = {"id": 1, "nome": "Ana", "ativo": True}


def buscar_tickets(ids: list[int]) -> list[dict[str, Any]]:
    """Recebe lista de IDs e retorna lista de dicts."""
    return [{"id": i, "status": "aberto"} for i in ids]


# -----------------------------------------------------------------------------
# Optional — valor que pode ser None
# -----------------------------------------------------------------------------

# Optional[str] = str | None — o valor pode ser uma string ou None
# Muito comum em retornos de funções que podem não encontrar nada

def buscar_ticket(ticket_id: int) -> Optional[dict]:
    """Retorna o ticket ou None se não encontrado."""
    tickets = {1: {"id": 1, "titulo": "Erro ao logar"}}
    return tickets.get(ticket_id)   # retorna None se não existir

# Python 3.10+ — sintaxe mais limpa com |
def buscar_ticket_moderno(ticket_id: int) -> dict | None:
    tickets = {1: {"id": 1, "titulo": "Erro ao logar"}}
    return tickets.get(ticket_id)


# -----------------------------------------------------------------------------
# Union — aceita mais de um tipo
# -----------------------------------------------------------------------------

# Union[str, int] = str | int — aceita um ou outro

def formatar_id(ticket_id: Union[str, int]) -> str:
    return f"TKT-{ticket_id:05}" if isinstance(ticket_id, int) else f"TKT-{ticket_id}"

# Python 3.10+ com |
def formatar_id_moderno(ticket_id: str | int) -> str:
    return f"TKT-{ticket_id:05}" if isinstance(ticket_id, int) else f"TKT-{ticket_id}"

print(formatar_id(123))         # TKT-00123
print(formatar_id("00456"))     # TKT-00456


# -----------------------------------------------------------------------------
# TypedDict — dict com campos e tipos definidos
# -----------------------------------------------------------------------------

# Documenta exatamente quais campos um dict deve ter.
# Útil para representar objetos que chegam de APIs.

class Ticket(TypedDict):
    id:         int
    titulo:     str
    status:     str
    prioridade: str

class TicketOpcional(TypedDict, total=False):
    # total=False torna todos os campos opcionais
    sla:         str
    responsavel: str

# Com TypedDict, o editor avisa se você acessar um campo que não existe
def processar_ticket(ticket: Ticket) -> str:
    return f"#{ticket['id']} — {ticket['titulo']} ({ticket['status']})"

ticket: Ticket = {
    "id":         1,
    "titulo":     "Erro ao logar",
    "status":     "aberto",
    "prioridade": "alta",
}
print(processar_ticket(ticket))


# -----------------------------------------------------------------------------
# Callable — tipo para funções passadas como argumento
# -----------------------------------------------------------------------------

from typing import Callable

# Callable[[tipos dos args], tipo do retorno]
def aplicar(valor: int, funcao: Callable[[int], int]) -> int:
    return funcao(valor)

def dobrar(x: int) -> int:
    return x * 2

print(aplicar(5, dobrar))       # 10


# -----------------------------------------------------------------------------
# Type alias — nomear tipos complexos para reutilizar
# -----------------------------------------------------------------------------

# Em vez de repetir dict[str, Any] em todo lugar, dê um nome
JsonDict  = dict[str, Any]
Tickets   = list[JsonDict]

def normalizar_tickets(tickets: Tickets) -> Tickets:
    return [{**t, "status": t.get("status", "desconhecido").lower()} for t in tickets]


# -----------------------------------------------------------------------------
# Juntando tudo — função bem tipada
# -----------------------------------------------------------------------------

from typing import Callable

class FiltroTicket(TypedDict):
    status:     Optional[str]
    prioridade: Optional[str]

def filtrar_tickets(
    tickets:  list[Ticket],
    filtro:   FiltroTicket,
    ordenar:  Callable[[Ticket], Any] | None = None,
) -> list[Ticket]:
    """
    Filtra tickets por status e/ou prioridade.
    Se ordenar for informado, aplica como key de ordenação.
    """
    resultado = tickets

    if filtro.get("status"):
        resultado = [t for t in resultado if t["status"] == filtro["status"]]

    if filtro.get("prioridade"):
        resultado = [t for t in resultado if t["prioridade"] == filtro["prioridade"]]

    if ordenar:
        resultado = sorted(resultado, key=ordenar)

    return resultado


tickets: list[Ticket] = [
    {"id": 1, "titulo": "Erro A", "status": "aberto",  "prioridade": "alta"},
    {"id": 2, "titulo": "Erro B", "status": "fechado", "prioridade": "normal"},
    {"id": 3, "titulo": "Erro C", "status": "aberto",  "prioridade": "critica"},
]

abertos = filtrar_tickets(
    tickets,
    filtro={"status": "aberto", "prioridade": None},
    ordenar=lambda t: t["id"]
)
print(abertos)