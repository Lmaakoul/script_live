import subprocess
import time
import requests


channel_url = "https://www.youtube.com/@flosssi/live" 

def is_live(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        if "isLiveNow" in response.text or "live" in response.url:
            return True
    except Exception as e:
        print(f"[!] Error checking live status: {e}")
    return False

def record_live():
    print("[🎥] البث بدأ! جاري التسجيل...")
    subprocess.call([
        "yt-dlp",
        "--live-from-start",
        "-f", "bestvideo+bestaudio",  
        "--merge-output-format", "mp4", 
        "-o", "mustaphaelmaakoul - %(title)s.%(ext)s",
        channel_url
    ])
    print("[🎥] تم تنزيل جزء من الفيديو.")

print("[⏳] جاري مراقبة القناة... انتظر بدء البث المباشر.")


while True:
    if is_live(channel_url):
        record_live()
    else:
        print("[⏳] البث غير متاح، سيتم التحقق مرة أخرى بعد 60 ثانية.")
    time.sleep(60) 
