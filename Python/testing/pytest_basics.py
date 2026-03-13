# =============================================================================
# Testes com pytest
# =============================================================================
# pytest é o framework de testes mais usado em Python.
# Testa se o código faz o que deveria fazer — detecta regressões quando
# você altera algo e quebra outra coisa sem perceber.
#
# Instalação:
#   pip install pytest pytest-mock
#
# Rodar testes:
#   pytest                        — roda todos os arquivos test_*.py
#   pytest python/testing/        — roda só esta pasta
#   pytest -v                     — modo verboso (mostra cada teste)
#   pytest -k "ticket"            — roda só testes com "ticket" no nome
# =============================================================================

import pytest
import requests
from unittest.mock import patch, MagicMock


# =============================================================================
# Funções que vamos testar — normalmente estariam em outro arquivo
# =============================================================================

def calcular_sla(horas_abertas: int, limite: int = 8) -> dict:
    excedido   = horas_abertas > limite
    percentual = round((horas_abertas / limite) * 100, 1)
    return {
        "horas":      horas_abertas,
        "limite":     limite,
        "percentual": percentual,
        "excedido":   excedido,
    }


def normalizar_status(status: str) -> str:
    return status.strip().lower()


def buscar_ticket_api(ticket_id: int, token: str) -> dict | None:
    """Busca ticket na API — esta é a função que vamos mockar."""
    response = requests.get(
        f"https://api.exemplo.com/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def extrair_ids(tickets: list[dict]) -> list[int]:
    return [t["id"] for t in tickets if "id" in t]


# =============================================================================
# Testes — funções que começam com test_
# =============================================================================

# -----------------------------------------------------------------------------
# Testes básicos — assert
# -----------------------------------------------------------------------------

def test_sla_dentro_do_limite():
    resultado = calcular_sla(horas_abertas=6, limite=8)
    assert resultado["excedido"] == False
    assert resultado["percentual"] == 75.0


def test_sla_excedido():
    resultado = calcular_sla(horas_abertas=10, limite=8)
    assert resultado["excedido"] == True
    assert resultado["percentual"] == 125.0


def test_sla_exatamente_no_limite():
    """Exatamente no limite não deve ser considerado excedido."""
    resultado = calcular_sla(horas_abertas=8, limite=8)
    assert resultado["excedido"] == False
    assert resultado["percentual"] == 100.0


def test_normalizar_status_lowercase():
    assert normalizar_status("ABERTO") == "aberto"


def test_normalizar_status_strip():
    assert normalizar_status("  fechado  ") == "fechado"


def test_normalizar_status_combinado():
    assert normalizar_status("  PENDENTE  ") == "pendente"


# -----------------------------------------------------------------------------
# Testando exceções — quando o código deve falhar
# -----------------------------------------------------------------------------

def dividir(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a / b


def test_divisao_normal():
    assert dividir(10, 2) == 5.0


def test_divisao_por_zero_levanta_excecao():
    with pytest.raises(ValueError, match="Divisão por zero"):
        dividir(10, 0)


# -----------------------------------------------------------------------------
# Fixtures — dados reutilizáveis entre testes
# -----------------------------------------------------------------------------

@pytest.fixture
def tickets_exemplo():
    """Fixture: retorna uma lista de tickets para usar nos testes."""
    return [
        {"id": 1, "titulo": "Erro A", "status": "aberto",  "prioridade": "alta"},
        {"id": 2, "titulo": "Erro B", "status": "fechado", "prioridade": "normal"},
        {"id": 3, "titulo": "Erro C", "status": "aberto",  "prioridade": "critica"},
    ]


def test_extrair_ids(tickets_exemplo):
    """A fixture é injetada automaticamente pelo pytest."""
    ids = extrair_ids(tickets_exemplo)
    assert ids == [1, 2, 3]


def test_extrair_ids_lista_vazia():
    assert extrair_ids([]) == []


def test_extrair_ids_sem_campo_id():
    tickets = [{"titulo": "sem id"}, {"id": 5, "titulo": "com id"}]
    assert extrair_ids(tickets) == [5]


# -----------------------------------------------------------------------------
# Parametrize — rodar o mesmo teste com vários inputs
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("status,esperado", [
    ("ABERTO",    "aberto"),
    ("Fechado",   "fechado"),
    ("PENDENTE",  "pendente"),
    ("  aberto ", "aberto"),
])
def test_normalizar_status_multiplos(status, esperado):
    """Roda 4 testes, um para cada par (status, esperado)."""
    assert normalizar_status(status) == esperado


@pytest.mark.parametrize("horas,limite,excedido", [
    (4,  8,  False),
    (8,  8,  False),
    (9,  8,  True),
    (24, 8,  True),
    (1,  24, False),
])
def test_sla_parametrizado(horas, limite, excedido):
    resultado = calcular_sla(horas, limite)
    assert resultado["excedido"] == excedido


# -----------------------------------------------------------------------------
# Mock — simular chamadas externas (API, banco, arquivo)
# -----------------------------------------------------------------------------

def test_buscar_ticket_sucesso(mocker):
    """
    Mocka requests.get para não fazer requisição real.
    Testa que a função processa corretamente a resposta.
    """
    # Cria um mock que simula o objeto Response do requests
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 101,
        "titulo": "Erro ao logar",
        "status": "aberto"
    }

    # Substitui requests.get pelo mock durante o teste
    mocker.patch("requests.get", return_value=mock_response)

    resultado = buscar_ticket_api(101, "token-fake")

    assert resultado["id"] == 101
    assert resultado["status"] == "aberto"


def test_buscar_ticket_nao_encontrado(mocker):
    """Simula um 404 da API."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        buscar_ticket_api(999, "token-fake")


def test_buscar_ticket_timeout(mocker):
    """Simula timeout na requisição."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(requests.exceptions.Timeout):
        buscar_ticket_api(101, "token-fake")


# -----------------------------------------------------------------------------
# Como rodar estes testes
# -----------------------------------------------------------------------------

# Na raiz do projeto:
#   pytest python/testing/pytest_basics.py -v
#
# Saída esperada:
#   PASSED test_sla_dentro_do_limite
#   PASSED test_sla_excedido
#   PASSED test_normalizar_status_parametrizado[ABERTO-aberto]
#   ... etc