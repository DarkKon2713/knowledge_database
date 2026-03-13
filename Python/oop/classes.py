# =============================================================================
# Classes em Python
# =============================================================================
# Uma classe é um molde para criar objetos — agrupa dados (atributos)
# e comportamentos (métodos) relacionados em uma única estrutura.
#
# No contexto de APIs e automação, classes são úteis para:
#   - encapsular a lógica de um cliente HTTP
#   - representar entidades do domínio (Ticket, Usuario, Requisição)
#   - organizar código que seria repetido em várias funções
# =============================================================================


# -----------------------------------------------------------------------------
# Classe básica — atributos e métodos
# -----------------------------------------------------------------------------

class Ticket:
    """Representa um ticket de suporte."""

    # __init__ é o construtor — executado ao criar um novo objeto
    def __init__(self, id: int, titulo: str, prioridade: str = "normal"):
        self.id         = id            # atributo de instância
        self.titulo     = titulo
        self.prioridade = prioridade
        self.status     = "aberto"      # valor padrão, não recebe como parâmetro
        self.historico  = []

    # Método de instância — sempre recebe self como primeiro argumento
    def fechar(self):
        self.status = "fechado"
        self.historico.append("Ticket fechado.")

    def escalar(self, motivo: str):
        self.prioridade = "critica"
        self.historico.append(f"Escalado: {motivo}")

    # __repr__ — representação do objeto como string (útil para debug)
    def __repr__(self) -> str:
        return f"Ticket(id={self.id}, status={self.status}, prioridade={self.prioridade})"


# Criando instâncias:
t1 = Ticket(id=1, titulo="Erro ao logar")
t2 = Ticket(id=2, titulo="Falha no pagamento", prioridade="alta")

print(t1)           # Ticket(id=1, status=aberto, prioridade=normal)
print(t2.titulo)    # Falha no pagamento

t1.escalar("Cliente VIP reclamou")
t1.fechar()
print(t1)           # Ticket(id=1, status=fechado, prioridade=critica)
print(t1.historico) # ['Escalado: Cliente VIP reclamou', 'Ticket fechado.']


# -----------------------------------------------------------------------------
# Métodos especiais (dunder methods)
# -----------------------------------------------------------------------------

class SLA:
    """Representa o SLA de um ticket."""

    def __init__(self, horas_limite: int):
        self.horas_limite  = horas_limite
        self.horas_usadas  = 0

    def registrar_horas(self, horas: int):
        self.horas_usadas += horas

    # __str__ — usado pelo print() e str()
    def __str__(self) -> str:
        return f"SLA: {self.horas_usadas}/{self.horas_limite}h"

    # __bool__ — define o valor booleano do objeto
    def __bool__(self) -> bool:
        return self.horas_usadas <= self.horas_limite

    # __len__ — define o que len() retorna
    def __len__(self) -> int:
        return self.horas_limite - self.horas_usadas


sla = SLA(horas_limite=8)
sla.registrar_horas(5)

print(sla)          # SLA: 5/8h
print(bool(sla))    # True — ainda dentro do limite
print(len(sla))     # 3 — horas restantes

sla.registrar_horas(4)
print(bool(sla))    # False — estourou o SLA


# -----------------------------------------------------------------------------
# Herança — reutilizar e estender comportamento
# -----------------------------------------------------------------------------

class Notificacao:
    """Classe base para notificações."""

    def __init__(self, destinatario: str, mensagem: str):
        self.destinatario = destinatario
        self.mensagem     = mensagem

    def enviar(self):
        raise NotImplementedError("Subclasse deve implementar enviar()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(para={self.destinatario})"


class NotificacaoEmail(Notificacao):
    def __init__(self, destinatario: str, mensagem: str, assunto: str):
        super().__init__(destinatario, mensagem)    # chama o __init__ da classe pai
        self.assunto = assunto

    def enviar(self):
        print(f"[EMAIL] Para: {self.destinatario} | Assunto: {self.assunto}")
        print(f"  {self.mensagem}")


class NotificacaoSlack(Notificacao):
    def __init__(self, destinatario: str, mensagem: str, canal: str):
        super().__init__(destinatario, mensagem)
        self.canal = canal

    def enviar(self):
        print(f"[SLACK] Canal: {self.canal} | Para: {self.destinatario}")
        print(f"  {self.mensagem}")


# Polimorfismo — chamar o mesmo método em objetos de tipos diferentes
notificacoes = [
    NotificacaoEmail("ana@empresa.com", "Seu ticket foi fechado.", "Ticket #101"),
    NotificacaoSlack("@ana", "SLA estourado no ticket #102.", "#suporte"),
]

for n in notificacoes:
    n.enviar()      # cada um executa sua própria versão de enviar()


# -----------------------------------------------------------------------------
# @classmethod e @staticmethod
# -----------------------------------------------------------------------------

class Ticket2:
    _contador = 0   # atributo de classe — compartilhado por todas as instâncias

    def __init__(self, titulo: str, prioridade: str = "normal"):
        Ticket2._contador += 1
        self.id         = Ticket2._contador
        self.titulo     = titulo
        self.prioridade = prioridade

    @classmethod
    def total_criados(cls) -> int:
        """Acessa atributos da classe, não da instância."""
        return cls._contador

    @classmethod
    def de_dict(cls, dados: dict) -> "Ticket2":
        """Factory method — cria um Ticket2 a partir de um dict (ex: resposta de API)."""
        return cls(
            titulo=dados["titulo"],
            prioridade=dados.get("prioridade", "normal")
        )

    @staticmethod
    def prioridade_valida(prioridade: str) -> bool:
        """Não acessa nem instância nem classe — é uma função utilitária agrupada aqui."""
        return prioridade in ["baixa", "normal", "alta", "critica"]


t1 = Ticket2("Erro ao logar")
t2 = Ticket2("Falha no pagamento", "alta")
t3 = Ticket2.de_dict({"titulo": "Timeout na API", "prioridade": "critica"})

print(Ticket2.total_criados())              # 3
print(Ticket2.prioridade_valida("alta"))    # True
print(Ticket2.prioridade_valida("urgente")) # False
print(t3)


# -----------------------------------------------------------------------------
# Juntando tudo — cliente HTTP orientado a objetos
# -----------------------------------------------------------------------------

import requests
from dotenv import load_dotenv
import os

load_dotenv()

class ClienteAPI:
    """
    Encapsula a lógica de comunicação com uma API REST.
    Centraliza autenticação, headers e tratamento de erros.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session  = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
        })

    def get(self, endpoint: str, params: dict = None) -> dict | None:
        try:
            r = self.session.get(f"{self.base_url}/{endpoint}", params=params, timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP {e.response.status_code} em GET /{endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"Erro em GET /{endpoint}: {e}")
        return None

    def post(self, endpoint: str, payload: dict) -> dict | None:
        try:
            r = self.session.post(f"{self.base_url}/{endpoint}", json=payload, timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP {e.response.status_code} em POST /{endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"Erro em POST /{endpoint}: {e}")
        return None

    def __repr__(self) -> str:
        return f"ClienteAPI(base_url={self.base_url})"


# Uso:
api = ClienteAPI(
    base_url=os.getenv("API_URL", "https://api.exemplo.com"),
    token=os.getenv("API_TOKEN", "")
)

tickets = api.get("tickets", params={"status": "aberto"})
novo    = api.post("tickets", {"titulo": "Erro crítico", "prioridade": "critica"})