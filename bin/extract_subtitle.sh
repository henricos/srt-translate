#!/bin/bash

# Descrição: Extrai legendas SRT de um arquivo de vídeo MKV.
# Autor: Henrico Scaranello
# Data: 2025-07-21
#
# Uso: ./extract_subtitle.sh /caminho/para/video.mkv

# Constantes
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly PASTA_SAIDA="${SCRIPT_DIR}/../output"

# Funções
function mostrar_ajuda() {
    echo "Uso: $SCRIPT_NAME <caminho_para_arquivo_mkv>"
    echo
    echo "Extrai todas as faixas de legenda no formato SRT de um arquivo de vídeo Matroska (MKV)."
    echo "Os arquivos de legenda são salvos na pasta '$PASTA_SAIDA' com o nome do vídeo e o código do idioma."
    echo
    echo "Opções:"
    echo "  -h, --help    Mostra esta ajuda"
}

function log() {
    # Log para stderr para não poluir a saída padrão
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] - $SCRIPT_NAME - $*" >&2
}

function tratar_erro() {
    local codigo_saida=$?
    log "ERRO na linha $1: O comando falhou com o código de saída $codigo_saida."
    exit "$codigo_saida"
}

# Trap para capturar erros
trap 'tratar_erro $LINENO' ERR

function main() {
    # 0. Verificar dependências
    if ! command -v ffmpeg &> /dev/null; then
        log "ERRO: O comando 'ffmpeg' não foi encontrado. Por favor, instale o ffmpeg."
        exit 1
    fi

    # 1. Validar argumentos de entrada
    if [[ "$#" -ne 1 || "$1" == "-h" || "$1" == "--help" ]]; then
        mostrar_ajuda
        exit 0
    fi

    local arquivo_mkv="$1"

    # 2. Validar o arquivo de entrada
    if [[ ! -f "$arquivo_mkv" ]]; then
        log "ERRO: O arquivo '$arquivo_mkv' não foi encontrado."
        exit 1
    fi

    if [[ "${arquivo_mkv##*.}" != "mkv" ]]; then
        log "ERRO: O arquivo '$arquivo_mkv' não parece ser um arquivo MKV. A extensão deve ser '.mkv'."
        exit 1
    fi

    # Garante que a pasta de saída exista
    mkdir -p "$PASTA_SAIDA"

    log "Processando arquivo: $arquivo_mkv"

    # 3. Obter informações do arquivo com ffmpeg
    local arquivo_log_ffmpeg
    arquivo_log_ffmpeg=$(mktemp)
    log "Usando arquivo de log temporário para ffmpeg: ${arquivo_log_ffmpeg}"

    # ffmpeg emite as informações para stderr. Redirecionamos tudo para um arquivo de log.
    # O '|| true' garante que o script não pare por causa do 'set -e' se o ffmpeg retornar um erro,
    # o que é comum ao apenas listar informações.
    ffmpeg -i "$arquivo_mkv" &> "${arquivo_log_ffmpeg}" || true

    local info_faixas
    info_faixas=$(cat "${arquivo_log_ffmpeg}")
    rm "${arquivo_log_ffmpeg}"

    log "Informações do ffmpeg capturadas. Analisando..."

    # 4. Gerar resumo das faixas na saída padrão
    echo "--- Resumo das Faixas de '$arquivo_mkv' ---"
    echo "$info_faixas" | grep "Stream #" | sed 's/^[[:space:]]*//'
    echo "-------------------------------------------------"

    # 5. Extrair todas as legendas no formato SRT
    log "Procurando por legendas SRT para extrair..."

    local nome_base_arquivo
    nome_base_arquivo=$(basename "$arquivo_mkv" .mkv)
    local legendas_encontradas=0
    
    # Itera sobre as linhas que contêm "Subtitle: subrip" usando Process Substitution
    # para evitar que o loop while seja executado em um subshell.
    while read -r linha; do
        ((legendas_encontradas++))
        
        # Extrai o índice da faixa (ex: Stream #0:2 -> 2) usando here-string e sed
        local indice_faixa
        indice_faixa=$(sed -n 's/.*Stream #[0-9]:\([0-9]*\).*/\1/p' <<< "$linha")

        if [[ -z "$indice_faixa" ]]; then
            log "AVISO: Não foi possível extrair o índice da faixa da linha, pulando: '${linha}'"
            continue
        fi

        # Extrai o código do idioma (ex: (eng) -> eng) usando here-string e sed
        local codigo_idioma
        codigo_idioma=$(sed -n 's/.*(\([a-zA-Z]*\)).*/\1/p' <<< "$linha")
        if [[ -z "$codigo_idioma" ]]; then
            codigo_idioma="und"
        fi
        
        # Mapeia códigos comuns para o formato desejado
        case "$codigo_idioma" in
            por) codigo_idioma="pt-BR" ;;
            eng) codigo_idioma="en" ;;
            spa) codigo_idioma="es" ;;
        esac

        log "Legenda SRT encontrada: Faixa #$indice_faixa, Idioma: $codigo_idioma"

        local arquivo_saida="${PASTA_SAIDA}/${nome_base_arquivo}.${codigo_idioma}.srt"

        log "Extraindo faixa #$indice_faixa para: $arquivo_saida"

        # Executa o ffmpeg para extrair a legenda
        # -y: sobrescreve o arquivo de saída se ele já existir
        # -map 0:indice: seleciona a faixa específica
        # -c:s srt: define o codec de legenda como srt (converte se necessário)
        # -loglevel error: mostra apenas erros fatais para não poluir o log
        ffmpeg -y -i "$arquivo_mkv" -map "0:$indice_faixa" -c:s srt "$arquivo_saida" -loglevel error
        
        log "Extração da faixa #$indice_faixa concluída."
    done < <(echo "$info_faixas" | grep -i 'subtitle: subrip')

    if [[ "$legendas_encontradas" -eq 0 ]]; then
        log "Nenhuma legenda no formato SRT foi encontrada no arquivo."
    fi

    log "Processo concluído."
}

# Ponto de entrada do script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
