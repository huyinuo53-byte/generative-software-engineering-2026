import pathlib,json,hashlib,datetime,runpy,copy,shutil,re
R=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-09'); C=R.parent
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
write=lambda p,x:pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
raw=runpy.run_path(str(R/'drafts/author.py'))['sections'];bykey={s['key']:i for i,s in enumerate(raw)}
idx=json.loads((R/'chunks/index.json').read_text())
notes={'schema_version':2,'title':'生成式软件工程 09｜DeepSeek Harness (1)','short_title':'DeepSeek Harness (1)','source_url':'https://www.bilibili.com/video/BV144nc6KEA4','limitations':[
'完整顺序阅读本视频 BaoCut 转写，18 个阅读块、518 个来源单元；主作者阅读原始ASR片段，独立审阅者逐块全文复核最终导出。术语结合原画面和官方材料校订，未逐秒听审全部音频。',
'视频原画幅为1280×410。全时长2秒采样、变化候选、30秒全幅兜底和关键转场加密回查覆盖整片；这是按所述方法的视觉盘点，不是逐帧或连续播放证明。原画面细小文字的辨认边界在相应图注和审核中保留。',
'官方讲义于2026-10-26逐页截图，封存为30页网页来源汇编，不是教师原生PDF。录制时已存在的紫色补注仍与实际口述区分；不能仅因class=aigc判断课后新增。现行源码/文档补充另标固定版本与范围。',
'正文、图和自测均内嵌，可离线阅读。原视频和网页引用需联网；桌面及390/320px浏览器模拟不等于真实手机测试，打印媒体检查不等于原生打印预览。'],
'read_chunks':[x['id'] for x in idx['chunks']],'omitted':[],
'summary':[
'本课用 DeepSeek Harness 说明：一个150行Agent循环能做原型，但真实产品还需要恢复、权限、共享状态和适应需求变化的架构。',
'架构用一部分自由换取可复用的基础能力。插件机制之外，还要为Session、Event、Agent和UI定义共同的世界模型。',
'校园三维图、Trajectory、Creator Mode、白板对象桥接与生成式UI展示了扩展空间；类型检查和插件化都不能自动消除业务语义冲突。'],
'sections':[],'supplements':[],'self_test':[]}
for a in raw:
 s={k:copy.deepcopy(a[k]) for k in ['title','start','end','paragraphs','examples','editor_notes']};s.update(source_ids=[],frames=[]);notes['sections'].append(s)
for u in idx['sentences']:
 mid=(u['start']+u['end'])/2;si=next((i for i,a in enumerate(raw) if a['start']<=mid<a['end']),len(raw)-1);s=notes['sections'][si];s['source_ids'].append(u['id']);s['start']=min(s['start'],u['start']);s['end']=max(s['end'],u['end'])
selected=json.loads((R/'visual/selected-frames.json').read_text());binding=[]
for x in selected:
 si=next(i for i,a in enumerate(raw) if a['start']<=x['time']<a['end'])
 f={'source_type':'video_frame','path':'visual/'+x['path'],'time':x['time'],'caption':x['caption_draft']}
 notes['sections'][si]['frames'].append(f);binding.append({'candidate_id':x['candidate_id'],'section':si+1,'frame':len(notes['sections'][si]['frames'])})
pagekeys={1:'organization',2:'organization',3:'concrete',4:'campus',5:'unknown',6:'prd',7:'prd',8:'changing',9:'changing',10:'history',11:'tradeoff',12:'assumptions',13:'assumptions',14:'classic',15:'classic',16:'classic',17:'classic',18:'mapreduce',19:'streaming',20:'plugin',21:'session',22:'projection',23:'steer',24:'hooks',25:'slots',26:'tui',27:'conflicts',28:'ecosystem',29:'bridge',30:'dynamic'}
pages=json.loads((R/'sources/materials/sources/slides9-pages.json').read_text())
for n in range(1,31):
 si=bykey[pagekeys[n]];s=notes['sections'][si];title=pages[n-1]['text'].split('\n')[0] or '开发者交流活动照片'
 s['frames'].append({'source_type':'pdf_page','path':f'sources/official-capture/page-{n:02d}.png','source_label':'官方网页讲义截图汇编（2026-10-26）','source_url':'https://jyywiki.cn/GSE/2026/slides9.html','page':n,'related_time':s['start'],'caption':f'现行官方讲义第{n}页：{title}。截图对应本地30页来源汇编；其中补注与课堂实际口述分别标明。'})
