# Python — OOP (Orientação a Objetos)

## O que é orientação a objetos?

É uma forma de organizar código agrupando dados e comportamentos relacionados em uma estrutura chamada **classe**. A classe é o molde, e os **objetos** são as instâncias criadas a partir dela.

Por exemplo: `Ticket` é uma classe. Cada ticket individual (ticket #101, ticket #202) é um objeto criado a partir dessa classe — cada um com seus próprios dados (título, status, prioridade) e comportamentos (fechar, escalar).

Antes de OOP, esses dados ficariam espalhados em variáveis e funções soltas. Com OOP, tudo relacionado a um ticket fica junto, organizado e reutilizável.

---Esta pasta cobre funções avançadas e classes em Python. Antes de começar aqui, garanta que está confortável com `python/basics/` — especialmente `loops_and_functions.py` e `dict_examples.py`.

---

## Estrutura

```text
oop/
├── functions.py   — type hints, lambdas, closures e decorators
├── classes.py     — classes, herança, métodos especiais e padrões práticos
└── Readme.md
```

---

## Ordem de leitura sugerida

1. `functions.py` — funções como objetos, closures, decorators
2. `classes.py` — classes, herança, `@classmethod`, `@staticmethod`

---

## O que cada arquivo cobre

### `functions.py`

| Conceito | O que é |
|---|---|
| Type hints | Documentar tipos esperados (`def f(x: int) -> str`) |
| Funções como objetos | Passar funções como argumento, armazenar em variáveis |
| Lambda | Funções anônimas de uma linha (`lambda x: x * 2`) |
| Closures | Função interna que "lembra" o contexto da função externa |
| Decorators | Modificar comportamento de uma função com `@decorator` |
| Decorator parametrizado | `@retry(tentativas=3)` — decorator com argumentos |

### `classes.py`

| Conceito | O que é |
|---|---|
| `__init__` | Construtor — executado ao criar um objeto |
| Atributos de instância | Dados específicos de cada objeto (`self.status`) |
| Métodos de instância | Funções do objeto, sempre recebem `self` |
| Dunder methods | `__repr__`, `__str__`, `__bool__`, `__len__` |
| Herança | Reutilizar e estender comportamento de outra classe |
| `super()` | Chamar o método da classe pai |
| Polimorfismo | Mesmo método, comportamentos diferentes por classe |
| `@classmethod` | Acessa a classe, não a instância — útil como factory |
| `@staticmethod` | Função utilitária agrupada na classe, sem acesso a `self` |
| Atributo de classe | Compartilhado por todas as instâncias (`_contador`) |

---

## Quando usar classes

Use classes quando:
- O mesmo conjunto de dados e funções aparece em vários lugares do código
- Você precisa manter estado entre chamadas (ex: sessão HTTP, contador)
- Quer criar múltiplos objetos do mesmo tipo com comportamentos independentes

Para scripts simples e funções utilitárias, funções soltas são suficientes — não force OOP onde não faz sentido.

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `TypeError: __init__() missing argument` | Criou objeto sem passar parâmetro obrigatório | Verificar quais parâmetros não têm valor padrão |
| `AttributeError` | Acessou atributo que não existe no objeto | Verificar se foi definido no `__init__` |
| `TypeError: método() takes 1 positional argument but 2 were given` | Esqueceu o `self` na definição do método | Adicionar `self` como primeiro parâmetro |
| Todos os objetos compartilham a mesma lista | Usou lista mutável como valor padrão no `__init__` | Usar `None` como padrão e inicializar dentro do `__init__` |