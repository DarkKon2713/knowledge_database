# =============================================================================
# Entrada de dados com input()
# =============================================================================
# input() pausa o script e espera o usuário digitar algo.
# Tudo que vem do input() é string — converta o tipo quando necessário.
#
# Útil para: scripts interativos, CLIs, ferramentas internas de suporte.
# =============================================================================


# -----------------------------------------------------------------------------
# Uso básico
# -----------------------------------------------------------------------------

# Lê uma linha digitada pelo usuário e retorna como string
nome = input("Digite seu nome: ")
print(f"Olá, {nome}!")

# .strip() remove espaços acidentais nas bordas — use sempre
nome = input("Digite seu nome: ").strip()


# -----------------------------------------------------------------------------
# Conversão de tipos — tudo chega como string
# -----------------------------------------------------------------------------

# ERRADO — comparar string com int nunca é True:
# idade = input("Digite sua idade: ")
# if idade >= 18:  →  TypeError

# CERTO — converter antes de usar:
idade = int(input("Digite sua idade: ").strip())
print(f"Você tem {idade} anos.")

# Outros exemplos de conversão:
ticket_id = int(input("ID do ticket: ").strip())
limite    = float(input("Limite de SLA (horas): ").strip())


# -----------------------------------------------------------------------------
# Validando entrada — evitar que o script quebre com dados inválidos
# -----------------------------------------------------------------------------

def ler_inteiro(mensagem):
    """
    Lê um inteiro do usuário. Fica pedindo até receber um valor válido.
    """
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print(f"  '{entrada}' não é um número válido. Tente novamente.")


def ler_opcao(mensagem, opcoes_validas):
    """
    Lê uma opção do usuário dentro de uma lista de valores aceitos.
    """
    while True:
        entrada = input(mensagem).strip().lower()
        if entrada in opcoes_validas:
            return entrada
        print(f"  Opção inválida. Escolha entre: {', '.join(opcoes_validas)}")


# -----------------------------------------------------------------------------
# Entrada de múltiplos valores — linha separada por vírgula
# -----------------------------------------------------------------------------

# Usuário digita: TKT-001, TKT-002, TKT-003
entrada = input("IDs dos tickets (separados por vírgula): ").strip()
ids = [id.strip() for id in entrada.split(",") if id.strip()]

print(f"{len(ids)} tickets informados: {ids}")
# ['TKT-001', 'TKT-002', 'TKT-003']


# -----------------------------------------------------------------------------
# Confirmação — sim/não
# -----------------------------------------------------------------------------

def confirmar(mensagem):
    """Retorna True para 's' e False para 'n'."""
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    return resposta == "s"


# -----------------------------------------------------------------------------
# Entrada silenciosa — senhas e tokens
# -----------------------------------------------------------------------------

import getpass

# getpass() esconde o que o usuário digita — não aparece no terminal
# Use para senhas, tokens e qualquer dado sensível
token = getpass.getpass("Token de API: ")
print("Token recebido." if token else "Nenhum token informado.")

# Nunca use input() para senhas — o valor fica visível no terminal.


# -----------------------------------------------------------------------------
# Juntando tudo — CLI simples de criação de ticket
# -----------------------------------------------------------------------------

def cli_criar_ticket():
    """
    Interface de linha de comando para criar um ticket.
    Exemplo de como combinar input(), validação e confirmação.
    """
    print("\n=== Criar novo ticket ===\n")

    titulo     = input("Título: ").strip()
    if not titulo:
        print("Título não pode ser vazio.")
        return None

    prioridade = ler_opcao(
        "Prioridade (baixa/normal/alta/critica): ",
        ["baixa", "normal", "alta", "critica"]
    )

    descricao  = input("Descrição (opcional): ").strip()

    print(f"\nResumo:")
    print(f"  Título:     {titulo}")
    print(f"  Prioridade: {prioridade}")
    print(f"  Descrição:  {descricao or '—'}")

    if not confirmar("\nConfirmar criação?"):
        print("Operação cancelada.")
        return None

    ticket = {
        "titulo":     titulo,
        "prioridade": prioridade,
        "descricao":  descricao,
        "status":     "aberto",
    }

    print(f"\nTicket criado: {ticket}")
    return ticket


if __name__ == "__main__":
    cli_criar_ticket()