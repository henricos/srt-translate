import os
import re
import sys
from datetime import datetime
from typing import List, Dict

from google import genai
from google.genai.types import HttpOptions

from src.core.models import SubtitleSpeech

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
    falas: List[SubtitleSpeech],
    log_dir: str,
    file_prefix: str
) -> Dict[int, str]:
    """
    Envia um único lote de falas para a API de tradução.
    """
    client = get_translation_client()
    
    # Prepara os textos para tradução no formato "indice| texto"
    texts_to_translate = [f"{f.idx}| {f.text.replace('\n', ' ')}" for f in falas]
    
    # Constrói um exemplo dinâmico para o formato de resposta
    # para guiar o modelo a usar os índices corretos do lote.
    exemplo_resposta = '\n'.join([
        f"{falas[0].idx}| Texto traduzido da fala {falas[0].idx}",
        f"{falas[1].idx}| Texto traduzido da fala {falas[1].idx}",
        "..."
    ])

    prompt = (
        "Traduza os textos abaixo para o português do Brasil. Cada linha contém um índice seguido por '|' e o texto original.\n"
        "Sua resposta DEVE manter o formato 'indice| texto traduzido' para cada linha.\n"
        "Sua resposta DEVE ser encapsulada entre as tags <TRADUCAO_INICIO> e <TRADUCAO_FIM>.\n"
        "Não adicione comentários ou texto extra fora dessas tags. Apenas as linhas traduzidas dentro das tags.\n\n"
        "Textos para traduzir:\n"
        f"{'\n'.join(texts_to_translate)}\n\n"
        "Formato de resposta esperado:\n"
        "<TRADUCAO_INICIO>\n"
        f"{exemplo_resposta}\n"
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
    todas_as_falas: List[SubtitleSpeech],
    fala_inicial: int,
    fala_final: int,
    tamanho_lote: int,
    input_file_path: str,
    project_root: str
) -> List[SubtitleSpeech]:
    """
    Orquestra o processo completo de tradução de legendas.
    """
    falas_a_processar = [f for f in todas_as_falas if fala_inicial <= f.idx <= fala_final]
    
    if not falas_a_processar:
        print("Nenhuma fala para processar no intervalo especificado.")
        return todas_as_falas

    total_a_processar = len(falas_a_processar)
    print(f"Total de {len(todas_as_falas)} falas encontradas. Processando {total_a_processar} falas (de {fala_inicial} a {fala_final}).")
    
    mapa_falas_traduzidas = {f.idx: f for f in todas_as_falas}

    for i in range(0, total_a_processar, tamanho_lote):
        num_lote = (i // tamanho_lote) + 1
        lote = falas_a_processar[i:i + tamanho_lote]
        
        start_idx, end_idx = lote[0].idx, lote[-1].idx
        print(f"\n--- Processando Lote {num_lote} (falas {start_idx} a {end_idx}) ---")

        file_prefix = f"{os.path.splitext(os.path.basename(input_file_path))[0]}-lote{num_lote:03d}"
        log_dir = os.path.join(project_root, "logs")
        
        textos_traduzidos = _translate_batch(lote, log_dir=log_dir, file_prefix=file_prefix)

        for fala_original in lote:
            texto_traduzido = textos_traduzidos.get(fala_original.idx)
            if texto_traduzido:
                mapa_falas_traduzidas[fala_original.idx] = fala_original._replace(text=texto_traduzido)
            else:
                print(f"Aviso: Tradução não encontrada para a fala #{fala_original.idx}. Mantendo original.")

    return [mapa_falas_traduzidas[i] for i in sorted(mapa_falas_traduzidas.keys())]


def run_translation_handler(args, project_root: str):
    """
    Ponto de entrada para o processo de tradução a partir dos argumentos da CLI.
    """
    from src.core import io  # Import local para evitar dependência circular a nível de módulo

    print(f"Iniciando tradução para o arquivo: {args.input_file}")

    # 1. Ler configurações do ambiente
    try:
        tamanho_lote = int(os.getenv("LOTE_SIZE", 100))
    except (ValueError, TypeError):
        print("Aviso: LOTE_SIZE inválido. Usando o padrão de 100.")
        tamanho_lote = 100

    # 2. Ler e parsear o arquivo SRT
    try:
        todas_as_falas = io.read_srt_file(args.input_file)
        if not todas_as_falas:
            print("Nenhuma fala de legenda válida encontrada no arquivo.")
            return
    except FileNotFoundError:
        print(f"Erro fatal: Arquivo de entrada '{args.input_file}' não encontrado.")
        sys.exit(1)

    # 3. Definir intervalo de falas
    fala_inicial = args.start_speech or 1
    fala_final = args.end_speech or len(todas_as_falas)

    # 4. Executar o pipeline de tradução
    falas_finais = translation_pipeline(
        todas_as_falas=todas_as_falas,
        fala_inicial=fala_inicial,
        fala_final=fala_final,
        tamanho_lote=tamanho_lote,
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
    io.save_srt_file(falas_finais, output_file)
    print("Processo concluído com sucesso.")
