# =============================================================================
# Parsing de HTML com BeautifulSoup
# =============================================================================
# BeautifulSoup é uma biblioteca para extrair dados de HTML e XML.
# Ela não abre navegador — recebe HTML como string e permite navegar
# pela estrutura do documento como se fosse um dicionário/lista.
#
# Use com requests ou curl_cffi para buscar o HTML,
# e BeautifulSoup para extrair os dados.
#
# Instalação:
#   pip install beautifulsoup4 lxml requests
#
# lxml é o parser mais rápido e recomendado.
# html.parser é o parser nativo do Python (mais lento, sem instalação extra).
# =============================================================================

import requests
from bs4 import BeautifulSoup


# -----------------------------------------------------------------------------
# Parsing básico — criar um objeto BeautifulSoup
# -----------------------------------------------------------------------------

html = """
<html>
  <head><title>Portal de Tickets</title></head>
  <body>
    <h1 class="titulo">Tickets Abertos</h1>
    <div id="lista">
      <div class="ticket" data-id="101">
        <span class="titulo-ticket">Erro ao fazer login</span>
        <span class="prioridade alta">Alta</span>
        <a href="/tickets/101">Ver detalhes</a>
      </div>
      <div class="ticket" data-id="102">
        <span class="titulo-ticket">Falha no pagamento</span>
        <span class="prioridade critica">Crítica</span>
        <a href="/tickets/102">Ver detalhes</a>
      </div>
      <div class="ticket" data-id="103">
        <span class="titulo-ticket">Dúvida sobre fatura</span>
        <span class="prioridade normal">Normal</span>
        <a href="/tickets/103">Ver detalhes</a>
      </div>
    </div>
  </body>
</html>
"""

# Criar o objeto soup — "lxml" é o parser recomendado
soup = BeautifulSoup(html, "lxml")

# Alternativa sem instalar lxml:
# soup = BeautifulSoup(html, "html.parser")


# -----------------------------------------------------------------------------
# Buscar elementos — find() e find_all()
# -----------------------------------------------------------------------------

# find() — retorna o primeiro elemento que bate com o seletor
titulo = soup.find("h1")
print(titulo)           # <h1 class="titulo">Tickets Abertos</h1>
print(titulo.text)      # Tickets Abertos — só o texto, sem tags
print(titulo.get_text(strip=True))  # mesmo resultado, com strip automático

# find_all() — retorna lista com todos os elementos
todos_tickets = soup.find_all("div", class_="ticket")
print(f"{len(todos_tickets)} tickets encontrados")  # 3

# Buscar por ID
lista = soup.find("div", id="lista")
print(lista is not None)    # True


# -----------------------------------------------------------------------------
# Acessar atributos dos elementos
# -----------------------------------------------------------------------------

for ticket in todos_tickets:
    # Acessar atributo com .get() — retorna None se não existir
    ticket_id = ticket.get("data-id")

    # Navegar para elementos filhos com find()
    titulo_el    = ticket.find("span", class_="titulo-ticket")
    prioridade_el = ticket.find("span", class_="prioridade")
    link_el      = ticket.find("a")

    print(f"ID: {ticket_id}")
    print(f"  Título:     {titulo_el.get_text(strip=True) if titulo_el else '—'}")
    print(f"  Prioridade: {prioridade_el.get_text(strip=True) if prioridade_el else '—'}")
    print(f"  Link:       {link_el.get('href') if link_el else '—'}")

# Saída:
# ID: 101
#   Título:     Erro ao fazer login
#   Prioridade: Alta
#   Link:       /tickets/101


# -----------------------------------------------------------------------------
# Seletores CSS — select() e select_one()
# -----------------------------------------------------------------------------

# select_one() — equivale ao find() mas usa sintaxe CSS
titulo = soup.select_one("h1.titulo")
print(titulo.text)      # Tickets Abertos

# select() — equivale ao find_all() mas usa sintaxe CSS
# .classe, #id, tag, tag.classe, tag[atributo]
tickets     = soup.select("div.ticket")
altas       = soup.select("span.prioridade.alta")
links       = soup.select("div.ticket a")
criticos    = soup.select("span.prioridade.critica")

print(f"Tickets: {len(tickets)}")       # 3
print(f"Alta prioridade: {len(altas)}") # 1
print(f"Links: {[a.get('href') for a in links]}")


# -----------------------------------------------------------------------------
# Navegar pela estrutura — parent, children, siblings
# -----------------------------------------------------------------------------

ticket = soup.find("div", class_="ticket")

# Elemento pai
print(ticket.parent.get("id"))          # lista

# Filhos diretos — generator, converta para lista
filhos = list(ticket.children)
filhos_tags = [f for f in filhos if f.name]  # filtra só tags (remove texto)
print(f"Filhos: {len(filhos_tags)}")

# Próximo e anterior irmão
proximo = ticket.find_next_sibling("div", class_="ticket")
if proximo:
    print(proximo.get("data-id"))       # 102


# -----------------------------------------------------------------------------
# Buscar com requests + BeautifulSoup
# -----------------------------------------------------------------------------

def extrair_titulos(url: str) -> list[str]:
    """
    Busca uma página e retorna todos os títulos h1, h2, h3.
    Exemplo de uso combinado: requests para buscar, BS4 para parsear.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar {url}: {e}")
        return []

    soup    = BeautifulSoup(response.text, "lxml")
    titulos = soup.select("h1, h2, h3")
    return [t.get_text(strip=True) for t in titulos]


def extrair_links(url: str, apenas_internos: bool = True) -> list[str]:
    """Extrai todos os links de uma página."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar {url}: {e}")
        return []

    soup  = BeautifulSoup(response.text, "lxml")
    links = []

    for a in soup.select("a[href]"):    # só <a> com atributo href
        href = a.get("href", "")
        if not href or href.startswith("#"):
            continue
        if apenas_internos and href.startswith("http"):
            continue
        links.append(href)

    return links


# -----------------------------------------------------------------------------
# Juntando tudo — exemplo prático
# -----------------------------------------------------------------------------

def extrair_tickets_de_pagina(html_str: str) -> list[dict]:
    """
    Parseia uma página HTML e extrai os dados de cada ticket.
    Retorna lista de dicts prontos para usar no código.
    """
    soup       = BeautifulSoup(html_str, "lxml")
    tickets_el = soup.select("div.ticket")
    tickets    = []

    for el in tickets_el:
        titulo_el     = el.select_one("span.titulo-ticket")
        prioridade_el = el.select_one("span.prioridade")
        link_el       = el.select_one("a[href]")

        tickets.append({
            "id":         el.get("data-id"),
            "titulo":     titulo_el.get_text(strip=True) if titulo_el else None,
            "prioridade": prioridade_el.get_text(strip=True).lower() if prioridade_el else None,
            "link":       link_el.get("href") if link_el else None,
        })

    return tickets


resultado = extrair_tickets_de_pagina(html)
for t in resultado:
    print(t)

# {'id': '101', 'titulo': 'Erro ao fazer login',  'prioridade': 'alta',    'link': '/tickets/101'}
# {'id': '102', 'titulo': 'Falha no pagamento',   'prioridade': 'crítica', 'link': '/tickets/102'}
# {'id': '103', 'titulo': 'Dúvida sobre fatura',  'prioridade': 'normal',  'link': '/tickets/103'}