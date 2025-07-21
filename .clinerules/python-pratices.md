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

### Nomes de Variáveis
- **Sempre em português brasileiro**
- **snake_case para variáveis e funções**
- **PascalCase para classes**

```python
# Variáveis
nome_usuario = "João"
idade_maxima = 65
lista_produtos = []

# Funções
def calcular_desconto():
    pass

def obter_dados_usuario():
    pass

# Classes
class GerenciadorUsuarios:
    pass
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