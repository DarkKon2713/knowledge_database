# =============================================================================
# Logging em Python — configuração completa
# =============================================================================
# `logging` é o módulo nativo para registrar eventos do sistema.
# Substitui print() em código de produção — permite controlar nível,
# formato, destino (console, arquivo) e filtrar por módulo.
#
# Você já viu logging usado nos exemplos de error_handling.py e postgres.py.
# Aqui você aprende a configurar do zero.
# =============================================================================

import logging
import logging.handlers
import os
from datetime import datetime


# -----------------------------------------------------------------------------
# Por que não usar print() em produção
# -----------------------------------------------------------------------------

# print()   — sem nível, sem timestamp, sem destino configurável, sem filtro
# logging   — nível, timestamp, destino (console/arquivo), filtro por módulo

# print("Erro ao buscar ticket")           ← sem contexto
# logging.error("Erro ao buscar ticket")   ← com timestamp, nível, origem


# -----------------------------------------------------------------------------
# Níveis de log — do menos ao mais grave
# -----------------------------------------------------------------------------

# DEBUG    (10) — detalhes internos, só em desenvolvimento
# INFO     (20) — fluxo normal, confirmações
# WARNING  (30) — algo errado mas o sistema continua
# ERROR    (40) — erro que impediu uma ação
# CRITICAL (50) — erro grave, sistema pode parar

# O nível configurado filtra tudo abaixo dele:
#   level=INFO   → mostra INFO, WARNING, ERROR, CRITICAL (oculta DEBUG)
#   level=ERROR  → mostra só ERROR e CRITICAL


# -----------------------------------------------------------------------------
# Configuração básica — basicConfig()
# -----------------------------------------------------------------------------

# Configuração mínima — boa para scripts simples
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("Isso não aparece — DEBUG está abaixo de INFO")
logging.info("Script iniciado")
logging.warning("SLA próximo do limite")
logging.error("Falha ao buscar ticket")
logging.critical("Banco de dados inacessível")

# Saída:
# 2024-01-15 10:32:01 [INFO] Script iniciado
# 2024-01-15 10:32:01 [WARNING] SLA próximo do limite
# 2024-01-15 10:32:01 [ERROR] Falha ao buscar ticket
# 2024-01-15 10:32:01 [CRITICAL] Banco de dados inacessível


# -----------------------------------------------------------------------------
# Campos de formato disponíveis
# -----------------------------------------------------------------------------

# %(asctime)s    — data e hora
# %(levelname)s  — nível (INFO, ERROR...)
# %(message)s    — mensagem
# %(name)s       — nome do logger
# %(filename)s   — nome do arquivo
# %(lineno)d     — número da linha
# %(funcName)s   — nome da função


# -----------------------------------------------------------------------------
# Logger por módulo — forma recomendada
# -----------------------------------------------------------------------------

# Em vez de usar o logger raiz (logging.info()),
# crie um logger com o nome do módulo — facilita rastrear a origem dos logs.

logger = logging.getLogger(__name__)
# __name__ = nome do módulo atual (ex: "utils.logging_config")

logger.info("Mensagem do módulo atual")
logger.error("Erro no módulo atual")

# Em projetos com múltiplos arquivos, cada módulo tem seu logger:
#   logger = logging.getLogger(__name__)
# Todos herdam a configuração do logger raiz.


# -----------------------------------------------------------------------------
# Configuração com handlers — console + arquivo ao mesmo tempo
# -----------------------------------------------------------------------------

