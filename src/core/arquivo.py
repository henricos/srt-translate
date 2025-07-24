from typing import List
from src.core.modelos import FalaLegenda

def ler_arquivo_srt(caminho_arquivo: str) -> List[FalaLegenda]:
    """
    Lê um arquivo .srt e o parseia em uma lista de falas da legenda.

    Args:
        caminho_arquivo: O caminho para o arquivo .srt.

    Returns:
        Uma lista de objetos FalaLegenda.
    
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
        raise

    falas_texto = conteudo.strip().split('\n\n')
    falas_parseadas = []

    for fala_texto in falas_texto:
        linhas = fala_texto.strip().split('\n')
        if len(linhas) < 3:
            continue

        try:
            indice = int(linhas[0])
            marca_tempo = linhas[1]
            texto = "\n".join(linhas[2:])

            if "-->" not in marca_tempo:
                raise ValueError(f"Marca de tempo inválida na fala {indice}")

            falas_parseadas.append(FalaLegenda(indice, marca_tempo, texto))
        except (ValueError, IndexError) as e:
            print(f"Aviso: Ignorando fala malformada: {e}\n---\n{fala_texto}\n---")
            continue
            
    return falas_parseadas

def salvar_arquivo_srt(falas: List[FalaLegenda], caminho_saida: str):
    """
    Salva uma lista de falas de legenda em um arquivo .srt.

    Args:
        falas: A lista de FalaLegenda a ser salva.
        caminho_saida: O caminho para o arquivo de saída.
    """
    with open(caminho_saida, "w", encoding="utf-8") as f:
        for fala in falas:
            f.write(f"{fala.indice}\n")
            f.write(f"{fala.marca_tempo}\n")
            f.write(f"{fala.texto}\n\n")
