import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def baixar_video_mp4(url, pasta_destino, log_text):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        log_text.insert(tk.END, f"Baixando vídeo: {yt.title}\n")
        caminho_video = video.download(output_path=pasta_destino)
        log_text.insert(tk.END, f"Vídeo baixado com sucesso em: {caminho_video}\n")
        return caminho_video
    except Exception as e:
        log_text.insert(tk.END, f"Erro ao baixar vídeo: {e}\n")
        return None

def converter_para_mp3(caminho_video, pasta_destino, log_text):
    try:
        log_text.insert(tk.END, "Convertendo vídeo para MP3...\n")
        video_clip = VideoFileClip(caminho_video)
        if not video_clip.audio:
            log_text.insert(tk.END, "Erro: O vídeo não contém áudio.\n")
            return
        caminho_audio = os.path.join(pasta_destino, os.path.splitext(os.path.basename(caminho_video))[0] + '.mp3')
        video_clip.audio.write_audiofile(caminho_audio)
        video_clip.close()
        log_text.insert(tk.END, f"Áudio salvo com sucesso em: {caminho_audio}\n")
    except Exception as e:
        log_text.insert(tk.END, f"Erro ao converter vídeo para MP3: {e}\n")

def iniciar_download(opcao, url, pasta_destino, log_text):
    def download_em_thread():
        try:
            log_text.insert(tk.END, "Iniciando download...\n")
            if opcao == "MP4":
                baixar_video_mp4(url, pasta_destino, log_text)
            elif opcao == "MP3":
                caminho_video = baixar_video_mp4(url, pasta_destino, log_text)
                if caminho_video:
                    converter_para_mp3(caminho_video, pasta_destino, log_text)
                    os.remove(caminho_video)
            else:
                log_text.insert(tk.END, "Opção inválida. Tente novamente.\n")
        except Exception as e:
            log_text.insert(tk.END, f"Erro ao baixar vídeo: {e}\n")
        finally:
            log_text.config(state=tk.DISABLED)
            log_text.see(tk.END)

    thread = threading.Thread(target=download_em_thread)
    thread.start()

def criar_interface():
    janela = tk.Tk()
    janela.title("TikTok Video Downloader")
    janela.geometry("600x500")
    janela.resizable(False, False)
    janela.configure(bg="#f7f7f7")

    botao_style = {"bg": "#4caf50", "fg": "white", "font": ("Arial", 12, "bold"), "bd": 0, "relief": "flat"}
    rotulo_style = {"bg": "#f7f7f7", "font": ("Arial", 12)}

    tk.Label(janela, text="URL do Vídeo do TikTok:", **rotulo_style).pack(pady=10)
    url_entry = tk.Entry(janela, width=60, font=("Arial", 12), relief="solid")
    url_entry.pack(pady=5)

    formato_var = tk.StringVar(value="MP4")
    formato_frame = tk.Frame(janela, bg="#f7f7f7")
    formato_frame.pack(pady=10)
    tk.Radiobutton(formato_frame, text="MP4", variable=formato_var, value="MP4", **rotulo_style).grid(row=0, column=0, padx=10)
    tk.Radiobutton(formato_frame, text="MP3", variable=formato_var, value="MP3", **rotulo_style).grid(row=0, column=1, padx=10)

    log_text = tk.Text(janela, height=15, font=("Courier New", 10), state=tk.DISABLED, bg="#ffffff", relief="solid")
    log_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    pasta_destino = ""

    def escolher_pasta():
        nonlocal pasta_destino
        pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino")
        if pasta_destino:
            log_text.insert(tk.END, f"Pasta selecionada: {pasta_destino}\n")

    def iniciar():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Erro", "URL não pode estar vazia.")
            return
        if not pasta_destino:
            messagebox.showerror("Erro", "Selecione uma pasta de destino.")
            return
        iniciar_download(formato_var.get(), url, pasta_destino, log_text)

    tk.Button(janela, text="Escolher Pasta", command=escolher_pasta, **botao_style, height=2, width=20).pack(pady=10)
    tk.Button(janela, text="Iniciar Download", command=iniciar, **botao_style, height=2, width=20).pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()
