# srt-translate

Cansado de esperar pela legenda daquele episódio novo ou de não encontrar uma tradução de qualidade para um curso em outro idioma? O `srt-translate` nasceu para resolver exatamente isso.

Este projeto é um canivete suíço para quem precisa de legendas em português. Utilizando o poder da IA do Google Gemini, ele automatiza todo o processo, desde a extração de uma legenda embutida em um vídeo até a transcrição de um áudio do zero, culminando sempre em um arquivo `.srt` traduzido para o nosso bom português brasileiro.

## 🚀 Como Funciona? Os 3 Pontos de Partida

Não importa qual o seu ponto de partida, o `srt-translate` tem uma solução. Existem três pontos de partida possíveis para o processo, mas todos eles convergem para a mesma etapa final: a tradução.

1.  **Ponto de Partida 1: Você só tem o vídeo**
    *   **Problema:** Você tem um arquivo de vídeo (um filme, uma aula, etc.) com o áudio em outro idioma, mas sem nenhuma legenda.
    *   **Solução:** Execute o script `transcrever_audio.sh`. Ele extrai o áudio, gera um arquivo de legenda (`.srt`) no idioma original e o prepara para a etapa de tradução.

2.  **Ponto de Partida 2: O vídeo tem uma legenda embutida**
    *   **Problema:** Seu arquivo de vídeo (geralmente `.mkv`) veio com uma ou mais legendas embutidas, mas nenhuma delas em português.
    *   **Solução:** Execute o script `extrair_legendas.sh`. Ele "pesca" essa legenda de dentro do arquivo de vídeo e a salva como um arquivo `.srt` separado, deixando-a pronta para a tradução.

3.  **Ponto de Partida 3: Você já tem o arquivo de legenda**
    *   **Problema:** Você já baixou o arquivo de legenda (`.srt`), mas ele está em inglês, espanhol ou qualquer outro idioma.
    *   **Solução:** Ótimo! Você já tem tudo o que precisa para a etapa final. Nenhuma ação de preparação é necessária.

### Etapa Final: A Tradução

Todos os caminhos levam aqui. Uma vez que você tenha um arquivo de legenda `.srt` em mãos (seja ele gerado pelos scripts de preparação ou baixado por você), o passo final é sempre o mesmo: usar o script `traduzir_legenda.sh` para obter sua legenda perfeitamente traduzida para o português.

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

A seguir, os comandos são apresentados em uma ordem que reflete os possíveis fluxos de trabalho descritos acima.

### 1. `transcrever_audio.sh` (Ponto de Partida 1)

Use este comando quando você tem apenas o arquivo de vídeo e precisa criar a legenda a partir do áudio.

```bash
# Irá extrair o áudio, transcrevê-lo e salvar como .srt no idioma original
./bin/transcrever_audio.sh /caminho/para/seu/video.mkv
```
*Este comando está em desenvolvimento.*

### 2. `extrair_legendas.sh` (Ponto de Partida 2)

Use este comando quando seu vídeo (`.mkv`) já possui uma legenda embutida que você deseja extrair.

```bash
# Irá extrair a legenda embutida e salvá-la como um arquivo .srt
./bin/extrair_legendas.sh /caminho/para/seu/video.mkv
```

### 3. `traduzir_legenda.sh` (Etapa Final)

Este é o passo principal e comum a todos os pontos de partida. Use-o para traduzir qualquer arquivo de legenda `.srt` para o português.

```bash
# Irá traduzir o arquivo de legenda especificado para pt-BR
./bin/traduzir_legenda.sh /caminho/para/sua/legenda.srt
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
