# =============================================================================
# Async/Await e asyncio em Python
# =============================================================================
# Código assíncrono permite executar múltiplas tarefas "ao mesmo tempo"
# sem precisar de threads — ideal para operações de I/O como requisições HTTP,
# leitura de arquivos e consultas a banco.
#
# Conceito central: enquanto uma tarefa espera (ex: resposta da API),
# Python executa outra tarefa em vez de ficar parado.
#
# Instalação:
#   pip install aiohttp  (cliente HTTP assíncrono)
# =============================================================================

import asyncio
import aiohttp
import time


# -----------------------------------------------------------------------------
# Comparação — síncrono vs assíncrono
# -----------------------------------------------------------------------------

# SÍNCRONO — executa uma tarefa por vez, cada uma espera a anterior terminar
def sincrono():
    print("Tarefa 1 iniciada")
    time.sleep(2)           # bloqueia — nada mais roda durante esses 2s
    print("Tarefa 1 concluída")

    print("Tarefa 2 iniciada")
    time.sleep(2)
    print("Tarefa 2 concluída")
    # Tempo total: ~4 segundos


# ASSÍNCRONO — executa tarefas intercaladas, sem bloquear
async def assincrono():
    print("Tarefa 1 iniciada")
    await asyncio.sleep(2)  # libera o loop para outras tarefas durante 2s
    print("Tarefa 1 concluída")

    print("Tarefa 2 iniciada")
    await asyncio.sleep(2)
    print("Tarefa 2 concluída")
    # Tempo total: ~4s (mesma coisa — as tarefas ainda são sequenciais)
    # Para rodar em paralelo, use asyncio.gather() (veja abaixo)


# -----------------------------------------------------------------------------
# async def e await — conceitos base
# -----------------------------------------------------------------------------

# `async def` define uma corrotina — uma função que pode ser pausada
# `await` pausa a corrotina e entrega o controle para o event loop
# Só pode usar `await` dentro de funções `async def`

async def buscar_dados(id: int) -> dict:
    """Simula uma requisição que leva algum tempo."""
    print(f"Buscando ticket {id}...")
    await asyncio.sleep(1)      # simula latência de 1 segundo
    print(f"Ticket {id} recebido.")
    return {"id": id, "status": "aberto"}


# Para rodar uma corrotina: asyncio.run()
resultado = asyncio.run(buscar_dados(101))
print(resultado)


# -----------------------------------------------------------------------------
# asyncio.gather() — rodar múltiplas corrotinas em paralelo
# -----------------------------------------------------------------------------

async def buscar_varios_tickets(ids: list[int]) -> list[dict]:
    """
    Busca todos os tickets ao mesmo tempo em vez de um por vez.
    Com 5 tickets de 1s cada:
      - sequencial: ~5 segundos
      - gather():   ~1 segundo
    """
    tarefas   = [buscar_dados(id) for id in ids]
    resultados = await asyncio.gather(*tarefas)
    return list(resultados)


inicio = time.time()
tickets = asyncio.run(buscar_varios_tickets([1, 2, 3, 4, 5]))
print(f"Tempo: {time.time() - inicio:.2f}s")    # ~1.0s em vez de ~5.0s
print(f"Tickets: {tickets}")


# -----------------------------------------------------------------------------
# gather() com tratamento de erros
# -----------------------------------------------------------------------------

async def buscar_com_erro(id: int) -> dict | None:
    """Simula uma busca que pode falhar."""
    await asyncio.sleep(0.5)
    if id == 3:
        raise ValueError(f"Ticket {id} não encontrado")
    return {"id": id, "status": "aberto"}


async def buscar_com_fallback(ids: list[int]) -> list:
    """
    return_exceptions=True faz o gather() retornar a exceção
    como resultado em vez de cancelar todas as tarefas.
    """
    tarefas    = [buscar_com_erro(id) for id in ids]
    resultados = await asyncio.gather(*tarefas, return_exceptions=True)

    tickets = []
    for id, resultado in zip(ids, resultados):
        if isinstance(resultado, Exception):
            print(f"Erro no ticket {id}: {resultado}")
        else:
            tickets.append(resultado)

    return tickets


tickets = asyncio.run(buscar_com_fallback([1, 2, 3, 4, 5]))
print(f"Tickets válidos: {tickets}")


# -----------------------------------------------------------------------------
# Requisições HTTP assíncronas com aiohttp
# -----------------------------------------------------------------------------

async def buscar_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Faz uma requisição GET assíncrona."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            response.raise_for_status()
            return {
                "url":    url,
                "status": response.status,
                "dados":  await response.json(),
            }
    except aiohttp.ClientError as e:
        print(f"Erro em {url}: {e}")
        return {"url": url, "erro": str(e)}


async def buscar_multiplas_urls(urls: list[str]) -> list[dict]:
    """
    Faz todas as requisições ao mesmo tempo reutilizando a mesma sessão.
    Muito mais rápido que requests em loop sequencial.
    """
    async with aiohttp.ClientSession() as session:
        tarefas    = [buscar_url(session, url) for url in urls]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)
        return list(resultados)


urls = [
    "https://api.ipify.org?format=json",
    "https://httpbin.org/get",
    "https://httpbin.org/status/200",
]

inicio = time.time()
resultados = asyncio.run(buscar_multiplas_urls(urls))
print(f"Tempo: {time.time() - inicio:.2f}s")

for r in resultados:
    print(r.get("status", r.get("erro")))


# -----------------------------------------------------------------------------
# asyncio.Semaphore — limitar o número de tarefas simultâneas
# -----------------------------------------------------------------------------

async def buscar_com_limite(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> dict:
    """
    Semaphore limita quantas requisições rodam ao mesmo tempo.
    Importante para respeitar rate limits de APIs.
    """
    async with sem:         # só N tarefas passam ao mesmo tempo
        return await buscar_url(session, url)


async def buscar_com_rate_limit(urls: list[str], max_simultaneas: int = 3) -> list[dict]:
    """Busca todas as URLs mas no máximo `max_simultaneas` ao mesmo tempo."""
    sem = asyncio.Semaphore(max_simultaneas)

    async with aiohttp.ClientSession() as session:
        tarefas    = [buscar_com_limite(session, url, sem) for url in urls]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)
        return list(resultados)


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

async def processar_tickets_async(ticket_ids: list[int], base_url: str, token: str) -> list[dict]:
    """
    Busca múltiplos tickets em paralelo com rate limit de 5 simultâneos.
    """
    sem = asyncio.Semaphore(5)

    async def buscar_ticket(session: aiohttp.ClientSession, id: int) -> dict | None:
        url     = f"{base_url}/tickets/{id}"
        headers = {"Authorization": f"Bearer {token}"}
        async with sem:
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as r:
                    r.raise_for_status()
                    return await r.json()
            except aiohttp.ClientResponseError as e:
                print(f"HTTP {e.status} no ticket {id}")
            except aiohttp.ClientError as e:
                print(f"Erro no ticket {id}: {e}")
            return None

    async with aiohttp.ClientSession() as session:
        tarefas    = [buscar_ticket(session, id) for id in ticket_ids]
        resultados = await asyncio.gather(*tarefas)
        return [r for r in resultados if r is not None]


if __name__ == "__main__":
    ids = list(range(1, 21))    # 20 tickets
    # resultados = asyncio.run(processar_tickets_async(ids, "https://api.exemplo.com", "TOKEN"))
    # print(f"{len(resultados)} tickets carregados")
    print("Exemplo de uso: processar_tickets_async(ids, base_url, token)")