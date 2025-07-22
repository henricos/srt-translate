import os
import json
import re
from datetime import datetime
from typing import List, Dict

from google import genai
from google.genai.types import HttpOptions

from src.core.srt_parser import SubtitleBlock

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

def translate_blocks(
    blocks: List[SubtitleBlock], 
    log_dir: str = "logs", 
    file_prefix: str = "translation"
) -> Dict[int, str]:
    """
    Traduz uma lista de blocos de legenda usando a API.

    Args:
        blocks: Lista de SubtitleBlock a serem traduzidos.
        log_dir: Diretório para salvar os logs.
        file_prefix: Prefixo para os nomes dos arquivos de log.

    Returns:
        Um dicionário mapeando o índice do bloco ao texto traduzido.
    """
    client = get_translation_client()
    
    # Monta o payload para o prompt, com os textos originais
    texts_to_translate = {str(b.index): b.text.replace("\n", " ") for b in blocks}
    
    prompt = (
        "Traduza os textos do objeto JSON abaixo para o português do Brasil.\n"
        "Sua resposta DEVE ser um único objeto JSON, mantendo as mesmas chaves numéricas (como strings) "
        "e contendo apenas os textos traduzidos como valores.\n"
        "Não adicione comentários, explicações ou qualquer texto fora do objeto JSON.\n\n"
        f"{json.dumps(texts_to_translate, indent=2, ensure_ascii=False)}"
    )

    _save_log(log_dir, file_prefix, prompt, "prompt")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        raw_response_text = response.text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API de tradução: {e}")
        _save_log(log_dir, file_prefix, f"ERRO: {e}", "response")
        return {}

    _save_log(log_dir, file_prefix, raw_response_text, "response")

    # Extrai o JSON da resposta
    try:
        # A API pode retornar o JSON dentro de um bloco de código markdown
        match = re.search(r'```json\s*(\{.*?\})\s*```', raw_response_text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = raw_response_text
        
        translated_data = json.loads(json_str)
        
        # Converte as chaves de volta para inteiros
        return {int(k): v for k, v in translated_data.items()}

    except (json.JSONDecodeError, TypeError) as e:
        print(f"Erro ao decodificar a resposta JSON da API: {e}")
        return {}
