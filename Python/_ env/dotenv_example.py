# =============================================================================
# Variáveis de Ambiente com python-dotenv
# =============================================================================
# Variáveis de ambiente guardam informações sensíveis fora do código —
# tokens, chaves de API, senhas, URLs de ambiente.
#
# Nunca coloque esses valores diretamente no código. Se o repositório for
# público (ou mesmo privado), qualquer pessoa com acesso vê as credenciais.
#
# Instalação:
#   pip install python-dotenv
# =============================================================================

from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env para o ambiente do processo
load_dotenv()


# -----------------------------------------------------------------------------
# Lendo variáveis de ambiente
# -----------------------------------------------------------------------------

# os.getenv() retorna None se a variável não existir — não lança erro
api_token = os.getenv("API_TOKEN")
print(api_token)    # valor definido no .env, ou None se não existir

# Com valor padrão — útil pra variáveis opcionais
ambiente = os.getenv("AMBIENTE", "development")
print(ambiente)     # usa "development" se AMBIENTE não estiver definido

# os.environ[] lança KeyError se a variável não existir
# — use apenas quando a variável for obrigatória e a ausência for um bug:
try:
    api_token = os.environ["API_TOKEN"]
except KeyError:
    raise EnvironmentError("Variável API_TOKEN não definida. Verifique o .env.")


# -----------------------------------------------------------------------------
# Estrutura do arquivo .env
# -----------------------------------------------------------------------------

# Crie um arquivo chamado `.env` na raiz do projeto com o seguinte formato:
#
#   API_TOKEN=seu_token_aqui
#   API_URL=https://api.exemplo.com
#   AMBIENTE=development
#   TIMEOUT=10
#
# Regras do .env:
#   - uma variável por linha, no formato CHAVE=VALOR
#   - sem espaços ao redor do =
#   - sem aspas (a menos que o valor contenha espaços)
#   - linhas começando com # são comentários


# -----------------------------------------------------------------------------
# .env.example — documente as variáveis sem expor os valores
# -----------------------------------------------------------------------------

# Crie também um arquivo `.env.example` e commite ele no repositório.
# Ele serve de referência pra quem clonar o projeto — mostra quais variáveis
# são necessárias sem expor os valores reais:
#
#   API_TOKEN=
#   API_URL=
#   AMBIENTE=development
#   TIMEOUT=10


# -----------------------------------------------------------------------------
# .gitignore — nunca commite o .env
# -----------------------------------------------------------------------------

# Adicione no seu .gitignore:
#
#   .env
#
# O .env.example deve ser commitado. O .env nunca.


# -----------------------------------------------------------------------------
# Validando variáveis obrigatórias na inicialização
# -----------------------------------------------------------------------------

# Boa prática: verificar no início do script se todas as variáveis
# obrigatórias estão definidas, em vez de deixar o código quebrar no meio.

VARIAVEIS_OBRIGATORIAS = ["API_TOKEN", "API_URL"]

def validar_env():
    ausentes = [v for v in VARIAVEIS_OBRIGATORIAS if not os.getenv(v)]
    if ausentes:
        raise EnvironmentError(
            f"Variáveis de ambiente não definidas: {', '.join(ausentes)}\n"
            f"Verifique o arquivo .env — use .env.example como referência."
        )

validar_env()


# -----------------------------------------------------------------------------
# Convertendo tipos — tudo no .env chega como string
# -----------------------------------------------------------------------------

# Os valores lidos do .env são sempre strings — converta quando necessário:

timeout   = int(os.getenv("TIMEOUT", "10"))         # string → int
debug     = os.getenv("DEBUG", "false").lower() == "true"   # string → bool
max_retry = float(os.getenv("MAX_RETRY", "3"))      # string → float

print(type(timeout))    # <class 'int'>
print(type(debug))      # <class 'bool'>


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

# Padrão comum: um módulo de configuração que centraliza todas as variáveis

import os
from dotenv import load_dotenv

load_dotenv()

def validar_env(obrigatorias):
    ausentes = [v for v in obrigatorias if not os.getenv(v)]
    if ausentes:
        raise EnvironmentError(
            f"Variáveis não definidas: {', '.join(ausentes)}. "
            f"Consulte o .env.example."
        )

validar_env(["API_TOKEN", "API_URL"])

# Configurações centralizadas — importe esse dict nos outros módulos
CONFIG = {
    "api_token":  os.getenv("API_TOKEN"),
    "api_url":    os.getenv("API_URL"),
    "ambiente":   os.getenv("AMBIENTE", "development"),
    "timeout":    int(os.getenv("TIMEOUT", "10")),
    "debug":      os.getenv("DEBUG", "false").lower() == "true",
}

# Uso em outro módulo:
# from dotenv_example import CONFIG
#
# headers = {"Authorization": f"Bearer {CONFIG['api_token']}"}
# response = requests.get(CONFIG['api_url'], headers=headers, timeout=CONFIG['timeout'])