def configurar_logging(
    nivel_console: int = logging.INFO,
    nivel_arquivo: int = logging.DEBUG,
    arquivo: str = "app.log",
) -> logging.Logger:
    """
    Configura logging com dois destinos:
      - console: mostra INFO e acima
      - arquivo: salva DEBUG e acima (mais detalhado)

    Retorna o logger raiz configurado.
    """
    logger = logging.getLogger()            # logger raiz
    logger.setLevel(logging.DEBUG)          # nível mínimo do logger raiz
                                            # cada handler filtra por conta própria

    # Formato com mais contexto para arquivo
    fmt_console = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fmt_arquivo = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # %(levelname)-8s — alinha o nível em 8 caracteres (INFO    , WARNING )

    # Handler de console
    handler_console = logging.StreamHandler()
    handler_console.setLevel(nivel_console)
    handler_console.setFormatter(fmt_console)

    # Handler de arquivo — sobrescreve a cada execução
    handler_arquivo = logging.FileHandler(arquivo, encoding="utf-8")
    handler_arquivo.setLevel(nivel_arquivo)
    handler_arquivo.setFormatter(fmt_arquivo)

    # Limpa handlers anteriores (evita duplicar se chamado mais de uma vez)
    logger.handlers.clear()
    logger.addHandler(handler_console)
    logger.addHandler(handler_arquivo)

    return logger


# -----------------------------------------------------------------------------
# RotatingFileHandler — limita o tamanho do arquivo de log
# -----------------------------------------------------------------------------

def configurar_logging_rotativo(
    arquivo: str = "app.log",
    tamanho_max_mb: int = 5,
    backups: int = 3,
) -> logging.Logger:
    """
    Arquivo de log com rotação automática:
      - quando app.log chega em 5MB, é renomeado para app.log.1
      - app.log.1 vira app.log.2, etc.
      - mantém até `backups` arquivos antigos
    """
    logger  = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.handlers.RotatingFileHandler(
        arquivo,
        maxBytes=tamanho_max_mb * 1024 * 1024,  # MB → bytes
        backupCount=backups,
        encoding="utf-8"
    )
    handler.setFormatter(fmt)
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


# -----------------------------------------------------------------------------
# TimedRotatingFileHandler — rotação por tempo (diária, semanal)
# -----------------------------------------------------------------------------

def configurar_logging_diario(pasta_logs: str = "logs") -> logging.Logger:
    """
    Cria um novo arquivo de log a cada dia.
    Arquivos antigos são nomeados: app.log.2024-01-15
    """
    os.makedirs(pasta_logs, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(pasta_logs, "app.log"),
        when="midnight",        # rotaciona à meia-noite
        interval=1,             # a cada 1 dia
        backupCount=7,          # mantém 7 dias
        encoding="utf-8"
    )
    handler.setFormatter(fmt)
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


# -----------------------------------------------------------------------------
# Silenciar logs de bibliotecas externas
# -----------------------------------------------------------------------------

# requests, urllib3 e outras bibliotecas usam logging internamente.
# Por padrão aparecem nos seus logs — para silenciar:

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


# -----------------------------------------------------------------------------
# Juntando tudo — configuração de produção
# -----------------------------------------------------------------------------

def setup_logging(debug: bool = False) -> logging.Logger:
    """
    Configuração pronta para uso em produção.
    debug=True ativa logs detalhados no console.
    """
    nivel_console = logging.DEBUG if debug else logging.INFO

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fmt_simples  = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s", "%Y-%m-%d %H:%M:%S")
    fmt_detalhado = logging.Formatter("%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d — %(message)s", "%Y-%m-%d %H:%M:%S")

    # Console — nível configurável
    console = logging.StreamHandler()
    console.setLevel(nivel_console)
    console.setFormatter(fmt_simples)

    # Arquivo rotativo — sempre DEBUG
    arquivo = logging.handlers.RotatingFileHandler(
        "logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    arquivo.setLevel(logging.DEBUG)
    arquivo.setFormatter(fmt_detalhado)

    # Silencia bibliotecas externas
    for lib in ["urllib3", "requests", "httpx", "aiohttp"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logger.handlers.clear()
    logger.addHandler(console)
    logger.addHandler(arquivo)

    logger.info(f"Logging configurado — nível console: {'DEBUG' if debug else 'INFO'}")
    return logger


if __name__ == "__main__":
    logger = setup_logging(debug=False)

    logger.debug("Detalhe interno — não aparece no console")
    logger.info("Script iniciado")
    logger.warning("Aviso importante")
    logger.error("Algo deu errado")

    # Uso em outros módulos:
    # import logging
    # logger = logging.getLogger(__name__)
    # logger.info("Mensagem do meu módulo")