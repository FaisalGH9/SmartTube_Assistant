from urllib.parse import urlparse, parse_qs
import yt_dlp
import os
from yt_dlp import YoutubeDL


def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        return parse_qs(query.query).get('v', [None])[0]
    return None

def download_audio(youtube_url, output_path):
    proxy = os.getenv("PROXY_URL")

    ydl_opts = {
        'format': 'bestaudio[ext=webm]',
        'outtmpl': output_path,
        'quiet': False,
    }

    if proxy:
        ydl_opts['proxy'] = proxy  # ✅ إضافة البروكسي من .env

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
