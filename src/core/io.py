from typing import List
from src.core.models import SubtitleSpeech

def read_srt_file(file_path: str) -> List[SubtitleSpeech]:
    """
    Lê um arquivo .srt e o parseia em uma lista de falas da legenda.

    Args:
        file_path: O caminho para o arquivo .srt.

    Returns:
        Uma lista de objetos SubtitleSpeech.
    
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{file_path}'")
        raise

    falas_texto = content.strip().split('\n\n')
    falas_parseadas = []

    for fala_texto in falas_texto:
        linhas = fala_texto.strip().split('\n')
        if len(linhas) < 3:
            continue

        try:
            index = int(linhas[0])
            timestamp = linhas[1]
            texto = "\n".join(linhas[2:])

            if "-->" not in timestamp:
                raise ValueError(f"Timestamp inválido na fala {index}")

            falas_parseadas.append(SubtitleSpeech(index, timestamp, texto))
        except (ValueError, IndexError) as e:
            print(f"Aviso: Ignorando fala malformada: {e}\n---\n{fala_texto}\n---")
            continue
            
    return falas_parseadas

def save_srt_file(falas: List[SubtitleSpeech], output_path: str):
    """
    Salva uma lista de falas de legenda em um arquivo .srt.

    Args:
        falas: A lista de SubtitleSpeech a ser salva.
        output_path: O caminho para o arquivo de saída.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for fala in falas:
            f.write(f"{fala.idx}\n")
            f.write(f"{fala.timestamp}\n")
            f.write(f"{fala.text}\n\n")
