import json,pathlib,hashlib,datetime,copy
R=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-08')
S=pathlib.Path('/tmp'); ns={'__name__':'gse_draft'}
for name in ['gse08-author.py','gse08-author-part2.py','gse08-author-part3.py','gse08-author-part4.py','gse08-author-part5.py']:
 exec((S/name).read_text(),ns)
raw=ns['sections']; bykey={s['key']:i for i,s in enumerate(raw)}
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
idx=json.loads((R/'chunks/index.json').read_text())
notes={'schema_version':2,'title':'生成式软件工程 08｜Agent-native 开发','source_url':'https://www.bilibili.com/video/BV11LWw6VEHW','limitations':[
 '完整阅读 BaoCut 原始转写的19个分块（394个来源单元），结合讲义与真实视频画面校订术语；未逐秒听审整片音频。课堂观点、现场Agent回答与整理者解释在正文中分别标明。',
 '视频为1280×410全画幅；原画面中细小板书存在辨认限制。完整视频轨及尾段解码已检查；以2秒扫描、变化候选、定时兜底和关键转场加密回查盘点全时间轴，非逐帧或连续播放证明。',
 '官方讲义为2026-10-19获取的24页网页截图汇编，可能含课后补注；配图标记的是汇编页，不冒充官方原生PDF。Humanize补充固定v2；当前仓库补充若晚于录制日期，会另标提交。',
 '本篇HTML的图片全部内嵌，可离线阅读；原视频及网页链接需要联网。桌面与窄屏浏览器模拟不等同于真实手机测试，打印媒体模拟不等同于原生打印。'],
 'read_chunks':[c['id'] for c in idx['chunks']],'omitted':[],
 'summary':[
 'Agent-native 开发把工作区当作状态，把一次实现、审查或重构当作状态转移，再用门禁和反馈约束每一步。',
 '本课从约150行MiniAgent与Ralph循环实演，走到CI/CD、双语文档、Agent Notes和代码评审，解释成熟系统为什么需要这些机制。',
 '更多token、更多Agent或更多检查都不自动等于更好的结果：还要比较候选路线、核实证据，并区分机械检查与语义判断。'],
 'sections':[],'supplements':[],'self_test':[]}
for s in raw:
 notes['sections'].append({k:copy.deepcopy(s[k]) for k in ['title','start','end','paragraphs','examples','editor_notes']})
for s in notes['sections']:s.update(source_ids=[],frames=[])
for unit in idx['sentences']:
 t=(unit['start']+unit['end'])/2
 si=next((i for i,s in enumerate(raw) if s['start']<=t<s['end']),len(raw)-1)
 s=notes['sections'][si];s['source_ids'].append(unit['id']);s['start']=min(s['start'],unit['start']);s['end']=max(s['end'],unit['end'])
