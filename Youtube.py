from pytubefix import YouTube
from pytubefix.cli import on_progress
import shutil
import subprocess
import time
from pathlib import Path

url = input('Digite a URL do vídeo do YouTube: ')
yt = YouTube(url, on_progress_callback=on_progress)

def itags(resolution=None):
    max_audio = 0
    audio_value = None
    for audio_stream in yt.streams.filter(only_audio=True):
        abr = int(audio_stream.abr.replace('kbps', ''))
        if abr > max_audio:
            max_audio = abr
            audio_value = audio_stream.itag

    if audio_value is None:
        raise RuntimeError('Nenhum stream de áudio encontrado.')

    if resolution is None:
        available_resolutions = sorted(
            {stream.resolution for stream in yt.streams.filter(only_video=True) if stream.resolution},
            key=lambda r: int(r.replace('p', ''))
        )
        if not available_resolutions:
            raise ValueError('Nenhum stream de vídeo disponível.')
        resolution = available_resolutions[-1]
        print(f'Usando maior resolução disponível: {resolution}')

    video_streams = yt.streams.filter(only_video=True, res=resolution)
    if not video_streams:
        available = sorted(
            {stream.resolution for stream in yt.streams.filter(only_video=True) if stream.resolution},
            key=lambda r: int(r.replace('p', ''))
        )
        raise ValueError(
            f'Nenhum stream de vídeo encontrado para {resolution}. Resoluções disponíveis: {available}'
        )

    # Preferir MP4 em vez de WebM para melhor compatibilidade
    mp4_streams = video_streams.filter(mime_type='video/mp4')
    
    for fps in (60, 30, 24):
        if mp4_streams:
            fps_streams = mp4_streams.filter(fps=fps)
            if fps_streams:
                print(f'{fps} FPS (MP4)')
                return audio_value, fps_streams[0].itag
        
        fps_streams = video_streams.filter(fps=fps)
        if fps_streams:
            print(f'{fps} FPS')
            return audio_value, fps_streams[0].itag

    print('Nenhum stream 60/30/24 FPS encontrado, usando o primeiro disponível.')
    return audio_value, video_streams[0].itag


def convert_to_mp3(input_file, output_file=None):
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.with_suffix('.mp3')
    output_path = Path(output_file)

    ffmpeg_exe = r'D:\Video\ffmpeg-2026-05-18-git-b4d11dffbf-essentials_build\bin\ffmpeg.exe'
    if ffmpeg_exe is None:
        raise RuntimeError(
            'ffmpeg não foi encontrado. Instale o ffmpeg e adicione ao PATH para converter para mp3.'
        )

    subprocess.run(
        [
            ffmpeg_exe,
            '-y',
            '-i', str(input_path),
            '-vn',
            '-c:a', 'libmp3lame',
            '-q:a', '2',
            str(output_path),
        ],
        check=True,
    )

    print(f'Arquivo convertido para MP3: {output_path.name}')
    return output_path


def wait_for_file(path, timeout=60):
    path = Path(path)
    start = time.monotonic()
    while not path.exists():
        if time.monotonic() - start > timeout:
            raise FileNotFoundError(f'O arquivo {path} não apareceu após {timeout} segundos.')
        time.sleep(1)
    return path


audio, video = itags()  # usa a maior resolução disponível

audio_stream = yt.streams.get_by_itag(audio)
video_stream = yt.streams.get_by_itag(video)

print('Iniciando download do áudio...')
audio_path = Path(audio_stream.download(filename='audio'))
wait_for_file(audio_path, timeout=120)
print(f'Áudio baixado: {audio_path.name}')

print('Iniciando download do vídeo...')
video_path = Path(video_stream.download(filename='video'))
wait_for_file(video_path, timeout=120)

# Renomear para adicionar extensão correta baseado no tipo MIME
mime_type = video_stream.mime_type
if 'mp4' in mime_type:
    video_path_renamed = video_path.parent / (video_path.name + '.mp4')
elif 'webm' in mime_type:
    video_path_renamed = video_path.parent / (video_path.name + '.webm')
else:
    video_path_renamed = video_path

if video_path != video_path_renamed:
    video_path.rename(video_path_renamed)
    video_path = video_path_renamed

print(f'Vídeo baixado: {video_path.name} ({video_stream.mime_type})')

print('Convertendo áudio para MP3...')
mp3_path = convert_to_mp3(audio_path)

print(f'Arquivo MP3 gerado: {mp3_path.name}')