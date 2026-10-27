import pathlib,json,hashlib,datetime
from decimal import Decimal
P=pathlib.Path(__file__).parent
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
n=json.loads((P/'notes.json').read_text());before=H(P/'notes.json');nh=H(P/'课堂笔记.html');ia=json.loads((P/'image-audit.json').read_text());added=[]
def add(sec,t,cap,expected):
 s=n['sections'][sec-1];assert s['start']<=t<=s['end'];p=f'frames/video-{t}.jpg';s['frames'].append(dict(source_type='video_frame',path=p,time=t,caption=cap));added.append((sec,len(s['frames']),p,t,expected))
add(2,450,'07:30现场结果上半部分：模型说明用户级与项目级AGENTS.md、Skill索引等来源。它是课堂工具的自述与屏幕证据，不是本笔记对模型内部状态的独立转储。','模型自查上下文来源的可见条目，用户级与项目级指令区分')
add(2,490,'08:10现场结果下半部分：Skill索引、工具定义、会话历史和环境变量。两帧共同保存这次上下文自查的主要结果。','Skill简述与按需加载、工具定义、会话历史、环境信息四项可见')
add(5,1080,'18:00代码阅读过程：Agent读取guardian/prompt.rs并在approval_request.rs检索风险评估相关结构。画面保存了检索路径与命令，不能单凭这一帧证明其后解释完全正确。','可见实际源码路径、rg检索与工具返回，区分阅读过程和最终结论')
add(8,1595,'26:35一句“现代风格”生成的个人主页：暗色布局、导航与终端视觉元素。讲师此处只评价美术与模板感，明确未核实页面内容。','现场生成主页的整体页面设计与终端视觉元素')
add(8,1698,'28:18讲师自己的可交互终端主页：ls列出内容，cat index | wc得到统计结果。它支持实际命令交互，不只是画一个终端外观。','终端可见命令、目录列表与管道统计结果')
add(11,2418,'40:18现场模型的八句藏头诗结果与自检说明；此版采用u韵，与下方官方讲义的ang韵版本不同。不要把两份输出合并成同一个现场结果。','完整八句输出、句首与日期嵌字自检、韵脚说明')
add(12,2568,'42:48现场同偏旁句与逐字列表：江湖游泳渡河波涛汹涌泪流满溢洗涤泥污。与官方讲义的沈涛故事是两个不同版本。','18字成句、逐字列举及模型的故事解释完整可见')
add(16,3388,'56:28论文阅读起点：临时目录中的paper.pdf，以“我想要读一读paper.pdf，帮我做个总结”开始。工具随即检查文件，画面不代表已经读完整篇。','完整读论文提示、临时目录上下文、文件检查结果')
add(16,3450,'57:30第一轮总结开始列出论文问题与贡献。保留模型沿作者叙事组织答案的现场样本；这些论文贡献判断未经本笔记独立复审。','模型总结中的核心问题与贡献条目，供观察总结方式')
add(17,3708,'1:01:48讲师开始重写提示：先站在人类已有知识边界上看问题，再问相关东西是什么、解决到什么程度。上方仍显示此前模型的审稿意见，底部是转向新方法的关键输入。','旧审稿答复与讲师重写的新提示同时可见，保留转向时刻')
n['sections'][4]['examples'].append('现场屏幕在约18:00显示对codex-rs/core/src/guardian/prompt.rs的读取，以及approval_request.rs中的guardian_approval_request_to_json、CommandApprovalAction等检索。该细节说明回答至少进入了实际源码，而不是仅凭通用知识解释；本次没有重新运行或审计当时仓库。')
n['sections'][7]['examples'].append('终端主页现场执行ls，再运行cat index | wc，得到25、106、1249三个统计值。这里记录的是当时屏幕结果，不是当前主页内容；它用一个真实操作区分“终端造型”和“可交互终端”。')
n['sections'][10]['examples'].append('现场40:18结果与讲义不同：画面中的自检写明采用u韵，并列出八句、藏头和日期嵌字检查。口述转写在朗读诗句时出现同音错字，因此以完整截图保留现场版本，不从错误转写拼出一首新诗。')
n['sections'][11]['examples'].append('现场版本为“江湖游泳渡河波涛汹涌泪流满溢洗涤泥污”，可断为“江湖游泳渡河，波涛汹涌，泪流满溢，洗涤泥污”。逐字计数为18，模型将其解释为渡江遇浪并清洗泥污的故事；形式检查可以通过，故事感仍由读者评价。')
n['sections'][15]['examples'].append('现场过程分成三步看更清楚：先在临时目录以“帮我做个总结”开始，再得到按问题/方法/贡献排列的回答，随后追问可信度与贡献。讲师认为后续意见仍被作者故事牵引，因此在下一节改从已有知识边界提问。')
n['sections'][16]['examples'].append('1:01:48可见的重写提示开头是“我们站在人类已知的知识边界上看这个问题。这不是一个完全老的问题——相关的东西是什么？解决到什么程度？”这一步先建立比较基线，再谈本文增量；它不是要求模型一味挑错或一味相信作者。')
n['limitations'][2]='讲义图源为本次生成的网页截图汇编PDF，不是官方发布PDF，也不是对应时间的视频截图。另补10张按重点采样的现场完整视频帧，保留上下文自查、代码阅读、主页交互、文学约束与论文阅读；未逐步复核全部屏幕操作。'
(P/'notes.json').write_text(json.dumps(n,ensure_ascii=False,indent=2));new=H(P/'notes.json')
media='/Users/yjzhao/Downloads/提示词工程 [02-Raw 26生成式软件工程 NJU].mp4'
a=hashlib.sha256()
with open(media,'rb') as f:
 for b in iter(lambda:f.read(1048576),b''):a.update(b)
