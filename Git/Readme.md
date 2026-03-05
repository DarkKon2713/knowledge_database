#  Instalar Git e Clonar um Repositório do GitHub

Este guia mostra passo a passo como:

1.  Instalar o **Git**
2.  Configurar seu usuário
3.  Conectar com o **GitHub**
4.  Fazer **git clone** de um repositório

------------------------------------------------------------------------

# 1. O que é Git?

O **Git** é um sistema de controle de versão.

Ele serve para:

-   salvar versões do seu código
-   acompanhar mudanças
-   colaborar com outras pessoas
-   enviar código para o **GitHub**

------------------------------------------------------------------------

# 2. O que é GitHub?

O **GitHub** é uma plataforma online que hospeda repositórios Git.

Você pode:

-   armazenar projetos
-   colaborar com outros programadores
-   compartilhar código

Site:

https://github.com

------------------------------------------------------------------------

# 3. Instalando o Git

## Windows

1.  Acesse:

https://git-scm.com/download/win

2.  Baixe o instalador
3.  Execute o `.exe`
4.  Clique **Next** nas opções padrão

Depois da instalação, abra o **Git Bash**.

------------------------------------------------------------------------

## Linux (Ubuntu / Debian)

``` bash
sudo apt update
sudo apt install git
```

------------------------------------------------------------------------

## Mac

``` bash
brew install git
```

ou instale via:

https://git-scm.com

------------------------------------------------------------------------

# 4. Verificando se o Git foi instalado

Abra o terminal e rode:

``` bash
git --version
```

Exemplo de saída:

    git version 2.43.0

------------------------------------------------------------------------

# 5. Configurando seu usuário no Git

Antes de usar o Git, você precisa definir:

-   nome
-   email

Execute:

``` bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@gmail.com"
```

Exemplo:

``` bash
git config --global user.name "João Silva"
git config --global user.email "joao@gmail.com"
```

Verificar configuração:

``` bash
git config --list
```

------------------------------------------------------------------------

# 6. Criando uma conta no GitHub

1.  Acesse:

https://github.com

2.  Clique em **Sign up**

3.  Crie:

-   username
-   email
-   senha

------------------------------------------------------------------------

# 7. Encontrando um repositório para clonar

Exemplo de repositório:

    https://github.com/psf/requests

Clique no botão **Code**.

Copie a URL:

    https://github.com/psf/requests.git

------------------------------------------------------------------------

# 8. O que é `git clone`?

O comando **git clone** baixa um repositório remoto para seu computador.

Ele cria uma **cópia completa do projeto**.

------------------------------------------------------------------------

# 9. Clonando um repositório

Abra o terminal e vá até a pasta onde deseja salvar o projeto.

Exemplo:

``` bash
cd Desktop
```

Agora execute:

``` bash
git clone https://github.com/psf/requests.git
```

Saída esperada:

    Cloning into 'requests'...
    remote: Enumerating objects...
    Receiving objects...

------------------------------------------------------------------------

# 10. Entrando na pasta do projeto

Depois do clone:

``` bash
cd requests
```

Ver arquivos:

``` bash
ls
```

ou no Windows:

``` bash
dir
```

------------------------------------------------------------------------

# 11. Verificando o repositório Git

Você pode ver o status com:

``` bash
git status
```

Isso mostra:

-   arquivos modificados
-   branch atual
-   estado do repositório

------------------------------------------------------------------------

# 12. Comandos Git básicos

### Ver status

``` bash
git status
```

### Ver histórico

``` bash
git log
```

### Baixar atualizações

``` bash
git pull
```

### Ver repositório remoto

``` bash
git remote -v
```

------------------------------------------------------------------------

# 13. Estrutura de um repositório clonado

Depois do clone você terá algo assim:

    projeto/
    │
    ├─ README.md
    ├─ src/
    ├─ requirements.txt
    └─ .git/

A pasta `.git` contém todo o histórico do projeto.

------------------------------------------------------------------------

# 14. Problemas comuns

## Git não reconhecido

Erro:

    git: command not found

Solução:

-   reinicie o terminal
-   verifique se instalou corretamente

------------------------------------------------------------------------

## Permissão negada no GitHub

Pode acontecer se estiver usando SSH sem configurar chave.

Use a URL **HTTPS** para começar.

Exemplo:

    https://github.com/user/repositorio.git

------------------------------------------------------------------------

# 15. Próximos passos para aprender

Depois de aprender `git clone`, vale estudar:

-   `git add`
-   `git commit`
-   `git push`
-   `git branch`
-   `git merge`

Esses comandos permitem **contribuir com projetos no GitHub**.

------------------------------------------------------------------------

# Resumo

Passos principais:

