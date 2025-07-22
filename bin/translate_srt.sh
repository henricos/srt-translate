#!/bin/bash

# Descrição: Script para traduzir um arquivo de legenda .srt.
# Autor: Cline
# Data: 2025-07-22

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Função para mostrar ajuda
function mostrar_ajuda() {
    echo "Uso: $SCRIPT_NAME <caminho_para_arquivo_srt>"
    echo
    echo "Este script traduz o conteúdo de um arquivo .srt para português do Brasil."
    echo "Requer que um arquivo .env exista na pasta 'config' com as chaves da API."
}

# Função principal
function main() {
    # Validar número de argumentos
    if [[ "$#" -ne 1 ]]; then
        echo "Erro: Número incorreto de argumentos." >&2
        mostrar_ajuda
        exit 1
    fi

    local arquivo_srt="$1"

    # Validar se o argumento é -h ou --help
    if [[ "$arquivo_srt" == "-h" || "$arquivo_srt" == "--help" ]]; then
        mostrar_ajuda
        exit 0
    fi

    # Validar se o arquivo de entrada existe
    if [[ ! -f "$arquivo_srt" ]]; then
        echo "Erro: Arquivo '$arquivo_srt' não encontrado." >&2
        exit 1
    fi

    # Carregar variáveis de ambiente do arquivo .env
    local arquivo_env="${PROJECT_ROOT}/config/.env"
    if [[ -f "$arquivo_env" ]]; then
        export $(grep -v '^#' "$arquivo_env" | xargs)
    else
        echo "Erro: Arquivo de configuração '$arquivo_env' não encontrado." >&2
        exit 1
    fi

    # Validar se as variáveis de ambiente essenciais estão definidas
    if [[ -z "${GEMINI_API_KEY:-}" ]]; then
        echo "Erro: A variável de ambiente GEMINI_API_KEY não está definida no arquivo .env." >&2
        exit 1
    fi

    echo "Iniciando tradução para o arquivo: $arquivo_srt"

    # Executar o script Python principal
    python3 "${PROJECT_ROOT}/src/main.py" translate --input-file "$arquivo_srt"

    echo "Tradução concluída."
}

# Execução principal
main "$@"
