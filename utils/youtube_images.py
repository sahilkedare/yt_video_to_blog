# utils/youtube_images.py
import yt_dlp
import requests
from PIL import Image 
import logging

def extract_video_images(state):
    """Extract video metadata and thumbnail from YouTube URL"""
    logging.info("[YouTubeImages] Extracting video images started.")
    video_url = state.get("video_url")
    if not video_url:
        logging.error("[YouTubeImages] No video URL provided.")
        return {"thumbnail": None, "title": None, "duration": None}
    
    ydl_opts = {
        'writethumbnail': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            thumbnail_url = info.get('thumbnail')
            logging.info(f"[YouTubeImages] Thumbnail URL extracted: {thumbnail_url}")

        return {
            'thumbnail': thumbnail_url,
            'title': info.get('title'),
            'duration': info.get('duration')
        }
    except Exception as e:
        logging.error(f"[YouTubeImages] Error extracting video info: {e}")
        return {"thumbnail": None, "title": None, "duration": None}