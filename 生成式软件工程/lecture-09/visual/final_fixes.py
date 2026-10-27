from pathlib import Path
import subprocess,json,hashlib
p=Path('/tmp/gse09-visual');rs=json.loads((p/'selected-frames.json').read_text());media='/Users/yjzhao/Downloads/DeepSeek Harness (1) [09-Raw 26生成式软件工程 NJU].mp4'
rs=[x for x in rs if x['candidate_id']!='v0478']
for x in rs:
 if x['candidate_id'] in ['v0262','v0524']:
  t={'v0262':2905.,'v0524':4658.}[x['candidate_id']];out=p/'full'/f"{x['candidate_id']}-{int(t)}-final.jpg"
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-ss',str(t),'-i',media,'-frames:v','1','-q:v','2',str(out)],check=True)
  x['correction']['reason']+='; dense0.5s review chose visible stable state'
  x.update(time=t,path=str(out.relative_to(p)),sha256=hashlib.sha256(out.read_bytes()).hexdigest())
 if x['candidate_id']=='v0347':x['caption_draft']='新会话模式菜单显示 Standard、PTC、Minimal 与 Creator 模式，说明各模式用途。'
 if x['candidate_id']=='v0539':x['caption_draft']='五子棋交互中的中间失败状态：棋盘只显示较少行且有“AI思考中”提示，不能把它当完成的对弈。'
(p/'selected-frames.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n')
print(len(rs))
