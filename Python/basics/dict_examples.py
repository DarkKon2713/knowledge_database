# Exemplo básico de dicionário (dict) em Python

# Criando um dicionário
# Um dict armazena dados no formato chave:valor
usuario = {
    "nome": "Leonardo",
    "idade": 30,
    "ativo": True
}

# Acessando um valor usando a chave
# Se a chave não existir, Python gera erro (KeyError)
print(usuario["nome"])


# Acessar com segurança usando .get()
# Se a chave não existir, retorna None ao invés de erro
print(usuario.get("email"))


# Também podemos definir um valor padrão
# Se a chave não existir, ele retorna o valor definido
print(usuario.get("email", "Sem email"))


# Adicionando uma nova chave ao dicionário
usuario["email"] = "leo@email.com"


# Agora a chave existe
print(usuario.get("email"))


# Imprime o dicionário completo
print(usuario)