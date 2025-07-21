# Fluxo de Trabalho

## Encerramento de Sessões

Quando solicitado para encerrar uma sessão de desenvolvimento:

1. **SEMPRE lembrar o usuário de fazer commit das mudanças**
2. **Gerar automaticamente uma entrada no arquivo `/docs/historico.md`**

### Formato da Entrada no Histórico

```markdown
## [DATA] - [TÍTULO DA SESSÃO]

[Parágrafo descritivo do trabalho realizado na sessão, incluindo principais implementações, correções ou melhorias feitas]
```

### Exemplo:
```markdown
## 2024-01-15 - Implementação do Sistema de Autenticação

Implementado o sistema básico de autenticação com JWT, incluindo endpoints de login e registro. Criada a estrutura de middleware para validação de tokens e configuração inicial do banco de dados SQLite. Adicionados testes unitários para as funções de hash de senha.
```

## Responsabilidades ao Finalizar

- [ ] Revisar arquivos modificados
- [ ] Sugerir mensagem de commit apropriada
- [ ] Gerar entrada no histórico
- [ ] Verificar se documentação precisa ser atualizada