import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

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
    blog_text = state["blog"]
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
    response = model.generate_content(prompt)
    output = response.text
    return {"optimized_blog": output}

if __name__ == "__main__":
    """Run the SEO optimizer pipeline from transcript to optimized blog."""
    transcript = get_transcript("https://www.youtube.com/watch?v=ar62HDh5yn4")
    summary = summarize_transcript(transcript)
    blog = generate_blog_from_summary(summary)
    optimized_content = seo_optimize_blog(blog)
    print(optimized_content)  # Print the raw output for debugging