# 候选全幅图均经视觉盘点代理原尺寸查看；额外81:00由主作者再次查看。
selected=json.loads((R/'visual/selected-frames.json').read_text())
selected=[x for x in selected if x['candidate_id'] not in {'v0378','v0429','v0440'}]
selected.append({'candidate_id':'v0574','time':4860,'event':'history-archaeology','path':'scan/sample-02431.jpg','sha256':sha(R/'visual/scan/sample-02431.jpg'),'original_resolution_reviewed':True,'legibility':'主作者实际原尺寸查看六次历史变化总结'})
selected.sort(key=lambda x:x['time'])
caps={
 'v0005':'Lab2 背景页中的个人助手与 Morning Paper 示例。', 'v0010':'Lab2 要求增加探索与查证的 effort；板书开始展开搜索树。',
 'v0016':'Lab2 引用 Humanize，并将更深入的研究连接到迭代求解。','v0019':'Lab2 页面继续展示上下文工程与效果评估；这些要求不等于增加轮数就必然提升。',
 'v0033':'Intent、Spec 与 Implementation 的多层选择；板书细字以对应口述解释为准。','v0054':'MiniAgent 的 imports、key读取函数和工具定义；画面未显示实际密钥。',
 'v0061':'run_bash 的命令执行与60秒timeout，暴露最小原型的环境假设。','v0070':'请求与read_reply接收流式回复、工具调用。','v0073':'main循环把bash结果以tool消息送回模型。',
 'v0100':'浏览器打开生成的GSE简介卡，展示任务从指令到页面的执行结果。','v0121':'现场Agent以截图和颜色统计继续verify；这不是完整页面语义验收。',
 'v0131':'Ralph循环与上下文/历史的板书讨论。','v0164':'工作区状态、不同转移动作以及并行分支再合并的板书。','v0173':'ralf-loop.sh约定每轮工作与<RALPH_DONE>终止标记。',
 'v0205':'第一轮语言研究写出NEXT_STEPS.md，留给下一轮继续。','v0216':'预先生成的蓝紫个人名片；教师指出其中邮箱与身份有误。','v0226':'另一张较朴素的名片；教师称来自loop，并检查联系方式。',
 'v0239':'语言研究输出完成标记并返回shell；标记本身不证明研究事实正确。','v0246':'打开第一份语言研究报告，其结论及数据属于现场Agent输出。','v0275':'普通agent.py再次生成研究结果，课堂对比两份报告；网页获取失败不因完成声明而消失。',
 'v0325':'Codex仓库workflow和现场AI总结；本笔记未对该提交重新运行CI。','v0347':'现场询问lint与测试的区别，屏幕展示AI解释。','v0371':'文档与代码的隐形关系、门禁与维护的板书。',
 'v0386':'课堂打开OpenAI Harness engineering原文；公开文章与课堂推测分开记录。','v0411':'现场AI用三层流程解释Codex CI。','v0420':'PR/main/发布的餐厅类比表，属于现场AI的教学说明。',
 'v0439':'左侧板书是教师自己项目的architecture/logbook/dashboard与Agent分工；右侧投影仍是Anthropic/GCC案例。','v0460':'打开DeepSeek Harness的architecture.md，观察文档结构与交叉引用。',
 'v0476':'现场Agent解释双语文档三件套与配对门禁。','v0499':'README.i18n.yaml按标题片段记录英文与中文哈希。','v0501':'两侧内容及其配对关系的板书；哈希不同可提示变化。',
 'v0514':'文档翻译流程与按需加载的规范入口。','v0523':'style-samples.md中的风格样例；样例不等于当前校验算法。','v0528':'terminology与一致性讨论，教师提示过严规则会误伤。',
 'v0536':'现场追问双语机制的开发历史，Agent开始检索Git记录。','v0556':'现场Agent列出的术语约定与三件套早期阶段。','v0574':'现场Agent总结六次演化，包括最小补丁、轻量路径与简化驱动；未独立重放这些历史提交。',
 'v0595':'分层AGENTS、字数预算和带生命周期的Agent Notes清单。','v0615':'现场查看skills分类，区分开发流程技能与产品提供的技能。','v0635':'本地自证、CI与人工评审的现场说明。','v0660':'机械门禁与文档分层清单；需看各脚本合同才能判断其保证范围。',
 'v0692':'尝试机会、经验和能力门槛的课堂讨论；板书用于观点说明。','v0712':'课程结束前回到agent.py的工具循环，连接最小核心与插件化系统。'}
frame_meta=[]
for x in selected:
 si=next(i for i,s in enumerate(raw) if s['start']<=x['time']<s['end'])
 f={'source_type':'video_frame','path':'visual/'+x['path'],'time':x['time'],'caption':caps[x['candidate_id']]}
 notes['sections'][si]['frames'].append(f);frame_meta.append({'section':si+1,'frame':len(notes['sections'][si]['frames']),'candidate_id':x['candidate_id'],'review_record':x})
slidetitles=['Intent—Spec—Implementation与复杂性','先构建原型、用具体用例检验','Agent Loop的模型与工具','Ralph名称的背景','Ralph循环与终止问题','Everything Is a State Machine','每次Transition都检查','CI与两种CD','Hook-Based CI/CD','业务规则与门禁边界','把CI/CD写成Spec','Agent的偏好与不可信开发者','六类可执行约束及人工判断','OpenAI Harness Engineering','把品味做成机制','Stripe Minions','Anthropic编译器实验','StrongDM Software Factory','DeepSeek Harness主题插画（不是架构图）','真正的经验与重构','Friendster背景','Webvan与Quibi背景','Token与尝试机会','学习机会断层插画（不是定量研究图）']
for si,s in enumerate(raw):
 for page in s['slides']:
  notes['sections'][si]['frames'].append({'source_type':'pdf_page','path':f'sources/official-20261019/slides/slide-{page:02}.jpg','source_label':'现行官方网页讲义逐页截图汇编（非原生PDF），2026-10-19','source_url':'https://jyywiki.cn/GSE/2026/slides8.html','page':page,'related_time':max(s['start'],min(s['end']-1,s['start']+5)),'caption':f'现行讲义第{page}页：{slidetitles[page-1]}。紫色或扩展内容与课堂口述的归属以正文标注为准。'})
