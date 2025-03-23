import subprocess
import time
import requests

# Update the channel URL
channel_url = "https://www.youtube.com/@flosssi/live"  # New channel URL

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
    print("[🎥] The live broadcast has started! Recording...")
    subprocess.call([
        "yt-dlp",
        "--live-from-start",
        "-f", "bestvideo+bestaudio",  # Download best video and audio
        "--merge-output-format", "mp4",  # Merge audio and video into one file
        "-o", "mustaphaelmaakoul - %(title)s.%(ext)s",
        channel_url
    ])
    print("[🎥] A part of the video has been downloaded.")

print("[⏳] Monitoring the channel... Waiting for the live broadcast to start.")

# Continuous check
while True:
    if is_live(channel_url):
        record_live()
    else:
        print("[⏳] The live broadcast is unavailable, checking again in 60 seconds.")
    time.sleep(60)  # Wait for 1 minute before the next check
