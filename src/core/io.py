from typing import List
from src.core.models import SubtitleBlock

def read_srt_file(file_path: str) -> List[SubtitleBlock]:
    """
    Lê um arquivo .srt e o parseia em uma lista de blocos de legenda.

    Args:
        file_path: O caminho para o arquivo .srt.

    Returns:
        Uma lista de objetos SubtitleBlock.
    
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        raise

    blocks = content.strip().split('\n\n')
    parsed_blocks = []

    for block_text in blocks:
        lines = block_text.strip().split('\n')
        if len(lines) < 3:
            continue

        try:
            index = int(lines[0])
            timestamp = lines[1]
            text = "\n".join(lines[2:])

            if "-->" not in timestamp:
                raise ValueError(f"Timestamp inválido no bloco {index}")

            parsed_blocks.append(SubtitleBlock(index, timestamp, text))
        except (ValueError, IndexError) as e:
            print(f"Aviso: Ignorando bloco malformado: {e}\n---\n{block_text}\n---")
            continue
            
    return parsed_blocks

def save_srt_file(blocks: List[SubtitleBlock], output_path: str):
    """
    Salva uma lista de blocos de legenda em um arquivo .srt.

    Args:
        blocks: A lista de SubtitleBlock a ser salva.
        output_path: O caminho para o arquivo de saída.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for block in blocks:
            f.write(f"{block.idx}\n")
            f.write(f"{block.timestamp}\n")
            f.write(f"{block.text}\n\n")
