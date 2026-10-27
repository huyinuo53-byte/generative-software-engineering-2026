# -*- coding: utf-8 -*-
import json,hashlib,datetime,subprocess
from pathlib import Path
from html.parser import HTMLParser
p=Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat();run='BV1kybV6DE47-20261002'
def h(x):
 a=hashlib.sha256()
 with open(x,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):a.update(b)
 return a.hexdigest()
def write(name,o):(p/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
n=json.loads((p/'notes.json').read_text());idx=json.loads((p/'chunks/index.json').read_text());mv=json.loads((p/'sources/media-validation.json').read_text());media=Path(mv['path']);pdfh=h(p/'sources/source-slides.pdf')
assert mv['sha256']=='fcede16cd375e2d371e5a4e67c64cf39c840754674677f4fb06cabdb23d91d6a'
assert mv['tail_decode']['exit_code']==0
obs={1:'开场标题和模型进展漫画完整',2:'开放设计问题两组列表及Simon补充完整',3:'数学路线判断与研究经历截图完整',4:'概念、理解与进入工程任务两段完整',5:'目录intent/spec/impl→build→应用/exe图完整',6:'优盘损坏与邮件打包两种情境图完整',7:'clone/pull/make submit及其项目自定义边界完整',8:'GitHub素材与学习问题两段完整',9:'virtually implement的比较分支与注意力说明完整',10:'面试问题、0/10、文本冲突与status说明完整',11:'目录副本、RCS、CVS/SVN、Git对比文字完整',12:'1991–2002、2002、2005三阶段Git简史图及底部引文完整',13:'回溯、快照、代码配置配套及存盘/提交边界完整',14:'三个经验外推例与删除已提交文件的说明完整',15:'init/clone/add/commit和add后再改的反例完整',16:'两个追问、构建产物及绝对路径反例完整',17:'AGENTS.md示例与源码/产物判断完整',18:'构建产物、个人配置、密钥、临时文件、例外及ignore限制完整',19:'大小写规则示例与直觉问题完整',20:'标识/自然语言角色、RFC类比及一致性边界完整',21:'可视化学习主张三项完整',22:'完整gitv提示词、对比链接及学习研究补充完整',23:'细节标准、愿意学懂与有限时间三组完整',24:'Conventional Commit标题例、正文例与理由作用完整',25:'检查点/备份/整理/可检验历史四项完整',26:'共享历史/分支发布/CI/追溯四项及底部分类完整',27:'SWE-bench输入输出、流程、两类测试完整',28:'Astropy问题、矩阵根因、PR测试交付完整',29:'issue→修改→commit→push→PR→CI/review→合并流程与反馈箭头完整',30:'原子变更、任务分解、bisect/冲突与linear history完整',31:'单线程架构和n≤3实现两组列表完整',32:'1000倍思想实验、瓶颈与change algebra三类问题完整',33:'两Agent、H/C、验证、CAS、重试箭头与可交换公式完整',34:'Jujutsu三机制和值班write skew反例完整',35:'短锁边界、人与机器历史及正确性/恢复/审计边界完整'}
imgs=[]
for si,s in enumerate(n['sections'],1):
 for fi,f in enumerate(s['frames'],1):
  video=f['source_type']=='video_frame';page=f.get('page')
  imgs.append(dict(section=si,frame=fi,path=f['path'],sha256=h(p/f['path']),purpose=f['caption'],expected_information=f['caption'] if video else '第%d页完整标题、内容、图示/公式和物理页码；%s'%(page,obs[page]),observed_information='已单独目视完整1280×410帧：'+f['caption'] if video else '已逐页目视：'+obs[page],comparison_evidence=('原视频实际秒数'+str(f['time'])+'，与该节原句时间对照' if video else f'sources/contact-{(page-1)//4+1}.jpg及逐页slides-text.json；第35页另外单图放大，第33页PDF重新渲染核对'),sources=[dict(path=str(media) if video else 'sources/source-slides.pdf',sha256=mv['sha256'] if video else pdfh,detail='原媒体完整画幅' if video else '官方网页35页截图汇编，不是官方原生PDF')],status='passed',known_gap=False,resolution='动态演示按阶段补帧：冲突前/中/后，汉诺塔增加盘数后的播放状态' if video else '复用协调者完整官网截图，逐页重新目视核对'))
write('image-audit.json',dict(schema_version=1,notes_sha256=h(p/'notes.json'),review_method='35页通过9张四页联系表逐页目视且读全文DOM文本；35页单图放大；18入选帧逐张目视，另1候选重复PPT未用；截图PDF第33页重新渲染目视。',images=imgs))
issues=[
('03-01','未来VCS被误作当堂讲授','s-g1234.0~3 5999.47–6012.51明确下一课再讨论','页32–35标为讲义补充，区分开场问题与完整方案','prevented'),
('03-02','SWE-bench/Astropy未在转写展开','官方页27–28与5488.51–5610的gh/glab口述对照','完整保存案例但明确课堂未展开、未独立执行PR','prevented'),
('03-03','分支引用与tree混淆','s-g1043.0~7 4530.64–4539.58，官方全文，4520/4678帧','分支通常指commit，commit关联根tree；标明整理者校正','corrected'),
('03-04','AI表格错误不能照抄','2380秒表格；int main() {}','C99语法小检查通过，注明不能因无include/return便推断无法编译','corrected'),
('03-05','提示音hook结果不确定','s-g839.0–s-g844.0 3722.9–3762.47','记录听感不确定且未继续修复，不能称功能验收通过','clarified'),
('03-06','SVN/delta比较过度简化','s-g412.0~8–s-g439.0~21 1886.69–1978.18','只保留帮助理解Git的直觉，不据此描述其他VCS的完整实现','clarified'),
('03-07','现场演示仅有静态概念图','3950、4349、4409、4520、4640、4678、4906、4919、4985、5048帧','补全真实bytes→对象、分支→冲突→合并、可视化前后阶段','added_evidence'),
('03-08','AI能力与研究预测被扩大','0–406.78开场、5019–5186学习讨论','限定课堂时点个人经历，无统一benchmark或普遍模型排名','clarified'),
('03-09','历史重写授权条件过窄','2935–2962现场确认无remote','说明无remote仅为练习线索，还应确认是否有人以其他途径依赖历史','clarified'),
('03-10','future lock方案错误扩大','官方32–35页','快照/文本可交换不等于不变量成立，发布需针对验证过确切版本，未承诺测试全绿绝对正确','clarified')]
write('audit.json',dict(schema_version=1,reviewer='lecture07-agent (lecture03 author second pass)',independent_reviewer=False,method='全文阅读后，回查关键原句、现行讲义与实际画面；这是作者第二遍核对。',coverage=dict(chunks_read=[c['id'] for c in idx['chunks']],sentences=533,omitted=0,slide_pages_visual=35,article='full',video_candidates_visual=19,video_frames_selected=18,whole_audio_manual=False,external_cited_papers='not independently read'),issues=[dict(id=a,issue=b,evidence=c,resolution=d,status=e) for a,b,c,d,e in issues],small_experiments=[dict(code='int main() {}',command='cc -std=c99 -fsyntax-only',exit_code=0,scope='单一语法反例，不验证整个课堂工程')],source_hashes={x:h(p/x) for x in ['notes.json','transcript.json','chunks/index.json','official-lecture.html','official-slides.html']},conclusion='关键案例、操作结果和补充来源已保留并限定范围。'))
class C(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.a=[];self.im=[]
 def handle_starttag(self,t,at):
  d=dict(at)
  if d.get('id'):self.ids.append(d['id'])
  if t=='a' and d.get('href','').startswith('#'):self.a.append(d['href'][1:])
  if t=='img':self.im.append(d.get('src',''))
c=C();c.feed((p/'课堂笔记.html').read_text());assert len(c.ids)==len(set(c.ids));assert all(a in c.ids for a in c.a);assert sum(x.startswith('data:image/') for x in c.im)==53
write('html-static-check.json',dict(status='passed',ids_unique=True,anchors_valid=True,embedded_images=53,all_content_images_offline=all(not x or x.startswith('data:image/') for x in c.im),sentences_coverage=533,omitted=0,ui_scope='not checked here; coordinator owns browser QA'))
write('run.json',dict(run_id=run,batch_id='GSE-20261002',item_id='lecture-03',scope_revision=1,video_id='BV1kybV6DE47',source_url=n['source_url'],requested_outputs=['per-video detailed mobile-readable offline HTML','timecodes','slides and demonstrations','quality review'],required_checks=['content','images','html_static','desktop','narrow'],project='/Users/yjzhao/Library/Application Support/BaoCut/projects/GSE-03-BV1kybV6DE47.bcut',media_fingerprint=mv['sha256'],sources=[dict(id='transcript',path='transcript.json',origin='coordinator-created ASR job reused after done',reuse='project ASR/layout fresh; mediahash matched;533 sentences from0.28 to6012.51;no repeated transcription'),dict(id='slides',path='official-slides.html',origin='coordinator frozen official webpage',url='https://jyywiki.cn/GSE/2026/slides3.html',pages=35),dict(id='article',path='official-lecture.html',origin='coordinator frozen official article',url='https://jyywiki.cn/GSE/2026/lect3.md')],toolchain=dict(cli='/Users/yjzhao/Downloads/BaoCut.app/Contents/Resources/skills/baocut/bin/bcut-cli',app='2.1.0 (coordinator preflight)',spec='1.249 (coordinator preflight)',transcription_engine='moss-transcribe-diarize',model=None),recorded_at=now))
review=dict(run_id=run,outcome='partial',summary='25节、533句完整阅读、53图；作者内容和图片核对完成，UI待协调者。',validation={k:dict(status=v,evidence=e) for k,v,e in [('content','passed','audit.json'),('images','passed','image-audit.json'),('html_static','passed','html-static-check.json'),('desktop','pending',None),('narrow','pending',None),('real_phone','not_requested',None),('pdf','not_requested','source-slides.pdf为来源截图汇编；35页，抽查第33页重新渲染，无笔记PDF交付')]},blocker=None,resume_condition='完成桌面/窄屏UI后更新review及依赖快照',source_hashes={x:h(p/x) for x in ['notes.json','transcript.json','chunks/index.json','课堂笔记.html','sources/source-slides.pdf']},audit='audit.json',delivered_files=['课堂笔记.html'],trace_snapshot='trace-r01.json',lessons=[],metrics=dict(wall_seconds=None,active_seconds=None,tokens=None,cost=None,media_hours=6013.205375/3600,chunks=20,sentences=533,slide_pages=35,images=53))
write('review.json',review)
events=[]
for stage,evidence in [('sources_reused','official-lecture.html and official-slides.html; media hash matched'),('transcript_export_read','original exported via CLI after fresh job;20 chunks533sentences full read'),('images','35 official slide pages and19 video candidateframes visually inspected,18selected'),('notes_render','25sections,533coverage,53images; finalize_html.py applied'),('content_review','audit.json second pass; UI pending')]:
 events.append(dict(schema_version=2,run_id=run,item_id='lecture-03',actor='lecture07-agent',attempt=1,job_id=None,stage=stage,status='completed',recorded_at=now,event_time=None,retrospective=True,detail=evidence))
(p/'events.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events))
art=[]
for q in sorted(p.rglob('*')):
 if q.is_file() and q.name not in ['trace-spec.json','trace-r01.json']:
  rel=str(q.relative_to(p));deps=[]
  if rel=='notes.json':deps=['chunks/index.json','sources/slides-text.json','sources/lecture-text.txt']
  if rel=='课堂笔记.html':deps=['notes.json','chunks/index.json','renderer','html_postprocess']+[f['path'] for s in n['sections'] for f in s['frames']]
  if rel=='image-audit.json':deps=['notes.json']+[f['path'] for s in n['sections'] for f in s['frames']]
  if rel=='review.json':deps=['notes.json','课堂笔记.html','audit.json','image-audit.json']
  if rel.startswith('chunks/'):deps=['transcript.json']
  art.append(dict(id=rel,path=rel,depends_on=deps))
art.extend([dict(id='renderer',path='/Users/yjzhao/.codex/skills/baocut-course-notes/scripts/course_notes.py',depends_on=[]),dict(id='html_postprocess',path=str(p.parent.resolve()/'finalize_html.py'),depends_on=[])])
write('trace-spec.json',dict(schema_version=1,run_id=run,basis='observed_build',root='.',artifacts=art))
print('audit finalized',len(imgs),'images')
