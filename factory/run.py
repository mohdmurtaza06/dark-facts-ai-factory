import argparse, json, subprocess, time
from pathlib import Path
from .content import choose_facts, build_package
from .voice import generate_voice
from .render import render_video
from .youtube import upload_video

def validate_video(path):
    probe=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",str(path)],text=True)
    data=json.loads(probe); duration=float(data["format"]["duration"])
    video=next(s for s in data["streams"] if s.get("codec_type")=="video")
    if not 19<=duration<=21: raise RuntimeError(f"Unexpected duration: {duration}")
    if video.get("width")!=1080 or video.get("height")!=1920: raise RuntimeError("Expected 1080x1920 video")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--count",type=int,default=5)
    ap.add_argument("--output",default="output")
    ap.add_argument("--upload",action="store_true")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for index,fact in enumerate(choose_facts(args.count),1):
        pkg=build_package(fact)
        slug=f"{time.strftime('%Y%m%d')}_{index}_{fact['id']}"
        work=out/"work"/slug; work.mkdir(parents=True,exist_ok=True)
        audio=work/"voice.mp3"; video=out/f"{slug}.mp4"
        print(f"[{index}/{args.count}] Producing {fact['id']}")
        generate_voice(pkg["script"],audio)
        render_video(pkg,audio,video,work)
        validate_video(video)
        item={**pkg,"video":str(video),"uploaded_id":None}
        if args.upload:
            item["uploaded_id"]=upload_video(video,pkg)
            print("Uploaded:",item["uploaded_id"])
        manifest.append(item)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(f"Finished {len(manifest)} Shorts.")

if __name__=="__main__": main()
