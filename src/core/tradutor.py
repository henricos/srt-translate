import os
import re
import sys
from datetime import datetime
from typing import List, Dict

from google import genai
from google.genai.types import HttpOptions

from src.core import arquivo
from src.core.modelos import FalaLegenda

# Variáveis de configuração lidas do ambiente
CHAVE_API = os.getenv("GEMINI_API_KEY")
MODELO_NOME = os.getenv("MODELO_GEMINI", "gemini-2.5-flash")
TAMANHO_LOTE = int(os.getenv("TAMANHO_LOTE", 100))

def obter_cliente_gemini():
    """
    Configura e retorna o cliente da API GenAI.
    """
    if not CHAVE_API:
        raise ValueError("A chave da API (GEMINI_API_KEY) não foi encontrada nas variáveis de ambiente.")
    
    cliente = genai.Client(
        http_options=HttpOptions(api_version="v1"),
        api_key=CHAVE_API
    )
    return cliente

def _traduzir_lote(
    falas: List[FalaLegenda],
    diretorio_log: str,
    prefixo_arquivo: str
) -> Dict[int, str]:
    """
    Envia um único lote de falas para a API de tradução.
    """
    cliente = obter_cliente_gemini()
    
    textos_para_traduzir = [f"{f.indice}| {f.texto.replace('\n', ' ')}" for f in falas]
    
    exemplo_resposta = '\n'.join([
        f"{falas[0].indice}| Texto traduzido da fala {falas[0].indice}",
        f"{falas[1].indice}| Texto traduzido da fala {falas[1].indice}",
        "..."
    ])

    prompt = (
        "Traduza os textos abaixo para o português do Brasil. Cada linha contém um índice seguido por '|' e o texto original.\n"
        "Sua resposta DEVE manter o formato 'indice| texto traduzido' para cada linha.\n"
        "Sua resposta DEVE ser encapsulada entre as tags <TRADUCAO_INICIO> e <TRADUCAO_FIM>.\n"
        "Não adicione comentários ou texto extra fora dessas tags. Apenas as linhas traduzidas dentro das tags.\n\n"
        "Textos para traduzir:\n"
        f"{'\n'.join(textos_para_traduzir)}\n\n"
        "Formato de resposta esperado:\n"
        "<TRADUCAO_INICIO>\n"
        f"{exemplo_resposta}\n"
        "<TRADUCAO_FIM>"
    )

    arquivo.salvar_log(diretorio_log, prefixo_arquivo, prompt, "prompt")

    try:
        resposta = cliente.models.generate_content(model=MODELO_NOME, contents=prompt)

        if not resposta or not resposta.text:
            feedback_prompt = ""
            if hasattr(resposta, 'prompt_feedback'):
                feedback_prompt = f" Causa provável: {resposta.prompt_feedback}"
            
            mensagem_erro = f"Erro: A API não retornou um conteúdo de texto válido.{feedback_prompt}"
            print(mensagem_erro)
            arquivo.salvar_log(diretorio_log, prefixo_arquivo, mensagem_erro, "response")
            return {}
            
        texto_resposta_raw = resposta.text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API de tradução: {e}")
        arquivo.salvar_log(diretorio_log, prefixo_arquivo, f"ERRO: {e}", "response")
        return {}

    arquivo.salvar_log(diretorio_log, prefixo_arquivo, texto_resposta_raw, "response")

    match = re.search(r'<TRADUCAO_INICIO>\s*(.*?)\s*<TRADUCAO_FIM>', texto_resposta_raw, re.DOTALL)
    
    if not match:
        print("Erro: As tags de início/fim de tradução não foram encontradas na resposta da API.")
        return {}

    conteudo_traduzido = match.group(1).strip()
    dados_traduzidos = {}
    
    for linha in conteudo_traduzido.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        
        match_linha = re.match(r'(\d+)\|\s*(.*)', linha)
        if match_linha:
            try:
                chave = int(match_linha.group(1))
                valor = match_linha.group(2).strip()
                dados_traduzidos[chave] = valor
            except ValueError:
                print(f"Aviso: Não foi possível parsear o índice da linha: {linha}")
        else:
            print(f"Aviso: Linha da resposta não corresponde ao formato esperado 'indice| texto': {linha}")
            
    return dados_traduzidos

