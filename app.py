from flask import Flask, render_template, request, redirect, url_for, session, make_response
from dotenv import load_dotenv
import os
import json
from io import BytesIO
from xhtml2pdf import pisa

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "supersecretkey_2025")  # ✅ constant, not random

# ======= Utility Imports =======
from utils.youtube_utils import extract_video_id, download_audio
from utils.whisper_utils import transcribe
from utils.summary_utils import summarize_transcript
from utils.qa_utils import process_and_store, load_chain
from utils.agent_memory_chain import get_smart_chain


# ======= ROUTES =======

import subprocess

@app.route("/", methods=["GET", "POST"])
def home():
    terminal_output = ""

    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        video_language = request.form["video_language"]

        # Capture terminal output (example with dir on Windows)
        try:
            # Change 'echo' to 'dir' or any valid command on Windows
            result = subprocess.run(['dir'], capture_output=True, text=True, shell=True)
            terminal_output = result.stdout  # Capture the output from the terminal

            # Video processing logic here...
            video_id = extract_video_id(youtube_url)
            session["youtube_url"] = youtube_url
            session["video_language"] = video_language
            session["video_id"] = video_id
            session.pop("qa_chain_ready", None)
            session.pop("chat_history", None)

            data_dir = os.path.join("data", video_id)
            os.makedirs(data_dir, exist_ok=True)
            audio_path = os.path.join(data_dir, "audio.webm")
            transcript_path = os.path.join(data_dir, "transcript.txt")

            download_audio(youtube_url, audio_path)
            transcribe(audio_path, transcript_path, language=video_language)

            # After processing, redirect to the next page
            return redirect(url_for("choice"))
        
        except Exception as e:
            terminal_output = f"❌ Failed to process video: {e}"

    return render_template("home.html", terminal_output=terminal_output)




@app.route("/choice")
def choice():
    return render_template("choice.html")


@app.route("/summary", methods=["GET", "POST"])
def summary():
    # 🔍 Debug session contents
    print("SESSION:", dict(session))

    video_id = session.get("video_id")
    if not video_id:
        return redirect(url_for("home"))

    transcript_path = os.path.join("data", video_id, "transcript.txt")
    summary_path = os.path.join("data", video_id, "summary.txt")
    summary_text = None

    if request.method == "POST":
        summary_language = request.form.get("summary_language", "en")
        summary_type = request.form.get("summary_type", "regular")

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_json = json.load(f)

        summary_text = summarize_transcript(transcript_json, summary_language, summary_type)

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_text)

    elif os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_text = f.read()

    return render_template("summary.html", summary_text=summary_text)




@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    video_id = session.get("video_id")
    if not video_id:
        return redirect(url_for("home"))

    transcript_path = os.path.join("data", video_id, "transcript.txt")
    if not os.path.exists(transcript_path):
        return "❌ Transcript not found. Please reprocess the video.", 500

    if not session.get("qa_chain_ready"):
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_json = json.load(f)

        if not transcript_json.get("segments"):
            return "❌ Transcript is empty. Make sure the video has spoken content.", 400

        process_and_store(video_id, transcript_json)
        session["qa_chain_ready"] = True

    # ✅ Use memory-aware conversational chain
    qa_chain = get_smart_chain(video_id)
    chat_history = session.get("chat_history", [])

    if request.method == "POST":
        question = request.form["question"]

        # ✅ Let chain handle context-aware answers
        result = qa_chain({"question": question})
        answer = result["answer"]

        # Optional: pull timestamp from sources
        sources = result.get("source_documents", [])
        if sources:
            source_text = sources[0].page_content
            if "[" in source_text and "]" in source_text:
                timestamp = source_text.split("]")[0].replace("[", "")
                answer = f"(⏱️ {timestamp}) {answer}"

        chat_history.append({"question": question, "answer": answer})
        session["chat_history"] = chat_history[-10:]

    return render_template("chatbot.html", chat_history=chat_history)


@app.route("/download_summary", methods=["POST"])
def download_summary():
    summary_text = request.form.get("summary_content", "")
    video_id = session.get("video_id", "summary")

    html = f"""
    <html>
    <head><meta charset="UTF-8"><style>body {{ font-family: Arial; }}</style></head>
    <body><h2>Summary</h2><p>{summary_text.replace('\n', '<br>')}</p></body>
    </html>
    """

    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        return "❌ Failed to generate PDF.", 500

    response = make_response(pdf_buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={video_id}_summary.pdf"
    return response


if __name__ == "__main__":
    print("🚀 Starting Flask app...")
    app.run(debug=True)
