# Boas Práticas Bash

## Sistema Operacional
- Assumir compatibilidade com Ubuntu

## Configurações Obrigatórias

### Shebang
```bash
#!/bin/bash
```

### Opções de Segurança
```bash
set -euo pipefail
# -e: sai se algum comando falhar
# -u: sai se usar variável não definida
# -o pipefail: falha em pipes se algum comando falhar
```

## Estrutura de Script

```bash
#!/bin/bash
set -euo pipefail

# Descrição do script
# Autor: [nome]
# Data: [data]

# Constantes
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Funções
function mostrar_ajuda() {
    echo "Uso: $SCRIPT_NAME [opções]"
    echo "Opções:"
    echo "  -h, --help    Mostra esta ajuda"
}

function main() {
    # Código principal aqui
    echo "Executando script..."
}

# Execução principal
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

## Boas Práticas

### Variáveis
- **Usar nomes descritivos em português**
- **MAIÚSCULAS para constantes**
- **minúsculas para variáveis locais**
- **readonly para constantes**

```bash
readonly ARQUIVO_CONFIG="/etc/meuapp/config.conf"
local nome_usuario
```

### Aspas
- **Sempre usar aspas duplas em variáveis**
```bash
echo "Usuário: $nome_usuario"
cp "$arquivo_origem" "$arquivo_destino"
```

### Verificações
```bash
# Verificar se arquivo existe
if [[ ! -f "$arquivo" ]]; then
    echo "Erro: Arquivo $arquivo não encontrado" >&2
    exit 1
fi

# Verificar se diretório existe
if [[ ! -d "$diretorio" ]]; then
    mkdir -p "$diretorio"
fi
```

### Tratamento de Erros
```bash
function tratar_erro() {
    echo "Erro na linha $1" >&2
    exit 1
}

trap 'tratar_erro $LINENO' ERR
```

### Logs
```bash
function log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

log "Iniciando processamento..."
```