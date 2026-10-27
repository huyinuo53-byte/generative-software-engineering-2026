from pathlib import Path
import json,hashlib,shutil,datetime,subprocess,sys
C=Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程');R=C/'lecture-09';V=C/'revisions/20261026-new-09';S=Path('/Users/yjzhao/.codex/skills/baocut-course-notes');now=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();wr=lambda p,x:Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
shutil.copy2('/tmp/gse09-finalize.py',R/'drafts/finalize.py');shutil.copy2('/tmp/gse09-freeze.py',R/'drafts/freeze.py');shutil.copy2('/tmp/gse09-index-journey.cjs',V/'index-journey.cjs');shutil.copy2('/tmp/gse09-all-materials-validation.json',R/'audits/course-materials-validation.json')
wr(V/'index-visual-review.json',{'status':'passed','reviewer':'root','index_sha256':sha(C/'课程索引.html'),'screenshots':[{'path':f'index-{w}-new-card.png','sha256':sha(V/f'index-{w}-new-card.png')} for w in [1280,390]],'observation':'两视口实际目视，09卡片位于08后、短片前；32节92图15自测可读，真实点击进入正确新课。','initial_check_issue':'初次读者脚本在导航后立即统计未完成解析的DOM，已保留失败记录；等待load后两视口均92图且通过。'})
b=json.loads((C/'review.json').read_text());b.update(index_validation='revisions/20261026-new-09/index-browser/audit.json',index_reader_validation='revisions/20261026-new-09/index-reader.json',index_sha256=sha(C/'课程索引.html'),final_trace_validation='revisions/20261026-new-09/trace-check.json',trace_snapshot='revisions/20261026-new-09/trace.json',latest_revision={'at':now,'review':'revisions/20261026-new-09/review.json','scope':'新增第09课；旧九篇HTML保持字节不变，来源与审查历史保留。完整正文/图片/材料/桌面与窄屏验收完成。'});wr(C/'review.json',b)
wr(V/'review.json',{'outcome':'completed','new_video':'BV144nc6KEA4','lecture_review':'../../lecture-09/review.json','index_validation':'index-browser/audit.json','index_reader_validation':'index-reader.json','index_visual_review':'index-visual-review.json','preservation':'preservation.json','old_completed_videos_preserved':9,'new_completed_videos':1,'total_delivered':10,'current_playlist_videos':9,'preserved_unlisted':1,'updated_files':['../../lecture-09/','../../materials.json','../../manifest.json','../../review.json','../../build_index.py','../../课程索引.html'],'scope':'新课独立验收；旧产物历史证据复用，不冒充重新阅读或重测整套课程。','completed_at':now})
o=json.loads((R/'ownership.json').read_text());o.update(status='released',released_at=now,reason='新课作者、材料、视觉和终审代理已结束，所有必要检查通过。');wr(R/'ownership.json',o)
with (R/'events.jsonl').open('a') as f:
 for stage,evidence in [('project_identity','sources/project-create.json'),('asr','logs/asr.jsonl'),('transcript_reading','audits/transcript-reading.json'),('materials','audits/material-integration.json'),('visual_review','visual-coverage.json'),('content_review','audits/content-review.json'),('browser_review','qa/reader/visual-review.json')]:
  f.write(json.dumps({'at':now,'occurred_at':None,'time_basis':'retrospective','run_id':'BV144nc6KEA4-20261026','item_id':'lecture-09','actor':'root','stage':stage,'attempt_id':stage+'-01','job_id':None,'status':'completed','evidence':evidence,'reason':'终审封存时补记；原始日志/独立报告保留，未反推精确阶段耗时。'},ensure_ascii=False)+'\n')
 f.write(json.dumps({'at':now,'occurred_at':now,'time_basis':'observed','run_id':'BV144nc6KEA4-20261026','item_id':'lecture-09','actor':'root','stage':'delivery','attempt_id':'delivery-01','job_id':None,'status':'completed','evidence':['review.json','qa/browser/audit.json','qa/reader/visual-review.json'],'reason':'新课与索引均验收；runtime为复用服务，保持运行；已关闭本次Chrome源标签。'},ensure_ascii=False)+'\n')
