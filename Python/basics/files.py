# =============================================================================
# Leitura e escrita de arquivos em Python
# =============================================================================
# Python tem suporte nativo para arquivos de texto, JSON e CSV —
# sem precisar instalar nada além de `csv` e `json` (já incluídos).
#
# Regra principal: sempre use `with open()` — ele fecha o arquivo
# automaticamente, mesmo se ocorrer um erro.
# =============================================================================

import json
import csv
import os


# -----------------------------------------------------------------------------
# Arquivos de texto — leitura
# -----------------------------------------------------------------------------

# Modos de abertura:
#   "r"  — leitura (padrão) — erro se o arquivo não existir
#   "w"  — escrita — cria ou sobrescreve
#   "a"  — append — adiciona ao final sem apagar o conteúdo
#   "r+" — leitura e escrita

def ler_arquivo(caminho: str) -> str:
    """Lê o conteúdo inteiro de um arquivo de texto."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return ""
    except PermissionError:
        print(f"Sem permissão para ler: {caminho}")
        return ""


def ler_linhas(caminho: str) -> list[str]:
    """Lê o arquivo e retorna uma lista de linhas."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            # readlines() mantém o \n no final de cada linha
            # Use strip() se não quiser o \n
            return [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        return []


def ler_linha_por_linha(caminho: str):
    """
    Itera linha por linha sem carregar o arquivo inteiro na memória.
    Ideal para arquivos grandes (logs, CSVs grandes).
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                print(linha.strip())
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")


# -----------------------------------------------------------------------------
# Arquivos de texto — escrita
# -----------------------------------------------------------------------------

def escrever_arquivo(caminho: str, conteudo: str) -> bool:
    """Escreve (ou sobrescreve) um arquivo de texto."""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
    except PermissionError:
        print(f"Sem permissão para escrever em: {caminho}")
        return False


def adicionar_ao_arquivo(caminho: str, linha: str) -> bool:
    """Adiciona uma linha ao final do arquivo sem apagar o conteúdo."""
    try:
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
        return True
    except PermissionError:
        print(f"Sem permissão para escrever em: {caminho}")
        return False


# -----------------------------------------------------------------------------
# JSON — ler e escrever
# -----------------------------------------------------------------------------

def ler_json(caminho: str) -> dict | list | None:
    """Lê um arquivo JSON e retorna dict ou list."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)     # json.load() lê de arquivo — json.loads() lê de string
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
    except json.JSONDecodeError as e:
        print(f"JSON inválido em {caminho}: {e}")
    return None


def escrever_json(caminho: str, dados: dict | list) -> bool:
    """Escreve dados em um arquivo JSON formatado."""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            # indent=4      — formatação legível
            # ensure_ascii  — preserva acentos e caracteres especiais
        return True
    except (PermissionError, TypeError) as e:
        print(f"Erro ao escrever JSON: {e}")
        return False


# -----------------------------------------------------------------------------
# CSV — ler e escrever
# -----------------------------------------------------------------------------

def ler_csv(caminho: str) -> list[dict]:
    """
    Lê um CSV e retorna lista de dicts.
    DictReader usa a primeira linha como cabeçalho automaticamente.
    """
    try:
        with open(caminho, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return []


def escrever_csv(caminho: str, dados: list[dict], campos: list[str] = None) -> bool:
    """
    Escreve lista de dicts em um arquivo CSV.
    Se campos não for informado, usa as chaves do primeiro dict.
    """
    if not dados:
        return False

    campos = campos or list(dados[0].keys())

    try:
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()        # escreve a linha de cabeçalho
            writer.writerows(dados)     # escreve todas as linhas
        return True
    except (PermissionError, KeyError) as e:
        print(f"Erro ao escrever CSV: {e}")
        return False


# -----------------------------------------------------------------------------
# Verificações úteis com os.path
# -----------------------------------------------------------------------------

def info_arquivo(caminho: str):
    """Exibe informações sobre um arquivo ou diretório."""
    print(f"Existe       : {os.path.exists(caminho)}")
    print(f"É arquivo    : {os.path.isfile(caminho)}")
    print(f"É diretório  : {os.path.isdir(caminho)}")

    if os.path.isfile(caminho):
        tamanho = os.path.getsize(caminho)
        print(f"Tamanho      : {tamanho} bytes")
        print(f"Nome         : {os.path.basename(caminho)}")
        print(f"Diretório    : {os.path.dirname(caminho)}")
        extensao = os.path.splitext(caminho)[1]
        print(f"Extensão     : {extensao}")


def listar_arquivos(diretorio: str, extensao: str = None) -> list[str]:
    """Lista arquivos em um diretório, opcionalmente filtrando por extensão."""
    try:
        arquivos = os.listdir(diretorio)
        if extensao:
            arquivos = [a for a in arquivos if a.endswith(extensao)]
        return arquivos
    except FileNotFoundError:
        print(f"Diretório não encontrado: {diretorio}")
        return []


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def salvar_tickets_csv(tickets: list[dict], caminho: str = "tickets.csv") -> bool:
    """Salva lista de tickets em CSV."""
    campos = ["id", "titulo", "status", "prioridade"]
    return escrever_csv(caminho, tickets, campos)


def carregar_tickets_csv(caminho: str = "tickets.csv") -> list[dict]:
    """Carrega tickets de um CSV."""
    return ler_csv(caminho)


def registrar_log(mensagem: str, caminho: str = "app.log"):
    """Adiciona uma linha de log com timestamp."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    adicionar_ao_arquivo(caminho, f"[{timestamp}] {mensagem}")


if __name__ == "__main__":
    tickets = [
        {"id": 1, "titulo": "Erro ao logar",       "status": "aberto",  "prioridade": "alta"},
        {"id": 2, "titulo": "Falha no pagamento",   "status": "aberto",  "prioridade": "critica"},
        {"id": 3, "titulo": "Dúvida sobre fatura",  "status": "fechado", "prioridade": "normal"},
    ]

    # Salvar e recarregar CSV
    salvar_tickets_csv(tickets, "tickets.csv")
    carregados = carregar_tickets_csv("tickets.csv")
    print(f"{len(carregados)} tickets carregados do CSV")

    # Salvar como JSON
    escrever_json("tickets.json", tickets)
    recarregados = ler_json("tickets.json")
    print(f"{len(recarregados)} tickets carregados do JSON")

    # Registrar log
    registrar_log("Script iniciado")
    registrar_log("Tickets processados com sucesso")