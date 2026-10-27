import json,pathlib,hashlib,datetime,subprocess
from html.parser import HTMLParser
from decimal import Decimal
P=pathlib.Path(__file__).parent; now=datetime.datetime.now(datetime.timezone.utc).isoformat(); run='BV1JGap6LE74-20261002'
def h(p):
 a=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):a.update(b)
 return a.hexdigest()
def write(name,o):(P/name).write_text(json.dumps(o,ensure_ascii=False,indent=2))
n=json.loads((P/'notes.json').read_text());pdfh=h(P/'sources/source-slides.pdf');media=pathlib.Path('/Users/yjzhao/Downloads/需求和架构 (2) [07-Raw 26生成式软件工程 NJU].mp4');mh=h(media)
assert mh=='df4344f9c61dfb2a247f734570b9d2ef3ec1d21010849efb4eed78347b5dcc12'
write('sources/media-validation.json',dict(path=str(media),sha256=mh,bytes=media.stat().st_size,video_duration=5981.10,audio_duration=5981.12,tail_decode={'range':[5920,5981.12],'status':'passed','method':'ffmpeg -ss 5920 -i media -f null - exited 0 with no error'},transcript_first=.96,transcript_last=5981.04,identity='matches project media hash',asr_state='stale',state_reason='未从项目证据确认stale原因，不作推断',reuse='已有transcribe done；原媒体指纹匹配，导出首尾覆盖，布局/润色fresh；不重转写'))
imgs=[]
for si,s in enumerate(n['sections'],1):
 for fi,f in enumerate(s['frames'],1):
  video=f['source_type']=='video_frame';page=f.get('page'); detail=f['path'].endswith('ledger-detail.webp')
  purpose=f['caption'].split('。')[0]
  expected=(f['caption'] if video else ('银行收支两项分录及资产负债表、利润表、现金流量表三组变化' if detail else f'官方讲义第{page}页完整标题、全部列表/代码/图示、页码'))
  observed=('已逐张查看完整原视频帧；'+f['caption'] if video else ('已单独放大查看：75、22.07、−52.93及三组变化完整；源图左上凭证名有意遮挡，正文不推测' if detail else f'已在contact-{(page-1)//6+1}.jpg逐页目视对照，标题、正文底端与页码完整；图/公式/代码与slides-text.json该页相符'))
  imgs.append(dict(section=si,frame=fi,path=f['path'],sha256=h(P/f['path']),purpose=purpose,expected_information=expected,observed_information=observed,comparison_evidence=f'对应notes第{si}节，'+('原视频实际时间'+str(f['time']) if video else f'当前官方网页第{page}/39页；截图汇编物理第{page}页'),sources=[dict(path=str(media) if video else 'sources/source-slides.pdf',sha256=mh if video else pdfh,detail='原媒体1280×410，完整全画幅' if video else '官方网页逐页截图汇编，非官方原生PDF')],status='passed',known_gap=False,resolution='选用完整官方页；第34页增补内嵌原图以便阅读' if not video else '选取操作/论证完整阶段；nano同时保留选择和打开结果'))
write('image-audit.json',dict(schema_version=1,notes_sha256=h(P/'notes.json'),images=imgs,review_method='39页在7张六页联系表中逐页目视与逐页DOM文本核对；第1页和银行图单图放大；6张选用视频帧均单独目视。'))
issues=[
 ('07-01','资料混课风险','父协调提供的旧lecture07_slide_evidence.json实际是CMU Computer Use Agents','排除；只使用NJU当前官方lect7/slides7和BV1JGap6LE74','sources/slides-text.json', 'prevented'),
 ('07-02','ASR状态误述','project显示ASR stale，不能称fresh转写','明确stale且原因未确认；原媒体hash匹配后复用导出','sources/media-validation.json','prevented'),
 ('07-03','历史年份口误','s-g477.0~19 / 3059.9–3070.27说管道大概1983年引入UNIX','不把该口述年份作为确定史实；保留1964年备忘录比喻','notes.json 第12节','clarified'),
 ('07-04','现场模型类比不等于事实','1954秒AI将MINISIM映射React Scheduler/Fiber','保留图但标记类比未经源码逐项验证','notes.json 第8节','clarified'),
 ('07-05','报表校验过度承诺','5229–5240相信AI与校验；5599–5606纠错无代价','明确平衡不保证业务真实、解释与规则仍需审核、纠错不是没有成本','notes.json 第21–23节','clarified'),
 ('07-06','静态截图字过小','官方第34页银行报表图横长、整页留白多','同时提供完整页与原始内嵌图，数字复核22.07-75=-52.93','frames/ledger-detail.webp','fixed'),
 ('07-07','当前状态模型绝对化','SQL Billion Dollar Mistake可误读为SQL没有view或约束','界定为讲师调侃及跨应用计算依赖视角，保留讲义修正','notes.json 第25节','clarified'),
 ('07-08','演示只保留起点','文件选择列表不能证明已成功打开','加入3232和3254两帧，后一帧可见GNU nano打开p1/lect/index.md','frames/video-3254.jpg','fixed')]
