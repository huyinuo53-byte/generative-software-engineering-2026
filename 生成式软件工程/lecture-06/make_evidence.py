from PIL import Image,ImageDraw
from pathlib import Path
import json
p=Path(__file__).parent;notes=json.loads((p/'notes.json').read_text());ims=[f['path'] for s in notes['sections'] for f in s['frames']]
(p/'sources/selected-images.json').write_text(json.dumps(ims))
for i in range(0,len(ims),3):
 out=Image.new('RGB',(1200,3*1000),'#aaa');d=ImageDraw.Draw(out)
 for j,path in enumerate(ims[i:i+3]):
  img=Image.open(p/path).convert('RGB');img.thumbnail((1200,960));out.paste(img,(0,j*1000+30));d.text((10,j*1000+5),path,fill='black')
 out.save(p/'sources'/f'audit-sheet-{i//3+1:02d}.jpg')
slides=[Image.open(p/'frames'/f'page-{i:03d}.png').convert('RGB') for i in range(1,48)]
slides[0].save(p/'sources/source-slides.pdf',save_all=True,append_images=slides[1:],resolution=144)
