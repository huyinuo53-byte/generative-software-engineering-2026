import pathlib,json,hashlib,shutil,datetime,subprocess,sys
C=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程');R=C/'lecture-08';rev=C/'revisions/20261019-new-08';S=pathlib.Path('/Users/yjzhao/.codex/skills/baocut-course-notes');now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();write=lambda p,x:pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
shutil.copy2('/tmp/gse08-harness-reading/delivery/delivery-sha256.json',R/'sources/harness-20261019/delivery-sha256.json')
write(R/'audits/evidence-path-map.json',{'purpose':'保留原独立报告不改写；将报告中制作期临时路径解析到本次冻结的永久副本。','mapping':{'/tmp/gse08-asr02.jsonl':'logs/asr-02-completed.jsonl','/tmp/gse08-visual/':'visual/','/tmp/gse08-materials/':'sources/official-20261019/','/tmp/gse08-harness-reading/delivery/':'sources/harness-20261019/','/tmp/gse08-content-review-early.json':'audits/gse08-content-review-early.json','/tmp/gse08-final-visual-review.json':'audits/gse08-final-visual-review.json','/tmp/gse08-event-binding-map.json':'audits/gse08-event-binding-map.json'}})
write(rev/'index-visual-review.json',{'status':'passed','reviewer':'root','index_sha256':sha(C/'课程索引.html'),'screenshots':['index-1280-new-card.png','index-390-new-card.png'],'observation':'实际目视两张新课卡片区域截图，排序08位于07之后、短片之前；30节/69图/16自测标识和手机换行清楚；两视口点击均进入正确新课。'})
# Update batch ledger to point at this revision; preserve previous record under before/.
batch=json.loads((C/'review.json').read_text());batch.update(index_validation='revisions/20261019-new-08/index-browser/audit.json',index_reader_validation='revisions/20261019-new-08/index-reader.json',index_sha256=sha(C/'课程索引.html'),final_trace_validation='revisions/20261019-new-08/trace-check.json',trace_snapshot='revisions/20261019-new-08/trace.json',latest_revision={'at':now,'review':'revisions/20261019-new-08/review.json','scope':'新增第08课，旧八篇保持字节不变；动态扩展索引清单，完成内容/图片/来源/浏览器验收。'})
write(C/'review.json',batch)
write(rev/'review.json',{'outcome':'completed','new_video':'BV11LWw6VEHW','lecture_review':'../../lecture-08/review.json','index_validation':'index-browser/audit.json','index_reader_validation':'index-reader.json','index_visual_review':'index-visual-review.json','preservation':'preservation.json','old_completed_videos_preserved':8,'new_completed_videos':1,'total_delivered':9,'current_playlist_videos':8,'preserved_unlisted':1,'updated_files':['../../lecture-08/','../../materials.json','../../manifest.json','../../review.json','../../build_index.py','../../课程索引.html'],'not_changed':'原有八篇课程产物和共享skill未修改；无commit/push/外部发布/新建自动化。','completed_at':now})
# Record current ownership as released after work finished; not included in immutable input graph.
o=json.loads((R/'ownership.json').read_text());o.update(status='released',released_at=now,reason='all required checks completed; reviewer agents finished; no active course writer');write(R/'ownership.json',o)
with (R/'events.jsonl').open('a') as f:
 f.write(json.dumps({'at':now,'run_id':'BV11LWw6VEHW-20261019','item_id':'lecture-08','actor':'root','stage':'delivery','status':'completed','evidence':['review.json','qa/browser/audit.json','qa/reader/visual-review.json'],'detail':'Final content and visuals reviewed; old8 kept; new index ready. Resource runtime24320 reused and left running.'},ensure_ascii=False)+'\n')
