"""Generate original pilot narration and a procedural ambient bed.

Requires edge-tts and ffmpeg. No paid API is used. The narration voice is selected
by the caller; generated files are local build artifacts and are not committed.
"""
from __future__ import annotations

import argparse
import asyncio
import math
import random
import shutil
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_AUDIO = ROOT / "public" / "audio"


def make_ambience(path: Path, duration: float = 60.0, sample_rate: int = 24000) -> None:
    """Create a restrained, original low drone with sparse elevator-like pulses."""
    random.seed(23)
    frames = int(duration * sample_rate)
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sample_rate)
        chunk = bytearray()
        for i in range(frames):
            t = i / sample_rate
            fade_in = min(1.0, t / 2.5)
            fade_out = min(1.0, max(0.0, (duration - t) / 2.0))
            hum = 0.055 * math.sin(2 * math.pi * 54.0 * t)
            overtone = 0.022 * math.sin(2 * math.pi * 81.0 * t + 0.2 * math.sin(t * 0.17))
            pulse_phase = t % 7.5
            pulse_env = math.exp(-pulse_phase * 3.8) if pulse_phase < 0.8 else 0.0
            pulse = 0.07 * pulse_env * math.sin(2 * math.pi * (440 - 170 * pulse_phase) * t)
            sample = max(-0.8, min(0.8, (hum + overtone + pulse) * fade_in * fade_out))
            value = int(sample * 32767)
            chunk.extend(value.to_bytes(2, "little", signed=True))
            if len(chunk) >= 8192:
                out.writeframesraw(chunk)
                chunk.clear()
        if chunk:
            out.writeframesraw(chunk)


async def make_voice(text: str, output: Path, voice: str, rate: str) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise SystemExit("Install edge-tts first: python -m pip install edge-tts") from exc
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(str(output))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default="en-US-GuyNeural")
    parser.add_argument("--rate", default="-8%")
    args = parser.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required to encode the ambience bed")
    PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    text = (ROOT / "audio" / "pilot_narration.txt").read_text(encoding="utf-8").strip()
    voice_mp3 = PUBLIC_AUDIO / "pilot-voice.mp3"
    ambience_wav = PUBLIC_AUDIO / "pilot-ambience.wav"
    ambience_mp3 = PUBLIC_AUDIO / "pilot-ambience.mp3"
    asyncio.run(make_voice(text, voice_mp3, args.voice, args.rate))
    make_ambience(ambience_wav)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(ambience_wav), "-codec:a", "libmp3lame",
        "-b:a", "128k", str(ambience_mp3)
    ], check=True, capture_output=True)
    ambience_wav.unlink(missing_ok=True)
    print(f"Generated narration: {voice_mp3}")
    print(f"Generated original ambience: {ambience_mp3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
