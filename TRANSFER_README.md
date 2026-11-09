# DARK FACTS V2 — Windows Transfer Guide

This bundle reconstructs the **V2 cinematic Blender pipeline** on top of the existing factory at commit `55b174f`.

## Surviving episode artifacts (already rendered)

| File | Description |
|------|-------------|
| `output/final.mp4` | 1080×1920, 20.0s, H.264 + AAC |
| `output/20261109_1_octopus-hearts.mp4` | Same episode (dated name) |
| `output/contact_sheet.jpg` | 6-scene contact sheet |
| `output/storyboard.json` | Full storyboard |
| `output/qc_report.json` | QC passed |

Do **not** re-render unless you want a new version. The prototype video is included.

## Files added or replaced

### Added
- `factory/story.py`
- `factory/blender/__init__.py`
- `factory/blender/scene_builder.py`
- `.github/workflows/v2-prototype.yml`
- `tests/test_story.py`
- `output/final.mp4`, `contact_sheet.jpg`, `storyboard.json`, `qc_report.json`, `20261109_1_octopus-hearts.mp4`
- `TRANSFER_README.md`

### Replaced
- `factory/render.py` — Blender + FFmpeg orchestrator
- `factory/run.py` — `--fact-id`, `--no-upload`, isolation
- `factory/voice.py` — Edge retries + gTTS fallback
- `factory/youtube.py` — SHA-256 upload dedup
- `requirements.txt` — adds `gTTS`
- `.gitignore` — keeps V2 output artifacts trackable

### Unchanged
- `.github/workflows/daily-shorts.yml` (daily production)
- `factory/content.py`, `data/facts.json`
- No OAuth secrets or tokens are included

## Windows requirements

1. **Python 3.11+** — https://www.python.org/downloads/
2. **FFmpeg** — add to PATH (`winget install FFmpeg` or download from https://ffmpeg.org)
3. **Blender 4.2 LTS** — https://www.blender.org/download/lts/4-2/
4. Optional: set `BLENDER_PATH` to the full path of `blender.exe`

Example:
```powershell
$env:BLENDER_PATH = "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
```

## Install & test

```powershell
cd path\to\dark-facts-ai-factory
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Inspect the included episode:
```powershell
ffprobe output\final.mp4
# Open output\contact_sheet.jpg and output\qc_report.json
```

## Run one prototype Short (no YouTube upload)

```powershell
python -m factory.run --count 1 --fact-id octopus-hearts --output output --no-upload
```

This re-renders with Blender (several minutes). To only keep the pre-built episode, skip this step.

## Safe commit & push (from your Windows clone)

1. Extract this ZIP **over** your local clone of the repo (or merge files carefully).
2. Confirm you are on `main` and up to date:
   ```powershell
   git fetch origin
   git checkout main
   git pull origin main
   ```
3. Stage and commit:
   ```powershell
   git add -A
   git status
   git commit -m "V2: cinematic 3D octopus episode (Blender Workbench)"
   git push origin main
   ```
4. Do **not** force-push.
5. Do **not** enable public YouTube uploads until you have reviewed quality.
6. Prototype GHA workflow is **manual only** (`workflow_dispatch`).

## GitHub Actions prototype

After push: **Actions → Dark Facts V2 Prototype → Run workflow**.

It installs Blender, runs tests, renders one Short with `--no-upload`, and uploads artifacts.


## Safety changes in this transfer package

- The daily workflow is manual-trigger only. Its scheduled cron trigger has been removed.
- The daily workflow now generates exactly one `octopus-hearts` prototype with `--no-upload`.
- YouTube credential environment variables were removed from this workflow.
- The separate V2 prototype workflow remains manual-trigger only and uses `--no-upload`.
- Do not restore the schedule or enable uploads until the V2 renderer has been tested on GitHub Actions and the resulting video has been reviewed.
