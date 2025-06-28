# YouTube to Blog AI Agent

An AI application that takes a YouTube video URL and automatically generates a publish-ready SEO-optimized blog post using an agent-based workflow. Each step in the content pipeline is handled by a dedicated agent.

## Key Features

- **YouTube Transcript Extraction**: Uses YouTube API or youtube-transcript-api to get transcript.
- **Summarization Agent**: Summarizes the transcript into structured bullet points or sections.
- **Blog Generator Agent**: Converts the summary into a well-written blog post.
- **SEO Optimizer Agent**: Enhances the blog with SEO-friendly title, meta description, and keywords.
- **Frontend UI**: Streamlit interface to enter URL, trigger generation, and preview/export blog.

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app**
   ```bash
   streamlit run ui/app.py
   ```

## Directory Structure

- `agents/` - Contains agent implementations for each step.
- `ui/` - Streamlit frontend code.
- `utils/` - Utility functions (e.g., YouTube transcript extraction).

## Configuration
- Add your Gemini API key as an environment variable: `GOOGLE_API_KEY`.

## Usage
- Enter a YouTube video URL in the UI and click generate. The app will extract the transcript, summarize it, generate a blog post, and optimize it for SEO. 