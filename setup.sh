#!/bin/bash

# --- setup.sh ---
# Script para configurar o ambiente de desenvolvimento.

# Cores para o output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando a configuração do ambiente...${NC}"

# 1. Verifica se o python3-venv está instalado
if ! dpkg -s python3-venv &> /dev/null; then
    echo -e "${YELLOW}O pacote python3-venv não está instalado. Por favor, instale-o com 'sudo apt update && sudo apt install python3-venv' e execute o script novamente.${NC}"
    exit 1
fi

# 2. Cria o ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual em 'venv/'..."
    python3 -m venv venv
else
    echo "Ambiente virtual 'venv/' já existe."
fi

# 3. Instala as dependências do requirements.txt
echo "Instalando dependências do requirements.txt..."
source venv/bin/activate
pip install -r requirements.txt
deactivate

echo -e "\n${GREEN}Ambiente configurado com sucesso!${NC}"
echo -e "Não se esqueça de criar o arquivo ${YELLOW}config/.env${NC} com a sua chave de API."
echo -e "Para usar as ferramentas, execute os scripts no diretório ${YELLOW}bin/${NC}."