# Material draft is integrated after the original reader has finished it.
mat=json.loads((R/'sources/materials/materials-draft.json').read_text())
sups=json.loads((R/'sources/materials/supplements-draft.json').read_text())
if isinstance(sups,dict):sups=sups['supplements']
xs={i:[] for i in range(len(raw))}
for a in sups:
 mapping={'prd':'prd','retry':'unknown','gc':'classic','lamp':'classic','event':'classic','mapreduce':'mapreduce','spark':'streaming','flink':'streaming','agent':'steer','session':'session','cordis':'plugin','bot':'changing','complexity':'organization','reorg':'assumptions','qje':'assumptions','toolkits':'creator','direct':'dynamic'}
 key=a.get('section_key') or mapping.get(a['id'].replace('gse09-supp-',''));si=bykey[key] if key in bykey else next((i for i,s in enumerate(raw) if s['start']<=a.get('related_time',0)<s['end']),0)
 j=len(notes['supplements']);xs[si].append(j)
 entry={k:v for k,v in a.items() if k in ['title','text','source_label','source_url','pages']}
 entry['text']='['+', '.join(a.get('material_ids',[]))+'；'+a.get('location','')+'] '+entry['text']
 if any(z.startswith('gse09-dsh-') for z in a.get('material_ids',[])):
  entry['text']='固定文档版本 687f282e8625c6b8d11ff58211a90524be2e4317（2026-10-17）；未确认是录制checkout。'+entry['text']
 if a['id']=='gse09-supp-bot':entry['text']='固定 dsh-bot 3acc759fc634d5d5c55792614b6bca03c630a345（2026-10-02）。'+entry['text']
 notes['supplements'].append(entry)
 # Stable material mapping for validators; the material reader's exact scope stays in original draft.
 for m in mat['materials']:
  if m['id'] in a.get('material_ids',[a.get('material_id')]):
   m.setdefault('contributions',[]).append({'item':'lecture-09','section':si+1,'location':a.get('location','原文范围见阅读台账'),'claim':a['text'],'role':'mechanism','note_target':f'supplements[{j}]'})
questions=[
('organization','有多个Agent，为什么还需要仓库与冲突控制？','它们最终共同修改一个产品，不同任务涉及的模块可能交叠。分工不自动消除共享状态、接口变化和合并后的验证。'),
('campus','校园3D图中哪些有数据依据，哪些仍是猜测？','OpenStreetMap可提供建筑和道路轮廓；楼高、空白区域用途、树木等可能是估计或程序化补全。真实布局不等于逐栋测量的数字孪生。'),
('unknown','请求发出后断网，能立即认定操作失败并重发吗？','不能。服务端可能已完成操作，客户端只是没有收到结果。先查询实际状态，并结合稳定操作标识、幂等设计与有限重试，避免重复副作用。'),
('prd','MVP与完整需求清单分别有什么用？','MVP让关键假设尽早接触使用反馈；需求清单保留预期功能与约束。两者都不能自动决定能适应未来变化的系统结构。'),
('tradeoff','“每个模块都能任意发消息”为什么还不够？','它只给了通信自由，尚未规定消息语义、状态归属、执行时机和冲突处理。架构需要合适约束，才减少开发者需要考虑的情况。'),
('mapreduce','MapReduce的便利来自什么限制？','任务必须表达为map、按key分组与reduce等形式，系统才能统一调度和重做失败任务。外部副作用、热点key和原实现master失败等仍有边界。'),
('session','会话事实日志、模型上下文和聊天UI是同一份数据吗？','它们相关但不同。会话事件提供事实依据，模型消息和不同UI是投影；流式open entry是尚未完成的可见状态。内存提交与磁盘落盘也需按具体实现区分。'),
('steer','运行中输入新消息，需要明确哪类产品语义？','新一轮等待、在约定边界注入、打断并转向等时机不同。需要说明何时接纳、已执行工具如何处理，而不是只增加一个输入框。'),
('creator','Creator Mode为什么会出现额外权限审批？','它不只是读写工作目录，还可以安装或卸载宿主插件、改变应用行为。动态生命周期提供能力，但权限、来源与实际结果仍需分别检查。'),
('conflicts','十个各压缩一半的插件串联，保留比例是多少？','(1/2)^10=1/1024，约0.098%。例子展示重复变换会累积损失；类型都正确也不能保证组合后的业务语义合理。'),
('bridge','把白板接入AI的三个动作是什么？','锁定选定对象，把对象序列化或交接给模型，再将结果取回并提交回应用。演示没有自动解决所有冲突、权限和失败恢复。'),
('dynamic','本课动态UI演示用的是局部patch吗？','不是。教师明确说样例重新生成整张卡片，局部patch和复用是可改进方向。不能把设想写成已实现。'),
('gomoku','一个可点击的五子棋界面证明了什么？','证明示例里用户动作、模型响应和UI更新能形成路径。落点、棋局规则、状态持久化和完整体验还需验证，课堂也明确它不是成熟产品。'),
('implementation','现场Agent解释“没有侵入”，能当作全面源码审计吗？','不能。教师追问后也看到额外适配和依赖。应沿具体文件、接口和数据流核对，区分解释、自述和实际测试证据。'),
('personal','直接对象协议为什么可能减少computer use，又有哪些前提？','应用可把任务和对象直接交给工具与个人数据库，减少截图和点击。仍需数据权限、正确来源、冲突控制和结果验收，不能宣称没有任何推理或成本。')]
for k,q,a in questions:notes['self_test'].append({'question':q,'answer':a,'section':bykey[k]+1})
notes['sections'][0]['editor_notes'].append('[gse09-lect9；gse09-slides9] 现行官方正文与30页讲义按本课主线回查；讲义补注不自动等于教师口述。NASA原站只返回网页壳，未独立核实其原始报告；此处仅保留官方讲义中的案例标注。')
paper_frames={}
paper_bind={}
for j,(key,img,page,cap,url) in paper_frames.items():
 si=bykey[key];ss=notes['sections'][si];ss['frames'].append({'source_type':'pdf_page','path':'sources/materials/sources/'+img,'source_label':'原始论文补充，非课堂口述','source_url':url,'page':page,'related_time':ss['start'],'caption':cap});paper_bind[j]=(si,len(ss['frames'])-1)