exclude={'events.jsonl','ownership.json','trace-spec.json','trace-r01.json','trace-check.json'}
paths=[p for p in sorted(R.rglob('*')) if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts and p.name!='.audit.lock']
external=[C/'materials.json',Path('/Users/yjzhao/Downloads/DeepSeek Harness (1) [09-Raw 26生成式软件工程 NJU].mp4'),S/'scripts/course_notes.py',S/'scripts/reading_layout.py',*[S/'assets'/x for x in ['template.html','editorial.html','editorial.css','editorial.js']],*[S/'scripts'/x for x in ['validate_image_audit.py','validate_visual_coverage.py','validate_materials.py','validate_reading_layout.py','trace_artifacts.py']],C.parent/'scripts/audit-report.mjs']
paths+=external;ids={p:f'a{i:05d}' for i,p in enumerate(paths)};refs=lambda ps:[ids[p] for p in ps];arts=[]
source=[p for p in paths if p.is_relative_to(R/'sources') or p.is_relative_to(R/'logs')];chunks=[p for p in paths if p.is_relative_to(R/'chunks')];frames=[R/f['path'] for s in json.loads((R/'notes.json').read_text())['sections'] for f in s['frames']]
for p in paths:
 rel=str(p.relative_to(R)) if p.is_relative_to(R) else str(p);deps=[]
 if rel=='transcript.json':deps=refs([R/'logs/asr.jsonl',R/'sources/project-final.json'])
 elif p in chunks:deps=refs([R/'transcript.json'])
 elif rel=='notes.json':deps=refs(chunks+source+frames+[R/'drafts/author.py',R/'drafts/build.py'])
 elif rel=='reading-layout.json':deps=refs([R/'notes.json',R/'drafts/build.py'])
 elif rel=='课堂笔记.html':deps=refs([R/'notes.json',R/'reading-layout.json',R/'drafts/render.py',*chunks,*frames,*[x for x in external if x.is_relative_to(S)]])
 elif rel in ['image-audit.json','visual-coverage.json']:deps=refs([R/'notes.json',R/'visual/native-frame-review.json',R/'visual-inventory.json',*frames])
 elif p.is_relative_to(R/'qa'):deps=refs([R/'课堂笔记.html',R/'drafts/reader-journey.cjs',C.parent/'scripts/audit-report.mjs'])
 elif rel=='review.json':deps=refs([R/'notes.json',R/'课堂笔记.html',R/'image-audit.json',R/'visual-coverage.json',R/'audits/content-review.json',R/'qa/browser/audit.json',R/'qa/reader/visual-review.json'])
 arts.append({'id':ids[p],'path':rel,'depends_on':list(dict.fromkeys(deps))})
wr(R/'trace-spec.json',{'schema_version':1,'run_id':'BV144nc6KEA4-20261026','basis':'observed_build','root':'.','artifacts':arts})
cmd=[sys.executable,str(S/'scripts/trace_artifacts.py')]
x=subprocess.run(cmd+['capture','--spec',str(R/'trace-spec.json'),'--out',str(R/'trace-r01.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr
x=subprocess.run(cmd+['check','--snapshot',str(R/'trace-r01.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr;wr(R/'trace-check.json',json.loads(x.stdout))
bpaths=[C/'manifest.json',C/'review.json',C/'materials.json',C/'build_index.py',C/'课程索引.html',C/'checks/2026-10-26.json',R/'review.json',R/'notes.json',R/'课堂笔记.html',R/'trace-r01.json',V/'preservation.json',V/'review.json',V/'index-browser/audit.json',V/'index-reader.json',V/'index-visual-review.json',*[C/i['html'] for i in b['items'] if i['folder']!='lecture-09']]
wr(V/'trace-spec.json',{'schema_version':1,'run_id':'GSE-weekly-20261026','basis':'observed_build','root':'../..','artifacts':[{'id':f'b{i}','path':str(p.relative_to(C)),'depends_on':[]} for i,p in enumerate(bpaths)]})
x=subprocess.run(cmd+['capture','--spec',str(V/'trace-spec.json'),'--out',str(V/'trace.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr
x=subprocess.run(cmd+['check','--snapshot',str(V/'trace.json')],capture_output=True,text=True);assert x.returncode==0,x.stdout+x.stderr;wr(V/'trace-check.json',json.loads(x.stdout))
print(json.dumps({'lecture_trace_files':len(arts),'batch_trace_files':len(bpaths),'lecture_trace':'unchanged','batch_trace':'unchanged','outcome':'completed'}))
