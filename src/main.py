import argparse
import os
import sys

# Adiciona o diretório do projeto ao sys.path para permitir imports de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core.translator import run_translation_handler


def main():
    """
    Ponto de entrada principal do script. Configura a CLI e delega a execução.
    """
    parser = argparse.ArgumentParser(description="Ferramenta para processamento de legendas e áudio.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponíveis")

    # Sub-comando para 'translate'
    parser_translate = subparsers.add_parser("translate", help="Traduzir um arquivo .srt.")
    parser_translate.add_argument("--input-file", required=True, help="Caminho para o arquivo .srt de entrada.")
    parser_translate.add_argument("--output-file", help="(Opcional) Caminho para o arquivo .srt de saída.")
    parser_translate.add_argument("--fala-inicial", type=int, dest="start_speech", help="(Opcional) Índice da fala inicial.")
    parser_translate.add_argument("--fala-final", type=int, dest="end_speech", help="(Opcional) Índice da fala final.")
    
    # Define a função que será chamada, passando os argumentos e o project_root
    parser_translate.set_defaults(func=lambda args: run_translation_handler(args, project_root))

    # (Futuro) Sub-comando para 'transcribe'
    # parser_transcribe = subparsers.add_parser("transcribe", help="Transcrever um arquivo de áudio/vídeo.")
    # ...

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
