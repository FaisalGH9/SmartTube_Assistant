# SmartTube Assistant 🎧
![home](https://github.com/user-attachments/assets/803e7b5d-2a15-4a62-bbc3-b066deef0b60)
![choise](https://github.com/user-attachments/assets/09adca8b-1ae3-4d20-9124-f1b872869f73)
![summery](https://github.com/user-attachments/assets/3206fabf-40c9-4759-a1e5-3fc1713e419d)
![chatboot](https://github.com/user-attachments/assets/2b7cafac-f33c-4d8c-aed1-3379be216423)

A web app that lets you:
- ▶️ Process any YouTube video
- 📄 Generate regular or tutorial-style summaries
- 💬 Chat with the video content (like ChatGPT)
- 🔄 Export summaries as PDF in multiple languages (Arabic supported)
- 🌙 Toggle between Dark and Light mode
- 📊 Trace interactions using LangSmith

---

## 📚 Features
- Extracts audio using `yt-dlp`
- Transcribes video using OpenAI Whisper
- Summarizes using `LangChain + OpenAI`
- Chats via context-aware Q&A with timestamps
- PDF export via `WeasyPrint` with RTL language support
- Full LangSmith tracing integration for summaries and chatbot

---

## 🚧 Requirements

### Python
- Python 3.8+

### Install dependencies
```bash
pip install -r requirements.txt
```

**If you're on Windows and using WeasyPrint:**
```bash
pip install cairocffi
```

---

## 🔢 Environment Setup
Create a `.env` file and include:
```env
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=YouTube AI Assistant
LANGCHAIN_TRACING_V2=true
FLASK_SECRET=your_flask_secret
```

---

## 🌐 Run the App
```bash
python app.py
```
Then open in your browser:
```
http://127.0.0.1:5000
```

---

## 📊 Folder Structure & File Descriptions
```
smarttube_assistant/
├── app.py                  # Main Flask app with all routes and server logic
├── requirements.txt        # Required Python packages
├── .env                    # Environment config for API keys and secrets
├── templates/              # HTML templates rendered via Flask
│   ├── base.html           # Base layout with nav, dark mode, and CSS
│   ├── home.html           # Homepage for YouTube URL input and language select
│   ├── choice.html         # Option selection: summary or chatbot
│   ├── summary.html        # Displays and downloads the video summary
│   └── chatbot.html        # Chat UI to ask questions about the video
├── static/                 # Static files like fonts or custom CSS
│   └── fonts/              # Optional Arabic font folder (not needed with WeasyPrint)
├── utils/                  # Utility modules for different tasks
│   ├── youtube_utils.py    # Handles YouTube video/audio download with yt-dlp
│   ├── whisper_utils.py    # Transcribes audio to text using OpenAI Whisper
│   ├── qa_utils.py         # Vector database setup and chatbot chain loading (LangChain)
│   ├── summary_utils.py    # Builds and runs summarization prompts using LangChain
│   └── agent_memory_chain.py # Memory-aware chatbot chain setup for context handling

---

## 📄 Sample `requirements.txt`
```txt
arabic-reshaper==3.0.0
asn1crypto==1.5.1
blinker==1.9.0
certifi==2025.4.26
cffi==1.17.1
chardet==5.2.0
charset-normalizer==3.4.2
click==8.1.8
colorama==0.4.6
cryptography==44.0.3
cssselect2==0.8.0
defusedxml==0.7.1
Flask==3.1.0
html5lib==1.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
lxml==5.4.0
MarkupSafe==3.0.2
oscrypto==1.3.0
pillow==11.2.1
pycparser==2.22
pyHanko==0.26.0
pyhanko-certvalidator==0.26.8
pypdf==5.4.0
python-bidi==0.6.6
python-dotenv==1.1.0
PyYAML==6.0.2
qrcode==8.2
reportlab==4.4.0
requests==2.32.3
six==1.17.0
svglib==1.5.1
tinycss2==1.4.0
tzdata==2025.2
tzlocal==5.3.1
uritools==5.0.0
urllib3==2.4.0
webencodings==0.5.1
Werkzeug==3.1.3
xhtml2pdf==0.2.17
flask
python-dotenv
openai
yt_dlp
langchain
xhtml2pdf
tiktoken
chromadb
langchain_community

```

---

## 🌐 LangSmith Dashboard
Log in at [smith.langchain.com](https://smith.langchain.com/) to see traces:
- Summarize Transcript
- Load Chatbot QA Chain
- Process and Store Transcript

---

## ✨ Credits
Built with Flask, OpenAI, LangChain, yt-dlp, and LangSmith

---


