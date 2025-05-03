from urllib.parse import urlparse, parse_qs
import yt_dlp

def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        return parse_qs(query.query).get('v', [None])[0]
    return None

def download_audio(youtube_url, output_path):
    ydl_opts = {
        'format': 'bestaudio[ext=webm]',
        'outtmpl': output_path,
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
