from pathlib import Path
import subprocess,concurrent.futures,json,hashlib
from PIL import Image,ImageDraw
import numpy as np
r=Path('/tmp/gse08-visual');(r/'dense').mkdir(exist_ok=True)
centers=[54,244,334,922,1098,1156,1218,1256,1272,2020,2086,2112,2148,2162,2276,2310,2340,2430,2872,2944,3698,3778,4168,4230,4274,4494,4674,4932,5004,5032,5078,5196,5284,5818]
media='/Users/yjzhao/Downloads/GSE-08-BV11LWw6VEHW.mp4'
def run(t):
 p=r/'dense'/f'around-{t:04}';p.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-ss',str(t-2),'-i',media,'-t','4','-vf','fps=2','-q:v','3',str(p/'frame-%02d.jpg')],check=True)
 return [{'id':f'd{t:04}-{i:02}','time':t-2+(i-1)*.5,'path':str(f.relative_to(r)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for i,f in enumerate(sorted(p.glob('*.jpg')),1)]
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(run,centers):rows+=result
# all dense frames retained and contact reviewed, not auto discarded
for s in range(0,len(rows),24):
 subset=rows[s:s+24];o=Image.new('RGB',(1460,1380),'#e7e8eb');d=ImageDraw.Draw(o)
 for j,c in enumerate(subset):
  im=Image.open(r/c['path']).crop((550,0,1280,410)).resize((365,205));x=j%4*365;y=j//4*230;o.paste(im,(x,y+25));d.text((x+2,y+2),f"{c['id']} t={c['time']}",fill='black')
 o.save(r/'contacts'/f'dense-{s//24+1:02}.jpg',quality=90)
json.dump({'method':'selected demo transitions, 4-second windows at 2fps (0.5 sec); decoder fps filter relative sampling approximate within one frame','centers':centers,'candidates':rows,'status':'unreviewed'},open(r/'dense-inventory.json','w'),ensure_ascii=False,indent=2)
print(len(rows))
