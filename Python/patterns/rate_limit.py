# =============================================================================
# Padrão Rate Limit — respeitar limites de requisições
# =============================================================================
# APIs limitam quantas requisições você pode fazer por segundo/minuto/hora.
# Ultrapassar o limite resulta em erro 429 (Too Many Requests).
#
# Estratégias:
#   1. Espera simples entre requisições
#   2. Detectar 429 e esperar o tempo indicado
#   3. Throttle — controlar o ritmo com token bucket
# =============================================================================

import time
import requests
import logging
from collections import deque
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

API_URL   = os.getenv("API_URL", "https://api.exemplo.com")
API_TOKEN = os.getenv("API_TOKEN")
HEADERS   = {"Authorization": f"Bearer {API_TOKEN}"}


# -----------------------------------------------------------------------------
# 1. Espera simples — time.sleep() entre requisições
# -----------------------------------------------------------------------------

def processar_lista_simples(ids: list[int], espera: float = 0.5) -> list[dict]:
    """
    Processa uma lista de IDs com pausa entre cada requisição.
    espera=0.5 → máximo 2 requisições por segundo.
    """
    resultados = []

    for i, ticket_id in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] Buscando ticket {ticket_id}...")

        try:
            response = requests.get(
                f"{API_URL}/tickets/{ticket_id}",
                headers=HEADERS,
                timeout=5
            )
            response.raise_for_status()
            resultados.append(response.json())

        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro {e.response.status_code} no ticket {ticket_id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro no ticket {ticket_id}: {e}")

        if i < len(ids):
            time.sleep(espera)  # não espera após o último

    return resultados


# -----------------------------------------------------------------------------
# 2. Detectar 429 e respeitar o Retry-After header
# -----------------------------------------------------------------------------

def buscar_com_retry_after(ticket_id: int, max_tentativas: int = 5) -> dict | None:
    """
    Quando recebe 429, lê o header Retry-After e aguarda o tempo indicado.
    Retry-After pode ser segundos (ex: "30") ou uma data HTTP.
    """
    for tentativa in range(1, max_tentativas + 1):
        try:
            response = requests.get(
                f"{API_URL}/tickets/{ticket_id}",
                headers=HEADERS,
                timeout=5
            )

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                logger.warning(f"Rate limit atingido. Aguardando {retry_after}s...")
                time.sleep(retry_after)
                continue    # tenta novamente após esperar

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na tentativa {tentativa}: {e}")
            if tentativa < max_tentativas:
                time.sleep(2 ** tentativa)  # backoff exponencial

    return None


# -----------------------------------------------------------------------------
# 3. RateLimiter — controla o ritmo automaticamente
# -----------------------------------------------------------------------------

class RateLimiter:
    """
    Garante que no máximo `max_chamadas` sejam feitas dentro de `periodo` segundos.
    Usa uma janela deslizante para controle preciso.

    Exemplo: RateLimiter(max_chamadas=10, periodo=1.0) → máximo 10 req/segundo
    """

    def __init__(self, max_chamadas: int, periodo: float = 1.0):
        self.max_chamadas = max_chamadas
        self.periodo      = periodo
        self.chamadas     = deque()     # timestamps das chamadas recentes

    def aguardar(self):
        """Bloqueia até que seja seguro fazer mais uma chamada."""
        agora = time.monotonic()

        # Remove chamadas fora da janela de tempo
        while self.chamadas and self.chamadas[0] < agora - self.periodo:
            self.chamadas.popleft()

        # Se atingiu o limite, aguarda até a chamada mais antiga sair da janela
        if len(self.chamadas) >= self.max_chamadas:
            espera = self.periodo - (agora - self.chamadas[0])
            if espera > 0:
                logger.debug(f"Rate limit: aguardando {espera:.2f}s")
                time.sleep(espera)

        self.chamadas.append(time.monotonic())


def processar_com_rate_limiter(ids: list[int], max_por_segundo: int = 5) -> list[dict]:
    """
    Processa lista de IDs respeitando o rate limit automaticamente.
    """
    limiter    = RateLimiter(max_chamadas=max_por_segundo, periodo=1.0)
    resultados = []

    for i, ticket_id in enumerate(ids, 1):
        limiter.aguardar()      # bloqueia se necessário antes de cada chamada

        print(f"[{i}/{len(ids)}] Buscando ticket {ticket_id}...")

        try:
            response = requests.get(
                f"{API_URL}/tickets/{ticket_id}",
                headers=HEADERS,
                timeout=5
            )
            response.raise_for_status()
            resultados.append(response.json())

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 5))
                logger.warning(f"429 recebido. Aguardando {retry_after}s...")
                time.sleep(retry_after)
            else:
                logger.error(f"Erro {e.response.status_code} no ticket {ticket_id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro no ticket {ticket_id}: {e}")

    return resultados


if __name__ == "__main__":
    ids = list(range(1, 21))    # 20 tickets
    resultados = processar_com_rate_limiter(ids, max_por_segundo=5)
    print(f"{len(resultados)} tickets processados")