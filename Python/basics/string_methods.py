texto = "  python,java,go  "

# remove espaços
texto = texto.strip()

print(texto)

# dividir string
linguagens = texto.split(",")

print(linguagens)

for linguagem in linguagens:
    print(linguagem)