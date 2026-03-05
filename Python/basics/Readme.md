# Conceitos Fundamentais

Esta pasta contém **exemplos simples e didáticos de conceitos fundamentais da linguagem Python**.
O objetivo é servir como **material de estudo para iniciantes**, mostrando de forma clara como funcionam algumas das estruturas mais usadas no dia a dia de quem programa em Python.

Mesmo desenvolvedores experientes utilizam esses conceitos constantemente. Por isso, dominar bem essas bases é essencial antes de avançar para temas mais complexos como APIs, bancos de dados, frameworks web ou automação.

---

# Estrutura da pasta

```text
basics/
├── dict_examples.py
├── if_else.py
├── input_examples.py
├── list_examples.py
└── string_methods.py
```

Cada arquivo aborda um conceito específico da linguagem.
A ideia é manter **um arquivo simples para cada tema**, facilitando o aprendizado e a consulta rápida.

---

# dict_examples.py

Este arquivo demonstra como trabalhar com **dicionários (`dict`) em Python**.

Dicionários são estruturas de dados usadas para armazenar informações no formato:

```
chave: valor
```

Eles são muito semelhantes a objetos JSON e aparecem com frequência em:

* respostas de APIs
* configurações de aplicações
* estruturas de dados mais complexas
* armazenamento de informações relacionadas

### Exemplo simples de dicionário

```python
usuario = {
    "nome": "Leonardo",
    "idade": 30,
    "ativo": True
}
```

Neste exemplo criamos um dicionário chamado `usuario` com três informações.

| chave | valor    |
| ----- | -------- |
| nome  | Leonardo |
| idade | 30       |
| ativo | True     |

---

## Acessando valores

Podemos acessar os valores usando a chave correspondente.

```python
print(usuario["nome"])
```

Saída:

```
Leonardo
```

Essa forma de acesso funciona bem quando temos certeza de que a chave existe.

Porém, se tentarmos acessar uma chave inexistente, ocorrerá um erro:

```
KeyError
```

---

## Acessando com segurança usando `.get()`

Para evitar erros quando uma chave pode não existir, usamos o método `.get()`.

```python
print(usuario.get("email"))
```

Saída:

```
None
```

Se a chave não existir, o Python retorna `None` ao invés de gerar erro.

---

## Definindo um valor padrão

Também podemos definir um valor padrão caso a chave não exista.

```python
print(usuario.get("email", "Sem email"))
```

Saída:

```
Sem email
```

Esse comportamento é muito útil quando trabalhamos com:

* dados incompletos
* APIs externas
* arquivos JSON
* configurações opcionais

---

## Adicionando novos valores

Podemos adicionar novas informações ao dicionário simplesmente atribuindo um valor a uma nova chave.

```python
usuario["email"] = "leo@email.com"
```

Agora o dicionário passa a ter mais uma chave.

```python
{
    "nome": "Leonardo",
    "idade": 30,
    "ativo": True,
    "email": "leo@email.com"
}
```

---

## Onde dicionários são usados na prática

Dicionários aparecem o tempo todo em aplicações Python:

Exemplo de resposta de uma API:

```python
resposta_api = {
    "status": "ok",
    "data": {
        "id": 10,
        "nome": "Produto A",
        "preco": 19.90
    }
}
```

Também são muito usados para representar objetos dentro do código.

---

# if_else.py

Este arquivo mostra como funcionam as **estruturas condicionais em Python**.

Estruturas condicionais permitem que o programa **tome decisões com base em condições**.

A estrutura básica é:

```python
if condição:
    código
elif outra_condição:
    código
else:
    código
```

---

## Exemplo prático

```python
numero = 10

if numero > 10:
    print("Maior que 10")
elif numero == 10:
    print("Igual a 10")
else:
    print("Menor que 10")
```

O programa verifica a condição e executa apenas o bloco correspondente.

Fluxo de execução:

