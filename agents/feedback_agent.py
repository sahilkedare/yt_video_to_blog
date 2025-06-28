import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def revise_blog_with_feedback(state):
    logging.info("[Feedback] Blog revision with feedback started.")
    blog_content = state.get("blog")
    feedback = state.get("feedback")
    if not blog_content or not isinstance(blog_content, str):
        logging.error("[Feedback] Invalid or missing blog content.")
        return {"blog": None, "error": "Invalid or missing blog content."}
    if feedback is None or not isinstance(feedback, str):
        logging.error("[Feedback] Invalid or missing feedback.")
        return {"blog": None, "error": "Invalid or missing feedback."}
    prompt = f"""
    You are an expert blog writer. Revise the following blog post based on the user feedback.
    Blog post:
    {blog_content}
    User feedback:
    {feedback}
    Revised blog post:
    """
    try:
        response = model.generate_content(prompt)
        logging.info("[Feedback] Blog revision with feedback done.")
        return {"blog": response.text}
    except Exception as e:
        logging.error(f"[Feedback] Error revising blog: {e}")
        return {"blog": None, "error": str(e)}
