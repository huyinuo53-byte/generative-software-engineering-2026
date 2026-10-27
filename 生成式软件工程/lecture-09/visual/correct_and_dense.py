from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json,hashlib,concurrent.futures
p=Path('/tmp/gse09-visual');rows=json.loads((p/'selected-frames.json').read_text());media='/Users/yjzhao/Downloads/DeepSeek Harness (1) [09-Raw 26生成式软件工程 NJU].mp4'
fixes={'v0019':360,'v0262':2908,'v0274':2934,'v0284':3024,'v0324':3421,'v0347':3524,'v0478':4443.5,'v0486':4478,'v0490':4501,'v0504':4540,'v0524':4652,'v0539':4701}
caps={'v0019':'DeepSeek Harness 的 Greeting 会话回答“你是谁”，并说明当前工作目录。','v0029':'miniagent.py 中的 RETRY_DELAY 配置、系统提示词与 bash 工具定义。','v0100':'办公Agent规格中 FR05 文档生成与修改、FR06 表格处理与计算等具体要求。','v0194':'MapReduce 原文 C++ 词频实现的 Mapper 与 Reducer 开头，按课堂浏览位置展示局部。','v0284':'Trajectory 展示含用户消息、上下文和 bash 调用的记录链；视图由日志记录生成。','v0347':'新会话模式菜单显示 Standard、Plan、Minimal 与 Creator 模式；菜单说明各模式用途。','v0421':'现场 Agent 汇报仪表盘替换结果，下方显示新增的累计 token 仪表盘；声明仍需实际验收。','v0457':'AI把绿色乌龟加入原有矩形，图中可见“乌龟”“龟壳”“头部”“尾巴”“鳍足”等标签。','v0462':'乌龟由多枚画布对象组成，可一起选中并继续编辑。','v0467':'右侧侧聊说明新画乌龟的结构和标签，画布与模型解释并排展示。','v0478':'对话中出现成语接龙卡片，给出第一轮多个可点击的成语选项。','v0486':'放大后的成语接龙卡片，完整选项与卡片底部操作提示可见。','v0490':'成语接龙选择后的红色反馈与状态变化。','v0524':'五子棋卡片初始棋盘，后续输入与模型响应围绕此状态交互。','v0539':'五子棋输入发给模型后，检查界面中的棋盘更新。','v0573':'现场解释的操作入口和事件映射局部，包含观察、取消、落盘和生命周期；不能把这一帧当完整表。','v0604':'现场 Agent 解释实现的边界，并指出先前棋盘截断来自事件构造/处理而非dynui核心。'}
for x in rows:
 if x['candidate_id'] in caps:x['caption_draft']=caps[x['candidate_id']]
 if x['candidate_id'] in fixes:
  old=x.copy();t=fixes[x['candidate_id']];out=p/'full'/f"{x['candidate_id']}-{str(t).replace('.','p')}.jpg"
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-ss',str(t),'-i',media,'-frames:v','1','-q:v','2',str(out)],check=True)
  x.update(time=t,path=str(out.relative_to(p)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),original_resolution_reviewed=False,correction={'original_time':old['time'],'original_path':old['path'],'reason':'exact native frame review found transition before desired state; moved to stable visible state'})
(p/'selected-frames.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(p/'dense').mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
centers=[2905,2933,3023,3419,3523,3708,4252,4443,4501,4537,4651,4694,4710]
times=[(c,round(c-2+j*.5,2)) for c in centers for j in range(9)]
def run(ct):
 c,t=ct;out=p/'dense'/f"d{c}-{str(t).replace('.','p')}.jpg";subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-ss',str(t),'-i',media,'-frames:v','1','-q:v','3',str(out)],check=True)
 return {'id':out.stem,'center':c,'time':t,'path':str(out.relative_to(p)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:dr=list(pool.map(run,times))
for b in range(0,len(dr),18):
 o=Image.new('RGB',(1460,1380),'#e7e8eb');d=ImageDraw.Draw(o)
 for j,x in enumerate(dr[b:b+18]):
  im=Image.open(p/x['path']).crop((550,0,1280,410)).resize((365,205));xx=j%4*365;yy=j//4*230;o.paste(im,(xx,yy+25));d.text((xx+2,yy+3),f"{x['id']} t={x['time']}",font=font,fill='black')
 o.save(p/'contacts'/f'dense-{b//18+1:02d}.jpg',quality=92)
(p/'dense-inventory.json').write_text(json.dumps({'method':'13 rapid transitions, ±2 seconds, exact individual seek every0.5sec; all original full frames retained','centers':centers,'candidates':dr,'status':'unreviewed'},ensure_ascii=False,indent=2)+'\n')
print('corrected',len(fixes),'dense',len(dr))
