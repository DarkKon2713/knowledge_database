# Python — Automação de Navegadores

## O que é parsing de HTML?

Quando você faz uma requisição HTTP, recebe o HTML da página como texto. Parsing é o processo de transformar esse texto em uma estrutura navegável — para extrair títulos, links, tabelas, preços, qualquer dado visível na página.

**BeautifulSoup** faz parsing de HTML estático (o que chegou na resposta HTTP).
**Selenium/Playwright/etc.** controlam um navegador real — necessários quando o conteúdo é gerado por JavaScript após o carregamento.

---

## Estrutura

```text
browser/
├── beautifulsoup_example.py — parsing de HTML com BeautifulSoup
├── selenium_example.py      — Selenium WebDriver
├── playwright_example.py    — Playwright
├── pyppeteer_example.py     — Pyppeteer (async)
├── botasaurus_example.py    — Botasaurus
├── drissionpage_example.py  — DrissionPage
└── Readme.md
```

---

## Qual ferramenta usar?

| Situação | Ferramenta |
|---|---|
| HTML estático (sem JS) | BeautifulSoup + requests |
| HTML gerado por JavaScript | Playwright ou Selenium |
| Site com detecção de bot | Botasaurus ou DrissionPage |
| Precisa de HTTP/2 ou imitar navegador | curl_cffi + BeautifulSoup |
| Alternar entre browser e HTTP na mesma sessão | DrissionPage |

---

## Instalação

```bash
# BeautifulSoup
pip install beautifulsoup4 lxml

# Selenium
pip install selenium webdriver-manager

# Playwright
pip install playwright
playwright install chromium

# Pyppeteer
pip install pyppeteer

# Botasaurus
pip install botasaurus

# DrissionPage
pip install DrissionPage
```

---

## O que cada arquivo demonstra

### `beautifulsoup_example.py`
Parsing de HTML com `find()`, `find_all()`, seletores CSS com `select()`, navegação pela estrutura (parent, children, siblings), uso combinado com `requests` e extração de dados estruturados.

### Arquivos de browser (Selenium, Playwright, Pyppeteer, Botasaurus, DrissionPage)
Todos cobrem os mesmos cenários, na mesma ordem:

1. Abrir uma URL e capturar título, HTML e cookies
2. Capturar headers de resposta HTTP
3. Navegar por uma lista de URLs reutilizando o mesmo browser
4. Funcionalidade exclusiva da biblioteca

---

## Referência rápida — o que cada biblioteca oferece

| Recurso | Selenium | Playwright | Pyppeteer | Botasaurus | DrissionPage |
|---|---|---|---|---|---|
| Headers de resposta | ✗ | ✓ | ✓ | ✓ via @request | ✓ modo session |
| Interceptar requests | ✗ | ✓ | ✓ | ✗ | ✗ |
| Anti-detecção nativo | ✗ | ✗ | ✗ | ✓ | parcial |
| Paralelismo built-in | ✗ | ✓ | ✓ async | ✓ parallel= | ✗ |
| Modo HTTP sem browser | ✗ | ✗ | ✗ | ✓ @request | ✓ SessionPage |
| Async/await | ✗ | opcional | obrigatório | ✗ | ✗ |

---

## Conceitos importantes

**Headless vs headful**
- `headless=True` — roda sem abrir janela (produção, servidores)
- `headless=False` — abre o navegador visível (debug, desenvolvimento)

**Por que Selenium não captura headers?**
Selenium controla o Chrome via WebDriver — ele interage com o DOM, não com o protocolo HTTP. Para capturar headers use Playwright, Pyppeteer, DrissionPage (modo session) ou combine com `requests`/`curl_cffi`.

**Cookies vs Headers**
- Cookies são acessíveis em qualquer biblioteca via métodos do browser
- Headers de resposta HTTP só estão disponíveis em bibliotecas que interceptam o protocolo (Playwright, Pyppeteer, DrissionPage session)

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `WebDriverException: chromedriver not found` | ChromeDriver não instalado | Usar `webdriver-manager` ou `playwright install` |
| Página carrega em branco | JS não terminou de renderizar | Usar `wait_until="networkidle"` ou `WebDriverWait` |
| Bloqueado como bot | Site detectou automação | Tentar Botasaurus ou DrissionPage com stealth |
| `TimeoutError` | Página demorou mais que o limite | Aumentar `timeout=` ou verificar a URL |
| Headers não disponíveis | Usando Selenium | Trocar para Playwright ou DrissionPage session |