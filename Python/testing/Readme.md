# Python — Testing

## Por que escrever testes?

Sem testes, a única forma de saber se o código funciona é rodar manualmente e torcer. Quando você altera uma função para corrigir um bug, pode quebrar outra coisa sem perceber — e só descobre em produção.

Testes automatizados verificam automaticamente se o código continua funcionando depois de cada alteração. É como ter um checklist que roda sozinho toda vez que você muda algo.

**Na prática:** um teste que leva 2 minutos para escrever pode evitar horas de debug em produção.

---Testes automatizados com `pytest` — verifica se o código faz o que deveria e detecta regressões quando algo muda.

```bash
pip install pytest pytest-mock
```

---

## Estrutura

```text
testing/
├── pytest_basics.py   — assert, fixtures, parametrize, mock
└── Readme.md
```

---

## O que o arquivo cobre

| Conceito | Descrição |
|---|---|
| `assert` | Verificar se o resultado é o esperado |
| `pytest.raises` | Testar que uma exceção é lançada |
| `@pytest.fixture` | Dados reutilizáveis entre testes |
| `@pytest.mark.parametrize` | Rodar o mesmo teste com vários inputs |
| `mocker.patch` | Substituir chamadas externas (API, banco) por mocks |
| `MagicMock` | Simular objetos e respostas de API |

---

## Comandos

```bash
# Rodar todos os testes
pytest

# Rodar com saída detalhada
pytest -v

# Rodar só uma pasta
pytest python/testing/

# Rodar só testes com "ticket" no nome
pytest -k "ticket"

# Parar no primeiro erro
pytest -x

# Ver print() dentro dos testes
pytest -s
```

---

## Estrutura de um teste

```python
def test_nome_descritivo():
    # 1. Arrange — preparar os dados
    ticket = {"id": 1, "status": "aberto"}

    # 2. Act — executar o que está sendo testado
    resultado = normalizar_status(ticket["status"])

    # 3. Assert — verificar o resultado
    assert resultado == "aberto"
```

---

## Referência rápida

### Testar exceção

```python
def test_divisao_por_zero():
    with pytest.raises(ValueError, match="Divisão por zero"):
        dividir(10, 0)
```

### Fixture

```python
@pytest.fixture
def tickets():
    return [{"id": 1, "status": "aberto"}]

def test_extrair_ids(tickets):   # injetado automaticamente
    assert extrair_ids(tickets) == [1]
```

### Parametrize

```python
@pytest.mark.parametrize("entrada,esperado", [
    ("ABERTO",  "aberto"),
    ("Fechado", "fechado"),
])
def test_normalizar(entrada, esperado):
    assert normalizar_status(entrada) == esperado
```

### Mock de API

```python
def test_buscar_ticket(mocker):
    mock = MagicMock()
    mock.json.return_value = {"id": 1, "status": "aberto"}
    mocker.patch("requests.get", return_value=mock)

    resultado = buscar_ticket_api(1, "token")
    assert resultado["id"] == 1
```

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `fixture não encontrada` | Nome da fixture diferente do parâmetro | Nome da função fixture deve ser idêntico ao parâmetro |
| Teste passa localmente, falha no CI | Dependência de ordem ou estado global | Cada teste deve ser independente — não depender de outro |
| Mock não funciona | Patch no lugar errado | Fazer patch onde a função é **usada**, não onde é **definida** |
| `assert` falso positivo | Comparando dict com ordem diferente | `assert resultado == esperado` funciona — dict não