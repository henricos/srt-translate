# Estrutura de Projeto

## Estrutura Base Genérica

```
projeto/
├── .clinerules/             # Regras do Cline
├── data/                    # Dados de exemplo/configuração
├── docs/                    # Documentação
│   ├── backlog.md           # Backlog de funcionalidades a serem implementadas
│   ├── historico.md         # Histórico das sessões de desenvolvimento
│   ├── tarefas.md           # Controle de tarefas das sessões de desenvolvimento
│   └── api.md               # Documentação da API (se aplicável)
├── logs/                    # Arquivos de log (git ignored)
├── bin/                     # Scripts bash/utilitários
├── src/                     # Código fonte (varia conforme linguagem utilizada)
│   └── ...
├── tests/                   # Testes (varia conforme linguagem utilizada)
│   └── ...
├── .env.example             # Exemplo de variáveis ambiente
├── .gitignore
├── LICENSE                  # Licença de uso
├── README.md                # Documentação principal
└── setup.sh                 # Script para configuração/instalação (se aplicável)
```

