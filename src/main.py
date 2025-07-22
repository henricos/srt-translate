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
        block_size = int(os.getenv("BLOCK_SIZE", 100))
    except (ValueError, TypeError):
        print("Aviso: BLOCK_SIZE inválido. Usando o padrão de 100.")
        block_size = 100

    # 2. Parsear o arquivo SRT
    try:
        all_blocks = srt_parser.parse_srt_file(args.input_file)
        if not all_blocks:
            print("Nenhum bloco de legenda válido encontrado no arquivo.")
            return
    except FileNotFoundError:
        print(f"Erro fatal: Arquivo de entrada '{args.input_file}' não encontrado.")
        sys.exit(1)

    # 3. Filtrar blocos se start/end foram fornecidos
    start_block = args.start_block or 1
    end_block = args.end_block or len(all_blocks)

    blocks_to_process = [b for b in all_blocks if start_block <= b.index <= end_block]
    
    if not blocks_to_process:
        print("Nenhum bloco para processar no intervalo especificado.")
        return

    total_to_process = len(blocks_to_process)
    print(f"Total de {len(all_blocks)} blocos encontrados. Processando {total_to_process} blocos (de {start_block} a {end_block}).")
    
    # Se estivermos processando um subconjunto, carregamos as traduções existentes
    translated_blocks_map = {b.index: b for b in all_blocks}

    # 4. Processar em lotes
    for i in range(0, total_to_process, block_size):
        batch_num = (i // block_size) + 1
        chunk = blocks_to_process[i:i + block_size]
        
        start_idx = chunk[0].index
        end_idx = chunk[-1].index
        print(f"\n--- Processando Lote {batch_num} (blocos {start_idx} a {end_idx}) ---")

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
                translated_blocks_map[original_block.index] = original_block._replace(text=translated_text)
            else:
                print(f"Aviso: Tradução não encontrada para o bloco #{original_block.index}. Mantendo original.")
                # Mantém o texto original ou o que já estava lá
                translated_blocks_map[original_block.index] = original_block

    # 5. Salvar o arquivo final
    final_blocks = [translated_blocks_map[i] for i in sorted(translated_blocks_map.keys())]

    if args.output_file:
        output_file = args.output_file
    else:
        base, ext = os.path.splitext(args.input_file)
        output_file = f"{base}.pt-BR{ext}"

    print(f"\nSalvando arquivo traduzido em: {output_file}")
    srt_parser.save_srt_file(final_blocks, output_file)
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
    parser_translate.add_argument(
        "--start-block",
        type=int,
        help="(Opcional) Índice do bloco inicial para tradução."
    )
    parser_translate.add_argument(
        "--end-block",
        type=int,
        help="(Opcional) Índice do bloco final para tradução."
    )
    parser_translate.set_defaults(func=handle_translate)

    # (Futuro) Sub-comando para 'transcribe'
    # parser_transcribe = subparsers.add_parser("transcribe", help="Transcrever um arquivo de áudio/vídeo.")
    # ...

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
