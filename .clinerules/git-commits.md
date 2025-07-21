# Convenções Git - Conventional Commits em Português

## Formato Padrão

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

## Tipos de Commit

- **feat**: nova funcionalidade
- **fix**: correção de bug
- **docs**: mudanças na documentação
- **style**: formatação, pontos e vírgulas, etc (sem mudança de código)
- **refactor**: refatoração de código (não é nova funcionalidade nem correção)
- **test**: adição ou modificação de testes
- **chore**: tarefas de manutenção, configurações, etc

## Exemplos de Mensagens

```bash
feat: adiciona sistema de autenticação JWT
fix: corrige validação de email no formulário
docs: atualiza README com instruções de instalação
refactor: reorganiza estrutura de pastas do projeto
test: adiciona testes para módulo de usuários
chore: atualiza dependências do requirements.txt
```

## Regras Importantes

- **Sempre em português brasileiro**
- **Usar infinitivo** (adiciona, corrige, atualiza)
- **Primeira linha até 50 caracteres**
- **Descrição clara e objetiva**
- **Sem ponto final na primeira linha**

## Com Escopo (quando aplicável)

```bash
feat(auth): adiciona middleware de validação de token
fix(api): corrige endpoint de busca de usuários
docs(readme): adiciona seção de contribuição
```