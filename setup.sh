#!/bin/bash
#
# setup.sh
# Autor: Henrico Scaranello
# Data: 2025-07-21
#
# Descrição: Script para configurar o ambiente de desenvolvimento do projeto.
# Este script verifica as dependências, cria o ambiente virtual Python
# e instala os pacotes necessários do requirements.txt.

# Opções de segurança:
# -e: sai imediatamente se um comando falhar
# -u: trata variáveis não definidas como um erro
# -o pipefail: o status de saída de um pipe é o do último comando que falhou
set -euo pipefail

# --- Constantes ---
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Cores para o output
readonly COR_VERDE='\033[0;32m'
readonly COR_AMARELA='\033[1;33m'
readonly COR_VERMELHA='\033[0;31m'
readonly SEM_COR='\033[0m'

# Nomes de arquivos e diretórios
readonly VENV_DIR="venv"
readonly REQUIREMENTS_FILE="requirements.txt"
readonly ENV_EXAMPLE_FILE="config/.env.example"
readonly ENV_FILE="config/.env"

# --- Funções ---

# Mostra uma mensagem de log formatada
function log() {
    local cor="$1"
    local mensagem="$2"
    echo -e "${cor}${mensagem}${SEM_COR}"
}

# Função principal do script
function main() {
    log "$SEM_COR" "--> Iniciando a configuração do ambiente..."
    cd "$SCRIPT_DIR" # Garante que estamos no diretório do script

    # 1. Verifica as dependências do sistema
    log "$SEM_COR" "--> Verificando dependências do sistema..."

    # Verifica ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        log "$COR_VERMELHA" "Erro: O comando 'ffmpeg' não foi encontrado."
        log "$SEM_COR" "Por favor, instale o ffmpeg (ex: 'sudo apt install ffmpeg') e tente novamente."
        exit 1
    fi

    # Verifica Python 3 e venv
    if ! python3 -m venv --help &> /dev/null; then
        log "$COR_VERMELHA" "Erro: O comando 'python3' não está disponível ou o módulo 'venv' não pôde ser encontrado."
        log "$SEM_COR" "Por favor, instale o Python 3 e o pacote python3-venv (ex: 'sudo apt install python3-venv') e tente novamente."
        exit 1
    fi
    log "$COR_VERDE" "Dependências do sistema (ffmpeg, Python, venv) verificadas com sucesso."


    # 2. Cria o ambiente virtual
    if [[ ! -d "$VENV_DIR" ]]; then
        log "$SEM_COR" "--> Criando ambiente virtual em '$VENV_DIR/'..."
        python3 -m venv "$VENV_DIR"
        log "$COR_VERDE" "Ambiente virtual criado."
    else
        log "$SEM_COR" "--> Ambiente virtual '$VENV_DIR/' já existe."
    fi

    # 3. Instala as dependências do requirements.txt
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        log "$SEM_COR" "--> Instalando dependências do '$REQUIREMENTS_FILE'..."
        "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE"
        log "$COR_VERDE" "Dependências instaladas com sucesso."
    else
        log "$COR_VERMELHA" "Erro: Arquivo '$REQUIREMENTS_FILE' não encontrado. Nenhuma dependência foi instalada."
    fi
    
    # 4. Verifica o arquivo de configuração .env
    if [[ ! -f "$ENV_FILE" && -f "$ENV_EXAMPLE_FILE" ]]; then
        log "$COR_AMARELA" "Aviso: O arquivo de configuração '$ENV_FILE' não foi encontrado."
        log "$COR_AMARELA" "Considere copiá-lo a partir de '$ENV_EXAMPLE_FILE' e preencher os valores."
    fi

    echo # Linha em branco para espaçamento
    log "$SEM_COR" "--> Ambiente configurado com sucesso!"
}

# --- Execução Principal ---
# Garante que o script só executa a função main se for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
