import os
import re
import sys
from datetime import datetime
from typing import List, Dict

from google import genai
from google.genai.types import HttpOptions

from src.core.models import SubtitleBlock

# Variáveis de configuração lidas do ambiente
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def get_translation_client():
    """
    Configura e retorna o cliente da API GenAI.
    """
    if not API_KEY:
        raise ValueError("A chave da API (GEMINI_API_KEY) não foi encontrada nas variáveis de ambiente.")
    
    client = genai.Client(
        http_options=HttpOptions(api_version="v1"),
        api_key=API_KEY
    )
    return client

def _save_log(log_dir: str, file_prefix: str, content: str, log_type: str):
    """
    Salva o conteúdo de log em um arquivo.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{file_prefix}-{log_type}-{timestamp}.log")
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Log salvo em: {log_file}")

def _translate_batch(
    blocks: List[SubtitleBlock], 
    log_dir: str, 
    file_prefix: str
) -> Dict[int, str]:
    """
    Envia um único lote de blocos para a API de tradução.
    """
    client = get_translation_client()
    
    # Prepara os textos para tradução no formato "indice| texto"
    texts_to_translate = [f"{b.idx}| {b.text.replace('\n', ' ')}" for b in blocks]
    
    prompt = (
        "Traduza os textos abaixo para o português do Brasil. Cada linha contém um índice seguido por '|' e o texto original.\n"
        "Sua resposta DEVE manter o formato 'indice| texto traduzido' para cada linha.\n"
        "Sua resposta DEVE ser encapsulada entre as tags <TRADUCAO_INICIO> e <TRADUCAO_FIM>.\n"
        "Não adicione comentários ou texto extra fora dessas tags. Apenas as linhas traduzidas dentro das tags.\n\n"
        "Textos para traduzir:\n"
        f"{'\n'.join(texts_to_translate)}\n\n"
        "Formato de resposta esperado:\n"
        "<TRADUCAO_INICIO>\n"
        "1| Texto traduzido do bloco 1\n"
        "2| Texto traduzido do bloco 2\n"
        "...\n"
        "<TRADUCAO_FIM>"
    )

    _save_log(log_dir, file_prefix, prompt, "prompt")

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)

        # Valida se a resposta contém o texto esperado antes de prosseguir.
        # O atributo .text pode ser None se a resposta for bloqueada por segurança.
        if not response or not response.text:
            feedback = ""
            if hasattr(response, 'prompt_feedback'):
                feedback = f" Causa provável: {response.prompt_feedback}"
            
            error_message = f"Erro: A API não retornou um conteúdo de texto válido.{feedback}"
            print(error_message)
            _save_log(log_dir, file_prefix, error_message, "response")
            return {} # Retorna um dicionário vazio em caso de erro
            
        raw_response_text = response.text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API de tradução: {e}")
        _save_log(log_dir, file_prefix, f"ERRO: {e}", "response")
        return {} # Retorna um dicionário vazio em caso de erro

    _save_log(log_dir, file_prefix, raw_response_text, "response")

    # Extrai o conteúdo entre as tags <TRADUCAO_INICIO> e <TRADUCAO_FIM>
    match = re.search(r'<TRADUCAO_INICIO>\s*(.*?)\s*<TRADUCAO_FIM>', raw_response_text, re.DOTALL)
    
    if not match:
        print("Erro: As tags de início/fim de tradução não foram encontradas na resposta da API.")
        return {}

    translated_content = match.group(1).strip()
    translated_data = {}
    
    for line in translated_content.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # Tenta parsear a linha no formato "indice| texto"
        match_line = re.match(r'(\d+)\|\s*(.*)', line)
        if match_line:
            try:
                key = int(match_line.group(1))
                value = match_line.group(2).strip()
                translated_data[key] = value
            except ValueError:
                print(f"Aviso: Não foi possível parsear o índice da linha: {line}")
        else:
            print(f"Aviso: Linha da resposta não corresponde ao formato esperado 'indice| texto': {line}")
            
    return translated_data

def translation_pipeline(
    all_blocks: List[SubtitleBlock],
    start_block: int,
    end_block: int,
    block_size: int,
    input_file_path: str,
    project_root: str
) -> List[SubtitleBlock]:
    """
    Orquestra o processo completo de tradução de legendas.
    """
    blocks_to_process = [b for b in all_blocks if start_block <= b.idx <= end_block]
    
    if not blocks_to_process:
        print("Nenhum bloco para processar no intervalo especificado.")
        return all_blocks

    total_to_process = len(blocks_to_process)
    print(f"Total de {len(all_blocks)} blocos encontrados. Processando {total_to_process} blocos (de {start_block} a {end_block}).")
    
    translated_blocks_map = {b.idx: b for b in all_blocks}

    for i in range(0, total_to_process, block_size):
        batch_num = (i // block_size) + 1
        chunk = blocks_to_process[i:i + block_size]
        
        start_idx, end_idx = chunk[0].idx, chunk[-1].idx
        print(f"\n--- Processando Lote {batch_num} (blocos {start_idx} a {end_idx}) ---")

        file_prefix = f"{os.path.splitext(os.path.basename(input_file_path))[0]}-lote{batch_num:03d}"
        log_dir = os.path.join(project_root, "logs")
        
        translated_texts = _translate_batch(chunk, log_dir=log_dir, file_prefix=file_prefix)

        for original_block in chunk:
            translated_text = translated_texts.get(original_block.idx)
            if translated_text:
                translated_blocks_map[original_block.idx] = original_block._replace(text=translated_text)
            else:
                print(f"Aviso: Tradução não encontrada para o bloco #{original_block.idx}. Mantendo original.")

    return [translated_blocks_map[i] for i in sorted(translated_blocks_map.keys())]


def run_translation_handler(args, project_root: str):
    """
    Ponto de entrada para o processo de tradução a partir dos argumentos da CLI.
    """
    from src.core import io  # Import local para evitar dependência circular a nível de módulo

    print(f"Iniciando tradução para o arquivo: {args.input_file}")

    # 1. Ler configurações do ambiente
    try:
        block_size = int(os.getenv("BLOCK_SIZE", 100))
    except (ValueError, TypeError):
        print("Aviso: BLOCK_SIZE inválido. Usando o padrão de 100.")
        block_size = 100

    # 2. Ler e parsear o arquivo SRT
    try:
        all_blocks = io.read_srt_file(args.input_file)
        if not all_blocks:
            print("Nenhum bloco de legenda válido encontrado no arquivo.")
            return
    except FileNotFoundError:
        print(f"Erro fatal: Arquivo de entrada '{args.input_file}' não encontrado.")
        sys.exit(1)

    # 3. Definir intervalo de blocos
    start_block = args.start_block or 1
    end_block = args.end_block or len(all_blocks)

    # 4. Executar o pipeline de tradução
    final_blocks = translation_pipeline(
        all_blocks=all_blocks,
        start_block=start_block,
        end_block=end_block,
        block_size=block_size,
        input_file_path=args.input_file,
        project_root=project_root
    )

    # 5. Determinar e salvar o arquivo de saída
    if args.output_file:
        output_file = args.output_file
    else:
        base, ext = os.path.splitext(args.input_file)
        
        # Verifica se o nome base termina com um código de idioma (ex: .en, .pt-BR)
        match = re.search(r'\.([a-zA-Z]{2,3}(-[a-zA-Z]{2})?)$', base)
        
        if match:
            # Se encontrou, substitui o código de idioma por .pt-BR
            base_sem_idioma = base[:match.start()]
            output_file = f"{base_sem_idioma}.pt-BR{ext}"
        else:
            # Se não, apenas adiciona .pt-BR
            output_file = f"{base}.pt-BR{ext}"

    print(f"\nSalvando arquivo traduzido em: {output_file}")
    io.save_srt_file(final_blocks, output_file)
    print("Processo concluído com sucesso.")
