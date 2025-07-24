# Boas Práticas Python

## Ambiente e Dependências

### Comando Python
- **Sempre usar `python3`** (padrão Ubuntu)
- **Nunca usar apenas `python`**

### Gerenciamento de Ambiente
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Gerar requirements
pip freeze > requirements.txt
```

### Documentação de Bibliotecas
- **SEMPRE usar MCP Context7** para consultar documentação atualizada das bibliotecas
- **Verificar versão mais recente** antes de implementar

## Estrutura de Projeto

```
projeto/
├── src/
│   ├── __init__.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   └── usuario.py
│   ├── servicos/
│   │   ├── __init__.py
│   │   └── autenticacao.py
│   ├── utilitarios/
│   │   ├── __init__.py
│   │   └── validadores.py
│   └── main.py
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Padrões de Código

### Nomenclatura e Idioma (Português Brasileiro)

**Regra Essencial:** Todo o código Python, incluindo nomes de **arquivos**, **variáveis**, **funções**, **classes** e **métodos**, DEVE ser escrito em português brasileiro. Esta é uma diretriz fundamental para manter a consistência e legibilidade do projeto.

- **Nomes de Arquivos:** `snake_case.py` (ex: `tradutor.py`, `leitor_srt.py`)
- **Variáveis e Funções:** `snake_case` (ex: `bloco_legenda`, `traduzir_lote`)
- **Classes:** `PascalCase` (ex: `BlocoLegenda`, `ClienteTraducao`)
- **Constantes:** `MAIUSCULAS_SNAKE_CASE` (ex: `CHAVE_API`, `TAMANHO_LOTE`)

#### Exemplo Prático

```python
# ✅ CORRETO (Português Brasileiro)

# Nomes de arquivos: `processador_legendas.py`, `modelos.py`

# Constantes
TAMANHO_MAXIMO_LOTE = 100

# Classes
class BlocoLegenda:
    pass

# Funções e variáveis
def processar_legenda(caminho_arquivo: str):
    todos_os_blocos = ler_arquivo_srt(caminho_arquivo)
    # ...

# ❌ INCORRETO (Inglês)

# Nomes de arquivos: `subtitle_processor.py`, `models.py`

# Constants
MAX_BATCH_SIZE = 100

# Classes
class SubtitleBlock:
    pass

# Functions and variables
def process_subtitle(file_path: str):
    all_blocks = read_srt_file(file_path)
    # ...
```

### Comentários e Documentação

#### Docstrings (sempre em português)
```python
def calcular_imposto(valor_bruto: float, percentual: float) -> float:
    """
    Calcula o valor do imposto baseado no valor bruto e percentual.
    
    Args:
        valor_bruto: Valor base para cálculo
        percentual: Percentual de imposto (0-100)
    
    Returns:
        Valor do imposto calculado
    """
    return valor_bruto * (percentual / 100)
```

#### Comentários em Código Complexo
```python
def processar_dados_complexos(dados):
    # Ordenar dados por prioridade antes do processamento
    dados_ordenados = sorted(dados, key=lambda x: x.prioridade)
    
    # Aplicar transformações específicas baseadas no tipo
    for item in dados_ordenados:
        if item.tipo == 'especial':
            # Lógica específica para itens especiais que requer
            # validação adicional e processamento diferenciado
            item = aplicar_validacao_especial(item)
    
    return dados_ordenados
```

#### Comentários Desnecessários (evitar)
```python
# ❌ Não fazer
contador = 0  # inicializa contador com zero

# ✅ Fazer (nome descritivo dispensa comentário)
contador_tentativas = 0
```

### Type Hints
```python
from typing import List, Dict, Optional

def buscar_usuarios(filtro: str) -> List[Dict[str, str]]:
    pass

def obter_usuario_por_id(id_usuario: int) -> Optional[Dict[str, str]]:
    pass
```

### Tratamento de Erros
```python
try:
    resultado = operacao_perigosa()
except ValueError as erro:
    logger.error(f"Erro de valor: {erro}")
    raise
except Exception as erro:
    logger.error(f"Erro inesperado: {erro}")
    return None
```

### Logs
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processar_arquivo(caminho_arquivo: str):
    logger.info(f"Iniciando processamento do arquivo: {caminho_arquivo}")
    # ... código ...
    logger.info("Processamento concluído com sucesso")
```

## Organização de Imports
```python
# 1. Bibliotecas padrão
import os
import sys
from datetime import datetime

# 2. Bibliotecas terceiros
import requests
from flask import Flask

# 3. Módulos locais
from src.modelos.usuario import Usuario
from src.utilitarios.validadores import validar_email
```
