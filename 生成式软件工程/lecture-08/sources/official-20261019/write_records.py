# -*- coding: utf-8 -*-
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime,re
p=Path('/tmp/gse08-materials');now=datetime.datetime.now(datetime.timezone.utc).isoformat(); sha=lambda f:hashlib.sha256((p/f).read_bytes()).hexdigest()
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.aigc=[];self.depth=0;self.cur=[];self.all=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='a':self.links.append(a.get('href'))
  if t=='span' and a.get('class')=='aigc':self.depth+=1
 def handle_endtag(self,t):
  if t=='span' and self.depth:self.depth-=1;self.aigc.append(''.join(self.cur));self.cur=[]
 def handle_data(self,d):
  self.all.append(d)
  if self.depth:self.cur.append(d)
slides=json.loads((p/'slides-data.json').read_text());inventory=[]
for i,s in enumerate(slides,1):
 z=P();z.feed(s);inventory.append({'page':i,'text':''.join(z.all),'aigc_additions':z.aigc,'urls':z.links,'screenshot':f'slides/slide-{i:02}.jpg','sha256':sha(f'slides/slide-{i:02}.jpg')})
(p/'slide-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
desc=[
'复习两组主题：项目管理、需求与架构；标题和列表完整。',
'原型与假设；紫色 AIGC 区含 NASA 莱特兄弟例子，清晰完整。',
'Agent 自主性与模型能力限制；两组标题及条目完整。',
'Ralph 命名解释和人物插画；人物脚部保留、非讲者现场图。',
'循环示例三行代码完整，停止条件补充与原文链接可辨。',
'Workspace/State，Agent/Transition；完整显示末行长任务说明。',
'每次迁移验证；不可信开发者及可执行条件完整。',
'CI 历史和 CI/两种 CD 区别；底部三条定义保留。',
'Hook 事件、pre-commit 与远端门控两组完整。',
'琐碎规则含并行PR、flaky测试、override、部署倒序；末行 Spec 条件完整。',
'合并与发布条件；底部失败路径验收行完整。',
'Agent 偏执清单、CI纠正、jidoka类比及不可降标准完整。',
'纯图六行表：20KB文档/冗余抽象/扩大重构/可读性/改测试/关CI，各有自动检查与人工判断；表头和阈值脚注完整。',
'OpenAI来源、空仓库、知识外部化、独立应用实例；底部bug换行完整。',
'架构约束和持续清理；ClosedAI吐槽澄清原文确有lint/结构测试/CI。',
'Stripe确定节点与Agent节点及最多两轮完整CI说明，紫色表示当前讲义补充。',
'Anthropic16Agent同一Bug、GCC参照、组合失败边界完整。',
'StrongDM场景和DTU；末尾选课例子完整。',
'Deepseek Harness人物装备隐喻全身图完整；无架构数据，不能推断实际系统。',
'经验、架构假设、垃圾回收的边界完整。',
'Friendster读副本负载与按用户分片；组织实施的推论完整。',
'Webvan/Quibi背景材料；容量百分比与管理层自述归因可辨。',
'Token实践机会、学习动机能力、教育风险推论完整。',
'纯图：Token=0，尝试/失败在左，反馈/重构/未来大学在右；学习机会被截断，完整保留图中标注。']
audit={'checked_at':now,'source_url':'https://jyywiki.cn/GSE/2026/slides8.html','source_html_sha256':sha('slides8.html'),'label':'官方网页讲义截图汇编（2026-10-19冻结，非官方原生PDF，非录制时同秒画面）','method':'Chrome via cua_repl; each slide key navigation then reload restores same page with no-anim; full viewport 961x772 JPEG; all24 visually inspected','repair':'Early animation-shifted images replaced; final 1–24 captured after reload, no-anim.','pdf':{'path':'source-slides.pdf','sha256':sha('source-slides.pdf'),'pages':24,'method':'lossless embedding of the24 full JPEG screenshots, same order, no crop'},'images':[{'page':i,'path':f'slides/slide-{i:02}.jpg','sha256':sha(f'slides/slide-{i:02}.jpg'),'status':'passed','detail':d} for i,d in enumerate(desc,1)],'boundary':'This verifies current official slide image legibility/completeness only. Does not prove video visual coverage or oral attribution.'}
(p/'slide-image-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
entries=[
('ralph','Ralph Wiggum as a software engineer','2025-07-14 / retrieved2026-10-19',[5],['article正文全部，含 one item per loop、backpressure、TODO、build/plan prompts'], 'Ralph 不只是重复提示词：把规格和计划每轮重新提供，一轮集中一件事，以构建、测试和静态检查拒绝坏状态，把失败原因及测试为何存在写回文件。作者还强调先查已有实现，并承认新项目引导更适合、既有仓库使用存疑，仍需资深判断。文中大规模并行数字和乐观能力判断是个人经验与主张，不是本课应照搬的默认配置。'),
('ci','Continuous Integration (original version)','2000-09-10',[8],['article全部：Benefits至Summing up'],'CI 的核心是集成频繁且构建可重复：从统一版本源取出代码、脚本、配置及数据库定义，在干净环境自动构建并跑验证测试。每天尝试构建但长期失败不算成功实践；只编译也不足以确认行为。作者明确说测试不能证明没有Bug，且CI收益依据经验，文中增长倍数不是测量结论。'),
('cd','Continuous Delivery vs Continuous Deployment','2010-08-13',[8],['正文全部'],'持续交付意味着每个合格构建具备随时发布的条件，是否发布由业务决定；持续部署把合格构建实际交给用户。原文强调可发布不只意味着单元测试通过，还要验证生产近似环境、容量、安全、可用性和跨系统集成。硬件耦合或版本支持成本可能合理地限制发布频率。'),
('github-protection','About protected branches','current docs retrieved2026-10-19',[9,10,11],['About branch protection rules','Require status checks before merging','Require merge queue'],'分支保护才把检查结果变成合并约束。必需状态检查可能接受 successful、skipped 或 neutral，所以流程设计还要确认相关检查确实运行。默认管理员和可绕过角色可能不受限制，须按项目权限规则设置。strict要求与主干保持最新；merge queue验证主干加队列前序PR的组合。文档描述机制，不证明某仓库配置已生效。'),
('git-hooks','Git hooks manual: pre-commit','current docs retrieved2026-10-19',[9],['pre-commit'],'pre-commit 在提交前运行，非零退出会中止提交，但可由 --no-verify 跳过。因此它适合快速本地反馈，不能独自承担远端合并门控。这里只阅读与本课论点直接相关的 pre-commit 段落。'),
('github-pages','Using custom workflows with GitHub Pages','current docs retrieved2026-10-19',[11],['About custom workflows','Configuring configure-pages','Configuring upload-pages-artifact','Deploying artifacts','Linking separate build and deploy jobs'],'Pages 的构建与部署可以在同一工作流分作不同job；部署通过 needs 依赖构建，并部署已经上传的产物。应把测试和构建成功落实为依赖关系，而非只在提示词里要求先后顺序。原文要求 pages:write、id-token:write 和部署环境规则；当前Action版本不是课堂冻结配置。'),
('github-deployments','Deploying with GitHub Actions','current docs retrieved2026-10-19',[10],['Triggering your deployment','Using environments','Using concurrency及其示例'],'同一concurrency组最多一个运行任务，可取消过时的pending任务，cancel-in-progress可取消正在运行者。环境名与并发组不是自动绑定：同环境的另一个工作流若没声明相同并发规则，仍不受它约束。整理者建议：发布验收须测试重叠任务，不能仅凭有 concurrency 字段就断言旧版本不会覆盖新版本。'),
('minions','Minions: Stripe’s one-shot, end-to-end coding agents—Part2','2026-02-19',[16],['article正文全部：Devboxes至In conclusion'],'Stripe把已知必做工序编成确定节点，让Agent负责实现与修复；本地lint反馈前移，随后完整CI最多两轮，第二次后交回人类审查。自主运行的前提是隔离devbox、无生产用户数据、受限网络和工具权限。文中的1300+周合并PR是Stripe自报吞吐，仍由人类审查，不是通用成功率。原图需谨慎：正文将Fix CI failures称Agent节点，但示意图画为矩形，不能靠图形替作者解决这一不一致。'),
('compiler','Building a C compiler with a team of parallel Claudes','2026-02-05',[17],['article正文全部：Enabling long-running Claudes至Looking forward'],'16个Opus4.6 Agent起初在Linux编译同一错误上互相覆盖；作者用GCC编译大部分文件、新编译器编译子集，逐步缩小失败集合，才让工作分开。还需delta debugging找出单独通过但组合失败的文件。结果来自近2000会话、两周、约20亿美元输入token量为20亿（非美元）、1.4亿输出token及近2万美元API成本；不要混淆。该编译器仍借助GCC处理x86的16位启动代码，汇编链接器亦非完整自研，生成代码效率和Rust质量有限，不是成熟编译器替代品。'),
('strongdm','Software Factories And The Agentic Moment','2026-02-06',[18],['article正文全部'],'StrongDM以场景表达端到端用户故事，常将其放在实现仓库外作为留出验收，避免Agent通过修改狭窄测试制造全绿。对于含Agent的产品，satisfaction观察多条轨迹中可能满足用户的比例，依然依赖场景与评判质量。其不手写/不人工审代码和每天每人1000美元token是团队主张与实验文化，不是可靠工程的普适门槛。'),
('dtu','Digital Twin Universe','current page retrieved2026-10-19',[18],['页面全文：Why DTU、四项优势、How It Works'],'DTU复制的是依赖服务边界上的可观察行为；先从API合同和边界案例做替身，再与真实依赖对照，直到不再找到行为差异。这样能高频重放场景、测试真实生产上危险或昂贵的故障。它不声称穷尽所有真实服务行为；替身和真实系统的差距仍会限制验收结论。'),
('friendster','Unorthodox approach to database design Part2:Friendster','2006-11-09',[21],['作者正文全文（不将评论当作者结论）'],'亲历工程师指出，完整从库仍要重放所有写入，大数据集和I/O会产生复制延迟；提出按用户分片，缩小每台数据规模并分散写负载，配对复制提供可用性。文中说组织环境未让方案在Friendster落地，后在Flickr采用。这是工程师回顾，不能单独解释公司兴衰；跨分片关联和迁移成本也不能从该短文视为已解决。'),
]
urls=json.loads((p/'source-urls.json').read_text());m=[]
for key,title,ver,pg,sections,summary in entries:
 file=key+'.html';m.append({'id':'gse08-'+key,'listed_title':title,'title':title,'listed_url':urls[key],'source_url':urls[key],'version':ver,'kind':'web','identity_status':'verified','recommendation_kind':'core_source' if key not in ['friendster'] else 'background_citation','required':key!='friendster','scope_reason':'直接支撑当前官方讲义核心机制；网页限声明章节' if key!='friendster' else '当前讲义背景案例，已额外阅读作者正文，不扩为数据库课程','path':file,'sha256':sha(file),'scope_sections':sections,'read_sections':sections,'reading_status':'full','slide_pages':pg,'known_gaps':[],'proposed_supplement':summary,'integration_status':'pending_parent_assignment','contributions':[]})
# Sources recovered with web tool: retain its line-numbered retrieval verbatim, not fake original HTML.
m.extend([
{'id':'gse08-harness','listed_title':'Harness engineering: leveraging Codex in an agent-first world','title':'Harness engineering: leveraging Codex in an agent-first world','listed_url':urls['harness'],'source_url':urls['harness'],'version':'2026-02-11 / retrieved2026-10-19','kind':'web','identity_status':'verified','recommendation_kind':'core_source','required':True,'path':'web-retrieval.json','sha256':sha('web-retrieval.json'),'source_format':'web tool line-numbered retrieval; direct HTTP403','scope_sections':['article正文全部，从We started with an empty git repository到What we are still learning'],'read_sections':['article正文全部，从We started with an empty git repository到What we are still learning'],'reading_status':'full','slide_pages':[14,15],'known_gaps':[],'proposed_supplement':'OpenAI把AGENTS.md做导航，知识放入版本化仓库；每工作区独立运行应用并开放UI、日志和指标给Agent；通过lint/结构测试守住依赖边界并持续小规模清理。原文同时采用较少阻塞合并门控，不等于没有CI；也承认多年架构一致性尚未知。这是特定内部产品经验，不能直接泛化为所有项目的最优规则。','integration_status':'pending_parent_assignment','contributions':[]},
{'id':'gse08-webvan','listed_title':'Webvan 2000 Form10-K','title':'Webvan Group, Inc. Form10-K, year ended2000-12-31','listed_url':urls['webvan'],'source_url':urls['webvan'],'version':'2000 Form10-K / SEC accession0001012870-01-001485','kind':'web','identity_status':'verified','recommendation_kind':'background_citation','required':False,'scope_reason':'仅核对讲义22页容量与亏损背景，不扩展为整份财报阅读','path':'webvan-source-excerpts.json','sha256':sha('webvan-source-excerpts.json'),'source_format':'web tool retrieved original SEC text excerpts','scope_sections':['Item7风险：需额外资本（印刷页18）','高容量业务系统未验证（印刷页21）'],'read_sections':['Item7风险：需额外资本（印刷页18）','高容量业务系统未验证（印刷页21）'],'reading_status':'full','slide_pages':[22],'known_gaps':['未读取整份年报；不得声称全文已读'],'proposed_supplement':'2000年报区分两类设施：配送中心低于原设计容量40%，CFC低于70%；且当时尚无设施现金流盈利。应写配送中心而非所有设施都低于40%。这些披露支持需求/设施失配的讨论，不能据此把破产归因于单一技术架构。','integration_status':'pending_parent_assignment','contributions':[]},
{'id':'gse08-quibi','listed_title':'An open letter from Quibi','title':'An open letter to the employees, investors, and partners','listed_url':urls['quibi'],'source_url':urls['quibi'],'version':'2020-10-21','kind':'web','identity_status':'verified','recommendation_kind':'background_citation','required':False,'scope_reason':'仅核对关停声明和管理层归因，不扩展到Quibi商业史','path':'web-retrieval.json','sha256':sha('web-retrieval.json'),'scope_sections':['声明主体网页行41–67'],'read_sections':['声明主体网页行41–67'],'reading_status':'full','slide_pages':[22],'known_gaps':['未将订阅UI、作者页及评论纳入阅读'],'proposed_supplement':'Quibi管理层宣布结束业务，并把失败可能归为独立流媒体构想不足、或推出时机，也明确表示无法确知。可用于提醒实现完成不等于独立产品需求成立；不能改写成已证实的单一失败因果。','integration_status':'pending_parent_assignment','contributions':[]}
])
for x in m:
 if x['id']=='gse08-compiler':x['proposed_supplement']=x['proposed_supplement'].replace('约20亿美元输入token量为20亿（非美元）','20亿输入token')
ledger={'schema_version':1,'course_url':'https://jyywiki.cn/GSE/2026/','checked_at':now,'item':'lecture-08','video_id':'BV11LWw6VEHW','mapping_evidence':{'course_title':'生成式软件工程（2026秋）','lecture_number':8,'title':'Agent Native 开发','course_html':'course.html','lecture_url':'https://jyywiki.cn/GSE/2026/lect8.md','slides_url':'https://jyywiki.cn/GSE/2026/slides8.html','mapping_note':'官网第8项明确链接lect8.md/slides8.html且标题一致；视频BV身份来自主代理，未由本子任务重新核对视频。'},'expected_material_ids':[x['id'] for x in m if x['required']],'materials':m,'scope_boundary':'已盘点当前官网/讲义全部链接；尚须主代理逐块转写补入课堂口述明确推荐及材料。未把来源文章内部视频推荐递归扩成课程推荐。未调用课程成品验收器，整合尚未发生。','unread_background_links':[{'url':u,'reading_status':'out_of_scope','recommendation_kind':'background_citation','required':False,'scope_reason':'当前讲义中的历史/命名/类比/工具入口，不是明确推荐；不扩展本课核心方法阅读。若转写明确推荐则须重新纳入。'} for u in sorted(set(u for x in inventory for u in x['urls'])-set(urls.values()))]}
(p/'materials-draft.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
print('created',len(m),'materials; slides',len(inventory))
