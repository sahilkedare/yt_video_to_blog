import streamlit as st
import sys
import os
import re

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

st.markdown('<div class="main-title">YouTube to Beautiful Blog Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste a YouTube video URL below and get a fully generated, SEO-optimized blog post!</div>', unsafe_allow_html=True)

# --- URL Input and Blog Generation ---
url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
generate = st.button("Generate Blog")

if generate and url:
    with st.spinner("Generating blog post. This may take a moment..."):
        result = graph.invoke({"video_url": url, "feedback": ""})
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
    st.markdown('<div class="blog-content">' + st.session_state['blog_content'] + '</div>', unsafe_allow_html=True)

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
st.markdown("<div style='text-align:center; color:#6A5ACD;'>Built with ❤️ using Streamlit and Gemini</div>", unsafe_allow_html=True)