1️⃣ Instalar Git\
2️⃣ Configurar usuário\
3️⃣ Criar conta no GitHub\
4️⃣ Copiar URL do repositório\
5️⃣ Executar:

``` bash
git clone URL_DO_REPOSITORIO
```

Pronto 🎉 você baixou um projeto do GitHub.


#  Conectar Git ao GitHub usando SSH

Este guia mostra passo a passo como:

1.  Gerar uma **chave SSH**
2.  Adicionar a chave no **GitHub**
3.  Testar a conexão
4.  Clonar repositórios usando **SSH**

------------------------------------------------------------------------

# 1. O que é SSH no GitHub?

SSH (Secure Shell) permite que você se conecte ao GitHub **sem precisar
digitar usuário e senha toda vez**.

Em vez disso, o Git usa:

-   uma **chave pública** (vai para o GitHub)
-   uma **chave privada** (fica no seu computador)

Isso torna a autenticação **mais segura e mais prática**.

------------------------------------------------------------------------

# 2. Verificando se você já tem uma chave SSH

Abra o terminal e execute:

``` bash
ls ~/.ssh
```

Se aparecer algo como:

    id_rsa
    id_rsa.pub

ou

    id_ed25519
    id_ed25519.pub

então você **já tem uma chave SSH**.

Caso contrário, vamos criar uma.

------------------------------------------------------------------------

# 3. Gerando uma nova chave SSH

Execute:

``` bash
ssh-keygen -t ed25519 -C "seuemail@gmail.com"
```

Explicação:

-   `ssh-keygen` → ferramenta para gerar chaves
-   `-t ed25519` → tipo de chave moderna e segura
-   `-C` → comentário (normalmente seu email)

Pressione **Enter** para aceitar os caminhos padrão.

Resultado esperado:

    ~/.ssh/id_ed25519
    ~/.ssh/id_ed25519.pub

------------------------------------------------------------------------

# 4. Iniciando o agente SSH

Execute:

``` bash
eval "$(ssh-agent -s)"
```

Agora adicione sua chave:

``` bash
ssh-add ~/.ssh/id_ed25519
```

------------------------------------------------------------------------

# 5. Copiando a chave pública

Agora precisamos copiar a **chave pública** para colocar no GitHub.

Execute:

``` bash
cat ~/.ssh/id_ed25519.pub
```

Aparecerá algo assim:

    ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... seuemail@gmail.com

Copie **todo esse texto**.

------------------------------------------------------------------------

# 6. Adicionando a chave no GitHub

1.  Acesse:

https://github.com/settings/keys

2.  Clique em **New SSH Key**

3.  Preencha:

**Title**

    Meu computador

**Key**

Cole a chave copiada.

4.  Clique em **Add SSH Key**

------------------------------------------------------------------------

# 7. Testando a conexão com GitHub

Agora teste:

``` bash
ssh -T git@github.com
```

Primeira vez aparecerá:

    Are you sure you want to continue connecting?

Digite:

    yes

Se tudo estiver certo:

    Hi username! You've successfully authenticated.

------------------------------------------------------------------------

# 8. Clonando repositórios usando SSH

Agora você pode usar a URL SSH.

Exemplo:

    git@github.com:psf/requests.git

Clone com:

``` bash
git clone git@github.com:psf/requests.git
```

------------------------------------------------------------------------

# 9. Diferença entre HTTPS e SSH

HTTPS:

    https://github.com/user/repositorio.git

SSH:

    git@github.com:user/repositorio.git

### HTTPS

-   pede login às vezes

### SSH

-   usa chave
-   não pede senha

------------------------------------------------------------------------

# 10. Verificando qual URL seu repositório usa

Dentro do projeto:

``` bash
git remote -v
```

Saída:

    origin  git@github.com:user/repositorio.git (fetch)
    origin  git@github.com:user/repositorio.git (push)

------------------------------------------------------------------------

# 11. Problemas comuns

### Permission denied (publickey)

Erro:

    Permission denied (publickey)

Soluções:

-   verificar se a chave foi adicionada no GitHub
-   rodar:

``` bash
ssh-add ~/.ssh/id_ed25519
```

------------------------------------------------------------------------

# Resumo

Passos principais:

1️⃣ Gerar chave SSH

``` bash
ssh-keygen -t ed25519 -C "email"
```

2️⃣ Iniciar agente

``` bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

3️⃣ Copiar chave pública

``` bash
cat ~/.ssh/id_ed25519.pub
```

4️⃣ Adicionar no GitHub

https://github.com/settings/keys

5️⃣ Testar conexão

``` bash
ssh -T git@github.com
```

Agora você pode usar GitHub via **SSH sem senha**.