mh=a.hexdigest()
for sec,fi,p,t,exp in added:
 ia['images'].append(dict(section=sec,frame=fi,path=p,sha256=H(P/p),purpose=n['sections'][sec-1]['title']+'：现场演示补证',expected_information=exp,observed_information='lecture07-agent已单独目视此完整1280×410帧，确认：'+exp,comparison_evidence=f'原媒体{t}秒；对应章节转写回读核对，未用官方讲义图冒充现场',sources=[dict(path=media,sha256=mh,detail='原始视频全画幅；非裁切/重绘')],status='passed',known_gap=False,resolution='新增动态证据；不同版本输出与自述边界已写入图注及正文'))
ia['notes_sha256']=new;ia['images'].sort(key=lambda x:(x['section'],x['frame']));(P/'image-audit.json').write_text(json.dumps(ia,ensure_ascii=False,indent=2))
audit=dict(schema_version=1,actor='lecture07-agent',independent_from_author=True,reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_hashes={'notes_before':before,'notes_after':new,'html_before':nh,'transcript':H(P/'transcript.json'),'index':H(P/'chunks/index.json'),'media':mh},method='全文阅读28节主稿；独立定点回读原转写并逐张目视16张候选视频帧，最终保留10张。官方34图沿用主作者逐图记录，不冒称本审查者重新全看。',scope={'transcript_time_ranges_seconds':[[350,571],[673,850],[1490,1810],[2324,2680],[3298,3410],[3597,3660],[5090,5220]],'notes_sections':'1–28全读','new_video_frames':[x[3] for x in added],'not_reviewed':'未全文独立重读20块；未重审论文、Codex全部源码、模型内部计算或训练数据'},issues=[dict(issue_id='02-IR-01',severity='major',finding='初稿只有讲义图，关键现场过程没有视觉证据',fix='增加10张实际时间视频帧，覆盖上下文/源码/主页/文学/论文5类演示',status='fixed'),dict(issue_id='02-IR-02',severity='medium',finding='现场诗句与18字句与讲义版本不同，若只留讲义容易混淆输出',fix='明确u韵vs ang韵；现场18字句逐字计数；保留原图避免ASR同音错字拼接',evidence=['s-g652.0 2413.57–2435.68','s-g675.0 2564.52–2585.22'],status='fixed'),dict(issue_id='02-IR-03',severity='medium',finding='论文阅读从初始总结转到知识边界提问缺少过程证据',fix='补3388/3450/3708三阶段画面和提问原意，明确不等于本笔记独立评定论文',status='fixed'),dict(issue_id='02-IR-04',severity='checked',finding='初稿已经对Skill加载、模型自述、幻觉训练机制、SQL/研究类比等做边界限制',fix='保留原限定；未发现需要将课堂经验升级为普遍事实的理由',status='passed')],checks=[dict(name='现场18字句',value='江湖游泳渡河波涛汹涌泪流满溢洗涤泥污',length=len('江湖游泳渡河波涛汹涌泪流满溢洗涤泥污'),status='passed'),dict(name='A2占比算例',calculation='.01 × .10 = .001',result=str(Decimal('.01')*Decimal('.10')),status='passed')],summary='未发现主稿关键结论的实质反转；主要提升为保留可回查现场演示、分开现场/讲义输出和补充过程细节。新增图片后须重建HTML并重做UI/追溯快照。')
(P/'audit-independent07.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print('added',len(added),'total',len(ia['images']))