# 已完整阅读的推荐材料；落点在本课主题附近。
mat=json.loads((R/'sources/official-20261019/materials-draft.json').read_text())
mat['scope']='本次新增第08课的材料台账；不追认或重写旧课阅读记录。'; mat['materials']=copy.deepcopy(mat['materials'])
placements={'gse08-ralph':'ralph-origin','gse08-ci':'ci-cd','gse08-cd':'ci-cd','gse08-github-protection':'hooks','gse08-git-hooks':'hooks','gse08-github-pages':'lint','gse08-github-deployments':'lint','gse08-minions':'industry','gse08-compiler':'industry','gse08-strongdm':'industry','gse08-dtu':'industry','gse08-friendster':'experience','gse08-harness':'openai','gse08-webvan':'experience','gse08-quibi':'experience'}
xs={i:[] for i in range(len(raw))}
for m in mat['materials']:
 si=bykey[placements[m['id']]]; xi=len(notes['supplements']);xs[si].append(xi)
 text=f"原文阅读补充 [{m['id']}，{m.get('version','获取版本')}，{'; '.join(m.get('read_sections',[]))}]："+m['proposed_supplement']
 notes['supplements'].append({'title':m['title'],'text':text,'source_label':'原始推荐/背景材料补充，非课堂逐项口述','source_url':m['source_url']})
 m['path']='lecture-08/sources/official-20261019/'+m['path'];m['related_items']=['lecture-08'];m['integration_status']='integrated_pending_semantic_review'
 if m.get('known_gaps'):m['reading_scope_limitations']=m['known_gaps'];m['known_gaps']=[]
 m['contributions']=[{'item':'lecture-08','section':si+1,'location':'; '.join(m['read_sections']),'claim':m['proposed_supplement'],'role':'background' if m.get('recommendation_kind')=='background_citation' else 'mechanism','note_target':f'supplements[{xi}]'}]
 # A primary retrieval transcript can bundle pages; keep its original hash.
# Humanize全文补充，分布到多样性、门禁和评估处。
hd=json.loads((R/'sources/lab2-humanize-20261019/materials-draft.json').read_text())
h=hd['materials'][0];h['path']='lecture-08/sources/lab2-humanize-20261019/humanize-v2.pdf';h['related_items']=['lecture-08'];h['contributions']=[]
hs=json.loads((R/'sources/lab2-humanize-20261019/supplements-draft.json').read_text())
hkeys=['humanize','constraints','humanize','humanize','harness-evaluation'];hx={}
for j,x in enumerate(hs):
 si=bykey[hkeys[j]];xi=len(notes['supplements']);xs[si].append(xi);hx[j]=xi
 notes['supplements'].append({k:x[k] for k in ['title','text','source_label','source_url','pages']})
 h['contributions'].append({'item':'lecture-08','section':si+1,'location':'PDF物理页'+','.join(map(str,x['pages'])),'claim':x['text'],'role':'mechanism' if j<3 else 'experiment','note_target':f'supplements[{xi}]'})
for page,j in [(5,0),(7,3)]:
 si=bykey['humanize'];notes['sections'][si]['frames'].append({'source_type':'pdf_page','path':f'sources/lab2-humanize-20261019/key-page-{page:02}.png','source_label':'Humanize论文补充，arXiv:2610.08900v2','source_url':f'https://arxiv.org/pdf/2610.08900v2#page={page}','page':page,'related_time':244,'caption':('图4：计划契约、builder交接、机械gate与独立reviewer；完整原页，区分文件完整与语义正确。' if page==5 else '图5：KDA的48小时、单个DSA TopK kernel团队自报消融；右图对数轴，8.58倍不是所有kernel或通用成功率。')})
