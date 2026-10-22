# 📚 Lecture Summarizer

> An AI-powered web application that helps university students quickly digest lecture notes and PDFs into structured study guides — powered by Google Gemini.

---

## 🌟 Features

- **Paste or Upload**: Accepts raw text notes or PDF lecture files
- **4-Section AI Summary**: Key Concepts, Definitions, Summary Paragraph, Exam Questions
- **PDF Text Extraction**: Powered by PyPDF2 — no OCR required for digital PDFs
- **Session Logging**: Every summarization is logged for progress tracking
- **Session History**: Browse past sessions in a clean table view
- **Modern UI**: Responsive, university-themed design with tab-based input
- **Drag & Drop PDF**: Intuitive file upload experience

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, Flask 3.x |
| AI | Google Gemini API (Multi-model fallback: `gemini-3.5-flash-lite`, `gemini-flash-lite-latest`, `gemini-3.8-flash`), `google-genai` SDK |
| PDF | PyPDF2 |
| Config | python-dotenv |
| Frontend | Jinja2 templates, vanilla JS, Google Fonts (Inter) |
| Deployment | Gunicorn |

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/lakkireddymokshithmanikantareddy/lecture-summarizer.git
cd lecture-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

```
GEMINI_API_KEY=your_actual_gemini_api_key
FLASK_SECRET_KEY=some_random_string_here
```

Get your Gemini API key at: https://aistudio.google.com/app/apikey

### 5. Run the application

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

---

## 📖 Usage

1. Navigate to the home page
2. Choose **Paste Notes** to type/paste lecture text, or **Upload PDF** to upload a lecture file
3. Click **✨ Summarize with AI**
4. Review your structured study guide with key concepts, definitions, a summary, and exam questions
5. Visit **/logs** to see your summarization history

---

## 📸 Screenshots

> _Add screenshots here after first run_

---

## 📈 Self-Improvement Journey

| Version | Feature Added | Why |
|---------|--------------|-----|
| v1.0 | Basic text input + Gemini summary | Working prototype |
| v1.1 | PDF upload support | Real-world lecture files |
| v1.2 | Structured output (4 sections) | More useful for studying |
| v1.3 | Session logging | Tracks improvement over time |
| v1.4 | Polished UI | Better user experience |
| v1.5 | GitHub deployment | Portfolio-ready |
| v1.6 | High-Availability Engine & Multi-Model Fallback | Resilient against LLM traffic spikes & cleaner definition formatting |


---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
