import re

# Retrive video id from URL
def get_yt_video_id(url: str) -> str:
    
    # Pattern of URL
    video_url_pattern = r"^https://youtu.be/([a-zA-Z0-9_-]{11})"

    # Check if url is matched with the pattern
    video_match = re.match(video_url_pattern, url)
    if video_match:
        return video_match.group(1)

    return None