write('audit.json',dict(schema_version=1,actor='lecture07-agent',method='完成主稿后独立进行第二遍关键证据复查；不是独立第三方审稿',coverage={'transcript_chunks':'1–20全读','sentences':909,'omitted':0,'official_slide_pages':'1–39全读并目视','lecture_article':'全文阅读','cited_classics':'未全文外延阅读'},issues=[dict(issue_id=a,issue=b,before=c,after=d,evidence=e,status=f,verification='原转写、当前讲义或实际像素复查') for a,b,c,d,e,f in issues],math_checks=[dict(expression='Decimal(22.07)-Decimal(75)',result=str(Decimal('22.07')-Decimal('75')),status='passed')],source_hashes={x:h(P/x) for x in ['transcript.json','chunks/index.json','notes.json','sources/slides7.html','sources/lect7.md']},conclusion='主稿保留论证、反例、具体代码语义和现场演示；课堂与官网补充已标注；未逐秒听审。'))
class C(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.anchors=[];self.images=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id'in d:self.ids.append(d['id'])
  if t=='a' and d.get('href','').startswith('#'):self.anchors.append(d['href'][1:])
  if t=='img':self.images.append(d.get('src',''))
c=C();c.feed((P/'课堂笔记.html').read_text());assert len(c.ids)==len(set(c.ids));assert all(a in c.ids for a in c.anchors);assert sum(x.startswith('data:image/') for x in c.images)==46;assert all((not x) or x.startswith('data:image/') for x in c.images)
write('html-static-check.json',dict(status='passed',ids_unique=True,anchors_valid=True,embedded_images=46,all_content_images_offline=True,script_render_coverage=909,not_verified_here=['desktop','narrow','real_phone','interactive zoom/print/console']))
write('run.json',dict(run_id=run,batch_id='GSE-20261002',item_id='lecture-07',scope_revision=1,scope_changes=[],video_id='BV1JGap6LE74',source_url=n['source_url'],requested_outputs=['per-video detailed mobile-readable offline HTML','notes.json','quality review'],required_checks=['content','image','html_static','desktop','narrow'],sources=[dict(id='transcript',path='transcript.json',kind='BaoCut original export',transcript_origin='reused',reuse_reason='已有转写done，媒体hash匹配，首尾覆盖',project=str(media.parent.parent/'Library/Application Support/BaoCut/projects/BV1JGap6LE74.bcut'),known_gaps=['ASR stale原因未确认，未逐秒听审']),dict(id='slides',path='sources/slides7.html',kind='official webpage',source_url='https://jyywiki.cn/GSE/2026/slides7.html',pages=39),dict(id='lecture',path='sources/lect7.md',kind='official article served as HTML',source_url='https://jyywiki.cn/GSE/2026/lect7.md')],toolchain=dict(cli='/Users/yjzhao/Downloads/BaoCut.app/Contents/Resources/skills/baocut/bin/bcut-cli',app='2.1.0 (coordinator preflight)',spec='1.249 (coordinator preflight)',transcription_engine='moss-transcribe-diarize',model=None),created_at=now))
review=dict(run_id=run,outcome='partial',summary='本课完整主稿与证据审查完成；桌面/窄屏UI由协调者继续验收。25节、909句、46图。',validation={k:dict(status=v,evidence=e) for k,v,e in [('content','passed','audit.json'),('images','passed','image-audit.json'),('html_static','passed','html-static-check.json'),('desktop','pending',None),('narrow','pending',None),('real_phone','not_requested',None),('pdf','not_requested','sources/source-slides.pdf仅为图片出处汇编，不是用户交付的笔记PDF')]},blocker=None,resume_condition='完成桌面与窄屏浏览器QA后更新review并重冻trace',source_hashes={x:h(P/x) for x in ['transcript.json','chunks/index.json','notes.json','课堂笔记.html','sources/source-slides.pdf']},scope_revision=1,audit='audit.json',delivered_files=['课堂笔记.html'],trace_snapshot='trace-r01.json',lessons=[dict(status='candidate',scope='课程复用证据识别',finding='同名lecture07旧证据实际属于另一门课，必须核对课程/视频身份',evidence='audit.json 07-01',next_action='复用前检查标题、URL和视频ID')],metrics=dict(wall_seconds=None,active_seconds=None,tokens=None,cost=None,media_hours=5981.12/3600,transcript_chunks=20,sentences=909,slide_pages=39,images=46))
write('review.json',review)
art=[]
for q in sorted(P.rglob('*')):
 if q.is_file() and q.name not in ['trace-spec.json','trace-r01.json']:
  rel=str(q.relative_to(P));deps=[]
  if rel=='notes.json':deps=['chunks/index.json','sources/slides-text.json','sources/lecture-text.txt']
  if rel=='课堂笔记.html':deps=['notes.json','chunks/index.json','renderer']+[f['path'] for s in n['sections'] for f in s['frames']]
  if rel=='image-audit.json':deps=['notes.json']+[f['path'] for s in n['sections'] for f in s['frames']]
  if rel=='review.json':deps=['notes.json','课堂笔记.html','audit.json','image-audit.json']
  if rel.startswith('chunks/'):deps=['transcript.json']
  art.append(dict(id=rel,path=rel,depends_on=deps))
art.append(dict(id='renderer',path='/Users/yjzhao/.codex/skills/baocut-course-notes/scripts/course_notes.py',depends_on=[]))
write('trace-spec.json',dict(schema_version=1,run_id=run,basis='observed_build',root='.',artifacts=art))
print('audit finalized',len(imgs),'images')
