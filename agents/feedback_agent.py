import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def revise_blog_with_feedback(state):
    if "feedback" not in state or not state["feedback"]:
        # No feedback provided, return the blog unchanged
        return {"blog": state.get("blog", "")}
    blog_content = state["blog"]
    feedback = state["feedback"]
    prompt = f"""
    You are an expert blog writer. Revise the following blog post based on the user feedback.
    Blog post:
    {blog_content}
    User feedback:
    {feedback}
    Revised blog post:
    """
    response = model.generate_content(prompt)
    return {"blog": response.text}
