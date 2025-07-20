# Regras de Desenvolvimento (Cline)

Este documento centraliza as regras e convenções adotadas para o desenvolvimento deste projeto, visando manter a consistência e a qualidade do código e da documentação.

## 1. Padrão de Commits

**Regra:** Todas as mensagens de commit devem ser escritas em português do Brasil.

**Formato:** Recomenda-se o uso do padrão "Conventional Commits", adaptado para o português.

*   **`feat:`** (funcionalidade) - Para novas funcionalidades.
*   **`fix:`** (correção) - Para correções de bugs.
*   **`docs:`** (documentação) - Para alterações na documentação.
*   **`style:`** (estilo) - Para formatação, ponto e vírgula, etc; sem alteração de código.
*   **`refactor:`** (refatoração) - Para refatoração de código que não altera a funcionalidade.
*   **`test:`** (teste) - Para adição ou modificação de testes.
*   **`chore:`** (tarefa) - Para atualizações de tarefas de build, configuração, etc.

**Exemplo:**
```
feat: adiciona script para extração de legendas
```

## 2. Histórico de Desenvolvimento

**Regra:** Ao final de cada sessão de desenvolvimento significativa, uma nova entrada deve ser adicionada ao arquivo `docs/historico.md`.

**Estrutura da Entrada:**

*   **Título:** Data da sessão no formato `DD/MM/AAAA` e um título breve.
*   **Resumo:** Uma frase em negrito resumindo a principal entrega da sessão.
*   **Parágrafo Explicativo:** Um parágrafo detalhando as alterações e o trabalho realizado.

**Exemplo:**
```markdown
## 20/07/2025: Estrutura Inicial do Projeto

**Resumo:** Criação da arquitetura de diretórios, arquivos de configuração e documentação inicial do projeto.

Nesta sessão inicial, foi definida e criada toda a estrutura de pastas para o projeto...
