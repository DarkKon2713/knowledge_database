# Docker

## O que é Docker?

Docker é uma plataforma que empacota aplicações em **containers** — ambientes isolados que carregam tudo o que o código precisa para rodar (sistema, dependências, configurações), independente da máquina onde está sendo executado.

## Container vs Imagem

- **Imagem**: o pacote estático, como uma receita. Define o que o container vai ter.
- **Container**: a imagem rodando. É a instância em execução da imagem.

Uma imagem pode gerar vários containers ao mesmo tempo.

---

## Instalação no WSL (Ubuntu)

> Instale o Docker diretamente no WSL, sem Docker Desktop. É mais leve e funciona igual ao servidor Linux.

### 1. Remover versões antigas

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

### 2. Instalar dependências

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
```

### 3. Adicionar a chave GPG oficial do Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### 4. Adicionar o repositório

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 5. Instalar o Docker

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 6. Iniciar o serviço

O WSL não usa systemd por padrão — inicie o Docker manualmente:

```bash
sudo service docker start
```

Para não precisar repetir isso toda vez, adicione ao final do seu `~/.bashrc`:

```bash
echo 'sudo service docker start > /dev/null 2>&1' >> ~/.bashrc
```

### 7. Usar Docker sem sudo

```bash
sudo usermod -aG docker $USER
```

Feche e reabra o terminal WSL para aplicar.

### 8. Verificar instalação

```bash
docker --version
docker compose version
docker run hello-world
```

---

## Imagens

Imagens são baixadas do [Docker Hub](https://hub.docker.com) ou construídas localmente com um `Dockerfile`.

```bash
# Baixar uma imagem
docker pull ubuntu
docker pull python:3.12
docker pull postgres:16

# Listar imagens locais
docker images

# Remover uma imagem
docker rmi python:3.12

# Remover todas as imagens não usadas
docker image prune -a
```

---

## Containers

### Criar e iniciar

```bash
# Rodar um container e entrar no terminal
docker run -it ubuntu bash

# Rodar em background (modo detached)
docker run -d nginx

# Rodar com nome definido
docker run -d --name meu-postgres postgres:16

# Rodar com porta mapeada  (host:container)
docker run -d -p 5432:5432 --name meu-postgres postgres:16

# Rodar com variável de ambiente
docker run -d \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=meu_banco \
  -p 5432:5432 \
  --name meu-postgres \
  postgres:16
```

### Gerenciar containers

```bash
# Listar containers em execução
docker ps

# Listar todos (incluindo parados)
docker ps -a

# Parar um container
docker stop meu-postgres

# Iniciar um container parado
docker start meu-postgres

# Reiniciar
docker restart meu-postgres

# Remover um container parado
docker rm meu-postgres

# Parar e remover de uma vez
docker rm -f meu-postgres
```

### Inspecionar e acessar

```bash
# Ver logs do container
docker logs meu-postgres

# Seguir logs em tempo real
docker logs -f meu-postgres

# Abrir terminal dentro de um container em execução
docker exec -it meu-postgres bash

# Ver detalhes do container (IP, volumes, variáveis, etc.)
docker inspect meu-postgres
```

---

## Volumes

Volumes persistem dados fora do container — sem volume, tudo é apagado quando o container é removido.

```bash
# Criar volume
docker volume create meus-dados

# Usar volume ao criar container
docker run -d \
  -v meus-dados:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=senha123 \
  -p 5432:5432 \
  --name meu-postgres \
  postgres:16

# Mapear pasta local como volume (bind mount)
docker run -d \
  -v /home/usuario/dados:/var/lib/postgresql/data \
  postgres:16

# Listar volumes
docker volume ls

# Remover volume
docker volume rm meus-dados

# Remover volumes não usados
docker volume prune
```

---

## Docker Compose

Compose sobe múltiplos containers com um único comando, usando um arquivo `docker-compose.yml`.

### Exemplo — PostgreSQL + aplicação

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: senha123
      POSTGRES_DB: meu_banco
    ports:
      - "5432:5432"
    volumes:
      - dados_postgres:/var/lib/postgresql/data

  app:
    image: python:3.12
    volumes:
      - .:/app
    working_dir: /app
    command: python main.py
    depends_on:
      - db

volumes:
  dados_postgres:
```

### Comandos Compose

```bash
# Subir todos os serviços em background
docker compose up -d

# Subir e reconstruir imagens
docker compose up -d --build

# Ver status dos serviços
docker compose ps

# Ver logs de todos os serviços
docker compose logs

# Ver logs de um serviço específico
docker compose logs db

# Parar os serviços (mantém containers e volumes)
docker compose stop

# Parar e remover containers (mantém volumes)
docker compose down

# Parar, remover containers e volumes
docker compose down -v

# Rodar um comando dentro de um serviço
docker compose exec db psql -U admin -d meu_banco
```

---

## Referência rápida

### Imagens

| Comando | O que faz |
|---|---|
| `docker pull <imagem>` | Baixa uma imagem |
| `docker images` | Lista imagens locais |
| `docker rmi <imagem>` | Remove uma imagem |
| `docker image prune -a` | Remove imagens não usadas |

### Containers

| Comando | O que faz |
|---|---|
| `docker run -d <imagem>` | Cria e inicia em background |
| `docker run -it <imagem> bash` | Cria e entra no terminal |
| `docker ps` | Lista containers em execução |
| `docker ps -a` | Lista todos os containers |
| `docker stop <nome>` | Para um container |
| `docker start <nome>` | Inicia um container parado |
| `docker rm <nome>` | Remove um container parado |
| `docker rm -f <nome>` | Para e remove de uma vez |
| `docker logs -f <nome>` | Segue os logs em tempo real |
| `docker exec -it <nome> bash` | Abre terminal no container |

### Compose

| Comando | O que faz |
|---|---|
| `docker compose up -d` | Sobe todos os serviços |
| `docker compose down` | Para e remove containers |
| `docker compose down -v` | Remove containers e volumes |
| `docker compose ps` | Status dos serviços |
| `docker compose logs <serviço>` | Logs de um serviço |
| `docker compose exec <serviço> bash` | Terminal no serviço |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `Cannot connect to the Docker daemon` | Serviço Docker não iniciado | Executar `sudo service docker start` |
| `permission denied` ao rodar `docker` | Usuário fora do grupo docker | `sudo usermod -aG docker $USER` e reabrir terminal |
| `port is already allocated` | Porta já em uso no host | Mudar a porta do host: `-p 5433:5432` |
| `container name already in use` | Container com esse nome já existe | `docker rm -f <nome>` antes de recriar |
| `no space left on device` | Disco cheio com imagens/volumes | `docker system prune -a` para limpar tudo |

---

## Boas práticas

- Use `--name` sempre que criar containers — facilita gerenciar depois
- Use volumes para qualquer dado que precisa persistir (banco, uploads, logs)
- Prefira `docker compose` para projetos com mais de um container
- Use `docker compose down -v` apenas quando quiser apagar os dados também
- Rode `docker system prune` periodicamente para limpar imagens e containers não usados