mat['materials'].append(h)
labpath=R/'sources/lab2.html';lab={'id':'gse08-lab2','kind':'web','recommendation_kind':'explicit_recommendation','required':True,'title':'实验(2): Deeper Research','listed_title':'实验(2): Deeper Research','listed_url':'https://jyywiki.cn/GSE/2026/lab2.md','source_url':'https://jyywiki.cn/GSE/2026/lab2.md','version':'2026-10-19获取','identity_status':'verified','path':'lecture-08/sources/lab2.html','sha256':sha(labpath),'reading_status':'full','scope_sections':['正文背景、实验要求、算力换智力、上下文工程、评估效果、提交'],'read_sections':['正文背景、实验要求、算力换智力、上下文工程、评估效果、提交'],'known_gaps':[],'related_items':['lecture-08'],'contributions':[{'item':'lecture-08','section':2,'location':'§2.1–2.3','claim':'固定输入与基础模型，比较不同effort并记录质量、延迟和成本','role':'exercise','note_target':'editor_notes[0]'}]}
notes['sections'][1]['editor_notes'][0]='[gse08-lab2，§2.1–2.3] '+notes['sections'][1]['editor_notes'][0]
mat['materials'].append(lab)
# 补读的固定版本仓库材料在完成后由主作者审核并加入此入口。
extra=R/'sources/harness-20261019/integration.json'
if extra.exists():
 d=json.loads(extra.read_text())
 for m in d['materials']:
  m['contributions']=[];mat['materials'].append(m)
 for x in d['supplements']:
  si=bykey[x['section_key']];xi=len(notes['supplements']);xs[si].append(xi);notes['supplements'].append({k:v for k,v in x.items() if k!='section_key'})
  d['materials'][0]['contributions'].append({'item':'lecture-08','section':si+1,'location':'固定提交原文件范围见source_files及正文出处','claim':x['text'],'role':'mechanism','note_target':f'supplements[{xi}]'})
mat['expected_material_ids']=[m['id'] for m in mat['materials']]
# 自测是整理者设计，答案指回实际主题。
questions=[
 ('search','同一任务跑更久，为什么未必更好？','它可能一直在错误或次优路线里深入。应留出比较候选的预算，并用固定指标、重复运行和成本记录判断改进。'),
 ('humanize','不同模型互相review，就能消除共同盲点吗？','不能。模型可能共享偏差，reviewer也会漏检或误报。独立上下文、外部知识和可执行反馈是降低风险的机制，论文没有证明所有任务上的普遍净收益。'),
 ('intent','Intent、Spec和Implementation各回答什么问题？','想达到什么；把目标写成怎样的约束；具体怎样实现。层间一对多，访谈、建模、架构讨论和原型帮助排除不合适的分支。'),
 ('miniagent','模型返回一个bash工具调用后，谁真正执行命令？','宿主程序解析参数并执行，再把输出和对应tool_call_id放回messages。工具描述是协议，不能自己执行。'),
 ('card-demo','截图像素统计通过，能证明HTML页面合格吗？','只能支持它实际测到的颜色或局部存在性。文本含义、交互路径、布局与读者体验仍需各自检查。'),
 ('ralph-script','为什么每轮都用相同提示词，仍可能推进任务？','工作区已发生变化：代码、进度、失败和下一步留在文件中，新一轮重新读取它们。提示词相同不代表状态相同。'),
 ('ralph-comparison','两张名片能证明loop比一次生成更好吗？','不能隔离提示词、随机性和上下文的作用。这次示例观察到差异；要形成较稳结论，需要控制条件、重复比较和真实验收。'),
 ('state','为什么分出多个Agent还需要共享状态与调度？','它们可能撞上同一个失败、覆盖彼此修改。独立任务、worktree、共同记录与合并后检查帮助形成真正分工。'),
 ('ci-cd','持续交付与持续部署的区别是什么？','持续交付让合格构建具备随时发布的条件，是否发布仍可由业务决定；持续部署把通过所需检查的构建实际交付用户。'),
 ('hooks','本地pre-commit通过，为什么还需要远端门禁？','本地hook可能被跳过或未运行。远端保护把必需结果接到合并规则，还要核实权限、绕过和检查确实执行。'),
 ('constraints','给文档设字数预算解决什么，又不解决什么？','可限制可判定的膨胀，提供及时失败反馈；不能判断内容真伪、是否有用或是否遗漏。例外阈值与语义需要另外评审。'),
 ('bilingual','两侧hash更新且检查为绿，能证明翻译忠实吗？','不能。它说明被记录或确认的版本关系满足机械条件；是否等义、是否自然仍要比较内容和样例，不能只重录hash。'),
 ('translation','为什么把所有规范放进AGENTS.md可能适得其反？','常驻上下文膨胀会稀释注意力。用导航、分层和任务时按需加载，在需要时提供足够规范。'),
 ('history','读Git历史比只读当前README多得到什么？','可以追问某个约束解决过什么失败、何时改过方向、为何保留或简化。现场AI报告仍要与真实提交对照，不能自动当作历史确证。'),
 ('review-gates','只改计划时，应该重跑全部代码CI吗？','根据真实依赖与改动范围选检查。没有受影响代码不意味着所有文档、链接或契约检查都不需要；不能一概全跑或全跳。'),
 ('opportunity','怎样把token预算转成学习能力？','选择可验证的小任务，观察完整执行轨迹，保留失败原因，比较方案并复盘。预算提供机会，不能替代判断和理解。')]
