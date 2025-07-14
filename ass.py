# app.py

import whisper
import gradio as gr
from transformers import pipeline
import re

# ----------------------------
# Load models
# ----------------------------

# Whisper model for transcription
whisper_model = whisper.load_model("base")

# Sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

# ----------------------------
# Helper functions
# ----------------------------

def transcribe_audio(audio_file):
    """Transcribe audio using Whisper."""
    result = whisper_model.transcribe(audio_file)
    return result["text"]

def extract_keywords(text):
    """Very basic keyword extraction using regex (skills, location, years). You can improve it with NLP later."""
    skills = re.findall(r"(Python|Java|SQL|React|AI|ML|Data Science|DevOps)", text, re.IGNORECASE)
    years = re.findall(r"(\d+) (years|year)", text)
    locations = re.findall(r"(Delhi|Bangalore|Hyderabad|Mumbai|Pune|Chennai)", text, re.IGNORECASE)
    return {
        "skills": list(set(skills)),
        "years": [y[0] for y in years],
        "locations": list(set(locations))
    }

def agent_decision(text, sentiment, keywords):
    """Simple reasoning logic for demo."""
    if sentiment == "NEGATIVE":
        decision = "Escalate to HR: candidate seems negative or hesitant."
        closing = "Thank you for your time. Our HR team will contact you further."
    elif len(keywords["skills"]) == 0:
        decision = "Escalate: No clear skills mentioned."
        closing = "Thank you! We will review your profile and get back to you."
    else:
        decision = "Candidate screened-in. Positive tone and clear skills."
        closing = "Thank you for your time! Our team will get back to you shortly."
    return decision, closing

def process_audio(audio_file):
    # Transcription
    text = transcribe_audio(audio_file)
    
    # Sentiment
    sentiment_result = sentiment_model(text)[0]
    sentiment = sentiment_result['label']
    
    # Keywords
    keywords = extract_keywords(text)
    
    # Reasoning
    decision, closing = agent_decision(text, sentiment, keywords)
    
    # Feedback card
    feedback = {
        "Transcript": text,
        "Sentiment": sentiment,
        "Keywords": keywords,
        "Agent Decision": decision,
        "Suggested Closing Line": closing
    }
    return feedback

# ----------------------------
# Gradio UI
# ----------------------------

iface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(type="filepath", label="Upload Candidate Audio"),
    outputs="json",
    title="Voice AI Agent for Candidate Screening",
    description="Upload candidate audio answer. The agent will transcribe, analyze sentiment, extract keywords, and provide a decision."
)

# ------------ Local testing code ------------
if __name__ == "__main__":
    # For manual testing, comment out Gradio launch and use this instead
    audio_path = "sample.mp3" 
    result = process_audio(audio_path)
    print("-------- Agent Feedback --------")
    for k, v in result.items():
        print(f"{k}: {v}")
    
    # Then launch Gradio (optional for UI demo)
    iface.launch()