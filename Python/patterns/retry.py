# =============================================================================
# Padrão Retry — tentar novamente em caso de falha
# =============================================================================
# Requisições HTTP podem falhar por instabilidade temporária.
# O padrão retry tenta executar novamente antes de desistir.
#
# Duas abordagens:
#   1. Manual com loop (sem dependência extra)
#   2. tenacity (biblioteca dedicada, mais poderosa)
#
# Instalação:
#   pip install tenacity
# =============================================================================

import time
import logging
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
    retry_if_exception_type,
    retry_if_result,
    before_sleep_log,
)
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

API_URL   = os.getenv("API_URL", "https://api.exemplo.com")
API_TOKEN = os.getenv("API_TOKEN")


# -----------------------------------------------------------------------------
# Retry manual — sem biblioteca
# -----------------------------------------------------------------------------

def buscar_ticket_manual(ticket_id: int, tentativas: int = 3, espera: float = 1.0) -> dict | None:
    """
    Tenta buscar o ticket até `tentativas` vezes.
    Aguarda `espera` segundos entre cada tentativa.
    """
    for tentativa in range(1, tentativas + 1):
        try:
            response = requests.get(
                f"{API_URL}/tickets/{ticket_id}",
                headers={"Authorization": f"Bearer {API_TOKEN}"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout na tentativa {tentativa}/{tentativas} — ticket {ticket_id}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Falha de conexão na tentativa {tentativa}/{tentativas}")
        except requests.exceptions.HTTPError as e:
            # Erros 4xx não vão melhorar com retry — desiste imediatamente
            if e.response.status_code < 500:
                logger.error(f"Erro {e.response.status_code} — sem retry")
                return None
            logger.warning(f"Erro {e.response.status_code} na tentativa {tentativa}/{tentativas}")

        if tentativa < tentativas:
            time.sleep(espera)

    logger.error(f"Ticket {ticket_id} não encontrado após {tentativas} tentativas.")
    return None


# -----------------------------------------------------------------------------
# Retry com tenacity — decorator @retry
# -----------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(3),             # máximo 3 tentativas
    wait=wait_fixed(1),                     # aguarda 1s entre tentativas
    retry=retry_if_exception_type(          # só faz retry nesses erros
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError)
    ),
    before_sleep=before_sleep_log(logger, logging.WARNING),  # loga antes de esperar
)
def buscar_ticket_tenacity(ticket_id: int) -> dict:
    """
    Retry automático com tenacity.
    Lança exceção se todas as tentativas falharem.
    """
    response = requests.get(
        f"{API_URL}/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        timeout=5
    )
    response.raise_for_status()
    return response.json()


# -----------------------------------------------------------------------------
# Backoff exponencial — aumenta o tempo de espera a cada tentativa
# -----------------------------------------------------------------------------

# Útil para rate limits e sobrecarga do servidor.
# Tentativa 1: espera 1s
# Tentativa 2: espera 2s
# Tentativa 3: espera 4s
# Tentativa 4: espera 8s (até o máximo definido)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def buscar_com_backoff(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


# -----------------------------------------------------------------------------
# Retry condicional — baseado no resultado, não na exceção
# -----------------------------------------------------------------------------

def resposta_vazia(resultado: dict | None) -> bool:
    """Retorna True se o resultado indica que deve tentar novamente."""
    return resultado is None or resultado.get("status") == "processando"


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_result(resposta_vazia),  # tenta de novo se a função retornar True
)
def aguardar_processamento(job_id: str) -> dict | None:
    """
    Alguns endpoints retornam status='processando' enquanto o job não termina.
    Retry até receber um status diferente ou esgotar as tentativas.
    """
    response = requests.get(
        f"{API_URL}/jobs/{job_id}",
        headers={"Authorization": f"Bearer {API_TOKEN}"},
        timeout=5
    )
    if response.status_code == 200:
        return response.json()
    return None


if __name__ == "__main__":
    resultado = buscar_ticket_manual(101)
    print(resultado)