# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,json,struct,datetime,shutil
r=Path('/tmp/gse08-lab2-materials')
shutil.copyfile('/tmp/gse08-lab2.html',r/'lab2-source.html')
records=[]
for p,fig,note in [(5,4,'已目视复核四条交接箭头、停止条件、code review入口、图注均完整。'),(7,5,'已目视复核知识/性能证据/harness输入，1x基线、对数轴、所有四个条形数值、single kernel/48h/team-reported脚注及图注均完整。')]:
 f=r/f'key-page-{p:02}.png'; b=f.read_bytes(); w,h=struct.unpack('>II',b[16:24])
 records.append({'path':str(f),'sha256':hashlib.sha256(b).hexdigest(),'width':w,'height':h,'source_kind':'pdf_page','page':p,'figure':fig,'source_url':'https://arxiv.org/abs/2610.08900v2','scope':'full PDF page, no crop','visual_check':'passed','detail':note,'final_html_integration':'pending'})
(r/'image-audit-draft.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'material_id':'humanize-2610.08900v2','images':records},ensure_ascii=False,indent=2)+'\n')
