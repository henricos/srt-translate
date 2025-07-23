# Histórico de Sessões de Desenvolvimento

## 2025-07-23 - Melhoria da Documentação e Storytelling do Projeto

Nesta sessão, o arquivo `README.md` foi significativamente aprimorado para melhorar a experiência de novos usuários. Foi introduzida uma narrativa de storytelling para explicar o propósito do projeto, um diagrama `Mermaid` foi adicionado para ilustrar visualmente os três possíveis fluxos de trabalho (partindo de um vídeo, de uma legenda embutida ou de um arquivo `.srt`), e a seção de "Uso" foi reorganizada para refletir essa estrutura de "Pontos de Partida" e "Etapa Final", tornando os comandos mais intuitivos.

---


## 2025-07-22 - Refinamento da Verificação de Dependências do Sistema

Nesta sessão, o script `setup.sh` foi ajustado para utilizar `dpkg -s` na verificação de pacotes do sistema como `ffmpeg`, `python3-venv` e `python3-pip`. Esta mudança garante uma checagem mais precisa da instalação dos pacotes APT, corrigindo a sintaxe de teste anterior que não estava surtindo o efeito desejado e melhorando a robustez da configuração do ambiente.

---

## 2025-07-22 - Melhoria na Verificação de Pré-requisitos e Documentação

Nesta sessão, o script `setup.sh` foi aprimorado para incluir verificações mais robustas de dependências (ffmpeg, python3, venv, pip) e tratamento de erros explícito, garantindo que o processo de configuração seja interrompido em caso de falha. Adicionalmente, o arquivo `README.md` foi atualizado para refletir a necessidade do `pip` como pré-requisito, fornecendo instruções de instalação mais claras para novos ambientes.

---

## 2025-07-22 - Adaptação para Formato de Tradução Resiliente

Nesta sessão, o projeto foi adaptado para um novo formato de comunicação com o modelo de tradução, trocando o JSON por um formato "índice| texto" para aumentar a resiliência contra erros de formatação. A função `_attempt_json_fix` e toda a lógica de parsing de JSON foram removidas de `src/core/translator.py`. O prompt e o parser de resposta foram atualizados para o novo formato, e foram adicionados delimitadores de segurança (`<TRADUCAO_INICIO>` e `<TRADUCAO_FIM>`) para garantir a extração segura da tradução. A importação `json` também foi removida de `src/core/translator.py`.

---

## 2025-07-22 - Correção de Tipagem e Atualização de Referências

Nesta sessão, foi corrigido um erro de tipagem no `NamedTuple` `SubtitleBlock` em `src/core/models.py`, renomeando o campo `index` para `idx` para evitar conflito com métodos internos do Python. Todas as referências a `block.index` em `src/core/io.py` e `src/core/translator.py` foram atualizadas para `block.idx`, garantindo a consistência e eliminando os erros do Pylance.

---

## 2025-07-22 - Refinamento da Lógica de Nomenclatura de Arquivos de Legenda

Nesta sessão, a lógica para nomear os arquivos de legenda traduzidos em `src/core/translator.py` foi aprimorada. A expressão regular utilizada para detectar o código de idioma no nome do arquivo original foi refinada para suportar formatos compostos (ex: `en-US`, `pt-BR`), garantindo que a substituição para `.pt-BR` seja aplicada corretamente em todos os cenários.

---

## 2025-07-22 - Refatoração Arquitetural do Core da Aplicação

Nesta sessão, foi realizada uma refatoração arquitetural significativa no núcleo da aplicação. A lógica de negócio foi movida de `src/main.py` para módulos especializados em `src/core/`. Foram criados `src/core/io.py` para operações de arquivo e `src/core/models.py` para as estruturas de dados. Toda a orquestração da tradução foi centralizada em `src/core/translator.py`, e `src/main.py` foi simplificado para atuar apenas como o ponto de entrada da CLI, melhorando a modularidade e o desacoplamento do código.

---


## 2025-07-22 - Melhoria da Usabilidade e Documentação de Convenções

Nesta sessão, a experiência de uso e desenvolvimento foi aprimorada. O script `bin/translate_srt.sh` foi modificado para ativar o ambiente virtual `venv` automaticamente, simplificando a execução. Para refletir essa mudança, o `README.md` foi atualizado. Adicionalmente, foi criado e expandido o arquivo `.clinerules/project-conventions.md` para documentar convenções específicas do projeto, como a função do `setup.sh` e a decisão de manter os scripts Bash simples para facilitar a manutenção.

---

## 2025-07-22 - Teste e Aumento da Resiliência do Script de Tradução

