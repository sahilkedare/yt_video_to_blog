import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.youtube_transcript import get_transcript

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def summarize_transcript(state):
    """Summarizes the transcript using Google Gemini."""
    logging.info("[Summarizer] Summarization started.")
    transcript = state.get("transcript")
    if not transcript or not isinstance(transcript, list):
        logging.error("[Summarizer] Invalid or missing transcript.")
        return {"summary": None, "error": "Invalid or missing transcript."}
    full_text = " ".join([entry['text'] for entry in transcript])
    truncated_text = full_text[:10000]  # Truncate to 10,000 characters
    prompt = f"Summarize the following YouTube video transcript in concise bullet points:\n\n{truncated_text}"
    try:
        response = model.generate_content(prompt)
        logging.info("[Summarizer] Summarization done.")
        return {"summary": response.text}
    except Exception as e:
        logging.error(f"[Summarizer] Error summarizing transcript: {e}")
        return {"summary": None, "error": str(e)}