shutil.copy2('/tmp/gse08-freeze.py',R/'drafts/gse08-freeze.py');shutil.copy2('/tmp/gse08-index-journey.cjs',rev/'index-journey.cjs')
# Immutable graph: originals -> transcript/chunks and visual inventory -> authored notes -> HTML -> evidence/review.
exclude={'events.jsonl','ownership.json','trace-spec.json','trace-r01.json','trace-check.json'}
paths=[p for p in sorted(R.rglob('*')) if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts and '.audit.lock' not in p.parts]
external=[C/'materials.json',pathlib.Path('/Users/yjzhao/Downloads/GSE-08-BV11LWw6VEHW.mp4'),S/'scripts/course_notes.py',S/'scripts/reading_layout.py',*[S/'assets'/x for x in ['template.html','editorial.html','editorial.css','editorial.js']],*[S/'scripts'/x for x in ['validate_image_audit.py','validate_visual_coverage.py','validate_materials.py','validate_reading_layout.py','trace_artifacts.py']],C.parent/'scripts/audit-report.mjs']
paths+=external;ids={p:f'a{i:04d}' for i,p in enumerate(paths)};arts=[]
def refs(ps):return [ids[p] for p in ps]
source=[p for p in paths if p.is_relative_to(R/'sources') or p.is_relative_to(R/'logs')]
frames=[p for p in paths if p.is_relative_to(R/'visual') and p.suffix.lower() in ['.jpg','.png']]
chunks=[p for p in paths if p.is_relative_to(R/'chunks')]
authors=[p for p in paths if p.is_relative_to(R/'drafts') and p.name.startswith('gse08-author')]
for p in paths:
 deps=[];rel=str(p.relative_to(R)) if p.is_relative_to(R) else str(p)
 if rel=='transcript.json':deps=refs([R/'logs/asr-02-completed.jsonl',R/'sources/project-after-asr.json'])
 elif p in chunks:deps=refs([R/'transcript.json'])
 elif rel=='notes.json':deps=refs(chunks+source+authors+frames+[C/'materials.json'])
 elif rel=='reading-layout.json':deps=refs([R/'notes.json',R/'drafts/gse08-build.py'])
 elif rel=='课堂笔记.html':deps=refs([R/'notes.json',R/'reading-layout.json',*chunks,*[x for x in external if x.is_relative_to(S)],R/'drafts/gse08-polish-html.py'])
 elif rel in ['image-audit.json','visual-coverage.json']:deps=refs([R/'notes.json',R/'audits/gse08-final-visual-review.json',R/'audits/gse08-event-binding-map.json',*frames])
 elif p.is_relative_to(R/'qa'):deps=refs([R/'课堂笔记.html',C.parent/'scripts/audit-report.mjs'])
 elif rel=='review.json':deps=refs([R/'notes.json',R/'课堂笔记.html',R/'image-audit.json',R/'visual-coverage.json',R/'audits/content-review.json',R/'qa/browser/audit.json',R/'qa/reader/visual-review.json'])
 arts.append({'id':ids[p],'path':rel,'depends_on':list(dict.fromkeys(deps))})
write(R/'trace-spec.json',{'schema_version':1,'run_id':'BV11LWw6VEHW-20261019','basis':'observed_build','root':'.','artifacts':arts})
cmd=[sys.executable,str(S/'scripts/trace_artifacts.py')]
x=subprocess.run(cmd+['capture','--spec',str(R/'trace-spec.json'),'--out',str(R/'trace-r01.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr
x=subprocess.run(cmd+['check','--snapshot',str(R/'trace-r01.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr;write(R/'trace-check.json',json.loads(x.stdout))
# Batch graph covers current top-level ledger, index and old output bytes; individual source graph is checked above.
bpaths=[C/'manifest.json',C/'review.json',C/'materials.json',C/'build_index.py',C/'课程索引.html',R/'review.json',R/'notes.json',R/'课堂笔记.html',R/'trace-r01.json',rev/'preservation.json',rev/'review.json',rev/'index-browser/audit.json',rev/'index-reader.json',rev/'index-visual-review.json',*[C/i['html'] for i in batch['items'] if i['folder']!='lecture-08']]
write(rev/'trace-spec.json',{'schema_version':1,'run_id':'GSE-weekly-20261019','basis':'observed_build','root':'../..','artifacts':[{'id':f'b{i}','path':str(p.relative_to(C)),'depends_on':[]} for i,p in enumerate(bpaths)]})
x=subprocess.run(cmd+['capture','--spec',str(rev/'trace-spec.json'),'--out',str(rev/'trace.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr
x=subprocess.run(cmd+['check','--snapshot',str(rev/'trace.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr;write(rev/'trace-check.json',json.loads(x.stdout))
print(json.dumps({'lecture_trace_files':len(arts),'batch_trace_files':len(bpaths),'lecture_trace':'unchanged','batch_trace':'unchanged','outcome':'completed'}))