1. Python verifica `numero > 10`
2. Se for falso, verifica `numero == 10`
3. Se nenhuma condição for verdadeira, executa o `else`

---

## Operadores comuns em condições

| operador | significado    |
| -------- | -------------- |
| `==`     | igual          |
| `!=`     | diferente      |
| `>`      | maior          |
| `<`      | menor          |
| `>=`     | maior ou igual |
| `<=`     | menor ou igual |

Também podemos combinar condições:

```python
if idade >= 18 and ativo:
    print("Usuário permitido")
```

---

# input_examples.py

Este arquivo demonstra como ler **dados digitados pelo usuário** usando a função `input()`.

A função `input()` pausa o programa e espera o usuário digitar algo.

Exemplo:

```python
nome = input("Digite seu nome: ")
print(nome)
```

---

## Removendo espaços com `.strip()`

Usuários frequentemente digitam espaços sem perceber.

Por isso usamos `.strip()` para remover espaços no início e no final da string.

```python
nome = input("Digite seu nome: ").strip()
```

Exemplo:

Entrada do usuário:

```
   Leonardo
```

Resultado após `.strip()`:

```
Leonardo
```

---

## Validando entrada do usuário

Também podemos validar o valor digitado.

```python
if nome == "":
    print("Nome vazio")
else:
    print(f"Olá {nome}")
```

Esse tipo de validação é muito comum em:

* formulários
* CLI tools
* scripts de automação

---

# list_examples.py

Este arquivo demonstra como trabalhar com **listas em Python**.

Listas são usadas para armazenar **vários valores em sequência**.

Exemplo de lista:

```python
numeros = [10, 20, 30]
```

Cada valor possui uma **posição (índice)**.

| índice | valor |
| ------ | ----- |
| 0      | 10    |
| 1      | 20    |
| 2      | 30    |

---

## Acessando elementos

```python
print(numeros[0])
```

Saída:

```
10
```

---

## Adicionando elementos

Para adicionar um item usamos `.append()`.

```python
numeros.append(40)
```

Agora a lista será:

```
[10, 20, 30, 40]
```

---

## Removendo elementos

Podemos remover valores usando `.remove()`.

```python
numeros.remove(20)
```

Lista resultante:

```
[10, 30, 40]
```

---

## Uso prático de listas

Listas são usadas em praticamente qualquer programa:

* lista de usuários
* lista de produtos
* resultados de consultas
* processamento de dados

Exemplo:

```python
usuarios = ["Ana", "João", "Carlos"]
```

---

# string_methods.py

Este arquivo mostra alguns **métodos importantes para trabalhar com strings**.

Strings representam **texto em Python**.

Exemplo:

```python
texto = "python"
```

---

## Removendo espaços com `.strip()`

```python
texto = "   python   "
texto = texto.strip()
```

Resultado:

```
python
```

---

## Dividindo texto com `.split()`

O método `.split()` divide uma string em várias partes.

```python
texto = "python,java,go"
linguagens = texto.split(",")
```

Resultado:

```
["python", "java", "go"]
```

---

## Percorrendo listas com `for`

Depois de usar `.split()`, normalmente percorremos os valores.

```python
for linguagem in linguagens:
    print(linguagem)
```

Saída:

```
python
java
go
```

---

# Por que esses conceitos são importantes

Os exemplos desta pasta cobrem alguns dos conceitos mais usados na linguagem Python:

* estruturas condicionais
* listas
* dicionários
* manipulação de strings
* entrada de dados

Essas estruturas aparecem em praticamente **todo código Python**, desde scripts simples até aplicações complexas.

Dominar bem esses conceitos facilita muito o aprendizado de tópicos mais avançados como:

* APIs
* automação
* análise de dados
* desenvolvimento web
* machine learning

---

# Documentação oficial Python

Para aprofundar o conhecimento, consulte a documentação oficial:

https://docs.python.org/3/tutorial/
