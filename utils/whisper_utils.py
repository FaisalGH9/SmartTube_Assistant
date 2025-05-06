import openai
import json
import os
import tempfile
import subprocess

MAX_FILE_SIZE_MB = 24
FFMPEG_PATH = r"C:\Users\WELCOME\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def get_audio_duration(file_path):
    result = subprocess.run(
        [FFMPEG_PATH, "-i", file_path],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    for line in result.stderr.splitlines():
        if "Duration" in line:
            duration_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = duration_str.split(":")
            return int(float(h) * 3600 + float(m) * 60 + float(s))
    return 0

def split_audio_ffmpeg(file_path, chunk_duration=600):  # 10 minutes = 600s
    duration = get_audio_duration(file_path)
    print(f"🎧 Audio duration: {duration} seconds")

    chunk_paths = []
    for i in range(0, duration, chunk_duration):
        start_time = i
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".webm").name

        # ffmpeg command to split + compress
        cmd = [
            FFMPEG_PATH, "-i", file_path,
            "-ss", str(start_time),
            "-t", str(chunk_duration),
            "-ac", "1",            # mono
            "-ar", "16000",        # 16kHz sample rate
            "-b:a", "48k",         # low bitrate for compression
            "-c:a", "libopus",     # efficient codec for .webm
            "-y", temp_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        size = get_file_size_mb(temp_path)
        if size <= MAX_FILE_SIZE_MB:
            print(f"✅ Chunk OK: {temp_path} ({size:.2f} MB)")
            chunk_paths.append(temp_path)
        else:
            os.remove(temp_path)
            print(f"⚠️ Chunk too big at {start_time}s ({size:.2f} MB) — skipped")

    return chunk_paths

def transcribe(file_path, transcript_path, language=None):
    final_transcript = {
        "segments": []
    }

    # Decide if we need to split or not
    if get_file_size_mb(file_path) <= MAX_FILE_SIZE_MB:
        audio_chunks = [file_path]
    else:
        audio_chunks = split_audio_ffmpeg(file_path)

    for i, chunk_path in enumerate(audio_chunks):
        print(f"🧠 Transcribing chunk {i + 1}/{len(audio_chunks)}...")
        with open(chunk_path, "rb") as f:
            kwargs = {"file": f, "response_format": "verbose_json"}
            if language and language != "auto":
                kwargs["language"] = language
            try:
                chunk_transcript = openai.Audio.transcribe("whisper-1", **kwargs)
                final_transcript["segments"].extend(chunk_transcript.get("segments", []))
            except Exception as e:
                print(f"❌ Error transcribing chunk: {e}")

        if chunk_path != file_path:
            os.remove(chunk_path)

    # Save the final full transcript
    with open(transcript_path, "w", encoding="utf-8") as f_out:
        json.dump(final_transcript, f_out, indent=2)

    print("✅ Transcription complete.")
    return final_transcript
