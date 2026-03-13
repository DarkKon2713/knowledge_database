# Git e GitHub

## O que é Git?

Git é um sistema de **controle de versão** — salva o histórico de todas as alterações do seu código. Se você quebrar algo, consegue voltar para uma versão anterior. Se duas pessoas editarem o mesmo projeto, o Git ajuda a juntar as mudanças.

## O que é GitHub?

GitHub é uma plataforma online que hospeda repositórios Git. Pense nele como um Google Drive para código — mas com histórico de versões, colaboração em equipe e controle de quem alterou o quê.

## O que é SSH?

SSH é um protocolo de conexão segura. No contexto do GitHub, ele permite que você envie e receba código **sem digitar usuário e senha toda vez** — a autenticação é feita por uma chave criptográfica que fica no seu computador.

## O que é uma branch?

Uma branch é uma linha de desenvolvimento independente. Por padrão você está na branch `main` — que é o código "oficial" do projeto. Quando você vai fazer uma alteração, cria uma branch nova, faz as mudanças lá, e só junta de volta ao `main` quando estiver pronto e revisado.

Isso evita que código incompleto ou com bug vá direto para a versão principal.

## O que é um Pull Request (PR)?

Um Pull Request é uma solicitação para juntar o código da sua branch na branch principal. No GitHub, você abre um PR, outra pessoa revisa, e só então o código é mesclado. É o fluxo padrão de trabalho em equipe.

---

Controle de versão com Git e integração com GitHub. Este guia cobre instalação, configuração, SSH e o fluxo básico do dia a dia.

---

## Instalação

**Windows**
Baixe o instalador em [git-scm.com/download/win](https://git-scm.com/download/win) e execute com as opções padrão.

**Linux (Ubuntu/Debian)**
```bash
sudo apt update && sudo apt install git
```

**Mac**
```bash
brew install git
```

Verificar instalação:
```bash
git --version
```

---

## Configuração inicial

Faça isso uma vez após instalar — identifica seus commits.

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@gmail.com"
```

Verificar:
```bash
git config --list
```

---

## Conectar ao GitHub via SSH

SSH evita digitar usuário e senha a cada push/pull.

### 1. Gerar chave SSH

```bash
ssh-keygen -t ed25519 -C "seuemail@gmail.com"
```

Pressione Enter para aceitar os caminhos padrão. Isso cria dois arquivos:
- `~/.ssh/id_ed25519` — chave privada (nunca compartilhe)
- `~/.ssh/id_ed25519.pub` — chave pública (vai para o GitHub)

### 2. Iniciar o agente e adicionar a chave

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 3. Copiar a chave pública

```bash
cat ~/.ssh/id_ed25519.pub
```

Copie o texto completo.

### 4. Adicionar no GitHub

Acesse [github.com/settings/keys](https://github.com/settings/keys) → **New SSH Key** → cole a chave → **Add SSH Key**.

### 5. Testar a conexão

```bash
ssh -T git@github.com
```

Resposta esperada:
```
Hi username! You've successfully authenticated.
```

---

## Fluxo básico do dia a dia

### Clonar um repositório

```bash
# HTTPS (sem SSH configurado)
git clone https://github.com/usuario/repositorio.git

# SSH (recomendado após configurar)
git clone git@github.com:usuario/repositorio.git
```

### Ver o estado atual

```bash
git status          # arquivos modificados, staged, branch atual
git log --oneline   # histórico resumido de commits
git diff            # diferença entre arquivos modificados e o último commit
```

### Salvar alterações

```bash
git add arquivo.py          # adiciona um arquivo específico
git add .                   # adiciona todos os arquivos modificados
git commit -m "mensagem"    # salva com mensagem descritiva
git push                    # envia para o GitHub
```

### Baixar atualizações

```bash
git pull                    # baixa e aplica as mudanças do remoto
```

### Fluxo de trabalho em equipe

O fluxo padrão ao trabalhar em equipe — nunca altere direto na `main`:

```bash
# 1. Garanta que sua main está atualizada
git checkout main
git pull

# 2. Crie uma branch para sua alteração
git checkout -b minha-feature

# 3. Faça as alterações e salve
git add .
git commit -m "descreve o que foi feito"

# 4. Envie a branch para o GitHub
git push origin minha-feature

# 5. Abra um Pull Request no GitHub para revisão
# Acesse o repositório no GitHub — ele vai sugerir abrir o PR automaticamente
```

---

## Referência rápida — comandos mais usados

| Comando | O que faz |
|---|---|
| `git status` | Mostra estado atual do repositório |
| `git add .` | Prepara todos os arquivos para commit |
| `git commit -m "msg"` | Salva as alterações com mensagem |
| `git push` | Envia commits para o GitHub |
| `git pull` | Baixa e aplica atualizações do remoto |
| `git clone <url>` | Baixa um repositório |
| `git log --oneline` | Histórico resumido |
| `git checkout -b <branch>` | Cria e muda para nova branch |
| `git remote -v` | Mostra URL do repositório remoto |

---

## HTTPS vs SSH

| | HTTPS | SSH |
|---|---|---|
| URL | `https://github.com/user/repo.git` | `git@github.com:user/repo.git` |
| Autenticação | Usuário e senha / token | Chave SSH |
| Recomendado para | Primeiro uso, leitura pública | Uso diário, push/pull frequente |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `git: command not found` | Git não instalado ou terminal não reiniciado | Reinstalar ou reiniciar o terminal |
| `Permission denied (publickey)` | Chave SSH não adicionada ao agente | Rodar `ssh-add ~/.ssh/id_ed25519` |
| `remote: Repository not found` | URL errada ou sem acesso ao repositório | Verificar URL e permissões no GitHub |
| `failed to push — updates were rejected` | Remoto tem commits que você não tem localmente | Rodar `git pull` antes do `git push` |
| `merge conflict` | Mesmo arquivo editado em duas branches | Resolver o conflito manualmente e fazer novo commit |

---

## Boas práticas

- Faça commits pequenos e frequentes — uma mudança por commit
- Escreva mensagens de commit descritivas: `"corrige timeout na busca de tickets"` em vez de `"fix"`
- Nunca commite o `.env` — adicione ao `.gitignore`
- Sempre crie uma branch antes de alterar código em produção
- Faça `git pull` antes de começar a trabalhar para evitar conflitos