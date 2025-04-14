import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import datetime
import vlc
from yt_dlp import YoutubeDL
import requests

# إعداد VLC
os.add_dll_directory(r"C:\\Program Files\\VideoLAN\\VLC")

# متغيرات عامة
is_recording = False
save_folder = os.getcwd()
notification_enabled = True
channel_url = ""
player = None

# استخراج رابط البث الحقيقي

def get_youtube_stream_url(channel_url):
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'noplaylist': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            return info.get('url', None)
    except Exception as e:
        log(f"خطأ في استخراج رابط البث: {e}")
        return None

# التحقق من حالة البث

def is_live(channel_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(channel_url, headers=headers)
        return "isLiveNow" in response.text or "/live" in response.url
    except:
        return False

# تشغيل VLC في كانفاس

def play_stream(url):
    global player
    try:
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(url)
        player.set_media(media)
        player.set_hwnd(canvas.winfo_id())
        player.play()
    except Exception as e:
        log(f"خطأ VLC: {e}")

# بدء التسجيل

def start_recording(stream_url):
    global is_recording
    try:
        filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
        filepath = os.path.join(save_folder, filename)
        log(f"بدء التسجيل: {filename}")
        ydl_opts = {
            'outtmpl': filepath,
            'quiet': True,
            'format': 'best'
        }
        is_recording = True
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([stream_url])
        log("تم انتهاء التسجيل.")
    except Exception as e:
        log(f"خطأ في التسجيل: {e}")
    is_recording = False

# المراقبة الذكية

def monitor():
    global is_recording
    log("بدء مراقبة القناة...")
    url = url_entry.get().strip()
    if not url:
        log("يرجى إدخال رابط القناة.")
        return
    global channel_url
    channel_url = url
    def loop():
        while True:
            last_attempt_label.config(text="آخر محاولة: " + datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y"))
            if is_live(channel_url):
                log("تم العثور على بث مباشر!")
                stream_url = get_youtube_stream_url(channel_url)
                if stream_url:
                    play_stream(stream_url)
                    if not is_recording:
                        threading.Thread(target=start_recording, args=(stream_url,), daemon=True).start()
                break
            else:
                log("لا يوجد بث حاليا...")
                time.sleep(60)
    threading.Thread(target=loop, daemon=True).start()

# تحديث مكان الحفظ

def choose_folder():
    global save_folder
    folder = filedialog.askdirectory()
    if folder:
        save_folder = folder
        log(f"تم تحديد مكان الحفظ: {save_folder}")

# تسجيل في سجل الأحداث

def log(msg):
    timestamp = time.strftime("[%H:%M:%S]")
    logs.insert(tk.END, f"{timestamp} {msg}\n")
    logs.yview(tk.END)

# إعداد واجهة Tkinter
root = tk.Tk()
root.title("Live Monitor App")
root.configure(bg="#1e1e2f")

# العنوان
header = tk.Label(root, text="\U0001F4FA Live Monitor App", font=("Segoe UI", 20), fg="white", bg="#1e1e2f")
header.pack(pady=10)

# حقل رابط القناة
url_frame = tk.Frame(root, bg="#1e1e2f")
tk.Label(url_frame, text="رابط القناة:", fg="white", bg="#1e1e2f").pack(side=tk.LEFT)
url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=5)
url_frame.pack(pady=5)

# تروس الوضع
last_attempt_label = tk.Label(root, text="... في وضع المراقبة", fg="gray", bg="#1e1e2f")
last_attempt_label.pack()

# كانفاس VLC
canvas = tk.Canvas(root, width=800, height=450, bg="black")
canvas.pack(pady=5)

# أزرار التحكم
btn_frame = tk.Frame(root, bg="#1e1e2f")
start_btn = tk.Button(btn_frame, text="ابدأ المراقبة", command=monitor)
start_btn.grid(row=0, column=0, padx=5)
choose_btn = tk.Button(btn_frame, text="اختر مكان الحفظ", command=choose_folder)
choose_btn.grid(row=0, column=1, padx=5)
notify_chk = tk.Checkbutton(btn_frame, text="تنبيه صوتي", variable=tk.BooleanVar(value=True))
notify_chk.grid(row=0, column=2, padx=5)
btn_frame.pack(pady=5)

# سجل النشاط
logs = tk.Text(root, height=10, bg="black", fg="lightgreen")
logs.pack(fill=tk.BOTH, padx=10, pady=5)

root.mainloop()