for key,q,a in questions:notes['self_test'].append({'question':q,'answer':a,'section':bykey[key]+1})
R.joinpath('notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
R.parent.joinpath('materials.json').write_text(json.dumps(mat,ensure_ascii=False,indent=2)+'\n')
# 布局按语义主题插入补充；课堂图与相应段落交错，资料图在其说明之后。
layout={'version':1,'notes_sha256':sha(R/'notes.json'),'course_title':'生成式软件工程 · NJU 2026','issue':'08','title':'Agent-native 开发','subtitle':'从一个小循环，走到可持续维护的工程系统','summary_title':'先把握本课主线','summary_terms':['工作区','状态转移','机械检查与语义判断'],'groups':[{'start':1,'label':'一 / 先设计探索与反馈'},{'start':6,'label':'二 / 从最小Agent到Ralph循环'},{'start':14,'label':'三 / 把验证接入开发流程'},{'start':20,'label':'四 / 真实项目中的Harness'},{'start':28,'label':'五 / 从失败与开源中学习'}],'sections':[],'bridges':{}}
terms={'search':['宽度优先','深度优先'],'humanize':['知识'],'intent':['intent','specification'],'prototype':['典型 use case'],'miniagent':['tool_call_id','timeout'],'ralph-origin':['Harness','工作区'],'state':['状态转移'],'ci-cd':['自动化'],'constraints':['字数预算'],'bilingual':['哈希','语义'],'translation':['渐进式披露'],'history':['Git'],'inventory':['Agent Notes','按需加载'],'review-gates':['依赖关系'],'opportunity':['试错']}
for i,(a,b) in enumerate(zip(raw,notes['sections'])):
 tokens=[];nf=len(b['frames']);video=[j for j,f in enumerate(b['frames']) if f['source_type']=='video_frame'];official=[j for j,f in enumerate(b['frames']) if f['source_type']=='pdf_page' and 'official-' in f['path']];paper=[j for j,f in enumerate(b['frames']) if f['source_type']=='pdf_page' and 'humanize' in f['path']]
 # 将真实截图分散到解释链，官方页在课堂叙述之后保留。
 for j in range(len(b['paragraphs'])):
  tokens.append(f'p{j}')
  for n,fj in enumerate(video):
   slot=min(len(b['paragraphs'])-1, int((n+1)*len(b['paragraphs'])/(len(video)+1)))
   if slot==j:tokens.append(f'f{fj}')
 for j in range(len(b['examples'])):tokens.append(f'e{j}')
 for j in range(len(b['editor_notes'])):tokens.append(f'n{j}')
 for fj in official:tokens.append(f'f{fj}')
 for xi in xs[i]:
  tokens.append(f'x{xi}')
  if i==bykey['humanize'] and xi==hx[0]:tokens.append(f'f{paper[0]}')
  if i==bykey['humanize'] and xi==hx[3]:tokens.append(f'f{paper[1]}')
 body=' '.join(b['paragraphs']+b['examples']+b['editor_notes']+[notes['supplements'][x]['text'] for x in xs[i]])
 selectedterms=[t for t in terms.get(a['key'],[]) if t in body]
 layout['sections'].append({'short':a['title'].split('：')[0],'takeaway':a['takeaway'],'terms':selectedterms,'flow':' '.join(tokens)})
R.joinpath('reading-layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
R.joinpath('drafts/assembly-map.json').write_text(json.dumps({'sections':[{'key':s['key'],'start':s['start'],'end':s['end']} for s in raw],'frames':frame_meta,'supplement_sections':{str(k+1):v for k,v in xs.items()}},ensure_ascii=False,indent=2))
print(json.dumps({'sections':len(raw),'images':sum(len(s['frames']) for s in notes['sections']),'supplements':len(notes['supplements']),'self_test':len(notes['self_test']),'source_units':len(idx['sentences'])},ensure_ascii=False))
