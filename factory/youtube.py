"""YouTube upload with SHA-256 dedup and safe retries."""
from __future__ import annotations
import hashlib, json, logging, os, time
from pathlib import Path
logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
UPLOADED_DB = ROOT / "data" / "uploaded_videos.json"
MAX_UPLOAD_RETRIES, BASE_BACKOFF = 3, 2.0
PERMANENT = {400, 401, 403, 404}

def _load():
    if UPLOADED_DB.exists():
        try:
            return json.loads(UPLOADED_DB.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def _save(db):
    UPLOADED_DB.parent.mkdir(parents=True, exist_ok=True)
    tmp = UPLOADED_DB.with_suffix(".tmp")
    tmp.write_text(json.dumps(db, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(UPLOADED_DB)

def content_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def already_uploaded(video_path: Path, fact_id=None):
    db = _load()
    d = content_hash(video_path)
    if db.get(d, {}).get("youtube_id"):
        return db[d]["youtube_id"]
    if fact_id:
        for rec in db.values():
            if rec.get("fact_id") == fact_id and rec.get("youtube_id"):
                return rec["youtube_id"]
    return None

def record_upload(video_path, youtube_id, fact_id=None, title=None):
    db = _load()
    d = content_hash(video_path)
    db[d] = {
        "youtube_id": youtube_id, "fact_id": fact_id, "title": title,
        "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sha256": d, "size": Path(video_path).stat().st_size,
    }
    _save(db)

def upload_video(video_path, package) -> str:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request

    video_path = Path(video_path)
    fact_id = package.get("fact_id")
    existing = already_uploaded(video_path, fact_id=fact_id)
    if existing:
        return existing
    miss = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.getenv(k)]
    if miss:
        raise RuntimeError("Missing secrets: " + ", ".join(miss))
    creds = Credentials(
        token=None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    creds.refresh(Request())
    yt = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": package["title"][:100],
            "description": (package.get("description", "") + "\n\n" + package.get("hashtags", ""))[:5000],
            "tags": ["Shorts", "Dark Facts"], "categoryId": "27",
        },
        "status": {
            "privacyStatus": os.getenv("YT_PRIVACY_STATUS", "unlisted"),
            "selfDeclaredMadeForKids": False,
        },
    }
    last = None
    for attempt in range(1, MAX_UPLOAD_RETRIES + 1):
        try:
            media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True, chunksize=8 << 20)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
            vid = resp.get("id")
            if not vid:
                raise RuntimeError("no id")
            record_upload(video_path, vid, fact_id=fact_id, title=package.get("title"))
            return vid
        except Exception as e:
            last = e
            time.sleep(BASE_BACKOFF * (2 ** (attempt - 1)))
    raise RuntimeError(f"Upload failed: {last}") from last