Nesta sessão, o script `bin/translate_srt.sh` foi testado pela primeira vez em um arquivo de legenda real. O teste revelou uma falha na decodificação de respostas JSON da API. Para resolver o problema, o script `src/core/translator.py` foi aprimorado para ser mais resiliente, com um prompt mais robusto e uma função para recuperar dados de JSONs malformados. Adicionalmente, o script `src/main.py` foi modificado para aceitar um intervalo de blocos, permitindo o reprocessamento de lotes específicos. Após as melhorias, o lote com falha foi reprocessado com sucesso e a tradução do arquivo foi concluída.

---

## 2025-07-22 - Implementação Inicial do Script de Tradução de Legendas

Nesta sessão, foi implementada a primeira versão do sistema de tradução de legendas (`bin/translate_srt.sh`). O trabalho envolveu uma refatoração completa da abordagem anterior, modularizando o código em `src/core`, adotando o uso de variáveis de ambiente (`.env`) para configuração, e aprimorando a comunicação com a API para solicitar respostas em JSON, o que aumenta a robustez do parsing. Também foi implementado um sistema de logging detalhado para prompts e respostas. Esta é uma versão inicial que ainda não foi testada em um cenário real.

---

## 2025-07-22 - Refatoração e Correção do Script de Extração de Legendas

Nesta sessão, o script `bin/extract_subtitle.sh` foi extensivamente revisado e depurado para funcionar corretamente sem a diretiva `set -euo pipefail`. O complexo `trap ERR` foi removido em favor de um tratamento de erro explícito e mais simples, e a extração de informações das faixas foi refatorada para usar regex, tornando o script mais robusto e legível. O funcionamento foi validado com sucesso.

---

## 2025-07-21 - Implementação do Script de Extração de Legendas

Nesta sessão, foi criado e depurado o script `bin/extract_subtitle.sh`. O script utiliza `ffmpeg` para identificar e extrair todas as faixas de legenda no formato SRT de arquivos de vídeo MKV, salvando-as no diretório `output/` com nomes padronizados contendo o idioma. O processo incluiu a implementação de validações, tratamento de erros e um ciclo de depuração para garantir a robustez e portabilidade do script.

---

## 2025-07-21 - Adição do Diretório de Saída

Nesta sessão, foi criado o diretório `output` para armazenar os arquivos gerados pelos scripts, como legendas e áudios extraídos. A estrutura do projeto foi atualizada, incluindo a configuração do `.gitignore` para ignorar o conteúdo deste novo diretório e a documentação no `README.md` foi ajustada para refletir a mudança.

---

## 2025-07-21 - Refatoração da Configuração e Estrutura

Nesta sessão, foram realizados ajustes na configuração e estrutura do projeto. O `README.md` foi corrigido para refletir a localização correta do arquivo de ambiente, a variável no `.env.example` foi padronizada para `GEMINI_API_KEY`, e o diretório `logs` foi criado com a devida configuração no `.gitignore` para ser versionado corretamente.

---

## 2025-07-21 - Ajuste de Dependências e Setup

Nesta sessão, o arquivo `requirements.txt` foi atualizado para especificar as versões mínimas das dependências `google-genai` e `python-dotenv`. Adicionalmente, o script `setup.sh` foi ajustado para garantir a correta configuração do ambiente de desenvolvimento.

---

## 2025-07-21 - Melhorias na Documentação do README

Nesta sessão, o arquivo `README.md` foi aprimorado para maior clareza. A seção de pré-requisitos foi atualizada para especificar que o projeto assume um ambiente Ubuntu e que os comandos são exemplificativos. Além disso, foi adicionada uma nota na seção de uso indicando que a funcionalidade de transcrição de áudio ainda será implementada.

---

## 2025-07-21 - Adequação da Documentação às Regras do Projeto

Nesta sessão, foram revisadas as regras definidas no diretório `.clinerules` e, com base nelas, os arquivos `README.md` e `docs/historico.md` foram atualizados para se alinharem aos padrões de documentação, estrutura e formato de data do projeto.

---


## 2025-07-20 - Estrutura Inicial do Projeto

Nesta sessão inicial, foi definida e criada toda a estrutura de pastas para o projeto `srt-translate`, incluindo os diretórios `bin`, `src`, `config`, `docs` e `tests`. Adicionalmente, foram criados arquivos essenciais como o `README.md` com as instruções de uso, `LICENSE` com a licença MIT, `.gitignore` para controle de versão, `requirements.txt` com as dependências Python e o script `setup.sh` para automatizar a configuração do ambiente de desenvolvimento.

---
