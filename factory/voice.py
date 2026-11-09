"""Robust TTS with Edge retries and gTTS fallback."""
from __future__ import annotations
import asyncio, logging, random, subprocess, time
from pathlib import Path
logger = logging.getLogger(__name__)
EDGE_VOICE, EDGE_RATE, EDGE_VOLUME = "en-US-AndrewNeural", "+8%", "+0%"
MAX_EDGE_RETRIES, BASE_BACKOFF, MAX_BACKOFF = 3, 1.5, 12.0
MIN_AUDIO_DURATION, MAX_AUDIO_DURATION = 8.0, 35.0

class TTSError(RuntimeError):
    pass

def _cleanup(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except OSError as e:
        logger.warning("cleanup %s: %s", path, e)

def _probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True, timeout=15).strip()
    return float(out)

def _validate(path: Path) -> float:
    if not path.exists():
        raise TTSError(f"missing: {path}")
    if path.stat().st_size < 1024:
        raise TTSError("too small")
    d = _probe_duration(path)
    if d < MIN_AUDIO_DURATION:
        raise TTSError(f"too short {d:.2f}s")
    if d > MAX_AUDIO_DURATION:
        raise TTSError(f"too long {d:.2f}s")
    return d

async def _edge_save(text, path):
    import edge_tts
    c = edge_tts.Communicate(
        text, EDGE_VOICE, rate=EDGE_RATE, volume=EDGE_VOLUME,
        connect_timeout=30, receive_timeout=60)
    await c.save(str(path))

def _generate_edge(text, path: Path) -> float:
    last = None
    for attempt in range(1, MAX_EDGE_RETRIES + 1):
        _cleanup(path)
        try:
            logger.info("Edge TTS %d/%d", attempt, MAX_EDGE_RETRIES)
            asyncio.run(_edge_save(text, path))
            return _validate(path)
        except Exception as e:
            last = e
            logger.warning("Edge TTS fail %d: %s", attempt, e)
            _cleanup(path)
            if attempt < MAX_EDGE_RETRIES:
                time.sleep(random.uniform(0, min(MAX_BACKOFF, BASE_BACKOFF * (2 ** (attempt - 1)))))
    raise TTSError(f"Edge TTS failed: {last}") from last

def _generate_gtts(text, path: Path) -> float:
    try:
        from gtts import gTTS
    except ImportError as e:
        raise TTSError("gTTS not installed") from e
    _cleanup(path)
    try:
        gTTS(text=text, lang="en", slow=False).save(str(path))
        return _validate(path)
    except Exception as e:
        _cleanup(path)
        raise TTSError(f"gTTS failed: {e}") from e

def generate_voice(text, output_path) -> dict:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not text or not text.strip():
        raise TTSError("Empty text")
    edge_err = None
    try:
        d = _generate_edge(text, output_path)
        return {"path": output_path, "provider": "edge-tts", "duration": d}
    except TTSError as e:
        edge_err = e
        logger.warning("Edge exhausted, trying gTTS: %s", e)
    try:
        d = _generate_gtts(text, output_path)
        return {"path": output_path, "provider": "gtts", "duration": d}
    except TTSError as g:
        raise TTSError(f"All TTS failed. Edge: {edge_err}; gTTS: {g}") from g
