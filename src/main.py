import argparse
import os
import sys

# Adiciona o diretório do projeto ao sys.path para permitir imports de 'src'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core import srt_parser, translator

def handle_translate(args):
    """
    Lida com a sub-rotina de tradução, orquestrando todo o processo.
    """
    print(f"Iniciando tradução para o arquivo: {args.input_file}")

    # 1. Ler configurações do ambiente
    try:
        block_size = int(os.getenv("BLOCK_SIZE", 50))
    except (ValueError, TypeError):
        print("Aviso: BLOCK_SIZE inválido. Usando o padrão de 50.")
        block_size = 50

    # 2. Parsear o arquivo SRT
    try:
        original_blocks = srt_parser.parse_srt_file(args.input_file)
        if not original_blocks:
            print("Nenhum bloco de legenda válido encontrado no arquivo.")
            return
    except FileNotFoundError:
        print(f"Erro fatal: Arquivo de entrada '{args.input_file}' não encontrado.")
        sys.exit(1)

    total_blocks = len(original_blocks)
    print(f"Total de {total_blocks} blocos de legenda encontrados.")
    
    translated_blocks = []
    
    # 3. Processar em lotes
    for i in range(0, total_blocks, block_size):
        batch_num = (i // block_size) + 1
        chunk = original_blocks[i:i + block_size]
        print(f"\n--- Processando Lote {batch_num} (blocos {i+1} a {i+len(chunk)}) ---")

        file_prefix = f"{os.path.splitext(os.path.basename(args.input_file))[0]}-lote{batch_num:03d}"
        
        translated_texts = translator.translate_blocks(
            chunk,
            log_dir=os.path.join(project_root, "logs"),
            file_prefix=file_prefix
        )

        # Atualiza os blocos com as traduções
        for original_block in chunk:
            translated_text = translated_texts.get(original_block.index)
            if translated_text:
                translated_blocks.append(original_block._replace(text=translated_text))
            else:
                print(f"Aviso: Tradução não encontrada para o bloco #{original_block.index}. Mantendo original.")
                translated_blocks.append(original_block._replace(text=f"[TRADUÇÃO FALHOU] {original_block.text}"))

    # 4. Salvar o arquivo final
    if args.output_file:
        output_file = args.output_file
    else:
        base, ext = os.path.splitext(args.input_file)
        output_file = f"{base}.pt-BR{ext}"

    print(f"\nSalvando arquivo traduzido em: {output_file}")
    srt_parser.save_srt_file(translated_blocks, output_file)
    print("Processo concluído com sucesso.")


def main():
    """
    Ponto de entrada principal do script.
    """
    parser = argparse.ArgumentParser(description="Ferramenta para processamento de legendas e áudio.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponíveis")

    # Sub-comando para 'translate'
    parser_translate = subparsers.add_parser("translate", help="Traduzir um arquivo .srt.")
    parser_translate.add_argument(
        "--input-file",
        required=True,
        help="Caminho para o arquivo .srt de entrada."
    )
    parser_translate.add_argument(
        "--output-file",
        help="(Opcional) Caminho para o arquivo .srt de saída. Se não for fornecido, será gerado automaticamente."
    )
    parser_translate.set_defaults(func=handle_translate)

    # (Futuro) Sub-comando para 'transcribe'
    # parser_transcribe = subparsers.add_parser("transcribe", help="Transcrever um arquivo de áudio/vídeo.")
    # ...

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
