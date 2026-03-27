# Python — Utils

Utilitários do dia a dia — datas, regex, logging e debugging.

```bash
pip install python-dateutil
```

---

## Estrutura

```text
utils/
├── datetime_examples.py   — datas, horários, timedelta, SLA
├── regex_examples.py      — busca, extração e validação com regex
├── logging_config.py      — configuração de logging: handlers, rotação, múltiplos destinos
├── log_handling.py        — tratamento de logs: exceções, contexto, LoggerAdapter
├── print_debug.py         — print vs logging, pprint, f-string com =, progresso
└── Readme.md
```

---

## O que cada arquivo cobre

### `datetime_examples.py`

| Conceito | Descrição |
|---|---|
| `datetime.now()` | Data e hora atual |
| `strftime()` | datetime → string formatada |
| `strptime()` | string com formato fixo → datetime |
| `dateutil.parser.parse()` | string com formato variável → datetime |
| `timedelta` | Somar/subtrair horas, dias, minutos |
| `relativedelta` | Somar/subtrair meses e anos |
| Timestamp Unix | Conversão de/para segundos desde 1970 |
| Timezone | `datetime.now(tz=timezone.utc)` |

### `regex_examples.py`

| Função | Descrição |
|---|---|
| `re.search()` | Primeira ocorrência no texto |
| `re.findall()` | Todas as ocorrências |
| `re.sub()` | Substituição de padrões |
| `re.fullmatch()` | Validação de formato |
| Grupos de captura | Extrair partes específicas com `()` |
| Grupos nomeados | `(?P<nome>...)` para acesso por nome |
| `re.compile()` | Reutilizar padrão compilado |
| Flags | `re.I` (case insensitive), `re.M` (multiline) |

### `logging_config.py`

| Conceito | Descrição |
|---|---|
| `basicConfig()` | Configuração mínima para scripts simples |
| Níveis | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `getLogger(__name__)` | Logger por módulo — rastreia a origem dos logs |
| `FileHandler` | Salvar logs em arquivo |
| `StreamHandler` | Exibir logs no console |
| `RotatingFileHandler` | Rotação por tamanho (ex: máx 5MB) |
| `TimedRotatingFileHandler` | Rotação por tempo (diária, semanal) |
| Silenciar libs externas | `logging.getLogger("urllib3").setLevel(WARNING)` |

### `log_handling.py`

| Conceito | Descrição |
|---|---|
| `logger.exception()` | Loga erro + traceback completo (usar dentro de `except`) |
| `logger.error()` | Loga erro sem traceback (quando erro já é esperado) |
| `exc_info=True` | Adiciona traceback em qualquer nível (`warning`, `info`) |
| `% formatting` | `logger.info("%s", val)` — lazy, não formata se nível inativo |
| `extra={}` | Adiciona campos customizados acessíveis no formatter |
| `LoggerAdapter` | Contexto persistente sem repetir `extra=` a cada chamada |
| `propagate=False` | Impede logs de subirem para o logger raiz (evita duplicação) |
| Loop com progresso | Logar a cada N iterações para evitar flood |

### `print_debug.py`

| Conceito | Descrição |
|---|---|
| Quando usar print | Scripts simples, notebooks, saída para usuário, debug rápido |
| Quando usar logging | Produção, múltiplos módulos, timestamp, filtro por nível |
| `sep=`, `end=`, `flush=` | Parâmetros de print para controlar saída |
| `f"{var=}"` | Mostra nome e valor automaticamente (Python 3.8+) |
| `pprint.pprint()` | Formata dicts/listas complexas com indentação |
| `pprint.pformat()` | Retorna string formatada (para passar ao logging) |
| Progresso com `\r` | Sobrescreve linha no terminal sem criar novas linhas |

| Padrão | Significado |
|---|---|
| `\d` | Dígito (0-9) |
| `\w` | Letra, dígito ou `_` |
| `\s` | Espaço, tab, newline |
| `.` | Qualquer caractere |
| `+` | 1 ou mais |
| `*` | 0 ou mais |
| `?` | 0 ou 1 (opcional) |
| `{n,m}` | Entre n e m vezes |
| `^` / `$` | Início / fim da string |
| `[abc]` | a, b ou c |
| `(...)` | Grupo de captura |

---

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `ValueError: time data does not match format` | Formato do `strptime` não bate com a string | Usar `dateutil.parser.parse()` ou corrigir o formato |
| `re.error: nothing to repeat` | Padrão regex inválido (ex: `+` sem caractere antes) | Revisar o padrão |
| `AttributeError: 'NoneType'` | `re.search()` retornou `None` | Verificar `if match:` antes de `.group()` |
| Datas com timezone incompatível | Misturar datetime com e sem timezone | Usar sempre `tz=timezone.utc` ou sempre sem timezone |
| `logging` duplicando mensagens | `basicConfig()` chamado mais de uma vez | Limpar handlers com `logger.handlers.clear()` antes de adicionar |
| `logger.exception()` fora de `except` | Chamado fora de bloco de exceção — traceback fica vazio | Usar só dentro de `except`, ou usar `logger.error()` fora |
| `logger.info(f"val={x}")` | f-string sempre formata, mesmo se nível inativo | Usar `logger.info("val=%s", x)` para lazy formatting |
| `KeyError` no formatter com `extra` | Campo do `extra={}` não definido em todas as chamadas | Usar `LoggerAdapter` para garantir contexto em todos os logs |