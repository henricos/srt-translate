# srt-translate

Um conjunto de scripts para traduzir arquivos de legenda `.srt` para o português brasileiro, utilizando a biblioteca `google-genai` para interagir com a API do Google Gemini.

## 🚀 Funcionalidades

Este projeto oferece um conjunto de ferramentas de linha de comando para automatizar tarefas relacionadas a legendas de vídeos, incluindo:

- Extração de legendas de arquivos de vídeo (MKV).
- Extração de áudio e transcrição para gerar uma legenda no idioma original.
- Tradução de arquivos de legenda (`.srt`) de qualquer idioma para o português do Brasil.

## 📁 Estrutura do Projeto

```
srt-translate/
├── bin/              # Scripts executáveis
├── config/           # Arquivos de configuração
├── docs/             # Documentação
├── src/              # Código fonte Python
├── tests/            # Testes (a serem implementados)
├── .env.example      # Exemplo de variáveis de ambiente
├── .gitignore
├── LICENSE
├── README.md
└── setup.sh
```

## 📋 Pré-requisitos

- `git`
- `ffmpeg`
- `python3`
- `python3-venv`

## 🔧 Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/henricos/srt-translate.git
    cd srt-translate
    ```

2.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo e adicione sua chave da API do Google Gemini.
    ```bash
    cp config/.env.example config/.env
    nano config/.env
    ```

3.  **Execute o script de configuração:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

## 💻 Uso

-   **Para traduzir um arquivo de legenda:**
    ```bash
    ./bin/translate_srt.sh /caminho/para/sua/legenda.srt
    ```

-   **Para extrair a legenda de um arquivo de vídeo:**
    ```bash
    ./bin/extract_subtitle.sh /caminho/para/seu/video.mkv
    ```

-   **Para transcrever o áudio de um vídeo e gerar uma legenda:**
    ```bash
    ./bin/transcribe_audio.sh /caminho/para/seu/video.mkv
    ```

## 🧪 Testes

Ainda não há testes automatizados para este projeto.

## 🤝 Contribuição

1.  Fork o projeto
2.  Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit suas mudanças (`git commit -m 'feat: adiciona funcionalidade incrível'`)
4.  Push para a branch (`git push origin feature/AmazingFeature`)
5.  Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
