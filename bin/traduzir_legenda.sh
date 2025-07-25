#!/bin/bash

# Descrição: Script para traduzir um arquivo de legenda .srt.
# Autor: Cline
# Data: 2025-07-22

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly RAIZ_PROJETO="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Função para mostrar ajuda
function mostrar_ajuda() {
    echo "Uso: $SCRIPT_NAME [opções] <caminho_para_arquivo_srt>"
    echo
    echo "Este script traduz o conteúdo de um arquivo .srt para português do Brasil."
    echo "Requer que um arquivo .env exista na pasta 'config' com as chaves da API."
    echo
    echo "Opções:"
    echo "  --fala-inicial <número>   Índice da primeira fala a ser traduzida."
    echo "  --fala-final <número>     Índice da última fala a ser traduzida."
    echo "  -h, --help                Mostra esta ajuda."
}

# Função principal
function main() {
    # --- Parsing de Argumentos ---
    local arquivo_srt=""
    local argumentos_python=()

    # Loop para processar todos os argumentos
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -h|--help)
                mostrar_ajuda
                exit 0
                ;;
            --fala-inicial|--fala-final)
                if [[ -z "$2" || "$2" == -* ]]; then
                    echo "Erro: O argumento '$1' requer um valor numérico." >&2
                    exit 1
                fi
                # Adiciona o argumento e seu valor para o script python
                argumentos_python+=("$1" "$2")
                shift 2 # Pula o argumento e seu valor
                ;;
            -*)
                echo "Erro: Opção desconhecida '$1'" >&2
                mostrar_ajuda
                exit 1
                ;;
            *)
                # Assume que o último argumento sem flag é o arquivo srt
                if [[ -n "$arquivo_srt" ]]; then
                    echo "Erro: Apenas um arquivo .srt pode ser especificado." >&2
                    mostrar_ajuda
                    exit 1
                fi
                arquivo_srt="$1"
                shift
                ;;
        esac
    done

    # Validar se o arquivo SRT foi fornecido
    if [[ -z "$arquivo_srt" ]]; then
        echo "Erro: O caminho para o arquivo .srt não foi fornecido." >&2
        mostrar_ajuda
        exit 1
    fi

    # Validar se o arquivo de entrada existe
    if [[ ! -f "$arquivo_srt" ]]; then
        echo "Erro: Arquivo '$arquivo_srt' não encontrado." >&2
        exit 1
    fi

    # Carregar variáveis de ambiente do arquivo .env
    local arquivo_env="${RAIZ_PROJETO}/config/.env"
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

    # Ativar o ambiente virtual se não estiver ativo
    if [[ -z "$VIRTUAL_ENV" ]]; then
        local venv_path="${RAIZ_PROJETO}/venv/bin/activate"
        if [[ -f "$venv_path" ]]; then
            echo "Ativando ambiente virtual..."
            source "$venv_path"
        else
            echo "Erro: Ambiente virtual 'venv' não encontrado em ${RAIZ_PROJETO}." >&2
            echo "Execute o script 'setup.sh' para criar o ambiente." >&2
            exit 1
        fi
    fi

    # Executar o script Python principal
    python3 "${RAIZ_PROJETO}/src/main.py" translate --arquivo-entrada "$arquivo_srt" "${argumentos_python[@]}"

    echo "Tradução concluída."
}

# Execução principal
main "$@"
