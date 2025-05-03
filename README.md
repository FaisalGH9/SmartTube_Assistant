# YouTube AI Assistant 🎧

A web app that lets you:
- ▶️ Process any YouTube video
- 📄 Generate regular or tutorial-style summaries
- 💬 Chat with the video content (like ChatGPT)
- 🔄 Export summaries as PDF in multiple languages (Arabic supported)
- 🌙 Toggle between Dark and Light mode

---

## 📚 Features
- Extracts audio using `yt-dlp`
- Transcribes video using OpenAI Whisper
- Summarizes using `LangChain + OpenAI`
- Chats via context-aware Q&A with timestamps
- PDF export via `WeasyPrint` with RTL language support

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

### Recommended Tools
- Google Chrome (for full PDF font support)
- Git (to clone)
- VS Code (to edit)

---

## 🔧 Installation

1. **Clone the repo**
```bash
git clone https://github.com/yourname/youtube-ai-assistant.git
cd youtube-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # on Windows
# OR
source venv/bin/activate  # on macOS/Linux
```

3. **Install Python packages**
```bash
pip install -r requirements.txt
```

4. **Set OpenAI API key**
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_key_here
```

---

## 🌐 Run the App
```bash
python app.py
```
Then open:
```
http://127.0.0.1:5000
```

---

## 📊 Folder Structure
```
project/
├── app.py
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── choice.html
│   ├── summary.html
│   └── chatbot.html
├── static/
│   └── fonts/ (optional)
├── utils/
│   ├── youtube_utils.py
│   ├── whisper_utils.py
│   ├── qa_utils.py
│   ├── summary_utils.py
```

---

## ✅ Requirements.txt (sample)
```txt
Flask
python-dotenv
yt-dlp
openai
weasyprint
langchain
faiss-cpu
cairocffi
```

---

## ✨ Credits
Built with love using Flask, OpenAI, LangChain, yt-dlp, and WeasyPrint.


