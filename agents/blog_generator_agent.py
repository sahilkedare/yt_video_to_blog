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
from agents.summarizer_agent import summarize_transcript

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_blog_from_summary(state):
    logging.info("[BlogGen] Blog generation started.")
    summary = state.get("summary")
    tone = state.get("tone","Formal")
    if not summary or not isinstance(summary, str):
        logging.error("[BlogGen] Invalid or missing summary.")
        return {"blog": None, "error": "Invalid or missing summary."}
    prompt = f"""
    Write a detailed and engaging blog post based on the following summary. 
    The blog should include an introduction, key points in well-structured sections, and a conclusion. 
    Use a {tone.lower()} tone. Add examples if appropriate.

    Summary:
    {summary}
    """
    try:
        response = model.generate_content(prompt)
        logging.info("[BlogGen] Blog generation done.")
        return {"blog": response.text}
    except Exception as e:
        logging.error(f"[BlogGen] Error generating blog: {e}")
        return {"blog": None, "error": str(e)}

