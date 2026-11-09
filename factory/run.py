"""DARK FACTS V2 orchestrator — per-video isolation, single-fact testing."""
from __future__ import annotations
import argparse, json, logging, subprocess, time, traceback
from pathlib import Path
from .content import choose_facts, load_json, FACTS
from .story import build_storyboard, storyboard_summary
from .voice import generate_voice, TTSError
from .render import render_video
try:
    from .youtube import upload_video, already_uploaded
except ImportError:
    def upload_video(*a, **k):
        raise RuntimeError("youtube deps missing")
    def already_uploaded(*a, **k):
        return None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("factory.run")

def validate_video(path: Path) -> dict:
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"Bad video: {path}")
    probe = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=codec_type,width,height,codec_name",
        "-of", "json", str(path),
    ], text=True, timeout=30)
    data = json.loads(probe)
    dur = float(data["format"]["duration"])
    vs = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
    aus = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    if not vs:
        raise RuntimeError("No video stream")
    if not aus:
        raise RuntimeError("No audio stream")
    if not 18 <= dur <= 22.5:
        raise RuntimeError(f"Duration {dur}")
    if vs[0].get("width") != 1080 or vs[0].get("height") != 1920:
        raise RuntimeError(f"Res {vs[0].get('width')}x{vs[0].get('height')}")
    return {
        "duration": dur, "width": vs[0].get("width"), "height": vs[0].get("height"),
        "video_codec": vs[0].get("codec_name"), "audio_codec": aus[0].get("codec_name"),
    }

def produce_one(index, total, fact, out: Path, do_upload: bool) -> dict:
    sb = build_storyboard(fact)
    slug = f"{time.strftime('%Y%m%d')}_{index}_{fact['id']}"
    work = out / "work" / slug
    work.mkdir(parents=True, exist_ok=True)
    audio = work / "voice.mp3"
    video = out / f"{slug}.mp4"
    record = {
        "topic": sb.get("topic"), "fact_id": fact["id"], "title": sb.get("title"),
        "video": str(video), "duration": None, "rendering_status": "pending",
        "tts_provider": None, "upload_status": "skipped", "youtube_id": None,
        "failure_reason": None, "scene_count": len(sb["scenes"]),
    }
    logger.info("[%d/%d] %s\n%s", index, total, fact["id"], storyboard_summary(sb))
    try:
        tts = generate_voice(sb["script"], audio)
        record["tts_provider"] = tts["provider"]
        logger.info("TTS via %s (%.1fs)", tts["provider"], tts["duration"])
    except Exception as e:
        logger.warning("TTS failed (%s); placeholder audio", e)
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=220:duration=20",
            "-c:a", "libmp3lame", "-q:a", "5", str(audio),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        record["tts_provider"] = "placeholder"
        record["failure_reason"] = f"TTS unavailable: {e}"
    try:
        render_video(sb, audio, video, work)
        probe = validate_video(video)
        record["duration"] = probe["duration"]
        record["rendering_status"] = "success"
        logger.info("Rendered %s (%.2fs)", video.name, probe["duration"])
    except Exception as e:
        record["rendering_status"] = "failed"
        record["failure_reason"] = (record.get("failure_reason") or "") + f" Render: {type(e).__name__}: {e}"
        logger.exception("Render failed")
        return record
    if not do_upload:
        record["upload_status"] = "skipped"
        return record
    try:
        existing = already_uploaded(video, fact_id=fact["id"])
        if existing:
            record["youtube_id"] = existing
            record["upload_status"] = "already_uploaded"
            return record
        vid = upload_video(video, sb)
        record["youtube_id"] = vid
        record["upload_status"] = "success"
    except Exception as e:
        record["upload_status"] = "failed"
        record["failure_reason"] = (record.get("failure_reason") or "") + f" Upload: {e}"
    return record

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--output", default="output")
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--fact-id", default=None)
    args = ap.parse_args()
    do_upload = args.upload and not args.no_upload
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if args.fact_id:
        facts = [f for f in load_json(FACTS, []) if f["id"] == args.fact_id]
        if not facts:
            raise SystemExit(f"Fact not found: {args.fact_id}")
    else:
        facts = choose_facts(args.count)
    manifest = []
    for i, fact in enumerate(facts, 1):
        try:
            rec = produce_one(i, len(facts), fact, out, do_upload)
        except Exception as e:
            logger.exception("Catastrophic")
            rec = {
                "fact_id": fact.get("id"), "rendering_status": "failed",
                "failure_reason": f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
                "upload_status": "skipped", "youtube_id": None,
            }
        manifest.append(rec)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    report = {
        "total_attempted": len(facts),
        "successfully_generated": sum(1 for m in manifest if m.get("rendering_status") == "success"),
        "successfully_uploaded": sum(1 for m in manifest if m.get("upload_status") in ("success", "already_uploaded")),
        "failed": sum(1 for m in manifest if m.get("rendering_status") == "failed"),
        "engine": "blender_cinematic_v2",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (out / "daily_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Done: %s", report)
    if report["successfully_generated"] == 0:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
