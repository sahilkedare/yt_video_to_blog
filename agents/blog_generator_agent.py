import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

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
    summary = state["summary"]
    prompt = f"""
    Write a detailed and engaging blog post based on the following summary. 
    The blog should include an introduction, key points in well-structured sections, and a conclusion. 
    Use a friendly and informative tone. Add examples if appropriate.

    Summary:
    {summary}
    """
    response = model.generate_content(prompt)
    return {"blog": response.text}

