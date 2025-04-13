import os
import requests
import vlc
import tkinter as tk
from tkinter import messagebox
import threading
from yt_dlp import YoutubeDL

# 🔧 إضافة مسار VLC
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")

# ✅ استخراج رابط البث المباشر الحقيقي من YouTube
def get_youtube_stream_url(channel_url):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'extract_flat': False,
            'noplaylist': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            return info['url']
    except Exception as e:
        print(f"[!] Error extracting stream URL: {e}")
        return None

# ✅ التحقق من حالة البث (اختياري)
def is_live(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if "isLiveNow" in response.text or "live" in response.url:
            return True
    except Exception as e:
        print(f"[!] Error checking live status: {e}")
    return False

# ✅ تشغيل البث داخل Canvas
def play_live_stream(url):
    try:
        stream_url = get_youtube_stream_url(url)
        if not stream_url:
            status_label.config(text="❌ تعذر تشغيل البث", fg="red")
            return

        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(stream_url)
        player.set_media(media)

        hwnd = canvas.winfo_id()
        player.set_hwnd(hwnd)

        player.play()
        status_label.config(text="✅ البث مباشر الآن!", fg="green")
    except Exception as e:
        print(f"[❌] Error playing live stream: {e}")
        status_label.config(text="❌ خطأ أثناء تشغيل البث", fg="red")

# ✅ مراقبة حالة البث وتشغيله
def monitor_live():
    channel_url = channel_url_entry.get().strip()
    if not channel_url:
        messagebox.showerror("خطأ", "يرجى إدخال رابط القناة.")
        return

    if not channel_url.endswith("/live"):
        channel_url += "/live"

    if is_live(channel_url):
        play_live_stream(channel_url)
    else:
        status_label.config(text="🚫 البث غير متاح حاليًا", fg="red")
        root.after(60000, monitor_live)

# 🔁 تشغيل المراقبة في Thread
def start_monitoring():
    threading.Thread(target=monitor_live, daemon=True).start()

# ✅ واجهة المستخدم
root = tk.Tk()
root.title("مراقب البث المباشر")

tk.Label(root, text="أدخل رابط القناة:").pack(pady=10)

channel_url_entry = tk.Entry(root, width=50)
channel_url_entry.pack(pady=10)

start_button = tk.Button(root, text="ابدأ مراقبة البث", command=start_monitoring)
start_button.pack(pady=20)

status_label = tk.Label(root, text="حالة البث: غير متاح", fg="red")
status_label.pack(pady=10)

canvas = tk.Canvas(root, width=640, height=360, bg="black")
canvas.pack(pady=20)

root.mainloop()

