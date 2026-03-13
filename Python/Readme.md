# Python

Esta pasta reúne tudo que você precisa para começar a desenvolver em Python — dos conceitos fundamentais da linguagem até o consumo de APIs e configuração de ambiente.

---

## Estrutura

```text
python/
├── basics/       — fundamentos da linguagem
├── _env/         — variáveis de ambiente e credenciais
├── http/
│   ├── requests/     — requisições HTTP com requests
│   └── curl_cffi/    — requisições HTTP com curl_cffi
├── oop/          — orientação a objetos
├── database/     — conexão e operações com PostgreSQL
├── browser/      — automação de navegadores
├── utils/        — utilitários do dia a dia
├── async/        — programação assíncrona
├── patterns/     — padrões de código reutilizáveis
└── testing/      — testes automatizados
```

---

## Ordem de aprendizado sugerida

```
basics/  →  _env/  →  http/requests/  →  http/curl_cffi/
```

Garanta que está confortável com `basics/` antes de partir para `http/` — dicionários, loops e JSON aparecem em todo código que consome APIs.

---

## Instalação do Python 3.12

### Download

Acesse [python.org/downloads](https://python.org/downloads) e baixe o **Windows installer (64-bit)** da versão 3.12.x.

### Instalação

Ao abrir o instalador, siga esta ordem:

1. Marque **Add Python 3.12 to PATH** — sem isso, `python` e `pip` não funcionam no terminal
2. (Recomendado) Marque **Use admin privileges when installing py.exe**
3. Clique em **Install Now**

### Verificação

Após a instalação, abra o terminal (`Ctrl + '` no VS Code) e confirme:

```bash
python --version
# Python 3.12.x

pip --version
# pip 24.x.x (...)
```

### Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `python` abre a Microsoft Store | Alias do Windows sobrepõe o PATH | Pesquisar "Gerenciar aliases de execução de aplicativos" e desativar os aliases do Python |
| Comando não encontrado | PATH não foi adicionado na instalação | Reinstalar marcando "Add Python 3.12 to PATH" |
| Funciona no CMD mas não no VS Code | Terminal não foi reiniciado após instalação | Fechar e reabrir o VS Code |

---

## Ambiente virtual

Sempre use um ambiente virtual por projeto — evita conflito de dependências entre projetos diferentes.

```bash
# Criar
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Mac/Linux)
source .venv/bin/activate

# Instalar dependências
pip install requests curl_cffi python-dotenv

# Salvar dependências do projeto
pip freeze > requirements.txt

# Instalar a partir do requirements.txt
pip install -r requirements.txt
```

> O VS Code detecta o `.venv` automaticamente e pergunta se quer usá-lo como interpretador. Clique em **Yes**.

---

## Dependências deste repositório

```bash
pip install requests curl_cffi python-dotenv psycopg2-binary python-dateutil tenacity pytest pytest-mock aiohttp
```