# Guia de Instalação: Python 3.12

Este documento descreve o passo a passo para instalar o Python no Windows, garantindo que ele seja reconhecido globalmente pelo sistema.
## 1. Download do Instalador

Acesse o site oficial: python.org/downloads
Procure pela versão Python 3.12.x (sempre escolha a versão estável mais recente do 3.12).
Clique em Windows installer (64-bit).

## 2. Processo de Instalação (Ponto Crítico)

Ao abrir o instalador, siga estas etapas exatamente nesta ordem:

Marque a caixa: Add Python 3.12 to PATH (Esta é a opção mais importante!).

(Opcional, mas recomendado) Marque Use admin privileges when installing py.exe.

Clique em Install Now.

***
Por que marcar o "Add Path"?

Sem isso, você não conseguirá digitar python ou pip no seu terminal (CMD, PowerShell ou terminal do VS Code) sem configurar manualmente as variáveis de ambiente depois.
***
## 3. Verificação da Instalação

Após o término da instalação, abra o seu terminal (ou o terminal do VS Code com Ctrl + ') e digite os comandos abaixo para confirmar:
Verificando a Versão do Python
Bash

```bash
python --version
``` 

Deve retornar: Python 3.12.x
Verificando o Gerenciador de Pacotes (PIP)


```bash
pip --version
``` 
Deve retornar a versão do pip e o local da instalação.
## 4. Resolução de Problemas

Se você digitar python e abrir a Microsoft Store ou der erro de "comando não encontrado":

Reinicie o VS Code: O terminal precisa ser reiniciado para ler o novo PATH.

Verifique os aliases: No Windows, pesquise por "Gerenciar aliases de execução de aplicativos" no menu Iniciar e desative os que dizem "Python".

### Próximos Passos

Com o Python 3.12 instalado e no PATH, você já pode criar ambientes virtuais para seus projetos:
Bash

