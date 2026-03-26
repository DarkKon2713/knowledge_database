# WSL — Windows Subsystem for Linux

## O que é WSL?

WSL é o **Windows Subsystem for Linux** — um recurso do Windows que permite rodar um ambiente Linux diretamente no Windows, sem precisar de máquina virtual ou dual boot.

Com o WSL você tem acesso a um terminal Linux real, com os mesmos comandos, ferramentas e comportamento que você usaria em um servidor Ubuntu. Isso é importante porque a maioria dos servidores em produção roda Linux — desenvolver no mesmo ambiente evita surpresas no deploy.

## Por que usar WSL?

- Ambiente idêntico ao servidor de produção
- Ferramentas Linux nativas (`bash`, `curl`, `grep`, `ssh`, etc.)
- Melhor compatibilidade com Docker, Python, Node e bancos de dados
- Integração direta com o VS Code

---

## Requisitos

- Windows 10 versão 2004 ou superior (Build 19041+)
- Windows 11 (qualquer versão)

Verificar versão do Windows:
```
Configurações → Sistema → Sobre → Especificações do Windows
```

---

## Instalação

### Método rápido (recomendado)

Abra o **PowerShell como Administrador** e execute:

```powershell
wsl --install
```

Esse comando instala automaticamente:
- WSL 2 (versão mais recente)
- Ubuntu (distribuição padrão)

Após a instalação, **reinicie o computador**.

Na primeira abertura do Ubuntu, crie seu usuário Linux:
```
Enter new UNIX username: seu_usuario
Enter new UNIX password: sua_senha
```

---

## Verificar instalação

```bash
# Ver versão do WSL
wsl --version

# Listar distribuições instaladas
wsl --list --verbose

# Ver distribuição padrão
wsl --status
```

Saída esperada em `wsl --list --verbose`:
```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

---

## Atualizar o Ubuntu

Após instalar, atualize os pacotes:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Instalar ferramentas essenciais

```bash
# Ferramentas de desenvolvimento básicas
sudo apt install -y build-essential curl wget git unzip

# Python (geralmente já vem instalado)
python3 --version
python3 -m pip --version

# pip (se não tiver)
sudo apt install -y python3-pip

# pipenv ou virtualenv
pip3 install virtualenv
```

---

## Integração com VS Code

O VS Code detecta o WSL automaticamente com a extensão **WSL** (da Microsoft).

### Instalar a extensão

No VS Code, instale: `ms-vscode-remote.remote-wsl`

### Abrir o VS Code dentro do WSL

```bash
# Dentro do terminal WSL, na pasta do projeto
code .
```

Isso abre o VS Code conectado ao ambiente Linux — extensões, terminal e arquivos rodam no WSL.

---

## Navegar entre Windows e WSL

### Acessar arquivos do Windows dentro do WSL

Os arquivos do Windows ficam em `/mnt/`:

```bash
ls /mnt/c/Users/seu_usuario/Desktop
cd /mnt/c/Users/seu_usuario/OneDrive/Desktop/knowledge_database
```

### Acessar arquivos do WSL no Windows Explorer

Na barra de endereço do Explorer, digite:
```
\\wsl$\Ubuntu
```

Ou use o atalho no painel lateral do Explorer: **Linux → Ubuntu**.

---

## Configuração do Git no WSL

O Git dentro do WSL é separado do Git do Windows. Configure novamente:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@gmail.com"
```

Gerar chave SSH para o GitHub (dentro do WSL):

```bash
ssh-keygen -t ed25519 -C "seuemail@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub  # copie e adicione no GitHub
```

---

## Referência rápida — comandos WSL (PowerShell)

| Comando | O que faz |
|---|---|
| `wsl --install` | Instala WSL + Ubuntu |
| `wsl --list --verbose` | Lista distribuições e versões |
| `wsl --status` | Mostra configuração atual |
| `wsl --update` | Atualiza o WSL |
| `wsl --shutdown` | Encerra todas as instâncias WSL |
| `wsl --set-default Ubuntu` | Define Ubuntu como padrão |
| `wsl --unregister Ubuntu` | Remove a distribuição (apaga tudo) |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `WslRegisterDistribution failed with error: 0x80370102` | Virtualização desabilitada no BIOS | Ativar Intel VT-x / AMD-V na BIOS |
| `Error: 0xc03a001a` | Espaço insuficiente em disco | Liberar espaço no disco C: |
| `WSL 2 requires an update to its kernel component` | Kernel do WSL desatualizado | Executar `wsl --update` no PowerShell |
| VS Code não conecta ao WSL | Extensão WSL não instalada | Instalar `ms-vscode-remote.remote-wsl` |
| `Permission denied` ao acessar `/mnt/c/` | Problema de permissão | Rodar `sudo chmod` ou acessar via terminal normal |

---

## Boas práticas

- Mantenha seus projetos **dentro do WSL** (`~/projetos/`) em vez de em `/mnt/c/` — o desempenho de I/O é muito melhor
- Use `wsl --shutdown` ao terminar o dia para liberar memória RAM
- Prefira instalar ferramentas de desenvolvimento (Python, Node, pip) dentro do WSL, não no Windows
- Configure o Git separadamente no WSL — ele não compartilha configurações com o Git do Windows
