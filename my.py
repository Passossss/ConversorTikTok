from pytube import YouTube
from moviepy.editor import VideoFileClip
import os



def converter_para_mp3(caminho_video, pasta_destino):
    try:
        print("Convertendo vídeo para MP3...")
        video_clip = VideoFileClip(caminho_video)
        caminho_audio = os.path.join(pasta_destino, os.path.splitext(os.path.basename(caminho_video))[0] + '.mp3')
        video_clip.audio.write_audiofile(caminho_audio)
        video_clip.close()
        print(f"Áudio salvo com sucesso em: {caminho_audio}")
    except Exception as e:
        print(f"Erro ao converter vídeo para MP3: {e}")


def main():
    print("=== TikTok Video Downloader ===")
    url = input("Digite a URL do vídeo do TikTok: ").strip()
    opcao = input("Escolha o formato para baixar (1 = MP4, 2 = MP3): ").strip()
    pasta_destino = "downloads"

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    if opcao == '1':
        baixar_video_mp4(url, pasta_destino)
    elif opcao == '2':
        caminho_video = os.path.join(pasta_destino, "temp_video.mp4")
        baixar_video_mp4(url, pasta_destino)
        converter_para_mp3(caminho_video, pasta_destino)
        os.remove(caminho_video)
    else:
        print("Opção inválida. Encerrando o programa.")


if __name__ == "__main__":
    main()
