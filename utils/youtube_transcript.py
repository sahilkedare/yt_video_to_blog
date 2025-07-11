from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import logging

def get_video_id(url):
    parsed_url= urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path.lstrip('/')
    return None

def get_transcript(state):
    logging.info("[Transcript] Fetching transcript started.")
    video_url = state.get("video_url")
    if not video_url or not isinstance(video_url, str):
        logging.error("[Transcript] Invalid or missing video_url.")
        return {"transcript": None, "error": "Invalid or missing video_url."}
    video_id = get_video_id(video_url)
    if not video_id:
        logging.error("[Transcript] Invalid YouTube URL.")
        return {"transcript": None, "error": "Invalid YouTube URL."}
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for entry in transcript:
            entry['text'] = entry['text'].replace('\n', ' ')
        logging.info("[Transcript] Fetching transcript done.")
        return {"transcript": transcript}
    except Exception as e:
        logging.error(f"[Transcript] Error fetching transcript: {e}")
        return {"transcript": None, "error": str(e)}

