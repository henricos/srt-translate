# Convenções Específicas do Projeto

Este arquivo documenta convenções e decisões de arquitetura específicas para o projeto `srt-translate`. O objetivo é manter a simplicidade e facilitar tanto o uso por usuários finais quanto o desenvolvimento contínuo, inclusive por ferramentas de IA.

## Preparação do Ambiente com `setup.sh`

O projeto inclui um script `setup.sh` para automatizar a preparação do ambiente de desenvolvimento.

**Regra:** O script `setup.sh` é o ponto de partida para qualquer nova configuração do projeto. Ele é responsável por criar o ambiente virtual Python (`venv`) e instalar as dependências listadas em `requirements.txt`.

**Justificativa:** Centralizar a configuração em um único script garante consistência e simplifica o processo de instalação, evitando que o usuário ou a IA precisem executar múltiplos comandos manuais.

## Scripts em `bin/`

### Filosofia de Simplicidade em Scripts Bash

Para os scripts utilitários localizados no diretório `bin/`, a simplicidade é priorizada sobre a robustez extrema.

**Regra:** Evitar o uso de configurações de shell estritas como `set -euo pipefail`. Os scripts devem ser claros, legíveis e focados em sua tarefa principal, com tratamento de erro explícito onde for crítico (ex: validação de argumentos, existência de arquivos).

**Justificativa:** O objetivo é criar scripts que sejam fáceis de entender e manter. O uso de `set -e` pode levar a comportamentos inesperados e dificultar o debug em scripts simples. A abordagem adotada é que a falha de um comando deve ser tratada explicitamente se for crucial para o fluxo do script.

### Ativação Automática do Ambiente Virtual

Os scripts Bash localizados no diretório `bin/` são projetados para serem executados diretamente pelo usuário sem a necessidade de ativar manualmente o ambiente virtual Python (`venv`).

**Regra:** Todo script em `bin/` que dependa do ambiente Python deve incluir uma lógica para verificar se o `VIRTUAL_ENV` está ativo. Se não estiver, o script deve tentar ativar o ambiente localizado em `PROJECT_ROOT/venv/bin/activate` antes de prosseguir com a execução.

**Justificativa:** Isso simplifica a experiência do usuário final e reduz a chance de erros por esquecimento de ativação do ambiente. Também garante que as ferramentas de IA não adicionem etapas desnecessárias de ativação do `venv` ao interagir com o projeto.

**Exemplo de Implementação:**
```bash
# Ativar o ambiente virtual se não estiver ativo
if [[ -z "$VIRTUAL_ENV" ]]; then
    local venv_path="${PROJECT_ROOT}/venv/bin/activate"
    if [[ -f "$venv_path" ]]; then
        echo "Ativando ambiente virtual..."
        source "$venv_path"
    else
        echo "Erro: Ambiente virtual 'venv' não encontrado." >&2
        exit 1
    fi
fi

# O código python pode ser chamado com segurança
python3 ...
