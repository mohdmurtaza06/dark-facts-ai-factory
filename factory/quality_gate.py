"""Fail-closed validation for finished vertical Shorts.

This validates technical integrity only. It does not claim to assess story quality,
visual originality, character consistency, or copyright clearance.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


def probe_video(path: str | Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,width,height,codec_name",
            "-of", "json", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def validate_video(path: str | Path, min_duration: float = 15.0,
                   max_duration: float = 20.0) -> list[str]:
    file_path = Path(path)
    errors: list[str] = []
    if not file_path.is_file():
        return [f"File does not exist: {file_path}"]
    if file_path.stat().st_size < 100_000:
        errors.append("File is unexpectedly small (<100 KB).")
    try:
        data = probe_video(file_path)
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError) as exc:
        return errors + [f"ffprobe failed: {exc}"]

    try:
        duration = float(data["format"]["duration"])
    except (KeyError, TypeError, ValueError):
        duration = 0.0
    if not min_duration <= duration <= max_duration:
        errors.append(f"Duration {duration:.2f}s outside {min_duration:.0f}–{max_duration:.0f}s.")

    streams = data.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    if not videos:
        errors.append("Missing video stream.")
    else:
        video = videos[0]
        width, height = video.get("width"), video.get("height")
        if (width, height) != (1080, 1920):
            errors.append(f"Expected 1080x1920, got {width}x{height}.")
        if video.get("codec_name") != "h264":
            errors.append(f"Expected H.264 video, got {video.get('codec_name')}.")
    if not audios:
        errors.append("Missing audio stream.")
    elif audios[0].get("codec_name") not in {"aac", "mp3"}:
        errors.append(f"Unsupported audio codec: {audios[0].get('codec_name')}.")

    return errors


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Fail-closed Short MP4 quality gate")
    parser.add_argument("videos", nargs="+")
    args = parser.parse_args()
    failed = False
    for video in args.videos:
        errors = validate_video(video)
        if errors:
            failed = True
            print(f"FAIL: {video}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS: {video}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
