from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

ROOT=Path(__file__).resolve().parent
W,H,L,R,T,B=1600,960,32,16,32,32
QUADS={
 '20261107_232016.jpg':[[561,570],[3588,629],[3577,2452],[529,2443]],
 '20261107_232039.jpg':[[667,471],[3634,511],[3618,2298],[649,2281]],
 '20261107_232137.jpg':[[496,447],[3796,579],[3717,2577],[412,2439]],
 '20261107_232147.jpg':[[390,333],[3936,467],[3893,2557],[305,2496]],
}
PAIRS=[('Oblivion Remastered screenshot','20261107_232016.jpg','20261107_232137.jpg'),('Artwork inspired by Oblivion','20261107_232039.jpg','20261107_232147.jpg')]
for d in ['aligned','normalized','comparison']: (ROOT/d).mkdir(exist_ok=True)
arrays={}; geometry=[]
for name,quad in QUADS.items():
 src=cv2.imread(str(ROOT/'originals'/name)); assert src is not None
 quad=np.array(quad,np.float32)
 dst=np.array([[L,T],[L+W-1,T],[L+W-1,T+H-1],[L,T+H-1]],np.float32)
 matrix=cv2.getPerspectiveTransform(quad,dst)
 size=(L+W+R,T+H+B)
 valid=cv2.warpPerspective(np.full(src.shape[:2],255,np.uint8),matrix,size,flags=cv2.INTER_NEAREST)
 assert np.all(valid==255),(name,int(np.count_nonzero(valid==0)))
 aligned=cv2.warpPerspective(src,matrix,size,flags=cv2.INTER_CUBIC)
 arrays[name]=cv2.cvtColor(aligned,cv2.COLOR_BGR2RGB)
 Image.fromarray(arrays[name]).save(ROOT/'aligned'/name,quality=96,subsampling=0)
 geometry.append({'source':name,'screen_quad_xy':quad.tolist(),'homography':matrix.tolist(),'size':size,'bezel_margin_lrtb':[L,R,T,B],'missing_source_pixels':0})
# One shared affine RGB mapping for the entire set, never fitted separately to OFF/ON.
# The common dark reference comes only from the photographed bezel; the common light
# reference is a robust high percentile of all four screen regions. No spatial edits.
bezel=[];screens=[]
for a in arrays.values():
 bezel.extend([a[4:20,80:-80].reshape(-1,3),a[-20:-4,80:-80].reshape(-1,3)])
 screens.append(a[T+20:T+H-20,L+20:L+W-20].reshape(-1,3)[::8])
black=np.percentile(np.concatenate(bezel),20,axis=0)
white=np.percentile(np.concatenate(screens),99.5,axis=0)
assert np.all(white-black>35),(black,white)
normalized={}; clipped={}
for name,a in arrays.items():
 f=(a.astype(np.float32)-black)/(white-black)*230+12
 normalized[name]=np.clip(np.rint(f),0,255).astype(np.uint8)
 screen=f[T:T+H,L:L+W]
 clipped[name]={'channels_below_0_fraction':float(np.mean(screen<0)),'channels_above_255_fraction':float(np.mean(screen>255))}
 Image.fromarray(normalized[name]).save(ROOT/'normalized'/name,quality=96,subsampling=0)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
bold=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',42)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25)
IW,IH=L+W+R,T+H+B
for mode,images in [('aligned',arrays),('normalized',normalized)]:
 sheet=Image.new('RGB',(2*IW+72,2*(IH+95)+190),(248,248,245));draw=ImageDraw.Draw(sheet)
 draw.text((24,72),'Calibration OFF',font=bold,fill=(25,25,25));draw.text((IW+48,72),'Calibration ON',font=bold,fill=(25,25,25))
 draw.text((24,12),'Legendary Ayleid ruins near the Imperial City, Cyrodiil',font=bold,fill=(25,25,25))
 for row,(label,off,on) in enumerate(PAIRS):
  y=138+row*(IH+95)
  for col,name in enumerate([off,on]):
   x=24+col*(IW+24)
   draw.text((x,y),label+' | '+name[9:11]+':'+name[11:13]+':'+name[13:15],font=font,fill=(40,40,40))
   sheet.paste(Image.fromarray(images[name]),(x,y+45))
 footer='Shared RGB normalization across all four photos; no per-image tone matching.' if mode=='normalized' else 'Geometry alignment only. Original photographed colors and tonal differences retained.'
 draw.text((24,sheet.height-38),footer,font=small,fill=(65,65,65))
 sheet.save(ROOT/'comparison'/f'calibration-off-on-{mode}-ayleid.jpg',quality=95,subsampling=0)
 for row,(label,off,on) in enumerate(PAIRS,1):
  pair=Image.new('RGB',(2*IW+48,IH+76),(248,248,245));d=ImageDraw.Draw(pair)
  for col,(state,name) in enumerate([('Calibration OFF',off),('Calibration ON',on)]):
   x=16+col*(IW+16);d.text((x,12),state+' — '+label,font=font,fill=(25,25,25));pair.paste(Image.fromarray(images[name]),(x,56))
  pair.save(ROOT/'comparison'/f'scene-{row}-{mode}-ayleid.jpg',quality=95,subsampling=0)
(ROOT/'geometry.json').write_text(json.dumps(geometry,indent=2))
method={'normalization':'one identical global affine RGB map for all four images','black_rgb':black.tolist(),'white_rgb':white.tolist(),'output_black':12,'output_white':242,'per_image_histogram_matching':False,'local_tone_edits':False,'gamma_change':False,'inpainting_or_generation':False,'clipping':clipped,'pairs':[{'scene':s,'off':o,'on':n} for s,o,n in PAIRS],'owner_confirmed_order':True,'conditions':{'frontlight_brightness_percent':100,'frontlight_warmth_percent':100,'external_light':'ring lamp'},'camera_note':'EXIF exposure-bias tags differ (+0.3, +1.0, 0.0, -0.3 EV); shutter and ISO tags all show approximately 1/350 s and ISO 200. These photographs are illustrative, not a controlled metrology run.'}
(ROOT/'processing.json').write_text(json.dumps(method,indent=2))
manifest=json.loads((ROOT/'manifest.json').read_text())
for entry in manifest:assert hashlib.sha256(Path(entry['local_path']).read_bytes()).hexdigest()==entry['sha256']
print('Four perspective-aligned bezel crops; four normalized copies; two full comparison sheets and four paired sheets.')
print('Shared black/white RGB:',black.tolist(),white.tolist())
print('All original hashes preserved; no missing-source pixels in any crop.')
