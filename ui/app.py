import streamlit as st
import sys
import os

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.langgraph_workflow import graph

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
        font-size: 2.5rem;
        font-weight: bold;
        color: #483d8b;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6A5ACD;
        margin-bottom: 2em;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    .blog-content h2, .blog-content h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .blog-content strong {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #483d8b;
    }
    .blog-content pre, .blog-content code {
        font-family: 'Fira Mono', monospace;
        font-size: 1em;
    }
    .blog-content {
        background: var(--secondary-background-color, #f0f2f6);
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
        background-color: #483d8b;
        color: white;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.5em 2em;
        margin-top: 1em;
        box-shadow: 0 2px 8px 0 rgba(70,130,180,0.08);
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #6A5ACD;
    }
    .stSpinner > div > div {
        color: #483d8b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">YouTube to Beautiful Blog Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste a YouTube video URL below and get a fully generated, SEO-optimized blog post!</div>', unsafe_allow_html=True)

with st.form("yt_blog_form"):
    url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    submit = st.form_submit_button("Generate Blog")

if submit and url:
    with st.spinner("Generating blog post. This may take a moment..."):
        # Run the workflow graph
        result = graph.invoke({"video_url": url})
        blog = result.get("optimized_blog") or result.get("blog")
        if isinstance(blog, dict) and "raw_output" in blog:
            blog = blog["raw_output"]
    if blog:
        # Clean up and style the blog content
        import re
        # Remove field labels and bold markers
        blog_clean = re.sub(r"\*\*.*?\*\*:?", "", blog)
        blog_clean = blog_clean.replace("**", "")
        # Remove extra newlines
        blog_clean = re.sub(r"\n{3,}", "\n\n", blog_clean)
        # Style code blocks
        def style_code_blocks(text):
            return re.sub(r'```(\w+)?(.*?)```',
                lambda m: f'<pre style="background:#e3f0fa;padding:1em;border-radius:0.5em;overflow-x:auto;"><code>{m.group(2).strip()}</code></pre>',
                text, flags=re.DOTALL)
        blog_clean = style_code_blocks(blog_clean)
        # Convert headings and lists to HTML
        blog_clean = re.sub(r"^# (.*)$", r'<h2 style="color:#483d8b;">\1</h2>', blog_clean, flags=re.MULTILINE)
        blog_clean = re.sub(r"^## (.*)$", r'<h3 style="color:#6A5ACD;">\1</h3>', blog_clean, flags=re.MULTILINE)
        blog_clean = re.sub(r"^\* (.*)$", r'<li>\1</li>', blog_clean, flags=re.MULTILINE)
        blog_clean = re.sub(r"(<li>.*?</li>)", r'<ul>\1</ul>', blog_clean, flags=re.DOTALL)
        # Replace newlines with <br> for paragraphs
        blog_clean = blog_clean.replace("\n", "<br>")
        st.markdown('<div class="blog-content">' + blog_clean + '</div>', unsafe_allow_html=True)
    else:
        st.error("Failed to generate blog content. Please check the URL or try again later.")

st.markdown("<hr style='margin:2em 0;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#6A5ACD;'>Built with ❤️ using Streamlit and Gemini</div>", unsafe_allow_html=True)
