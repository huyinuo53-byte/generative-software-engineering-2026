# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime
p=Path('/tmp/gse09-visual');sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest();write=lambda name,x:(p/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inv=json.loads((p/'visual-inventory.json').read_text());selected=json.loads((p/'selected-frames.json').read_text());byid={x['candidate_id']:x for x in selected}
for x in selected:
 x['original_resolution_reviewed']=True
 x['reviewer']='gse09_visual_20261026'
 x['review_method']='Native1280x410 original full-frame inspected via view_image; matched contact sequence, dense transition where needed.'
 if x['candidate_id']=='v0524':x['caption_draft']='五子棋卡片开始交互后的首枚黑子，后续模型响应围绕此棋盘状态更新。'
 x['legibility']='投影和UI主要状态可辨；细小代码只按可见局部解释，不能由此逐字还原完整源码。'
write('selected-frames.json',selected)
# These manually identified semantic windows were reviewed against the contact sheets, not inferred as chapters.
e=[
(0,188,'review','软件工程/需求架构/Agent-native复习；Intent分支与系统板书',[1,2]),
(188,238,'conference','DeepSeek Harness活动照片',[3]),
(238,328,'lecture-source','原始讲义Markdown导航，准备运行Agent',[]),
(328,374,'greeting','Greeting会话回应身份与工作目录',[]),
(374,452,'miniagent','miniagent.py工具协议与bash执行函数',[]),
(452,618,'campus','3D校园全景、旋转、缩放和建筑局部',[]),
(618,758,'requirements','150行Agent工作与网络中断问题',[4]),
(758,874,'api-retry','API中断、可重试/不可重试/结果未知与幂等问题',[5]),
(874,926,'many-requirements','Agent周边能力与需求规格入口',[6]),
(926,1029,'product-spec','办公Agent规格v1.0（2026-10-18）：场景、功能、非功能、验收与发布要求',[]),
(1029,1076,'loop-world','小Agent循环被权限/预算/恢复等真实需求包围',[7]),
(1076,1156,'grok-bot','Grok Bot改变需求的课堂例子',[8]),
(1156,1332,'dsh-bot','dsh-bot角色接续与协作界面',[9]),
(1332,1412,'origin','项目2026-06-10起点与AGENTS/README初始化',[10]),
(1412,1888,'architecture-tradeoff','架构限制与收益；模块/流水线/进程示意板书逐步形成',[11]),
(1888,1982,'assumptions','架构假设失效及电力改变组织的例子',[12]),
(1982,1992,'ai-acceleration','AI产业加速器页',[13]),
(1992,2016,'abstraction-gallery','快速查看OS/语言/LAMP/EventSourcing/MapReduce/Spark/Flink架构例子',[14,15,16,17,18,19]),
(2016,2190,'mapreduce-paper','MapReduce原文词频伪代码、执行图及C++Appendix浏览',[]),
(2190,2298,'mapreduce-and-streaming','返回MapReduce、Spark、Flink架构与边界',[18,19]),
(2298,2304,'event-sourcing','Event Sourcing回放边界页',[17]),
(2304,2310,'architecture-return','短暂返回架构取舍和讲义源码',[11]),
(2310,2520,'everything-plugin','Everything Is a Plugin、Cordis以及插件化世界模型板书',[20]),
(2520,2842,'world-and-explanation','Session事实记录；现场Agent解释session、LLM、tools、scope、events',[21]),
(2842,2904,'free-thought','切回世界模型页与自由思考的现场Agent输出',[21]),
(2904,2942,'trajectory','Trajectory上下文、bash调用参数、结果与Timing',[]),
(2942,2974,'tool-reply','工具执行后模型总结目录和环境；输出属于当前会话',[]),
(2974,3027,'session-projection','Session从事实到投影，穿插Trajectory回查',[21,22]),
(3027,3070,'agent-inputs','followup/inject/steer及动态上下文',[23]),
(3070,3164,'hooks','pending决策hook与已发生事实事件的区别',[24,22]),
(3164,3204,'plugin-bus','总线图说明业务插件、Agent/Loop、LLM/Tools和Session投影',[25]),
(3204,3300,'plugin-ecosystem','TUI/pdf-reader/sidebar/Creator的插件生态入口',[26]),
(3300,3404,'greeting-return','Greeting、原有临时文件与侧栏入口',[]),
(3404,3500,'panels','Files/Terminal/SideChat面板及布局切换',[]),
(3500,3616,'modes','Standard/PTC/Minimal/Creator模式菜单及Creator任务输入',[26]),
(3616,3774,'creator-execution','Creator读代码、写插件文件、安装审批、停止与追加改要求',[]),
(3774,3928,'plugin-cost','插件语义冲突、顺序与作用域，1/2连续压缩10次示例',[27]),
(3928,3962,'dashboard','Agent完成声明、文件变化和累计token仪表盘',[]),
(3962,4048,'community','维护和生态、最终用户工具包',[28]),
(4048,4168,'app-ai','为已有App加入AI能力，lock/serialize/UI的抽象',[29]),
(4168,4354,'turtle','Excalidraw原有图形→AI侧聊→绿色乌龟→结构对象选择',[29]),
(4354,4442,'genui-intro','GenUI：Session卡片与模型的双向通道',[30]),
(4442,4650,'idiom','成语接龙卡片：HTML、初始候选、选择反馈、上下文回传与下一轮候选',[]),
(4650,4778,'gomoku','五子棋卡片：棋盘、落子、模型回应、显示/事件问题与调试',[]),
(4778,4888,'canvas-implementation','Excalidraw插件与dsh WebServer、iframe、Cordis服务的实现解释',[]),
(4888,5038,'dynui-implementation','dynui上下文注入/消息截断、公开API与实现边界的现场解释',[]),
(5038,5110,'scope','scope隔离、工具限制与各层影响范围',[]),
(5110,5363.541375,'summary-board','pending决策、应用锁与Agent自身世界区别；收束板书',[])]
events=[]
for i,(a,b,key,desc,pages) in enumerate(e,1):events.append({'id':f'e{i:02d}','key':key,'start':a,'end':b,'description':desc,'official_slide_pages':pages,'boundary_note':'semantic review window boundary; exact screenshot time in selected-frames','review_status':'reviewed'})
write('events.json',events)
# Draft dispositions are checked visually but await actual authored-note target binding by the coordinator.
states=[]
for c in inv['candidates']:
 event=next(x for x in events if x['start']<=c['time']<x['end']);row={'candidate_id':c['id'],'event_id':event['id'],'event_key':event['key'],'time':c['time'],'description':event['description'],'reviewer':'gse09_visual_20261026','known_gap':False,'targets':[],'evidence':'All representative and duplicate contact panels read; selected pedagogical images reviewed at native size. See native-frame-review.json and contact-review.json.'}
 if c['id'] in byid:
  s=byid[c['id']];row.update(disposition='included',selected_path=s['path'],selected_time=s['time'],selected_sha256=s['sha256'],caption_draft=s['caption_draft'])
 elif c['automated_duplicate_of']:
  row.update(disposition='duplicate',duplicate_of=c['automated_duplicate_of'],comparison_scope='projected screen pedagogical state; lecturer motion excluded. Board stages separately retained as full selected images.')
 elif event['official_slide_pages'] and event['key'] not in ['world-and-explanation','plugin-ecosystem','modes','turtle','session-projection']:
  row.update(disposition='official_page',official_slide_pages=event['official_slide_pages'],binding_required='Coordinator must match actual selected official slide page(s) and authored notes; this is not a claim all page text was orally spoken.')
 else:
  row.update(disposition='represented_in_text',binding_required='Coordinator must bind to actual chapter/explanation. Intermediate scrolling/waiting and model-generation text need not all be separate images; distinct interaction states retained in selected frames.')
 states.append(row)
inv['status']='visually_reviewed_pending_notes_binding';inv['reviewed_candidate_count']=len(states);inv['review_method_note']='634 candidates all visually screened through24 right-screen representative sheets,10 full-frame duplicate sheets and15 full-frame30s fallback sheets. Selected62 all inspected at native1280x410;117 dense frames screened around13 rapid transitions.'
write('visual-inventory.json',inv)
dense=json.loads((p/'dense-inventory.json').read_text());dense['status']='visually_reviewed';dense['review_notes']=['Trajectory shows only briefly at2904.5–2905.5 then returns to Chat; final image uses2905.','Bash Payload appears2933–2935; summary-only2932 rejected for parameters.','Files view begins3419; final uses3421.','Mode menu shown3523–3524.5; final3524; menu saysPTC, notPlan.','Turtle appears by4250 and consists of separate editable objects.','First idiom card preview4443 is subsecond and immediately followed bysource-code scroll; redundant preview omitted in favor4478full initial card.','Clicking initial idiom4501 shows red immediate feedback; later model-generated card carries new choices.','At4650still idiom,4651first Gomoku partial viewport;4658first black stone selected.','Gomoku transient reduced-row display and AI-thinking prompt are preserved as failure state, not successful game proof.'];write('dense-inventory.json',dense)
contactfiles=sorted((p/'contacts').glob('*.jpg'))
write('contact-review.json',{'reviewer':'gse09_visual_20261026','status':'reviewed','sheets':[{'path':str(q.relative_to(p)),'sha256':sha(q),'reviewed':True} for q in contactfiles],'counts':{'right_screen_representative_sheets':24,'full_frame30s_fallback_sheets':15,'full_frame_automated_duplicate_sheets':10,'dense_transition_sheets':7},'scope':'Contact sheets used only for navigation/coverage; selected originals reviewed separately; not per-second continuous playback.'})
observations={
'v0009':'复习页两组条目和Brooks紫色补注可见；教师部分遮挡左板，板书另以后续全幅保留。',
'v0019':'模型回复和当前目录均完整可见，已经不是加载中的“你是谁”状态。',
'v0100':'FR05文档生成/修改与FR06表格计算局部可读，原拟caption停止恢复已纠正。',
'v0107':'NFR01–NFR09条目、P95以及1秒/8秒/2秒等目标可读；NFR10在画面底部开始，完整规格需读原文。',
'v0152':'上下板均见多块/箭头示意，右投影保留架构限制和所得能力。',
'v0194':'Mapper主体可见；Reducer仅开头，caption明确局部，不宣称整段代码齐全。',
'v0262':'原尺寸确认Trajectory及USER/CONTEXT/ASSISTANT链在2905出现，2908已返回Chat，采用2905。',
'v0274':'选中Payload页签，description与command字段可读。',
'v0284':'Trajectory中CONTEXT、USER、ASSISTANT与3条TOOL记录同时可见。',
'v0347':'菜单原文是PTC mode，非Plan；Standard/Minimal/Creator均可见。',
'v0390':'Waiting for approval、操作名install_bundle以及Reject/Allow once可见；未操作真实审批。',
'v0396':'Stopped和用户随后新指令可见；仪表盘1.2M是现场读数。',
'v0457':'龟壳/头部/尾巴/鳍足标签明确，确认是乌龟，非导航初判的鸟。',
'v0462':'多对象边框与选中控件可见，支持结构化画布对象解释。',
'v0486':'初始成语8个候选和底部提示都完整可见；是放大卡片界面，不宣称OS独立窗口。',
'v0490':'点击惊弓之鸟后红色“就以…开局”反馈可见；红色不等于代码错误。',
'v0524':'五子棋卡片可见首枚黑子，棋盘局部受当前视口/输入框遮挡；完整后续棋盘另保留v0544。',
'v0539':'只较少棋盘行与AI思考中，按真实失败状态保留。',
'v0544':'黑白两子及后续棋盘状态可见，仍不足证明整局合法或所有交互通过。',
'v0573':'观察/取消/落盘/生命周期行可见；上方入口表格不在本帧全部展示。',
'v0604':'屏幕说明前一轮“棋盘被截断”来自事件构造/处理，不是dynui本身；只作为现场Agent解释。',
'v0608':'scoped上下文检查及报错文本可读；不由截图宣称已经验证真实权限隔离。',
'v0633':'结束前黑板上下板完整构图与屏幕的收束解释可见。'}
images=[]
for s in selected:
 images.append({'candidate_id':s['candidate_id'],'path':s['path'],'sha256':s['sha256'],'time':s['time'],'purpose':s['caption_draft'],'expected_information':s['caption_draft'],'observed_information':observations.get(s['candidate_id'],'原尺寸实际目视：'+s['caption_draft']),'comparison_evidence':'Matched full timeline sequence and native frame; rapid transitions additionally inspected throughdense0.5sec frames where listed.','visual_status':'passed','known_gap':False,'notes_binding':'pending','limitation':s['legibility']})
write('native-frame-review.json',{'status':'visual_review_passed_pending_notes_binding','reviewer':'gse09_visual_20261026','selected_count':len(images),'images':images,'superseded_frame_corrections':[{'candidate_id':x['candidate_id'],**x['correction'],'final_time':x['time'],'final_path':x['path']} for x in selected if x.get('correction')],'excluded_initial_preview':{'candidate_id':'v0478','reason':'native exact4443.5 shows sourcecode, while preview only briefly visible4443; full initialcard captured4478 (v0486) and feedback4501(v0490).'}})
coverage={'schema_version':1,'notes_sha256':None,'inventory':{'path':'visual-inventory.json','sha256':sha(p/'visual-inventory.json')},'media':inv['media'],'method':inv['review_method_note']+' Navigation fps samples are approxwithin1s; all delivered selected images exactseek and reviewed.','reviewed_windows':[{'start':0,'end':5363.541375,'evidence':'contact-review.json; native-frame-review.json; dense-inventory.json'}],'states':states,'pdf_pages':[],'known_gaps':[],'status':'pending_notes_binding','required_next':['bind notes_sha256 and each included/official_page/represented_in_text target to actual authored notes','review images against finalcaptions and section mapping','official30pages exactmatch audit by main author','run validate_visual_coverage.py after binding'],'limits':['2-second scan and13densewindows do not prove every subsecond event found','notcontinuous per-second playback or per-frame humanreview','source1280x410limits tiny handwriting/code legibility; screenshots preserve originalviewport, notfull source documents','currentofficialslide AIGC class does not establish post-recording additions; many purple annotations demonstrably appeared in this recording']}
write('visual-coverage-draft.json',coverage)
write('review-draft.json',{'status':'visual_source_review_complete_delivery_binding_pending','reviewer':'gse09_visual_20261026','media_sha256':inv['media']['sha256'],'source_samples':2682,'candidates':634,'selected_final':62,'dense_frames':117,'native_all_selected_reviewed':True,'remaining':['notes targets/SHA','officialpages matching and finalimageaudit binding','mainauthorsemantic review and HTML/browser checks'],'tokens':None,'cost':None})
print('sealed',len(selected),'selected',len(states),'states',len(contactfiles),'contact sheets')
