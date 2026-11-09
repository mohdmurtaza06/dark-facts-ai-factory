# DARK FACTS AI FACTORY

A free-first, GitHub Actions-based YouTube Shorts production pipeline.

## V1 scope
- Pick non-repeating topics from a reviewed fact library.
- Build short English narration and metadata from templates.
- Render original dark anime-inspired motion graphics (not full generative anime footage).
- Generate narration with Edge TTS.
- Render vertical MP4 using Pillow + FFmpeg.
- Upload with the official YouTube Data API v3 when OAuth secrets are configured.
- Keep output manifests and video artifacts.

## Important limitations
This MVP is template-based, not an autonomous web researcher or LLM scriptwriter. The visual renderer creates motion graphics, not full AI-generated scenes. Five unique topics per day requires expanding the reviewed fact library. Free-tier limits, TTS availability and YouTube quota can prevent a guaranteed five uploads each day.

## Setup
1. Add GitHub Actions secrets: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
2. Enable YouTube Data API v3 in a Google Cloud project and create an OAuth Desktop client.
3. Use `scripts/get_youtube_token.py` locally to obtain a refresh token. Never commit credentials.
4. Check YouTube OAuth consent-screen publishing status. External apps left in Testing can issue refresh tokens that expire after seven days.
5. Start with `YT_PRIVACY_STATUS=unlisted` and test before switching to public.

## Local run
```bash
pip install -r requirements.txt
python -m factory.run --count 1 --output output
```

Upload locally:
```bash
python -m factory.run --count 1 --output output --upload
```

## GitHub Actions
The workflow runs at 09:00 India time daily and supports manual dispatch. The scheduled workflow will fail at the upload step until all three YouTube secrets are added. Configure the consent screen and YouTube API quota before enabling public automation.

## Project layout
- `factory/content.py`: topic selection and metadata
- `factory/voice.py`: narration generation
- `factory/render.py`: anime-inspired motion graphics + FFmpeg
- `factory/youtube.py`: YouTube uploader
- `factory/run.py`: orchestration
- `data/facts.json`: fact library and source links
- `.github/workflows/daily-shorts.yml`: schedule
