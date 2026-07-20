# YouTube Audio Downloader com pytubefix

Script em Python para baixar o áudio e o vídeo de um vídeo do YouTube usando `pytubefix`, selecionar automaticamente a melhor resolução disponível e converter o áudio baixado para MP3 usando FFmpeg.

## Funcionalidades

* Recebe uma URL do YouTube pelo terminal.
* Busca automaticamente o melhor stream de áudio disponível.
* Busca automaticamente a maior resolução de vídeo disponível.
* Prioriza vídeo em formato MP4 para melhor compatibilidade.
* Exibe progresso do download.
* Baixa áudio e vídeo separadamente.
* Converte o áudio baixado para `.mp3` usando FFmpeg.
* Aguarda a criação dos arquivos antes de continuar o processo.

## Tecnologias utilizadas

* Python
* pytubefix
* FFmpeg
* pathlib
* subprocess

## Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

* Python 3.10 ou superior
* FFmpeg
* pip

## Instalação

Clone este repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Acesse a pasta do projeto:

```bash
cd seu-repositorio
```

Instale as dependências:

```bash
pip install pytubefix
```

## Configuração do FFmpeg

O script utiliza o FFmpeg para converter o áudio baixado para MP3.

Atualmente, o caminho do FFmpeg está definido diretamente no código:

```python
ffmpeg_exe = r'D:\Video\ffmpeg-2026-05-18-git-b4d11dffbf-essentials_build\bin\ffmpeg.exe'
```

Caso o FFmpeg esteja instalado em outro local no seu computador, altere esse caminho para o local correto do arquivo `ffmpeg.exe`.

Exemplo:

```python
ffmpeg_exe = r'C:\ffmpeg\bin\ffmpeg.exe'
```

Também é possível adicionar o FFmpeg ao PATH do sistema e adaptar o código para usar apenas:

```python
ffmpeg_exe = 'ffmpeg'
```

## Como usar

Execute o script pelo terminal:

```bash
python main.py
```

Em seguida, informe a URL do vídeo do YouTube:

```bash
Digite a URL do vídeo do YouTube: https://www.youtube.com/watch?v=exemplo
```

O programa irá:

1. Carregar o vídeo informado.
2. Selecionar o melhor áudio disponível.
3. Selecionar a maior resolução de vídeo disponível.
4. Baixar o áudio.
5. Baixar o vídeo.
6. Renomear o arquivo de vídeo com a extensão correta.
7. Converter o áudio para MP3.

## Exemplo de saída

```bash
Digite a URL do vídeo do YouTube: https://www.youtube.com/watch?v=exemplo
Usando maior resolução disponível: 1080p
30 FPS (MP4)
Iniciando download do áudio...
Áudio baixado: audio
Iniciando download do vídeo...
Vídeo baixado: video.mp4 (video/mp4)
Convertendo áudio para MP3...
Arquivo convertido para MP3: audio.mp3
Arquivo MP3 gerado: audio.mp3
```

## Estrutura esperada dos arquivos gerados

Após a execução, o diretório do projeto poderá conter arquivos como:

```bash
audio
audio.mp3
video.mp4
```

ou, dependendo do formato disponível:

```bash
audio
audio.mp3
video.webm
```

## Observações importantes

Este script baixa áudio e vídeo separadamente. A conversão final feita pelo programa é apenas do áudio para MP3.

O vídeo baixado não é combinado automaticamente com o áudio. Caso queira gerar um arquivo final com vídeo e áudio juntos, será necessário adicionar uma etapa extra usando FFmpeg.

Além disso, o caminho do FFmpeg está configurado de forma fixa no código. Para tornar o projeto mais portátil, recomenda-se futuramente utilizar `shutil.which('ffmpeg')` para localizar o FFmpeg automaticamente no sistema.

## Possíveis melhorias futuras

* Permitir escolher a resolução manualmente.
* Permitir baixar somente áudio ou somente vídeo.
* Unir áudio e vídeo em um único arquivo final.
* Detectar automaticamente o FFmpeg no PATH.
* Criar uma interface gráfica simples.
* Permitir escolher a pasta de destino.
* Tratar nomes de arquivos com base no título do vídeo.
* Adicionar suporte para playlists.

## Aviso legal

Use este projeto apenas para fins educacionais e para baixar conteúdos que você tem permissão para acessar e armazenar. Respeite os termos de uso do YouTube e os direitos autorais dos criadores de conteúdo.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
