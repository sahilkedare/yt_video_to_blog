from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed_url= urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path.lstrip('/')
    return None

def get_transcript(state):
    video_url = state["video_url"]
    video_id = get_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
        return

    try: 
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for entry in transcript:
            entry['text'] = entry['text'].replace('\n', ' ')
        return {"transcript": transcript}
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return {"transcript": None}

