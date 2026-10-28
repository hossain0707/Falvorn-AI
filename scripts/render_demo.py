"""Create an original 42s Falvorn product walkthrough from verified local UI captures.

Inputs are real Falvorn HTML rendered in headless Chromium and a locally verified
HTTP extraction. The video distinguishes illustrative planner events from verified
API output. No claims of live autonomous website navigation.
"""
from pathlib import Path
import math, os, wave, subprocess
import numpy as np
import cv2
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
WORK=Path(os.environ.get('FALVORN_DEMO_WORK_DIR', str(ROOT/'.build/demo-work')))
WORK.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'assets/demo'
OUT.mkdir(parents=True,exist_ok=True)
FPS=20
W,H=1280,720
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={s:ImageFont.truetype(BOLD,s) for s in [17,20,24,26,30,35,44,65]}

for src,name in [('brand-banner.svg','brand'),('architecture.svg','architecture')]:
    cairosvg.svg2png(url=str(ROOT/'assets'/src),write_to=str(WORK/(name+'.png')),output_width=1280)

# Scene frames are screenshots of Falvorn's actual UI, except for original intro/architecture graphics.
scenes=[
 ('brand.png','FALVORN AI','Intelligence without limits',5),
 ('dashboard.png','YOUR CONTROL CENTER','Falvorn Agent · Browser · API · Core',6),
 ('goal.png','GOAL-DRIVEN WORKFLOWS','Enter a destination and describe an outcome',6),
 ('execution.png','TRANSPARENT EXECUTION','Illustrative trace • real events require a configured LLM',6),
 ('extraction.png','VERIFIED LOCAL EXTRACTION','Actual API output from a synthetic offline webpage',6),
 ('architecture.png','MODULAR ENGINEERING','Independent modules, durable SQLite history, clear trust boundaries',6),
 ('verification.png','BUILT FOR VALIDATION','14 passing local tests · independent security review still pending',6),
]

# Default screenshots are 1440x900, containing functional dashboard, but with truncated lower UI.
def fit_image(path):
    img=Image.open(WORK/path).convert('RGB')
    ratio=max(W/img.width,H/img.height)
    rw,rh=int(img.width*ratio),int(img.height*ratio)
    img=img.resize((rw,rh),Image.Resampling.LANCZOS)
    x=(rw-W)//2;y=(rh-H)//2
    return img.crop((x,y,x+W,y+H))

imgs=[fit_image(s[0]) for s in scenes]
video_temp=str(WORK/'falvorn-silent.mp4')
writer=cv2.VideoWriter(video_temp,cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
if not writer.isOpened():raise RuntimeError('VideoWriter unavailable')
for idx,(name,heading,subtitle,secs) in enumerate(scenes):
    base=imgs[idx]
    count=secs*FPS
    for frame in range(count):
        t=frame/max(1,count-1)
        # Subtle cinematic move; avoid unnecessary UI zooms.
        scale=1.005+0.018*t
        rw,rh=int(W*scale),int(H*scale)
        zoom=base.resize((rw,rh),Image.Resampling.BILINEAR)
        x=int((rw-W)*(0.35+0.3*t)); y=int((rh-H)*(0.5-0.12*t))
        canvas=zoom.crop((x,y,x+W,y+H)).convert('RGBA')
        shade=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(shade)
        # Legible independent title treatments + status clarity.
        d.rectangle((0,0,W,114),fill=(6,12,28,216))
        d.rectangle((0,H-88,W,H),fill=(5,11,27,223))
        d.rounded_rectangle((32,20,155,51),radius=10,fill=(44,87,112,228))
        d.text((47,25),'FALVORN AI',font=fonts[17],fill=(218,248,252,255))
        d.text((180,19),heading,font=fonts[30],fill=(247,249,255,255))
        d.text((35,H-68),subtitle,font=fonts[20],fill=(226,239,249,255))
        d.text((W-340,H-64),'LOCAL PRODUCT WALKTHROUGH',font=fonts[17],fill=(143,193,213,255))
        d.rectangle((0,H-5,int(W*(idx+t)/len(scenes)),H),fill=(104,221,237,255))
        # brief dissolve between adjacent clips, so no hard abrupt cuts
        if idx>0 and frame<8:
            fade=1-frame/8
            prior=np.asarray(imgs[idx-1].resize((W,H),Image.Resampling.BILINEAR),dtype=np.float32)
            now=np.asarray(canvas.convert('RGB'),dtype=np.float32)
            canvas=Image.fromarray(np.clip(fade*prior+(1-fade)*now,0,255).astype('uint8'))
        else:
            canvas=Image.alpha_composite(canvas,shade).convert('RGB')
        # handle the fade overlay separately
        if idx>0 and frame<8:canvas=Image.alpha_composite(canvas.convert('RGBA'),shade).convert('RGB')
        writer.write(cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGB2BGR))
writer.release()

# Original, low-volume ambient technology motif, synthesized from scratch.
sec=sum(s[3] for s in scenes)
sr=24000
n=int(sec*sr)
t=np.arange(n,dtype=np.float64)/sr
a=np.zeros(n,dtype=np.float64)
notes=[130.8128,164.8138,196.0,261.6256]
for i,f in enumerate(notes):
    a+=0.045*np.sin(2*np.pi*f*t+i*0.75)*(0.68+0.32*np.sin(2*np.pi*0.045*t+i))
a+=0.012*np.sin(2*np.pi*523.25*t)*(np.sin(2*np.pi*0.24*t)**8)
fade=np.minimum(1,np.minimum(t/1.4,(sec-t)/1.8)).clip(0,1)
a=(a*fade*0.7).clip(-1,1)
with wave.open(str(WORK/'original-ambient.wav'),'wb') as f:
    f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr)
    f.writeframes((a*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',video_temp,'-i',str(WORK/'original-ambient.wav'),'-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(OUT/'falvorn-walkthrough.mp4')],check=True)
# Readme-safe short 7s GIF, scaled for lightweight GitHub autoplay.
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss','6','-t','7','-i',str(OUT/'falvorn-walkthrough.mp4'),'-vf','fps=8,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=bayer','-loop','0',str(OUT/'falvorn-preview.gif')],check=True)
print('Created',OUT/'falvorn-walkthrough.mp4',(OUT/'falvorn-walkthrough.mp4').stat().st_size)
print('Created',OUT/'falvorn-preview.gif',(OUT/'falvorn-preview.gif').stat().st_size)
