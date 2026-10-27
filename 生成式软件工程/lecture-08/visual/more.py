from PIL import Image,ImageDraw
from pathlib import Path
import json
root=Path('/tmp/gse08-visual');a=json.load(open(root/'visual-inventory.json'));cs=a['candidates']
def sheets(rows,prefix,full=False):
 w,h=(512,164) if full else (365,205);cols=3 if full else 4; per=21 if full else 20
 for s in range(0,len(rows),per):
  subset=rows[s:s+per];out=Image.new('RGB',(w*cols,(h+25)*((len(subset)+cols-1)//cols)), '#e7e8eb');d=ImageDraw.Draw(out)
  for j,c in enumerate(subset):
   im=Image.open(root/c['path']);im=im if full else im.crop((550,0,1280,410));im=im.resize((w,h));x=j%cols*w;y=j//cols*(h+25);out.paste(im,(x,y+25));d.text((x+3,y+3),f"{c['id']} t={c['time']} ->{c.get('automated_duplicate_of') or '-'}",fill='black')
  out.save(root/'contacts'/f'{prefix}-{s//per+1:02}.jpg',quality=90)
sheets([c for c in cs if c['automated_duplicate_of']], 'duplicates',True)
sheets([{'id':f'full-{t}','time':t,'path':f'scan/sample-{int(t//2)+1:05}.jpg'} for t in range(0,5829,60)],'full-overview',True)
print('dups',sum(bool(c['automated_duplicate_of']) for c in cs))
