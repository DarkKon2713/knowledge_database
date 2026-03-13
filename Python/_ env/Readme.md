# Variáveis de Ambiente

Variáveis de ambiente guardam informações sensíveis **fora do código** — tokens, chaves de API, senhas e URLs que mudam entre ambientes (desenvolvimento, produção).

Nunca coloque esses valores diretamente no código. Se o repositório for compartilhado, qualquer pessoa com acesso vê as credenciais.

---

## Instalação

```bash
pip install python-dotenv
```

---

## Estrutura

```text
_env/
├── dotenv_example.py   — como carregar e usar variáveis de ambiente
└── Readme.md           — este arquivo
```

No projeto, você vai precisar criar dois arquivos na raiz:

```text
projeto/
├── .env              ← seus valores reais (nunca commitar)
├── .env.example      ← modelo com as chaves, sem valores (commitar)
└── .gitignore        ← deve conter `.env`
```

---

## Formato do `.env`

```env
API_TOKEN=seu_token_aqui
API_URL=https://api.exemplo.com
AMBIENTE=development
TIMEOUT=10
DEBUG=false
```

Regras:
- uma variável por linha, no formato `CHAVE=VALOR`
- sem espaços ao redor do `=`
- sem aspas (a menos que o valor contenha espaços)
- linhas com `#` são comentários

---

## Formato do `.env.example`

O `.env.example` documenta quais variáveis o projeto precisa, sem expor os valores reais. Commite este arquivo no repositório.

```env
API_TOKEN=
API_URL=
AMBIENTE=development
TIMEOUT=10
DEBUG=false
```

---

## `.gitignore`

Adicione ao seu `.gitignore`:

```
.env
```

O `.env` nunca deve ser commitado. O `.env.example` sim.

---

## Uso básico

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv("API_TOKEN")           # None se não existir
ambiente  = os.getenv("AMBIENTE", "development")  # valor padrão
timeout   = int(os.getenv("TIMEOUT", "10"))  # converter para int
```

> Tudo que vem do `.env` é string — converta o tipo quando necessário.

---

## Erros comuns

| Situação | Causa | Solução |
|---|---|---|
| Variável retorna `None` | `.env` não foi carregado ou chave errada | Verificar se `load_dotenv()` foi chamado e se a chave bate com o `.env` |
| `KeyError` | Usou `os.environ[]` e a variável não existe | Usar `os.getenv()` ou validar antes |
| Valor numérico causa `TypeError` | Esqueceu de converter o tipo | Envolver com `int()`, `float()` etc. |
| Token vazou no repositório | `.env` foi commitado | Revogar o token imediatamente e recriar |

---

## Próximo passo

Com o `.env` configurado, veja como usar o token nas requisições HTTP em `python/http/`.