# Knowledge Base — Python, HTTP e Ferramentas de Desenvolvimento

Este repositório foi criado como uma **base de conhecimento para novos programadores** que estão começando a trabalhar com **Python, APIs, Git e ferramentas de desenvolvimento**.

O objetivo principal é **organizar e documentar conceitos importantes de forma simples, prática e bem explicada**, facilitando o aprendizado e a consulta durante o desenvolvimento de projetos.

A documentação reúne:

* exemplos de código
* explicações conceituais
* boas práticas de desenvolvimento
* ferramentas comuns utilizadas no dia a dia

Este repositório pode ser usado tanto como **material de estudo** quanto como **referência rápida durante o desenvolvimento**.

---

# Estrutura do Projeto

```
├── VSCode
│   └── Readme.md
├── git
│   └── Readme.md
├── python
│   ├── basics
│   │   ├── Readme.md
│   │   ├── dict_examples.py
│   │   ├── if_else.py
│   │   ├── input_examples.py
│   │   ├── list_examples.py
│   │   └── string_methods.py
│   ├── http
│   │   ├── curl_cffi
│   │   │   ├── examples
│   │   │   │   ├── get_request.py
│   │   │   │   ├── post_form_data.py
│   │   │   │   └── post_json.py
│   │   │   └── Readme.md
│   │   └── requests
│   │       ├── examples
│   │       │   ├── get_request.py
│   │       │   ├── post_form_data.py
│   │       │   └── post_json.py
│   │       └── Readme.md
│   └── Readme.md
└── Readme.md
```

Cada pasta contém documentação específica sobre uma **tecnologia, conceito ou ferramenta utilizada no desenvolvimento moderno**.

---

# Objetivo do Repositório

Este repositório tem como objetivo:

* ajudar novos programadores a entender conceitos importantes
* servir como material de estudo e referência
* documentar ferramentas comuns utilizadas no desenvolvimento
* explicar bibliotecas e tecnologias de forma didática
* reunir exemplos práticos de uso
* organizar conhecimento técnico de forma estruturada

A ideia é que **qualquer pessoa iniciando em programação consiga usar esta documentação como um guia de aprendizado progressivo**.

---

# Git

Local:

```
git/Readme.md
```

Esta seção documenta o **uso do Git e sua integração com GitHub**.

Os conteúdos abordam:

* instalação do Git
* configuração inicial
* configuração de usuário
* conexão com GitHub
* uso de SSH
* clonagem de repositórios
* fluxo básico de versionamento

Entre os comandos explicados estão:

* `git clone`
* `git add`
* `git commit`
* `git push`
* `git pull`
* `git status`
* `git branch`

Essa documentação ajuda iniciantes a entender **como versionar código e colaborar em projetos de software**.

---

# Python

A pasta **python** reúne conteúdos relacionados ao uso da linguagem Python.

Ela está dividida em duas partes principais:

* **fundamentos da linguagem**
* **requisições HTTP e consumo de APIs**

---

# Python Basics

Local:

```
python/basics/
```

Esta seção contém **exemplos simples de conceitos fundamentais da linguagem Python**.

Os arquivos foram criados para ajudar iniciantes a entender as estruturas mais utilizadas no dia a dia de quem programa.

Arquivos incluídos:

```
dict_examples.py
if_else.py
input_examples.py
list_examples.py
string_methods.py
```

Os exemplos abordam conceitos como:

* estruturas condicionais (`if`, `elif`, `else`)
* listas (`list`)
* dicionários (`dict`)
* manipulação de strings
* entrada de dados com `input()`

Esses conceitos são a base de praticamente qualquer programa Python.

---

# HTTP em Python

Local:

```
python/http/
```

Esta seção explica como realizar **requisições HTTP em Python**.

Requisições HTTP são usadas para:

* consumir APIs
* integrar serviços
* automatizar tarefas
* enviar e receber dados pela internet

Aqui são demonstradas duas bibliotecas populares:

* `requests`
* `curl_cffi`

---

# Requests

Local:

```
python/http/requests/
```

A biblioteca **Requests** é uma das bibliotecas HTTP mais utilizadas em Python.

Ela fornece uma interface simples para realizar requisições HTTP.

Os exemplos mostram como fazer:

* requisições **GET**
* requisições **POST**
* envio de dados de formulário
* envio de JSON
* leitura de respostas da API

Exemplos disponíveis:

```
get_request.py
post_form_data.py
post_json.py
```

Essa biblioteca é muito usada para:

* consumir APIs REST
* scripts de automação
* integração entre sistemas
* ferramentas internas

---

# curl_cffi

Local:

```
python/http/curl_cffi/
```

A biblioteca **curl_cffi** utiliza o **libcurl** para realizar requisições HTTP.

Ela oferece maior compatibilidade com navegadores e permite simular requisições de forma mais realista.

Entre os recursos dessa biblioteca estão:

* requisições HTTP avançadas
* suporte a HTTP/2 e HTTP/3
* simulação de navegadores
* controle de headers
* manipulação de sessões

Os exemplos disponíveis mostram como realizar:

* requisições GET
* envio de formulários
* envio de JSON

Exemplos incluídos:

```
get_request.py
post_form_data.py
post_json.py
```

Essa biblioteca é frequentemente utilizada em:

* scraping
* automação
* integração com serviços web
* APIs com proteções mais avançadas

---

# VSCode

Local:

```
VSCode/Readme.md
```

Esta seção documenta o uso do **Visual Studio Code**, um dos editores de código mais populares para desenvolvimento.

O conteúdo inclui:

* configuração do ambiente Python
* extensões recomendadas
* configuração de debugging
* organização de projetos
* boas práticas de desenvolvimento

O objetivo é ajudar novos programadores a **configurar um ambiente de desenvolvimento eficiente**.

---

# Como Utilizar Este Repositório

1. Escolha a tecnologia que deseja aprender.
2. Navegue até a pasta correspondente.
3. Leia o **README da seção**.
4. Execute os exemplos de código.
5. Experimente modificar os exemplos para aprender mais.

A estrutura foi organizada para permitir **aprendizado progressivo**.

---

# Conclusão

Esta base de conhecimento busca reunir **documentação simples, clara e prática** para ajudar novos programadores a entender ferramentas e conceitos importantes do desenvolvimento.

O objetivo é transformar este repositório em um **material de referência útil para estudo e consulta durante a prática de programação**.

Com o tempo, novos conteúdos, exemplos e tecnologias podem ser adicionados para expandir o material.