write(R/'notes.json',notes);write(R/'audits/frame-bindings.json',binding)
layout={'version':1,'notes_sha256':sha(R/'notes.json'),'course_title':'生成式软件工程 · NJU 2026','issue':'09','title':'DeepSeek Harness (1)','subtitle':'从150行循环，走到能承受变化的插件生态','summary_title':'先把握本课主线','summary_terms':['架构','共同的世界模型'],'groups':[{'start':1,'label':'一 / 原型碰到真实世界'},{'start':8,'label':'二 / 架构如何交换自由与便利'},{'start':14,'label':'三 / 建立共同的世界模型'},{'start':21,'label':'四 / 让插件长出不同产品'},{'start':25,'label':'五 / 对象桥接与生成式界面'}],'sections':[],'bridges':{}}
for i,(a,s) in enumerate(zip(raw,notes['sections'])):
 flow=[];nf=len(s['frames']);v=[j for j,f in enumerate(s['frames']) if f['source_type']=='video_frame'];o=[j for j,f in enumerate(s['frames']) if f['source_type']=='pdf_page' and 'official-capture/' in f['path']]
 for j in range(len(s['paragraphs'])):
  flow.append(f'p{j}')
  for n,fj in enumerate(v):
   slot=min(len(s['paragraphs'])-1,int((n+1)*len(s['paragraphs'])/(len(v)+1)))
   if slot==j:flow.append(f'f{fj}')
 for j in range(len(s['examples'])):flow.append(f'e{j}')
 for j in range(len(s['editor_notes'])):flow.append(f'n{j}')
 # Each supplement stays inside the relevant knowledge point, before its related official pages.
 for j in xs[i]:
  flow.append(f'x{j}')
  if j in paper_bind:flow.append('f'+str(paper_bind[j][1]))
 for j in o:flow.append(f'f{j}')
 layout['sections'].append({'short':s['title'],'takeaway':a['takeaway'],'terms':[t for t in ['事件溯源','共同概念','私有状态','状态','假设','接口','真实','重试','插件','原型','模型','用户'] if t in '\n'.join(s['paragraphs'])][:2],'flow':' '.join(flow)})
write(R/'reading-layout.json',layout)
# Normalize copies into course-relative material paths, preserving the reader's original JSON untouched.
for m in mat['materials']:
 m['related_items']=['lecture-09'];m['contributions']=[x for x in m.get('contributions',[]) if x.get('item')=='lecture-09' and isinstance(x.get('section'),int)]
 if m.get('path'):
  original=R/'sources/materials'/m['path'];m['kind']='pdf' if original.read_bytes()[:5]==b'%PDF-' else 'web'
 if m.get('kind')=='pdf' and m.get('read_pages') and len(m['read_pages'])!=m.get('total_pages'):m['scope_pages']=m['read_pages']
 if m['id'] in ['gse09-lect9','gse09-slides9']:m['contributions'].append({'item':'lecture-09','section':1,'location':'官方全文/30页逐页源；各主题与原图见分节正文','claim':'核对共同世界模型、接口与课堂讲义补注归属','note_target':'sections[0].editor_notes[-1]'})
 if m.get('reading_status')=='full' and not m['contributions']:m['not_adopted_reason']='背景参考按声明范围阅读；课堂或其他一手来源已覆盖本课所需论证，未另加独立补充。保留真实范围，不声称这些背景原文由教师逐句讲授。'
 for k in ['path']:
  if m.get(k):
   z=pathlib.Path(m[k]);
   if z.is_absolute() and str(z).startswith('/tmp/gse09-materials/'):m[k]='lecture-09/sources/materials/'+str(z.relative_to('/tmp/gse09-materials'))
   elif not z.is_absolute():m[k]='lecture-09/sources/materials/'+str(z)
 # reader may keep source_files/artifacts. Those stay recorded in source draft and are normalized below if needed.
mat['expected_material_ids']=[m['id'] for m in mat['materials']]
write(R/'materials.json',mat)
print('notes',len(notes['sections']),'images',sum(len(s['frames']) for s in notes['sections']),'supplements',len(notes['supplements']),'questions',len(notes['self_test']))
