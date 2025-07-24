import argparse
import os
import sys

# Adiciona o diretório do projeto ao sys.path para permitir imports de 'src'
raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, raiz_projeto)

from src.core.tradutor import executar_traducao


def main():
    """
    Ponto de entrada principal do script. Configura a CLI e delega a execução.
    """
    parser = argparse.ArgumentParser(description="Ferramenta para processamento de legendas e áudio.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponíveis")

    # Sub-comando para 'translate'
    parser_translate = subparsers.add_parser("translate", help="Traduzir um arquivo .srt.")
    parser_translate.add_argument("--arquivo-entrada", dest="arquivo_entrada", required=True, help="Caminho para o arquivo .srt de entrada.")
    parser_translate.add_argument("--arquivo-saida", dest="arquivo_saida", help="(Opcional) Caminho para o arquivo .srt de saída.")
    parser_translate.add_argument("--fala-inicial", type=int, dest="fala_inicial", help="(Opcional) Índice da fala inicial.")
    parser_translate.add_argument("--fala-final", type=int, dest="fala_final", help="(Opcional) Índice da fala final.")
    
    # Define a função que será chamada, passando os argumentos e a raiz do projeto
    parser_translate.set_defaults(func=lambda args: executar_traducao(args, raiz_projeto))

    # (Futuro) Sub-comando para 'transcribe'
    # parser_transcribe = subparsers.add_parser("transcribe", help="Transcrever um arquivo de áudio/vídeo.")
    # ...

    argumentos = parser.parse_args()
    if hasattr(argumentos, 'func'):
        argumentos.func(argumentos)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
