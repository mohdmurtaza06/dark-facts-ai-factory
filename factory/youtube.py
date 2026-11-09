import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_path, package):
    required = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError("Missing YouTube secrets: " + ", ".join(missing))
    creds = Credentials(
        token=None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"], scopes=SCOPES)
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": package["title"][:100],
            "description": (package["description"] + "\n\n" + package["hashtags"])[:5000],
            "tags": ["Shorts", "Dark Facts", "Science Facts", "Mind Blowing Facts"],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": os.getenv("YT_PRIVACY_STATUS", "unlisted"),
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True, chunksize=8*1024*1024)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        _, response = request.next_chunk()
    return response.get("id")
