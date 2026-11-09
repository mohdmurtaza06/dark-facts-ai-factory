import math, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

W, H, FPS, DURATION = 720, 1280, 12, 20
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/Library/Fonts/Arial Bold.ttf"
]

def font(size):
    for p in FONT_CANDIDATES:
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def frame_image(package, frame, total_frames):
    t = frame / max(1, total_frames-1)
    scene = min(4, int(t*5))
    # Render the gradient at quarter resolution, then upscale to keep daily
    # five-video batches practical on free GitHub-hosted runners.
    bg = Image.new("RGB", (180, 320), (3, 7, 18))
    bp = bg.load()
    for y in range(320):
        for x in range(180):
            glow = max(0, 1-math.sqrt(((x-90)/225)**2+((y-144)/200)**2))
            wave = (math.sin(x*.072+frame*.12)+1)*2
            bp[x,y] = (int(3+glow*4), int(7+glow*18+wave), int(18+glow*48+wave*2))
    im = bg.resize((W, H), Image.Resampling.BILINEAR)
    d=ImageDraw.Draw(im,"RGBA")
    random.seed(41)
    for i in range(65):
        x=(random.randint(0,W)+frame*(i%3+1)*.7)%W
        y=(random.randint(0,H)+frame*(i%4+1)*.5)%H
        rr=1+(i%3)
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(70,180,255,100))
    cx,cy=W//2,int(H*.42)
    for k in range(9):
        pts=[]
        phase=frame*.075+k*.7
        for j in range(24):
            u=j/23
            x=cx+math.sin(phase+u*4+k)*(45+u*230)+(k-4)*8
            y=cy+(u-.5)*560+math.cos(phase+u*3)*35
            pts.append((x,y))
        d.line(pts,fill=(4,18,42,255),width=25)
        d.line(pts,fill=(12,75,125,220),width=4)
        for j in range(3,22,4):
            x,y=pts[j]
            d.ellipse((x-4,y-4,x+4,y+4),fill=(80,190,255,180))
    pulse=.65+.35*math.sin(frame*.3)
    d.ellipse((cx-115,cy-175,cx+115,cy+55),outline=(35,150,220,190),width=5)
    d.ellipse((cx-72,cy-132,cx+72,cy+12),fill=(5,18,42,245),outline=(65,190,255,230),width=5)
    d.ellipse((cx-25,cy-85,cx+25,cy-35),fill=(255,45,70,int(150+100*pulse)))
    if scene==2:
        for k in range(3):
            x=cx+(k-1)*125
            d.ellipse((x-36,cy+190,x+36,cy+262),outline=(255,55,75,240),width=8)
    headlines=["LOOK CLOSER...","THIS IS REAL.",package["topic"].upper()+" IS STRANGER.","HERE'S THE TWIST.","NATURE IS INSANE."]
    headline=headlines[scene]
    f=font(43); bb=d.textbbox((0,0),headline,font=f)
    d.rounded_rectangle((30,95,W-30,190),radius=20,fill=(0,0,0,150),outline=(40,130,190,130),width=2)
    d.text(((W-(bb[2]-bb[0]))/2,117),headline,font=f,fill=(245,249,255,255),stroke_width=2,stroke_fill=(0,0,0,220))
    lines=["The world is full of hidden surprises.",package["hook"],package["short_fact"],"One detail changes everything.","Follow for more impossible facts."][scene]
    sf=font(27); wrapped=wrap(d,lines,sf,W-90)[:3]; y=H-300
    d.rounded_rectangle((34,y-25,W-34,H-110),radius=24,fill=(0,0,0,175),outline=(45,110,155,120),width=2)
    for line in wrapped:
        bb=d.textbbox((0,0),line,font=sf)
        d.text(((W-(bb[2]-bb[0]))/2,y),line,font=sf,fill=(238,244,255,255),stroke_width=1,stroke_fill=(0,0,0,255))
        y+=48
    d.rounded_rectangle((35,H-65,W-35,H-53),radius=6,fill=(70,90,110,120))
    d.rounded_rectangle((35,H-65,35+int((W-70)*t),H-53),radius=6,fill=(45,180,255,255))
    return im

def render_video(package,audio_path,output_path,workdir):
    workdir=Path(workdir); workdir.mkdir(parents=True,exist_ok=True)
    frames=workdir/"frames"; frames.mkdir(exist_ok=True)
    for i in range(FPS*DURATION):
        frame_image(package,i,FPS*DURATION).save(frames/f"f{i:04d}.jpg",quality=88)
    ffmpeg=shutil.which("ffmpeg")
    if not ffmpeg: raise RuntimeError("FFmpeg not found.")
    silent=workdir/"silent.mp4"
    subprocess.run([ffmpeg,"-y","-framerate",str(FPS),"-i",str(frames/"f%04d.jpg"),
      "-vf","fps=24,scale=1080:1920:flags=lanczos,format=yuv420p","-c:v","libx264",
      "-preset","ultrafast","-crf","25","-t",str(DURATION),str(silent)],
      check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run([ffmpeg,"-y","-i",str(silent),"-i",str(audio_path),"-map","0:v:0","-map","1:a:0",
      "-c:v","copy","-c:a","aac","-b:a","128k","-af","apad,atrim=0:20","-shortest",
      "-movflags","+faststart",str(output_path)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return Path(output_path)