def pipeline_traducao(
    todas_as_falas: List[FalaLegenda],
    fala_inicial: int,
    fala_final: int,
    tamanho_lote: int,
    caminho_arquivo_entrada: str,
    raiz_projeto: str
) -> List[FalaLegenda]:
    """
    Orquestra o processo completo de tradução de legendas.
    """
    falas_a_processar = [f for f in todas_as_falas if fala_inicial <= f.indice <= fala_final]
    
    if not falas_a_processar:
        print("Nenhuma fala para processar no intervalo especificado.")
        return todas_as_falas

    total_a_processar = len(falas_a_processar)
    print(f"Total de {len(todas_as_falas)} falas encontradas. Processando {total_a_processar} falas (de {fala_inicial} a {fala_final}).")
    
    mapa_falas_traduzidas = {f.indice: f for f in todas_as_falas}

    for i in range(0, total_a_processar, tamanho_lote):
        num_lote = (i // tamanho_lote) + 1
        lote = falas_a_processar[i:i + tamanho_lote]
        
        indice_inicio, indice_fim = lote[0].indice, lote[-1].indice
        print(f"\n--- Processando Lote {num_lote} (falas {indice_inicio} a {indice_fim}) ---")

        prefixo_arquivo = f"{os.path.splitext(os.path.basename(caminho_arquivo_entrada))[0]}-lote{num_lote:03d}"
        diretorio_log = os.path.join(raiz_projeto, "logs")
        
        textos_traduzidos = _traduzir_lote(lote, diretorio_log=diretorio_log, prefixo_arquivo=prefixo_arquivo)

        for fala_original in lote:
            texto_traduzido = textos_traduzidos.get(fala_original.indice)
            if texto_traduzido:
                mapa_falas_traduzidas[fala_original.indice] = fala_original._replace(texto=texto_traduzido)
            else:
                print(f"Aviso: Tradução não encontrada para a fala #{fala_original.indice}. Mantendo original.")

    return [mapa_falas_traduzidas[i] for i in sorted(mapa_falas_traduzidas.keys())]


def executar_traducao(argumentos, raiz_projeto: str):
    """
    Ponto de entrada para o processo de tradução a partir dos argumentos da CLI.
    """
    print(f"Iniciando tradução para o arquivo: {argumentos.arquivo_entrada}")

    try:
        tamanho_lote = int(os.getenv("TAMANHO_LOTE", 100))
    except (ValueError, TypeError):
        print("Aviso: TAMANHO_LOTE inválido. Usando o padrão de 100.")
        tamanho_lote = 100

    try:
        todas_as_falas = arquivo.ler_arquivo_srt(argumentos.arquivo_entrada)
        if not todas_as_falas:
            print("Nenhuma fala de legenda válida encontrada no arquivo.")
            return
    except FileNotFoundError:
        print(f"Erro fatal: Arquivo de entrada '{argumentos.arquivo_entrada}' não encontrado.")
        sys.exit(1)

    fala_inicial = argumentos.fala_inicial or 1
    fala_final = argumentos.fala_final or len(todas_as_falas)

    falas_finais = pipeline_traducao(
        todas_as_falas=todas_as_falas,
        fala_inicial=fala_inicial,
        fala_final=fala_final,
        tamanho_lote=tamanho_lote,
        caminho_arquivo_entrada=argumentos.arquivo_entrada,
        raiz_projeto=raiz_projeto
    )

    if argumentos.arquivo_saida:
        arquivo_saida = argumentos.arquivo_saida
    else:
        base, ext = os.path.splitext(argumentos.arquivo_entrada)
        
        match = re.search(r'\.([a-zA-Z]{2,3}(-[a-zA-Z]{2})?)$', base)
        
        if match:
            base_sem_idioma = base[:match.start()]
            arquivo_saida = f"{base_sem_idioma}.pt-BR{ext}"
        else:
            arquivo_saida = f"{base}.pt-BR{ext}"

    print(f"\nSalvando arquivo traduzido em: {arquivo_saida}")
    arquivo.salvar_arquivo_srt(falas_finais, arquivo_saida)
    print("Processo concluído com sucesso.")
