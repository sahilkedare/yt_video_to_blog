import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.blog_generator_agent import generate_blog_from_summary
from agents.summarizer_agent import summarize_transcript
from utils.youtube_transcript import get_transcript

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def seo_optimize_blog(state):
    logging.info("[SEO] SEO optimization started.")
    blog_text = state.get("blog")
    if not blog_text or not isinstance(blog_text, str):
        logging.error("[SEO] Invalid or missing blog content.")
        return {"optimized_blog": None, "error": "Invalid or missing blog content."}
    prompt = f"""
    You are an SEO expert. Optimize the following blog post for search engines.
    
    Goals:
    - Improve title with relevant keywords
    - Add a meta description (under 160 characters)
    - Add relevant tags/keywords
    - Format content with short paragraphs and bullet points
    - Make headings more SEO friendly

    Blog content:
    {blog_text}

    Please return:
    - Optimized Title
    - Meta Description
    - Keyword Tags
    - Optimized Blog Content
    """
    try:
        response = model.generate_content(prompt)
        output = response.text
        logging.info("[SEO] SEO optimization done.")
        return {"optimized_blog": output}
    except Exception as e:
        logging.error(f"[SEO] Error optimizing blog: {e}")
        return {"optimized_blog": None, "error": str(e)}
