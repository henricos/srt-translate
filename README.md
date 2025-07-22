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
├── logs/             # Arquivos de log
├── output/           # Arquivos de saída (legendas, áudios, etc.)
├── src/              # Código fonte Python
├── tests/            # Testes (a serem implementados)
├── .gitignore
├── LICENSE
├── README.md
└── setup.sh
```

## 📋 Pré-requisitos

Este projeto foi desenvolvido e testado em um ambiente Ubuntu. Os comandos a seguir são exemplos de como instalar as dependências necessárias nessa distribuição. Caso utilize outro sistema operacional, consulte a documentação oficial das ferramentas para obter as instruções de instalação corretas.

### FFmpeg

O `ffmpeg` é essencial para a manipulação de arquivos de áudio e vídeo, permitindo a extração de legendas e a conversão de formatos. Como exemplo, para instalá-lo em sistemas baseados em Debian/Ubuntu, pode-se utilizar o seguinte comando:

```bash
sudo apt install ffmpeg
```

### Python e Pip

O projeto utiliza `python3` para execução, `venv` para criar ambientes virtuais e `pip` para gerenciar as dependências. Em sistemas baseados em Debian/Ubuntu, o `python3-venv` geralmente inclui o `pip`. Para garantir que todos os componentes necessários estejam instalados, o comando de exemplo é:

```bash
sudo apt install python3 python3-venv python3-pip
```

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

Os scripts na pasta `bin/` foram projetados para serem auto-suficientes, gerenciando automaticamente a ativação do ambiente virtual (`venv`). Portanto, **não é necessário ativar o ambiente manualmente** antes de executá-los.

-   **Para traduzir um arquivo de legenda:**
    ```bash
    ./bin/translate_srt.sh /caminho/para/sua/legenda.srt
    ```

-   **Para extrair a legenda de um arquivo de vídeo:**
    ```bash
    ./bin/extract_subtitle.sh /caminho/para/seu/video.mkv
    ```

-   **Para transcrever o áudio de um vídeo e gerar uma legenda (em breve):**
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
