# -*- coding: utf-8 -*-
import json,hashlib,datetime,shutil
from pathlib import Path
from PIL import Image
r=Path('/tmp/gse08-visual');inv=json.load(open(r/'visual-inventory.json'));dense=json.load(open(r/'dense-inventory.json'))
# This table records actual visual inspection, not transcript-derived speech.
spec=[
(0,42,'opening','讲义 Markdown 源码和空终端；课题 Agent Native 开发。',[]),
(42,104,'lab2-background','实验(2): Deeper Research 页面；背景内嵌 Master Bot/Morning Paper 应用截图。',[56]),
(104,242,'lab2-effort','实验要求：增加 effort，投入更多探索/查证/修改；左板书逐步画出 breadth-first 与 depth-first 探索。',[120,210,240]),
(242,334,'lab2-harness','网页搜索/评估流程图、Humanize: Judgement Engineering for Agentic Coding 标题、Workspace 循环；2.2 上下文工程；2.3 评估效果。URL 栏未显示。',[244,306]),
(334,526,'review-gaps','转到 Review & Comments；intent/spec/impl 与 essential/accidental complexity；左板逐步画出三层图及落差箭头。',[480,510]),
(526,670,'prototype','开始：构建原型；左板继续指向需求/规格/实现。',[]),
(670,914,'agent-loop','Agent Loop；自主模型与 bash tool；原型与品味话题。',[]),
(914,984,'agent-source-config','打开 agent.py，imports、读取 API key 的函数（未显示实际 key）、system prompt、bash tool schema。',[922]),
(984,1082,'agent-source-bash','bash 工具 schema，run_bash：subprocess.run、bash -c、stdin DEVNULL、合并 stdout/stderr、60 秒 timeout。',[1006]),
(1082,1154,'agent-source-loop','DeepSeek 流式请求；read_reply 拼接 reasoning/content/tool_calls；main 内层循环收到工具调用后运行 bash 并把 output 放回 messages。',[1098,1106]),
(1154,1216,'agent-build-card','启动 ./agent.py，输入 Hi；目录检查、读已有 HTML；生成 GSE 介绍卡 HTML、调用 xdg-open，随后检查 DISPLAY/浏览器。',[]),
(1216,1255,'gse-card','浏览器显示深色 GSE 介绍卡；滚动/鼠标和动画变化，保留页面成品而非每个动画帧。',[1218]),
(1255,1274,'pixel-check','Agent 用 grim 截图、Pillow 统计色彩与红黄绿灯像素，随后报告页面已显示；这是现场 Agent 的验证策略，不是本审查对其充分性的认可。',[1266]),
(1274,1466,'ralph-origin','Agent Loop/Ralph Wiggum/Ralph Loop 来回切换；左板新增 token/历史路径草图。',[1410]),
(1466,2010,'state-machine','Ralph Loop 与 Everything Is a State Machine；上下推拉黑板，下板逐步画状态/分支圈图。',[1830,1920]),
(2010,2084,'ralph-script','展示 ralf-loop.sh：每轮只推进明确步骤，留下文件，下轮重读；只有确认完成才输出 <RALPH_DONE>；grep -Fxq 决定 break。',[2020]),
(2084,2148,'ralph-round1','启动“世界上最好的编程语言”研究；curl 超时后重试/解析 TIOBE、PYPL；写 research/NEXT_STEPS.md 作为下一轮进度。',[2146]),
(2148,2161,'ralph-round2','新 MiniAgent 进程启动，读取目录和 NEXT_STEPS，继续研究 Stack Overflow/GitHub。',[]),
(2161,2264,'card-comparison','研究终端仍存在；前台在蓝紫 jyy 个性名片与橙色 jyy 名片间切换；这是两种已有页面的视觉比较，不能写成本轮语言研究的输出。',[2174,2220]),
(2264,2284,'ralph-stop','回终端，写研究报告及 NEXT_STEPS；输出自评与 <RALPH_DONE>，shell 返回。报告内数据为现场 Agent 结果，未独立核实。',[2276]),
(2284,2310,'ralph-report-read','Vim 打开 research/世界上最好的编程语言-调研报告.md；方法局限、场景推荐、来源和原始数据等。',[2300]),
(2310,2350,'second-research','又一次运行研究，屏幕显示 ./agent.py 启动（需结合转写确认与 Ralph 比较意图）；curl/HTML 解析，IEEE 返回正文含隐私/会员内容、GitHub 出现 Page not found。',[]),
(2350,2422,'state-discussion','回 Everything Is a State Machine 静态讲义。',[]),
(2422,2458,'second-research-result','新报告宣称调研完成；编程语言调研报告.md 与语言榜单原始数据.txt；打开两栏报告；不是独立事实查证结果。',[2440]),
(2458,2644,'transition-check','每次 Transition 都检查；短暂回 ralf-loop.sh，强调评价/验证结果与持续保持好状态。',[]),
(2644,2800,'ci-cd','祝贺你，发明了 CI/CD；CI、Continuous Delivery、Continuous Deployment。',[]),
(2800,2872,'hooks','Hook-Based CI/CD；讲义/CI-CD 页切换。',[]),
(2872,3010,'codex-ci-explore','Pi 在 ~/Projects/codex/.github 上阅读 workflows；右边浏览 rust-ci-full.yml，format/cargo shear/argument lint/Python tests/平台 matrix；左边 AI 总结复用 workflow、fan-in、Bazel 与 Cargo 等。',[2944,3008]),
(3010,3136,'lint-explain','现场追问“什么是 Lint？它重要吗”；AI 表格与文字说明测试 vs lint、工程卫生、CI 快门禁；一度全屏正文。',[3048]),
(3136,3162,'ci-business-rules','Hook-Based CI/CD→琐碎业务规则→把 CI/CD 写成 Spec，快速翻页。',[]),
(3162,3458,'agent-bias-ci','开发者不可信、CI 阻止/Agent 修正；左下板新增两个泳道与门禁图。',[3330]),
(3458,3574,'constraint-table','把 Agent 的偏执变成可执行的约束：六行表，自动检查与人工判断分列。',[3458]),
(3574,3694,'openai-harness','Agent Native 开发、OpenAI Harness engineering 网页实际打开/滚动：标题、架构示意、repository knowledge；回讲义“把品味做成机制”。',[3600]),
(3694,3780,'codex-ci-three-layers','返回现场 AI 的 Codex CI 三层解释：PR 门禁 / main 全量 / 发布；餐厅试吃员、深度质检、端菜类比与对照表。',[3742,3778]),
(3780,3832,'taste-mechanism','回把品味做成机制；What we’re still learning 选中强调。',[]),
(3832,3844,'stripe','Stripe Minions 讲义：混合节点，完整 CI 最多两轮；未打开 Stripe 原文。',[3834]),
(3844,4006,'compiler','Anthropic 16 个 Agent 卡同一 bug；左板从多个文件盒子到输出/Agent 分工画法渐进；GCC 构造可独立验证任务。',[3990]),
(4006,4044,'strongdm-intro','StrongDM 讲义短暂出现；Deepseek Harness 人物图；真正的经验；转回终端。',[4006]),
(4044,4196,'harness-docs','打开 deepseek-harness，ls 与 docs 双语文件；architecture.md：Cordis 插件、profile、bundle、启动形态。',[4168]),
(4196,4274,'bilingual-contract','Pi 探查 docs/i18n 与 scripts；部分查找 no such file；AI 回答 foo.md/foo.zh.md/foo.i18n.yaml 三件套、一致性门禁；右侧 README 双语切换。',[4230]),
(4274,4466,'bilingual-hashes','右侧 README.i18n.yaml 展示逐 heading slug 的 en/zh 哈希；左侧 AI 解释三件套、结构签名、正文变化重新配对；左板新增输入输出/文件配对示意。',[4350,4380]),
(4466,4666,'translation-taste','区分机器一致性与翻译审美；展示 docs/i18n/style-samples.md、terminology.md；AI 说明人工校准段落、术语、不译词、原写作与翻译两遍策略。',[4480,4530,4590,4620]),
(4666,4870,'history-archaeology','追问这套双语机制的历史；AI 读取 archived notes、git log、git show，报告六阶段演进和贡献者；右侧看初始提交。仅为现场 Agent 的仓库考古结果。',[4674,4722]),
(4870,5004,'harness-inventory','请求类似机制盘点；AI 读 AGENTS/notes/skills/scripts/snapshots，列常驻规则、生命周期 Agent Notes、skills、机械门禁、上下文组织、状态等十六项。',[4894,4932]),
(5004,5066,'skills-detail','另开 Pi 查 skills：工作流/门禁、写作/规范、工程质量、元技能、维护；产品内置 skills 与开发仓库 skills 分开。',[5032]),
(5066,5196,'review-detail','追问 code review；AI 读 GitHub policy、workflows、pre-push skill、PR template；解释本地自证→CI→人工签署和覆盖率、approved/changes requested/draft/pending 门禁。',[5080]),
(5196,5283,'harness-final-inventory','回十六项清单：verify 脚本与 run-gates、文档分层、schema、snapshot、先验证再落盘、model-visible≠logged、prototype API、多余思维痕迹、归档简化。',[5244]),
(5283,5410,'experience','Deepseek Harness 人物图与真正的经验讲义；黑板推拉重排，指向过去失败/架构探索。',[]),
(5410,5478,'failures','Friendster、Webvan/Quibi 讲义；可对照当前官方页，但不从画面推测所有文字已口述。',[]),
(5478,5718,'learning-opportunity','推论：Token→尝试机会、学习动机+能力；左板补画需求/实现图上的连线、划叉。',[5610]),
(5718,5808,'closing-images','学习机会断层插画；快速回真正的经验、Deepseek Harness、Friendster。',[]),
(5808,5829.674667,'closing-source','回终端/目录；重新打开 agent.py 到 main tool loop，视频到这里结束。',[5822,5828])]
events=[{'id':s[2],'start':s[0],'end':s[1],'observation':s[3],'native_reviewed_times':s[4],'speech_alignment':'pending parent transcript comparison'} for s in spec]
json.dump(events,open(r/'events.json','w'),ensure_ascii=False,indent=2)
base=inv['candidates'];allcs=base+dense['candidates'];boardwindows=[(120,242),(350,526),(1300,1414),(1648,1950),(3210,3458),(3860,4006),(4310,4410),(4560,4630),(5550,5640)]
# Observed full-frame duplicates during active writing cannot be silently discarded.
def ev(t):return next((e for e in events if e['start']<=t<e['end']),events[-1])
native=set(t for s in spec for t in s[4]);native.update([244,922,1006,1098,1106,1218,1266,2020,2146,2282,2300,2440,2944,3008,3048,3742,3778,4168,4230,4480,4530,4674,4722,4894,4932,5032,5080,5244,5822,210,480,1380,1830,1920,3330,3990,4350,4590,5580,240,510,1410,1890,2220,2164,4380,4620,5610,2276,2174,2010,5828,56,306,3458,3600,3834,4006])
selected=[56,120,244,306,510,922,1006,1098,1106,1218,1266,1410,1920,2020,2146,2174,2220,2276,2300,2440,2944,3048,3330,3458,3600,3742,3778,3834,3990,4006,4168,4230,4350,4380,4480,4530,4590,4674,4722,4932,5032,5080,5244,5610,5822]
selectedrows=[]
for t in selected:
 p=r/'scan'/f'sample-{int(t/2)+1:05}.jpg';id=next((c['id'] for c in base if c['time']==t),f't{t}');dst=r/'full'/f'{id}-{int(t):04}.jpg';shutil.copy2(p,dst);im=Image.open(p);cp=r/'crops'/f'{id}-{int(t):04}-screen.jpg';im.crop((550,0,1280,410)).save(cp,quality=95)
 selectedrows.append({'candidate_id':id,'time':t,'event':ev(t)['id'],'path':str(dst.relative_to(r)),'screen_crop':str(cp.relative_to(r)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'original_resolution_reviewed':True,'notes_targets':[],'selection':'recommended, final inclusion pending parent','legibility':'screen legible at native 730x410; handwriting partial and must be explained with transcript' if t in [510,1410,1920,3330,3990,4350,4590,5610] else 'key displayed text visually checked at original 1280x410; do not enlarge as if adding detail'})
json.dump(selectedrows,open(r/'selected-frames.json','w'),ensure_ascii=False,indent=2)
states=[]
for c in allcs:
 t=c['time'];e=ev(t);dup=c.get('automated_duplicate_of');b=any(lo<=t<hi for lo,hi in boardwindows);is_sel=t in selected and c['id'].startswith('v');transition=(c['id'] in ['v0025','v0026','v0041','v0051','v0124','v0171','v0447','v0707','v0708'])
 # Draft entries deliberately remain pending if a notes target is required.
 prop='included' if is_sel else 'represented_in_text'
 if dup and not b:prop='duplicate'
 if transition:prop='transition'
 states.append({'candidate_id':c['id'],'time':t,'disposition':'duplicate' if prop=='duplicate' else 'transition' if prop=='transition' else 'pending','proposed_disposition':prop,'description':e['observation'],'event':e['id'],'evidence':('native frame + ' if t in native else '')+('contacts/dense-'+str(dense['candidates'].index(c)//24+1).zfill(2)+'.jpg' if c['id'].startswith('d') else 'contacts/duplicates-* full-frame' if dup else 'contacts/contact-* right-screen')+'; full-frame overview reviewed separately','duplicate_of':dup if prop=='duplicate' else None,'automated_duplicate_rejected_for_board_review':bool(dup and b),'targets':[],'pending_targets':prop in ['included','represented_in_text'],'known_gap':False,'review_scope':'visual state/operation chain; not word-for-word OCR or spoken transcript verification'})
for c in base:c['manual_status']='visually_reviewed_pending_integration'
for c in dense['candidates']:c['manual_status']='visually_reviewed_dense_window';c['trigger']=['dense_transition_review']
inv['candidates']=allcs;inv['candidate_count']=len(allcs);inv['base_candidate_count']=len(base);inv['dense_candidate_count']=len(dense['candidates']);inv['unique_count_note']='518 base automated screen representatives; dense candidates retained without claiming semantic uniqueness';inv['dense']={'path':'dense-inventory.json','windows':len(dense['centers']),'interval_seconds':.5};inv['status']='visual_review_performed_pending_notes_integration';inv['method']['limitations'].append('Board auxiliary crop in first pass missed lower-board details; corrected by full-frame duplicate inspection + 60s overview + original-resolution checks of board stages. Screen-only duplicates in writing windows promoted for notes mapping.')
json.dump(inv,open(r/'visual-inventory.json','w'),ensure_ascii=False,indent=2)
dense['status']='all_272_contact_frames_visually_reviewed_pending_integration';json.dump(dense,open(r/'dense-inventory.json','w'),ensure_ascii=False,indent=2)
coverage={'schema_version':1,'notes_sha256':None,'inventory':{'path':'visual-inventory.json','sha256':hashlib.sha256((r/'visual-inventory.json').read_bytes()).hexdigest()},'media':inv['media'],'method':'Full 2s scan, right screen changes +30s fallback; all712 candidate contacts inspected;194 screen-duplicates also full-frame inspected;60s full-frame overview;34 selected transition windows0.5s/272 frames inspected;native-resolution key code/board checks. Not continuous playback or every-frame proof.','reviewed_windows':[{'start':0,'end':5829.674667,'evidence':'contacts/contact-01..26,duplicates-01..10,full-overview-01..05; events.json; native-frame-review.json'}]+[{'start':c-2,'end':c+2,'evidence':'dense-inventory.json and contacts/dense-01..12'} for c in dense['centers']],'states':states,'known_gaps':[],'limitations':['Low-resolution handwritten board words cannot all be transcribed. Preserve complete board image; explain only what transcript supports.','Terminal AI outputs are observed evidence of demonstration, not independent validation of repository behavior or fetched ranking facts.','Final notes targets, static-slide page mapping, captions and semantic coverage remain for main writer.','272 dense-frame timestamp labels are nominal fps-filter times, within a source-frame/half-sample convention; use integer 2s scan frames for exact final citations.'],'status':'pending_targets','pdf_pages':[],'pdf_pages_note':'Current official 24-page audit is independently delivered under /tmp/gse08-materials; final actual lecture mapping belongs to main writer.'}
json.dump(coverage,open(r/'visual-coverage-draft.json','w'),ensure_ascii=False,indent=2)
json.dump({'times':sorted(native),'method':'Opened actual full-resolution source scan frames through view_image; no synthetic sharpening','status':'performed_not_delivery_pass','handwriting':'Partial legibility only'},open(r/'native-frame-review.json','w'),ensure_ascii=False,indent=2)
json.dump({'video_id':inv['video_id'],'base_candidates':712,'dense_candidates':272,'all_visual_candidate_count':984,'visually_inspected_contact_count':984,'contact_sheets':53,'native_frames_count':len(native),'notes_targets_mapped':0,'status':'pending_notes_integration','not_claimed':['transcript review','final notes coverage','all board handwriting readable','every frame watched','source code repository independently checked']},open(r/'review-draft.json','w'),ensure_ascii=False,indent=2)
print('wrote',len(states),'states',len(selectedrows),'selected',len(events),'events')
