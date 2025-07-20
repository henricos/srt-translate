# srt-translate

Um conjunto de scripts para traduzir arquivos de legenda `.srt` para o português brasileiro, utilizando a biblioteca `google-genai` para interagir com a API do Google Gemini.

## Visão Geral

Este projeto oferece um conjunto de ferramentas de linha de comando para automatizar tarefas relacionadas a legendas de vídeos, incluindo:

*   Extração de legendas de arquivos de vídeo (MKV).
*   Extração de áudio e transcrição para gerar uma legenda no idioma original.
*   Tradução de arquivos de legenda (`.srt`) de qualquer idioma para o português do Brasil.

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em seu sistema (Debian/Ubuntu/Mint):

*   `git`
*   `ffmpeg`
*   `python3`
*   `python3-venv`

## Instalação

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
    Este script irá criar um ambiente virtual Python (`venv`), instalar as dependências e garantir que tudo esteja pronto para uso.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

## Como Usar

Após a instalação, você pode usar os scripts diretamente do seu terminal.

*   **Para traduzir um arquivo de legenda:**
    ```bash
    ./bin/translate_srt.sh /caminho/para/sua/legenda.srt
    ```

*   **Para extrair a legenda de um arquivo de vídeo:**
    ```bash
    ./bin/extract_subtitle.sh /caminho/para/seu/video.mkv
    ```

*   **Para transcrever o áudio de um vídeo e gerar uma legenda:**
    ```bash
    ./bin/transcribe_audio.sh /caminho/para/seu/video.mkv
    ```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
