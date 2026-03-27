# =============================================================================
# Tratamento de Logs — exceções, contexto e boas práticas
# =============================================================================
# Como registrar erros corretamente, adicionar contexto aos logs,
# e padrões para uso em produção.
# =============================================================================

import logging
import logging.handlers

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Logando exceções — logger.exception() vs logger.error()
# -----------------------------------------------------------------------------

# logger.error()     — registra a mensagem, SEM o traceback
# logger.exception() — registra a mensagem + traceback completo (equivale a error + exc_info=True)
# Sempre use dentro de um bloco except

def buscar_dados(url: str):
    try:
        # ... código que pode falhar
        raise ConnectionError("Timeout na requisição")
    except ConnectionError as e:
        logger.exception("Falha ao buscar dados de %s", url)
        # Saída:
        # ERROR:__main__:Falha ao buscar dados de https://...
        # Traceback (most recent call last):
        #   ...
        # ConnectionError: Timeout na requisição

def buscar_dados_sem_traceback(url: str):
    try:
        raise ConnectionError("Timeout na requisição")
    except ConnectionError as e:
        logger.error("Falha ao buscar dados: %s", e)
        # Saída: ERROR:__main__:Falha ao buscar dados: Timeout na requisição
        # (sem traceback — use quando o erro já é esperado e tratado)


# -----------------------------------------------------------------------------
# exc_info=True — adicionar traceback em qualquer nível
# -----------------------------------------------------------------------------

try:
    x = 1 / 0
except ZeroDivisionError:
    logger.warning("Divisão por zero detectada", exc_info=True)
    # Adiciona traceback no nível WARNING (logger.exception só existe para ERROR)


# -----------------------------------------------------------------------------
# Passando variáveis na mensagem — % vs f-string
# -----------------------------------------------------------------------------

# Use % (lazy formatting) — a string só é formatada se o nível estiver ativo
# Mais eficiente: evita formatar strings que serão descartadas

usuario_id = 42
logger.info("Processando usuário %s", usuario_id)           # correto
logger.info(f"Processando usuário {usuario_id}")             # funciona, mas menos eficiente
logger.debug("Dados: %s", {"chave": "valor"})               # dict convertido automaticamente


# -----------------------------------------------------------------------------
# extra={} — adicionar campos customizados ao log
# -----------------------------------------------------------------------------

# Adiciona campos extras acessíveis no formatter com %(campo)s

logger_extra = logging.getLogger("app")

# Formato que usa o campo extra:
fmt = logging.Formatter("%(asctime)s [%(levelname)s] [usuario=%(usuario)s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(fmt)
logger_extra.addHandler(handler)

# Log com contexto extra
logger_extra.info("Login realizado", extra={"usuario": "joao"})
# Saída: 2024-01-15 10:00:00 [INFO] [usuario=joao] Login realizado

logger_extra.error("Permissão negada", extra={"usuario": "maria"})
# Saída: 2024-01-15 10:00:01 [ERROR] [usuario=maria] Permissão negada


# -----------------------------------------------------------------------------
# LoggerAdapter — contexto persistente sem repetir extra={} toda vez
# -----------------------------------------------------------------------------

class ContextLogger(logging.LoggerAdapter):
    """Adiciona contexto fixo a todos os logs sem precisar passar extra= toda vez."""
    def process(self, msg, kwargs):
        contexto = self.extra
        prefix = " ".join(f"[{k}={v}]" for k, v in contexto.items())
        return f"{prefix} {msg}", kwargs

# Cria logger com contexto fixo para uma operação
logger_base = logging.getLogger("app.worker")
log = ContextLogger(logger_base, {"job": "sync_tickets", "tenant": "empresa_abc"})

log.info("Iniciando sincronização")
# Saída: [job=sync_tickets] [tenant=empresa_abc] Iniciando sincronização
log.error("Falha na sincronização")
# Saída: [job=sync_tickets] [tenant=empresa_abc] Falha na sincronização


# -----------------------------------------------------------------------------
# Padrão: logar entrada e saída de funções críticas
# -----------------------------------------------------------------------------

def processar_pedido(pedido_id: int) -> dict:
    logger.info("Iniciando processamento do pedido %s", pedido_id)
    try:
        resultado = {"status": "ok", "id": pedido_id}   # lógica aqui
        logger.info("Pedido %s processado com sucesso", pedido_id)
        return resultado
    except Exception as e:
        logger.exception("Erro ao processar pedido %s", pedido_id)
        raise   # re-lança para o chamador tratar


# -----------------------------------------------------------------------------
# Padrão: logar em loops com controle de volume
# -----------------------------------------------------------------------------

itens = list(range(1000))
total = len(itens)

for i, item in enumerate(itens):
    # Só loga a cada 100 itens — evita flood de logs
    if i % 100 == 0:
        logger.info("Progresso: %d/%d itens processados", i, total)
    # ... processamento


# -----------------------------------------------------------------------------
# Silenciar log específico em trecho do código
# -----------------------------------------------------------------------------

# Temporariamente eleva o nível de um logger para suprimir mensagens
logging.getLogger("httpx").setLevel(logging.ERROR)
# ... código com muitas requisições
logging.getLogger("httpx").setLevel(logging.WARNING)  # restaura


# -----------------------------------------------------------------------------
# Evitar logs duplicados — propagate
# -----------------------------------------------------------------------------

# Por padrão, logs sobem (propagate=True) até o logger raiz.
# Se você configurar handlers no logger raiz E em loggers filhos, duplica.

logger_filho = logging.getLogger("app.modulo")
logger_filho.propagate = False   # este logger não sobe para o raiz
# Útil quando o módulo precisa de destino próprio (ex: arquivo separado)


# -----------------------------------------------------------------------------
# Resumo: qual método usar em cada situação
# -----------------------------------------------------------------------------

# logger.debug()     — detalhes internos, variáveis, loops (só em dev)
# logger.info()      — fluxo normal: início, fim, progresso
# logger.warning()   — situação inesperada mas tolerável
# logger.error()     — algo falhou, mas o sistema continua
# logger.exception() — dentro de except: erro + traceback completo
# logger.critical()  — falha grave, sistema pode parar
