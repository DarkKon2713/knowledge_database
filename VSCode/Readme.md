## 🚀 Guia de Configuração: VS Code Profissional

Este documento orienta a instalação de extensões essenciais e a organização do ambiente de desenvolvimento para evitar poluição visual de arquivos de cache.
### 1. Instalação de Extensões Essenciais

Para abrir o painel de extensões, utilize o atalho:

```bash
Ctrl + Shift + X
```

O que faz: Visualiza o histórico do Git em forma de gráfico interativo, facilitando o entendimento de branches e merges.


#### Gemini Code Assist

O que faz: Assistente de IA do Google para codificação, oferecendo preenchimento automático e explicações de lógica.

####   FileTree Pro

O que faz: Gera árvores de diretórios organizadas, ideais para documentar a estrutura do projeto.



### 2. Limpeza de Ambiente (Python)


Arquivos __pycache__ e .pyc são gerados automaticamente e poluem o explorador de arquivos. Veja como escondê-los:
Método 1: Interface Gráfica (Recomendado)

    Abra as Configurações: Ctrl + ,

    Pesquise por: files exclude

    Clique em Add Pattern e adicione:

        **/__pycache__/

        **/*.pyc

Método 2: Via settings.json (Direto)

    Abra a Command Palette: Ctrl + Shift + P

    Busque por: Preferences: Open User Settings (JSON)

    Cole o seguinte bloco de código:

JSON
```json
{
  "files.exclude": {
    "**/__pycache__/": true,
    "**/*.pyc": true
  },
  "search.exclude": {
    "**/__pycache__/": true,
    "**/*.pyc": true
  }
}
```

Com essas configurações, seu VS Code terá uma interface limpa, focada apenas no código-fonte, com ferramentas visuais poderosas para controle de versão e auxílio de IA.

