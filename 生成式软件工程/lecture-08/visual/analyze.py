from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,datetime,shutil
p=Path('/tmp/gse08-visual');files=sorted((p/'scan').glob('sample-*.jpg')); scans=[];candidates=[];representatives=[];prev=None;prevboard=None
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',15)
for n,f in enumerate(files):
 im=Image.open(f);a=np.array(im.crop((550,0,1280,410)).convert('L').resize((183,103)),dtype=np.int16);board=np.array(im.crop((0,70,548,255)).convert('L').resize((137,46)),dtype=np.int16)
 delta=np.abs(a-prev) if prev is not None else np.full_like(a,255);bd=np.abs(board-prevboard) if prevboard is not None else np.full_like(board,255)
 score=float(delta.mean());frac=float((delta>15).mean());bs=float(bd.mean());reason=[]
 if n%15==0:reason.append('30s_fallback')
 if score>1.5 and frac>.012:reason.append('screen_change')
 if bs>7.0:reason.append('board_change_or_occlusion')
 row={'sample_index':n+1,'source_frame_index':n*60,'time':n*2.0,'path':str(f.relative_to(p)),'screen_mean_delta':round(score,4),'screen_changed_pixel_fraction':round(frac,4),'board_mean_delta':round(bs,4),'selected_reasons':reason}
 if reason:
  k=len(candidates)+1;cid=f'v{k:04d}';row['candidate_id']=cid;duplicate=None
  for r in reversed(representatives):
   diff=np.abs(a-r['a'])
   if float(diff.mean())<.55 and float((diff>15).mean())<.008:
    duplicate=r['id'];break
  c={'id':cid,'time':n*2.0,'path':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'trigger':reason,'automated_duplicate_of':duplicate,'manual_status':'pending','screen_mean_delta':round(score,4)}
  candidates.append(c)
  if not duplicate:representatives.append({'id':cid,'a':a,'time':n*2.0,'path':f})
 scans.append(row);prev=a;prevboard=board
(p/'scan-mapping.json').write_text(json.dumps(scans,indent=2));
for batch in range((len(representatives)+19)//20):
 chunk=representatives[batch*20:(batch+1)*20];sheet=Image.new('RGB',(1460,1150),'#e5e7eb');d=ImageDraw.Draw(sheet)
 for j,r in enumerate(chunk):
  x=(j%4)*365;y=(j//4)*230;im=Image.open(r['path']).crop((550,0,1280,410)).resize((365,205));sheet.paste(im,(x,y+25));t=int(r['time']);d.text((x+4,y+4),f"{r['id']} {t//60:02d}:{t%60:02d} (t={t})",font=font,fill='black')
 sheet.save(p/'contacts'/f'contact-{batch+1:02d}.jpg',quality=92)
media=Path('/Users/yjzhao/Downloads/GSE-08-BV11LWw6VEHW.mp4');h=hashlib.sha256()
with media.open('rb') as f:
 for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
d={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'video_id':'BV11LWw6VEHW','media':{'path':str(media),'sha256':h.hexdigest(),'duration_seconds':5829.674667,'video_duration_seconds':5829.666625,'audio_duration_seconds':5829.674667,'integrity_note':'stream durations rechecked locally; tail30s decode passed as reported by parent'},'method':{'sample':'every60th source frame at30fps (2s); last regular sample5828s','screen_crop':[550,0,1280,410],'full_frame':[1280,410],'change':'right screen grayscale183x103; mean abs delta>1.5 and fraction pixels delta>15 >.012','fallback_seconds':30,'board_auxiliary':'left board region [0,70,548,255], mean delta>7; may include lecturer occlusion','dedup':'against previous retained right screen images: mean abs delta<.55 and changed fraction>15 <.008; automated proposals only','limitations':['Sub-2s visual events may be missed; suspected demos require denser local review','Contact sheets show screen crop for navigation; originals retain full frame','Automated similarity does not establish semantic equivalence']},'scan':{'path':'scan-mapping.json','sha256':hashlib.sha256((p/'scan-mapping.json').read_bytes()).hexdigest(),'sample_count':len(scans)},'candidate_count':len(candidates),'unique_count':len(representatives),'candidates':candidates,'status':'unreviewed'}
(p/'visual-inventory.json').write_text(json.dumps(d,indent=2));print(len(scans),len(candidates),len(representatives))
