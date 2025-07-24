#!/bin/bash

# Descrição: Transcreve o áudio de um arquivo de vídeo e gera uma legenda .srt.
# Autor: Henrico Scaranello
# Data: 2025-07-24
#
# Uso: ./transcrever_audio.sh /caminho/para/video.mp4

# Constantes
readonly DIRETORIO_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly NOME_SCRIPT="$(basename "$0")"
readonly RAIZ_PROJETO="$(cd "${DIRETORIO_SCRIPT}/.." && pwd)"

# Funções
function mostrar_ajuda() {
    echo "Uso: $NOME_SCRIPT <caminho_para_arquivo_de_video>"
    echo
    echo "Extrai o áudio de um arquivo de vídeo, transcreve e salva como um arquivo .srt."
    echo "AVISO: Esta funcionalidade ainda não foi implementada."
    echo
    echo "Opções:"
    echo "  -h, --help    Mostra esta ajuda"
}

function principal() {
    if [[ "$#" -ne 1 || "$1" == "-h" || "$1" == "--help" ]]; then
        mostrar_ajuda
        exit 0
    fi

    echo "Funcionalidade de transcrição de áudio ainda em desenvolvimento." >&2
    echo "O script será encerrado." >&2
    exit 1
}

# Ponto de entrada do script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    principal "$@"
fi
