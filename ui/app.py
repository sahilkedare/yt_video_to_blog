import streamlit as st
import sys
import os
import re
import logging

logging.basicConfig(level=logging.INFO)

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.langgraph_workflow import graph
from agents.feedback_agent import revise_blog_with_feedback

st.set_page_config(
    page_title="YouTube to Blog Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Fira+Mono&display=swap');
    body, .stApp {
        background-color: #f8fafd !important;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #483d8b;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        text-shadow: 1px 2px 8px #e6eaff;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #6A5ACD;
        margin-bottom: 2em;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        background: #e6eaff;
        border-radius: 0.7em;
        padding: 0.7em 1.5em;
        display: inline-block;
        box-shadow: 0 2px 12px 0 rgba(70,130,180,0.08);
    }
    .blog-content {
        background: #f0f2f6;
        border-radius: 1rem;
        padding: 2em 3em;
        box-shadow: 0 4px 24px 0 rgba(70,130,180,0.08);
        font-size: 1.1rem;
        color: #333;
        margin-top: 2em;
        margin-bottom: 2em;
        line-height: 1.7;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .stTextInput > div > input {
        border-radius: 0.5rem;
        border: 2px solid #483d8b;
        background: #e6eaff;
        color: #483d8b;
        font-size: 1.1rem;
        padding: 0.5em 1em;
    }
    .stButton > button {
        background-color: #6A5ACD;
        color: white;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.5em 2em;
        margin-top: 1em;
        box-shadow: 0 2px 8px 0 rgba(70,130,180,0.08);
        transition: background 0.2s;
    }

    .stSpinner > div > div {
        color: #483d8b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">YouTube to Beautiful Blog Generator</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;"><div class="subtitle">Paste a YouTube video URL below and get a fully generated, SEO-optimized blog post!</div></div>', unsafe_allow_html=True)
# --- URL Input and Blog Generation ---
tone = st.selectbox(
    "Select Blog Tone:",
    ["Formal", "Casual", "Humorous","Persuasive","Critical","Technical "],
    index=0,
    help="Choose the tone/style for your generated blog."
)
url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
generate = st.button("Generate Blog")

if generate and url:
    with st.spinner("Generating blog post. This may take a moment..."):
        result = graph.invoke({"video_url": url, "feedback": "", "tone": tone})
        # print(result)
        blog = result.get("optimized_blog") or result.get("blog")
        if isinstance(blog, dict) and "raw_output" in blog:
            blog = blog["raw_output"]
        # Extract only the main blog content after 'Optimized Blog Content:'
        blog_content = blog
        match = re.search(r"Optimized Blog Content:\s*([\s\S]*)", blog)
        if match:
            blog_content = match.group(1).strip()
        st.session_state['blog_content'] = blog_content
        st.session_state['feedback'] = ""

# --- Blog Display ---
if 'blog_content' in st.session_state and st.session_state['blog_content']:
    blog_content = st.session_state['blog_content']
    # Download button HTML (top right)
    download_button_html = f'''
    <div style="position: relative; max-width: 900px; margin-left: auto;  margin-right: auto;" >
        <div style="position: absolute; top: -2.5em; right: 0; margin-botton:10px; z-index: 10;">
            <form method="post">
                <button id="download-md" style="background:#6A5ACD;color:white;border:none;border-radius:0.5em;padding:0.5em 1.2em;font-weight:bold;cursor:pointer;box-shadow:0 2px 8px 0 rgba(70,130,180,0.08);font-size:1em;" onclick="window.open('data:text/markdown;charset=utf-8,' + encodeURIComponent(document.getElementById('blog-md-content').innerText))">Download as Markdown</button>
            </form>
        </div>
        <div id="blog-md-content" class="blog-content">{blog_content}</div>
    </div>
    '''
    st.markdown(download_button_html, unsafe_allow_html=True)

    # --- Feedback Loop ---
    feedback = st.text_input("Suggest a change to the blog (e.g., 'make it more humorous', 'add a summary', etc.)", key="feedback_input")
    regenerate = st.button("Regenerate with Feedback")
    if regenerate and feedback:
        with st.spinner("Updating blog with your feedback..."):
            result = revise_blog_with_feedback({"blog": st.session_state['blog_content'], "feedback": feedback})
            updated_blog = result.get("blog") if isinstance(result, dict) else result
            # Extract only the main blog content after 'Optimized Blog Content:'
            blog_content = updated_blog
            match = re.search(r"Optimized Blog Content:\s*([\s\S]*)", updated_blog)
            if match:
                blog_content = match.group(1).strip()
            st.session_state['blog_content'] = blog_content
            st.session_state['feedback'] = feedback
            st.rerun()

st.markdown("<hr style='margin:2em 0;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#6A5ACD;'>Built by Sahil ❤️ using Streamlit, langgraph and Gemini</div>", unsafe_allow_html=True)
