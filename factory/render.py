"""Cinematic 3D render orchestrator."""
from __future__ import annotations
import json, logging, os, shutil, subprocess
from pathlib import Path
from .story import build_storyboard, storyboard_summary
logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
BLENDER_SCRIPT = ROOT / "factory" / "blender" / "scene_builder.py"
DEFAULT_FPS, RENDER_W, RENDER_H, OUTPUT_W, OUTPUT_H = 12, 480, 854, 1080, 1920

def _find_blender() -> str:
    for c in (os.environ.get("BLENDER_PATH"), "/tmp/blender-4.2.5-linux-x64/blender",
              r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
              "/usr/bin/blender", shutil.which("blender")):
        if c and Path(c).exists():
            return str(c)
    raise RuntimeError("Blender not found. Set BLENDER_PATH.")

def render_blender_frames(storyboard, workdir: Path) -> Path:
    frames_dir = workdir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    story_path = workdir / "storyboard.json"
    story_path.write_text(json.dumps(storyboard, indent=2), encoding="utf-8")
    cmd = [_find_blender(), "--background", "--factory-startup", "-P", str(BLENDER_SCRIPT), "--",
           "--storyboard", str(story_path), "--out", str(frames_dir),
           "--fps", str(DEFAULT_FPS), "--width", str(RENDER_W), "--height", str(RENDER_H)]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "2"
    logger.info("Blender render starting…")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1200)
    if r.returncode != 0:
        logger.error("Blender stderr:\n%s", (r.stderr or "")[-4000:])
        raise RuntimeError(f"Blender failed code={r.returncode}")
    pngs = sorted(frames_dir.glob("f*.png"))
    if not pngs:
        raise RuntimeError(f"No frames in {frames_dir}")
    logger.info("Produced %d frames", len(pngs))
    return frames_dir

def assemble_video(frames_dir, audio_path, output_path, workdir) -> Path:
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    pngs = sorted(frames_dir.glob("f*.png"))
    start = int(pngs[0].stem.replace("f", ""))
    silent = workdir / "silent.mp4"
    subprocess.run([
        ffmpeg, "-y", "-framerate", str(DEFAULT_FPS), "-start_number", str(start),
        "-i", str(frames_dir / "f%04d.png"),
        "-vf", f"scale={OUTPUT_W}:{OUTPUT_H}:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(silent),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    amb = workdir / "ambience.wav"
    subprocess.run([
        ffmpeg, "-y", "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=20:sample_rate=44100",
        "-af", "volume=0.08,lowpass=f=800", str(amb),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        ffmpeg, "-y", "-i", str(silent), "-i", str(audio_path), "-i", str(amb),
        "-filter_complex",
        "[1:a]volume=1.0,apad,atrim=0:20[narr];[2:a]volume=0.35,apad,atrim=0:20[amb];"
        "[narr][amb]amix=inputs=2:duration=first:dropout_transition=0[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
        str(output_path),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def generate_contact_sheet(frames_dir, workdir) -> Path:
    try:
        from PIL import Image
    except ImportError:
        return workdir / "contact_sheet_missing.txt"
    sm_path = frames_dir / "scene_map.json"
    picks = []
    if sm_path.exists():
        sm = json.loads(sm_path.read_text())
        picks = [(s["frame_start"] + s["frame_end"]) // 2 for s in sm.get("scenes", [])]
    thumbs = []
    for fi in picks:
        path = frames_dir / f"f{fi:04d}.png"
        if path.exists():
            im = Image.open(path).convert("RGB")
            im.thumbnail((270, 480))
            thumbs.append(im)
    if not thumbs:
        p = workdir / "contact_sheet.txt"
        p.write_text("no frames\n")
        return p
    cols = min(3, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    w, h = thumbs[0].size
    sheet = Image.new("RGB", (cols * w, rows * h), (8, 12, 20))
    for i, im in enumerate(thumbs):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    out = workdir / "contact_sheet.jpg"
    sheet.save(out, quality=88)
    return out

def quality_check(video_path, storyboard) -> dict:
    report = {"passed": True, "checks": {}, "errors": []}
    def fail(n, m):
        report["passed"] = False
        report["checks"][n] = False
        report["errors"].append(m)
    def ok(n):
        report["checks"][n] = True
    vp = Path(video_path)
    if not vp.exists():
        fail("exists", "missing")
        return report
    ok("exists")
    if vp.stat().st_size < 50000:
        fail("size", f"small {vp.stat().st_size}")
    else:
        ok("size")
    try:
        probe = subprocess.check_output([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration:stream=codec_type,width,height",
            "-of", "json", str(vp),
        ], text=True, timeout=30)
        data = json.loads(probe)
        dur = float(data["format"]["duration"])
        vs = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
        aus = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
        if not vs:
            fail("video_stream", "no video")
        else:
            ok("video_stream")
            if vs[0].get("width") != OUTPUT_W or vs[0].get("height") != OUTPUT_H:
                fail("resolution", f"{vs[0].get('width')}x{vs[0].get('height')}")
            else:
                ok("resolution")
        if not aus:
            fail("audio_stream", "no audio")
        else:
            ok("audio_stream")
        if not 18 <= dur <= 22.5:
            fail("duration", f"{dur:.2f}s")
        else:
            ok("duration")
        sc = len(storyboard.get("scenes", []))
        if sc < 6:
            fail("scene_count", f"only {sc}")
        else:
            ok("scene_count")
        report["duration"] = dur
        report["size"] = vp.stat().st_size
        report["scene_count"] = sc
    except Exception as e:
        fail("probe", str(e))
    return report

def render_video(package_or_sb, audio_path, output_path, workdir) -> Path:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    if "scenes" in package_or_sb:
        sb = package_or_sb
    else:
        fact = {
            "id": package_or_sb.get("fact_id", "unknown"),
            "topic": package_or_sb.get("topic", ""),
            "hook": package_or_sb.get("hook", ""),
            "fact": package_or_sb.get("script", ""),
            "short_fact": package_or_sb.get("short_fact", ""),
            "source": package_or_sb.get("source", ""),
        }
        sb = build_storyboard(fact)
    logger.info("\n%s", storyboard_summary(sb))
    (workdir / "storyboard.json").write_text(json.dumps(sb, indent=2), encoding="utf-8")
    frames = render_blender_frames(sb, workdir)
    assemble_video(frames, Path(audio_path), Path(output_path), workdir)
    contact = generate_contact_sheet(frames, workdir)
    if contact.exists() and contact.suffix == ".jpg":
        shutil.copy(contact, Path(output_path).parent / "contact_sheet.jpg")
    qc = quality_check(Path(output_path), sb)
    (workdir / "qc_report.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    shutil.copy(workdir / "qc_report.json", Path(output_path).parent / "qc_report.json")
    shutil.copy(workdir / "storyboard.json", Path(output_path).parent / "storyboard.json")
    if not qc["passed"]:
        raise RuntimeError(f"QC failed: {qc['errors']}")
    return Path(output_path)
