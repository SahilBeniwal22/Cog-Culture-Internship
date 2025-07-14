# Cog-Culture-Internship

# Voice AI Agent for Telephonic Candidate Screening

## 💡 Use Case
An automated AI agent that transcribes candidate voice answers, analyzes sentiment, extracts key information, and makes screening decisions.

## ⚙️ Tech Stack
- Python
- Whisper (speech-to-text)
- Transformers (sentiment analysis)
- Gradio (frontend)

## 💬 Agent Flow
1. Upload audio (candidate answer)
2. Transcription using Whisper
3. Sentiment analysis (positive/negative)
4. Keyword extraction (skills, location, years)
5. Agent reasoning logic (accept/escalate)
6. Return insights & closing line

## 🚀 How to Run
```bash
pip install -r requirements.txt
python app.py
