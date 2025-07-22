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
    # O comando pode retornar um código de erro ao apenas listar informações, por isso o ignoramos.
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
    log "Procurando por legendas para extrair..."

    local nome_base_arquivo
    nome_base_arquivo=$(basename "$arquivo_mkv" .mkv)
    local legendas_encontradas=0
    local indice_legenda_ffmpeg=-1

    # Itera sobre todas as faixas de legenda para manter o índice correto para o ffmpeg.
    # O ffmpeg usa um índice baseado no tipo de faixa (ex: 0:s:0 para a primeira legenda).
    while read -r linha; do
        # O índice de legenda do ffmpeg (0:s:N) só deve ser incrementado para faixas de legenda.
        if [[ "$linha" == *": Subtitle: "* ]]; then
            ((indice_legenda_ffmpeg++))
        fi

        # Processa apenas as legendas que são do tipo subrip (SRT).
        if [[ "$linha" == *"Subtitle: subrip"* ]]; then
            ((legendas_encontradas++))
            
            # Extrai o índice da faixa e o idioma usando regex para mais robustez.
            # Extrai o índice da faixa e o idioma usando regex para mais robustez.
            local indice_faixa_geral=""
            local codigo_idioma="und" # Padrão

            local regex_com_idioma='Stream[[:space:]]#[0-9]:([0-9]+)\(([^)]+)\)'
            local regex_sem_idioma='Stream[[:space:]]#[0-9]:([0-9]+)'

            if [[ "$linha" =~ $regex_com_idioma ]]; then
                indice_faixa_geral="${BASH_REMATCH[1]}"
                codigo_idioma="${BASH_REMATCH[2]}"
            elif [[ "$linha" =~ $regex_sem_idioma ]]; then
                indice_faixa_geral="${BASH_REMATCH[1]}"
            fi
            
            # Mapeia códigos comuns para o formato desejado.
            case "$codigo_idioma" in
                por) codigo_idioma="pt-BR" ;;
                eng) codigo_idioma="en" ;;
                spa) codigo_idioma="es" ;;
            esac

            log "Legenda SRT encontrada: Faixa Geral #${indice_faixa_geral}, Faixa de Legenda #${indice_legenda_ffmpeg}, Idioma: $codigo_idioma"

            local arquivo_saida="${PASTA_SAIDA}/${nome_base_arquivo}.${codigo_idioma}.srt"

            log "Extraindo faixa de legenda #${indice_legenda_ffmpeg} para: ${arquivo_saida}"

            # Executa o ffmpeg para extrair a legenda.
            if ! ffmpeg -y -i "$arquivo_mkv" -map "0:s:${indice_legenda_ffmpeg}" -c:s srt "$arquivo_saida" -loglevel error; then
                log "AVISO: Falha ao extrair a faixa de legenda #${indice_legenda_ffmpeg}. Pulando."
                rm -f "$arquivo_saida" # Remove arquivo de saída parcial/vazio.
            else
                log "Extração da faixa #${indice_faixa_geral} (legenda #${indice_legenda_ffmpeg}) concluída."
            fi
        fi
    done < <(echo "$info_faixas" | grep -i 'stream #.*: subtitle:')

    if [[ "$legendas_encontradas" -eq 0 ]]; then
        log "Nenhuma legenda no formato SRT foi encontrada no arquivo."
    fi

    log "Processo concluído."
}

# Ponto de entrada do script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
