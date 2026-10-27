from pathlib import Path
import json,hashlib,datetime
r=Path('/tmp/gse08-lab2-materials')
h=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
vis=[(2,'Figure 1：完成权的归属；Humanize由reviewer COMPLETE加clean code review决定；底部应用数字非对照实验。'),(3,'Figure 2与公式：盲点交集图；m_R为条件漏检概率，论文只提供机制论证而非测得普遍准确率。'),(4,'Figure 3：实现阶段42轮上限；review阶段明确无上限；红箭头是不完成退出。'),(5,'Figure 4：builder提交代码/contract/summary，确定性hook检查后fresh reviewer看计划、历史和代码，不看builder推理；COMPLETE后仍有diff review。'),(7,'Figure 5：图左研究/优化/按shape专门化三阶段，KernelWiki和ncu-report-skill分别提供知识与性能证据；右图log scale、baseline 1x、single kernel、48h、team-reported，K-Search1.37/Humanize3.71/+Wiki6.14/+profiling8.58。'),(8,'Figure 6：纵轴review独立性、横轴oracle强度；公式b m_R m_O只覆盖被检查claim。'),(14,'Table1类别计数相加72；Table2分母118 postmortems，Present可多标签，Primary单标签；成本只有25报告涉及，不代表实际token成本已全面度量。')]
m={
'id':'humanize-2610.08900v2','kind':'paper','recommendation_kind':'core_source','required':True,
'scope_reason':'Lab2现行官方页面§2.1明确用其作为多模型求解/审查与内核优化的核心案例；材料补充不冒充第08课口述。',
'listed_title':'Humanize: Judgement Engineering for Agentic Coding','listed_url':'https://arxiv.org/abs/2610.08900',
'listing_source_url':'https://jyywiki.cn/GSE/2026/lab2.md','listing_location':'§2.1 算力换智力，Humanize案例段；原HTML /tmp/gse08-lab2.html 第17行',
'title':'Humanize: Judgement Engineering for Agentic Coding','authors':['Sihao Liu','Ligeng Zhu','Zijian Zhang','Dongyun Zou','Zhengyang Zhang','Changye Li','Song Bian','Song Han','Tony Nowatzki'],
'source_url':'https://arxiv.org/abs/2610.08900v2','pdf_url':'https://arxiv.org/pdf/2610.08900v2','version':'v2','version_date':'2026-10-08','identity_status':'verified','identity_note':'arXiv版本页、PDF首页标题/作者/arXiv v2标记一致。v1发表于2026-10-06，当前v2于2026-10-08更新。尚未核实课堂实际展示的是哪一版本，因此所有增量标现行官方材料与论文补充。',
'path':str(r/'humanize-v2.pdf'),'sha256':h(r/'humanize-v2.pdf'),'total_pages':14,
'reading_status':'full','read_pages':list(range(1,15)),'read_sections':['Abstract','1 Introduction','2 Judgement Engineering','2.1 Alternating Models as Joint Sampling','3 System Design','3.1 Planning as a Contract','3.2 The Round Protocol','3.3 Mechanical Gates','4 Deployment and Postmortem Study','5 Applications','6 Findings','7 Related Work','8 Limitations','9 Conclusion','Acknowledgments','References','Appendix A Mechanical Gates','Appendix B Corpus Coding'],
'visual_checks':[{'page':p,'path':str(r/f'page-{p:02}.png'),'sha256':h(r/f'page-{p:02}.png'),'detail':d} for p,d in vis],
'known_gaps':[],'related_items':['lecture-08'],'contributions':[],
'integration_status':'pending','integration_note':'补充草稿在supplements-draft.json；待主代理按实际课堂时间码和notes节号映射，复制到持久课程目录后刷新相对路径与contributions。',
'reading_evidence':{'text_path':str(r/'humanize-v2.txt'),'text_sha256':h(r/'humanize-v2.txt'),'sequential_read_line_ranges':[[1,220],[221,465],[466,715],[716,957]],'read_method':'对完整PDF按layout提取后顺序完整阅读，重要图表原页另实际目视；未递归阅读参考文献。','checked_at':now},
'validation_boundaries':['论文应用/赛事结果均作为论文作者报告转述，未独立重跑。','未以arXiv摘要代替全文。','未检验最新Humanize软件是否仍具备本版本描述的CLI兼容性或机制。','未读取下游KDA技术报告，KDA数字归因本论文§5团队自报。']}
alpha={'id':'alphazero-1712.01815','kind':'paper','recommendation_kind':'background_citation','required':False,'scope_reason':'官方Lab2 §2.1仅将问题搜索类比AlphaZero并立即说明开放任务缺少明确规则与胜负标准；不是要求掌握算法的明确推荐，故本轮不扩展完整旧论文。','listed_url':'https://arxiv.org/abs/1712.01815','identity_status':'unverified','version':None,'reading_status':'out_of_scope','read_pages':[],'read_sections':[],'related_items':['lecture-08'],'contributions':[]}
reg={'schema_version':1,'course_url':'https://jyywiki.cn/GSE/2026/','checked_at':now,'expected_material_ids':[m['id']],'materials':[m,alpha],'draft':True}
(r/'materials-draft.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
