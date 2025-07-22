#!/bin/bash
#
# setup.sh
# Autor: Henrico Scaranello
# Data: 2025-07-21
#
# Descrição: Script para configurar o ambiente de desenvolvimento do projeto.
# Este script verifica as dependências, cria o ambiente virtual Python
# e instala os pacotes necessários do requirements.txt.

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

# Função para tratar erros e sair (mantida para logs, mas exit será direto)
function tratar_erro() {
    local mensagem_erro="$1"
    log "$COR_VERMELHA" "Erro: $mensagem_erro"
    log "$SEM_COR" "A configuração foi interrompida."
    # O exit 1 será chamado diretamente nos blocos if para garantir saída imediata
}

# Função para verificar as dependências do sistema
function verificar_dependencias_sistema() {
    log "$SEM_COR" "--> Verificando dependências do sistema..."

    # Função auxiliar para verificar pacotes apt
    function verificar_pacote_apt() {
        local pacote="$1"
        local mensagem_erro="$2"
        if ! dpkg -s "$pacote" &> /dev/null; then
            log "$COR_VERMELHA" "Erro: O pacote '$pacote' não foi encontrado. Por favor, instale-o ($mensagem_erro)."
            log "$SEM_COR" "A configuração foi interrompida."
            exit 1
        fi
    }

    # Verifica ffmpeg
    verificar_pacote_apt "ffmpeg" "ex: 'sudo apt install ffmpeg'"

    # Verifica Python 3 (o executável)
    if ! command -v python3 &> /dev/null; then
        log "$COR_VERMELHA" "Erro: 'python3' não foi encontrado. Por favor, instale-o."
        log "$SEM_COR" "A configuração foi interrompida."
        exit 1
    fi

    # Verifica o pacote python3-venv
    verificar_pacote_apt "python3-venv" "ex: 'sudo apt install python3-venv'"

    # Verifica o pacote python3-pip
    verificar_pacote_apt "python3-pip" "ex: 'sudo apt install python3-pip'"

    log "$COR_VERDE" "Dependências do sistema (ffmpeg, Python, venv, pip) verificadas com sucesso."
}

# Função principal do script
function main() {
    log "$SEM_COR" "--> Iniciando a configuração do ambiente..."
    cd "$SCRIPT_DIR" # Garante que estamos no diretório do script

    # 1. Verifica as dependências do sistema
    verificar_dependencias_sistema

    # 2. Cria o ambiente virtual
    if [[ ! -d "$VENV_DIR" ]]; then
        log "$SEM_COR" "--> Criando ambiente virtual em '$VENV_DIR/'..."
        if ! python3 -m venv "$VENV_DIR"; then
            log "$COR_VERMELHA" "Erro: Falha ao criar o ambiente virtual. Verifique se o pacote 'python3-venv' (e suas dependências como 'python3-pip') está instalado corretamente."
            log "$SEM_COR" "A configuração foi interrompida."
            exit 1
        fi
        log "$COR_VERDE" "Ambiente virtual criado com sucesso."
    else
        log "$SEM_COR" "--> Ambiente virtual '$VENV_DIR/' já existe."
    fi

    # Verifica se o pip existe dentro do venv
    if [[ ! -f "$VENV_DIR/bin/pip" ]]; then
        log "$COR_VERMELHA" "Erro: O executável 'pip' não foi encontrado no ambiente virtual. A criação do venv pode ter falhado."
        log "$SEM_COR" "A configuração foi interrompida."
        exit 1
    fi

    # 3. Instala as dependências do requirements.txt
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        log "$SEM_COR" "--> Instalando dependências do '$REQUIREMENTS_FILE'..."
        if ! "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE"; then
            log "$COR_VERMELHA" "Erro: Falha ao instalar as dependências do '$REQUIREMENTS_FILE'."
            log "$SEM_COR" "A configuração foi interrompida."
            exit 1
        fi
        log "$COR_VERDE" "Dependências instaladas com sucesso."
    else
        log "$COR_AMARELA" "Aviso: Arquivo '$REQUIREMENTS_FILE' não encontrado. Nenhuma dependência foi instalada."
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
