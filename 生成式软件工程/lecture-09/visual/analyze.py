from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,datetime
p=Path('/tmp/gse09-visual');files=sorted((p/'scan').glob('sample-*.jpg'));scans=[];candidates=[];reps=[];prev=None;prevb=None
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14)
for n,f in enumerate(files):
 im=Image.open(f);a=np.array(im.crop((550,0,1280,410)).convert('L').resize((183,103)),dtype=np.int16);b=np.array(im.crop((0,75,548,340)).convert('L').resize((137,66)),dtype=np.int16)
 de=np.abs(a-prev) if prev is not None else np.full_like(a,255);bd=np.abs(b-prevb) if prevb is not None else np.full_like(b,255)
 score=float(de.mean());frac=float((de>15).mean());bs=float(bd.mean());reason=[]
 if n%15==0:reason.append('30s_fallback')
 if score>1.5 and frac>.012:reason.append('screen_change')
 if bs>7.0:reason.append('board_change_or_occlusion')
 row={'sample_index':n+1,'time':n*2.0,'time_basis':'2s fps-filter navigation sample; selected final frames re-extracted exact seek','path':str(f.relative_to(p)),'screen_mean_delta':round(score,4),'screen_changed_fraction':round(frac,4),'board_mean_delta':round(bs,4),'triggers':reason}
 if reason:
  cid=f'v{len(candidates)+1:04d}';row['candidate_id']=cid;dup=None
  for rr in reversed(reps):
   delta=np.abs(a-rr['a'])
   if float(delta.mean())<.55 and float((delta>15).mean())<.008 and not ('board_change_or_occlusion' in reason):dup=rr['id'];break
  c={'id':cid,'time':n*2.,'path':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'trigger':reason,'automated_duplicate_of':dup,'manual_status':'pending'};candidates.append(c)
  if not dup:reps.append({'id':cid,'a':a,'time':n*2.,'path':f})
 scans.append(row);prev=a;prevb=b
(p/'scan-mapping.json').write_text(json.dumps(scans,indent=2))
for batch in range((len(reps)+19)//20):
 chunk=reps[batch*20:(batch+1)*20];sheet=Image.new('RGB',(1460,1150),'#e5e7eb');d=ImageDraw.Draw(sheet)
 for j,rr in enumerate(chunk):
  x=j%4*365;y=j//4*230;im=Image.open(rr['path']).crop((550,0,1280,410)).resize((365,205));sheet.paste(im,(x,y+25));t=int(rr['time']);d.text((x+3,y+3),f"{rr['id']} {t//60:02d}:{t%60:02d} t={t}",font=font,fill='black')
 sheet.save(p/'contacts'/f'contact-{batch+1:02d}.jpg',quality=92)
# Full frame 30s fallback overview includes chalkboard.
fallback=[c for c in candidates if '30s_fallback' in c['trigger']]
for batch in range((len(fallback)+11)//12):
 chunk=fallback[batch*12:(batch+1)*12];o=Image.new('RGB',(1920,695),'#e5e7eb');d=ImageDraw.Draw(o)
 for j,c in enumerate(chunk):
  x=j%3*640;y=j//3*173;im=Image.open(p/c['path']).resize((640,205));o2=im.resize((480,154));# four rows fit; keep full aspect
  o.paste(o2,(x,y+19));d.text((x+4,y+3),f"{c['id']} t={c['time']}",font=font,fill='black')
 o.save(p/'contacts'/f'full-{batch+1:02d}.jpg',quality=92)
media=Path('/Users/yjzhao/Downloads/DeepSeek Harness (1) [09-Raw 26生成式软件工程 NJU].mp4');h=hashlib.sha256()
with media.open('rb') as mf:
 for z in iter(lambda:mf.read(4194304),b''):h.update(z)
meta={'schema_version':1,'video_id':'BV144nc6KEA4','media':{'path':str(media),'sha256':h.hexdigest(),'duration_seconds':5363.541375,'video_duration_seconds':5363.533,'audio_duration_seconds':5363.541333,'tail_decode':'passed'},'method':{'navigation_sample':'fps=1/2; source timing approximately within 1 sec. final selected frames exact -ss re-extraction','screen_crop':[550,0,1280,410],'full_frame':[1280,410],'change':'right screen grayscale183x103 mean>1.5 and fraction delta>15 >.012','fallback_seconds':30,'board_auxiliary':'left board [0,75,548,340] mean delta>7, may include occlusion','dedup':'same right screen mean<.55 and changed fraction<.008; automated suggestion not semantic equivalence'},'scan':{'path':'scan-mapping.json','sha256':hashlib.sha256((p/'scan-mapping.json').read_bytes()).hexdigest(),'sample_count':len(scans)},'candidate_count':len(candidates),'unique_count':len(reps),'candidates':candidates,'status':'unreviewed'}
(p/'visual-inventory.json').write_text(json.dumps(meta,indent=2));print('samples/candidates/representatives',len(scans),len(candidates),len(reps))
