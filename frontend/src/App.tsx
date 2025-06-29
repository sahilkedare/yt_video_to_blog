import React, { useState } from 'react';
import './App.css';

const API_BASE = 'http://localhost:8000/api';

const toneOptions = [
  'Formal', 'Casual', 'Humorous', 'Persuasive', 'Critical', 'Technical '
];

function App() {
  const [url, setUrl] = useState('');
  const [tone, setTone] = useState(toneOptions[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [blog, setBlog] = useState('');
  const [seo, setSeo] = useState<{title?: string, description?: string, keywords?: string}>({});
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [feedback, setFeedback] = useState('');
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setBlog('');
    setSeo({});
    setImageUrl(null);
    try {
      const res = await fetch(`${API_BASE}/generate_blog`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_url: url, tone })
      });
      if (!res.ok) throw new Error('Failed to generate blog');
      const data = await res.json();
      setBlog(data.blog_content);
      setSeo({
        title: data.seo_title,
        description: data.seo_description,
        keywords: data.seo_keywords
      });
      setImageUrl(data.image_url || null);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async () => {
    if (!blog || !feedback) return;
    setFeedbackLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/revise_blog`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blog, feedback })
      });
      if (!res.ok) throw new Error('Failed to revise blog');
      const data = await res.json();
      setBlog(data.blog);
      setFeedback('');
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setFeedbackLoading(false);
    }
  };

  // Function to extract title and content from blog
  const parseBlogContent = (blogContent: string) => {
    // Remove any leading ** or whitespace
    const cleanContent = blogContent.replace(/^\*\*\s*\n*/, '').trim();
    
    // Split by lines and find the first # heading
    const lines = cleanContent.split('\n');
    let titleIndex = -1;
    let title = '';
    
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith('# ')) {
        titleIndex = i;
        title = lines[i].replace('# ', '').trim();
        break;
      }
    }
    
    if (titleIndex !== -1) {
      // Remove the title line and join the rest
      const contentLines = [...lines];
      contentLines.splice(titleIndex, 1);
      const content = contentLines.join('\n').trim();
      return { title, content };
    }
    
    // If no # heading found, return the whole content as content
    return { title: '', content: cleanContent };
  };

  const { title: blogTitle, content: blogContent } = blog ? parseBlogContent(blog) : { title: '', content: '' };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1 className="title">🎬 YouTube to Blog</h1>
          <p className="subtitle">
            Transform any YouTube video into SEO-optimized blog content instantly
          </p>
        </div>

        {/* Main Form */}
        <form onSubmit={handleGenerate} className="form-card">
          <div className="form-group">
            <label className="form-label">
              📹 YouTube Video URL
            </label>
            <input
              type="url"
              value={url}
              onChange={e => setUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              ✨ Blog Tone
            </label>
            <select
              value={tone}
              onChange={e => setTone(e.target.value)}
              className="form-select"
            >
              {toneOptions.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          <button
            type="submit"
            className={`btn-primary ${loading ? 'loading' : ''}`}
            disabled={loading}
          >
            {loading ? '🔄 Generating Amazing Content...' : '🚀 Generate Blog'}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {/* Blog Content */}
        {blog && (
          <div className="blog-card">
            {imageUrl && (
              <div className="blog-image-container">
                <img 
                  src={imageUrl} 
                  alt="Blog visual" 
                  className="blog-image"
                />
              </div>
            )}
            
            {/* Blog Title */}
            {blogTitle && (
              <h1 className="blog-title">
                {blogTitle}
              </h1>
            )}
            
            {/* Blog Content */}
            <div className="blog-content">
              {blogContent}
            </div>

            {/* SEO Metadata */}
            {(seo.title || seo.description || seo.keywords) && (
              <div className="seo-card">
                <h3 className="seo-title">🎯 SEO Metadata</h3>
                {seo.title && (
                  <div className="seo-item">
                    <strong>Title:</strong> 
                    <span>{seo.title}</span>
                  </div>
                )}
                {seo.description && (
                  <div className="seo-item">
                    <strong>Meta Description:</strong> 
                    <span>{seo.description}</span>
                  </div>
                )}
                {seo.keywords && (
                  <div className="seo-item">
                    <strong>Keywords:</strong> 
                    <span>{seo.keywords}</span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
{/* Feedback Section */}
{blog && (
          <div className="feedback-card">
            <label className="form-label">
              💭 Suggest improvements
            </label>
            <p className="feedback-description">
              Tell us how to make it better: "add more examples", "make it shorter", "more technical details"
            </p>
            <input
              type="text"
              value={feedback}
              onChange={e => setFeedback(e.target.value)}
              placeholder="Your feedback..."
              className="form-input"
            />
            <button
              onClick={handleFeedback}
              className={`btn-secondary ${(feedbackLoading || !feedback) ? 'disabled' : ''}`}
              disabled={feedbackLoading || !feedback}
            >
              {feedbackLoading ? '🔄 Regenerating...' : '✨ Improve Content'}
            </button>
          </div>
        )}

        {/* Footer */}
        <div className="footer">
          <p className="footer-main">
            Built with ❤️ by <strong>Sahil</strong>
          </p>
          <p className="footer-sub">
            Powered by React • FastAPI • LangGraph • Gemini AI
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
