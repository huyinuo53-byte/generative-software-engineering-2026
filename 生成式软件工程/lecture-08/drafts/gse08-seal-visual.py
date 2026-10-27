import pathlib,json,hashlib,shutil,re,datetime
R=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-08');T=pathlib.Path('/tmp');sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
write=lambda p,x:pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
n=json.loads((R/'notes.json').read_text());nh=sha(R/'notes.json');aud=R/'audits';aud.mkdir(exist_ok=True)
# Preserve original independent review and its version; current reuse is independently checked below.
for name in ['gse08-final-visual-review.json','gse08-final-visual-coverage-draft.json','gse08-event-binding-map.json','gse08-content-review-early.json']:
 shutil.copy2(T/name,aud/name)
shutil.copy2(T/'gse08-harness-reading/delivery/HANDOFF.md',R/'sources/harness-20261019/HANDOFF.md')
v=json.loads((T/'gse08-final-visual-review.json').read_text());mapping=json.loads((T/'gse08-event-binding-map.json').read_text())
for e in mapping['events']:
 for p in e['exact_paragraphs']:
  assert p['text']==n['sections'][p['section']-1]['paragraphs'][p['paragraph']-1]
 for f in e['existing_frames']:
  nf=n['sections'][f['section']-1]['frames'][f['frame']-1];assert f['caption']==nf['caption'] and f['path']==nf['path'] and f['sha256']==sha(R/nf['path'])
# Derived root-relative inventory; original inventory bytes remain under visual/.
i=json.loads((R/'visual/visual-inventory.json').read_text());i['source_inventory']={'path':'visual/visual-inventory.json','sha256':sha(R/'visual/visual-inventory.json')};i['media_sha256']='dee8d8992246a868d973678ab85c152e3eaf3e07ccef70eb5a674556386552b7'
for c in i['candidates']:c['path']='visual/'+c['path']
write(R/'visual-inventory.json',i)
c=json.loads((T/'gse08-final-visual-coverage-draft.json').read_text());c.update(notes_sha256=nh,status='passed',inventory={'path':'visual-inventory.json','sha256':sha(R/'visual-inventory.json')},parent_review={'method':'主作者回读52事件的原观察→确切段落/图片映射，结合此前全文转写阅读；程序核对全部绑定段落及图片未变。最终仅修正section25例子的文务笔误，与视觉映射无关。','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_notes_sha256':v['notes_sha256']})
c['media']['tail_decode']='passed';c['pdf']={'path':'sources/official-20261019/source-slides.pdf','sha256':sha(R/'sources/official-20261019/source-slides.pdf'),'page_count':24};c['event_binding_map']={'path':'audits/gse08-event-binding-map.json','sha256':sha(aud/'gse08-event-binding-map.json')};c['final_visual_binding_review']='audits/gse08-final-visual-review.json';c['pdf_pages_note']='24张现行官方页均逐页检查并绑定；非录制时官方原生PDF。';c.pop('parent_action',None)
for w in c['reviewed_windows']:w['evidence']='visual/'+w['evidence']
write(R/'visual-coverage.json',c)
images=[]
for item in v['items']:
 match=re.search(r'frames\[(\d+)\]',item['notes_target']);si=item['section_number'];fi=int(match.group(1))+1;f=n['sections'][si-1]['frames'][fi-1]
 assert item['path']==f['path'] and item['caption']==f['caption'] and item['sha256']==sha(R/f['path']) and item['binding_result']=='matched'
 kind=item['source_type'];sources=[{'path':'audits/gse08-final-visual-review.json','sha256':sha(aud/'gse08-final-visual-review.json'),'detail':item['notes_target']+'; actual_view_basis='+item['actual_view_basis']}]
 sp='sources/official-20261019/source-slides.pdf' if 'official-' in f['path'] else ('sources/lab2-humanize-20261019/humanize-v2.pdf' if kind=='pdf_page' else 'sources/media-integrity.json')
 sources.append({'path':sp,'sha256':sha(R/sp),'detail':('physical page '+str(f['page'])) if kind=='pdf_page' else '已核对视频ID、媒体hash、音视频流时长和尾段解码，真实帧时间'+str(f['time'])})
 images.append({'section':si,'frame':fi,'path':f['path'],'sha256':item['sha256'],'purpose':n['sections'][si-1]['title'],'expected_information':f['caption'],'observed_information':item['rationale'],'comparison_evidence':item['actual_view_basis']+'; '+str(item.get('semantic_caveats',[])),'resolution':'保留完整原图；逐图语义绑定通过，最终正文笔误更改未触及图或图注。','status':'passed','known_gap':False,'sources':sources})
write(R/'image-audit.json',{'schema_version':1,'notes_sha256':nh,'images':images,'scope':'委派逐图目视审查+主作者绑定复核；不是连续播放或真实手机验收。'})
# Exact original chunks read completely by parent, distinct from sentence assignment check.
idx=json.loads((R/'chunks/index.json').read_text());chunks=[]
for p in sorted((R/'chunks').glob('*.json')):
 if p.name!='index.json':chunks.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
write(aud/'transcript-reading.json',{'status':'passed','reader':'root','method':'主作者完整读取ASR全部1911segment，随后按实际导出文件逐一完整读取19个chunk，按1–6、7–12、13–19分批；正文逐主题而非按分块分章。','read_chunks':n['read_chunks'],'chunk_files':chunks,'source_units':len(idx['sentences']),'transcript_sha256':sha(R/'transcript.json'),'index_sha256':sha(R/'chunks/index.json'),'audio_listening':'not_full_audio_review','retrospective_record':True})
# Preserve reproducible authoring and observed tool reports.
for p in T.glob('gse08-author*.py'):shutil.copy2(p,R/'drafts'/p.name)
for fn in ['gse08-build.py','gse08-integrate-repo.py','gse08-polish-html.py','gse08-reader-journey.cjs','gse08-seal-visual.py']:shutil.copy2(T/fn,R/'drafts'/fn)
p=pathlib.Path('/Users/yjzhao/Library/Application Support/BaoCut/projects/GSE-08-BV11LWw6VEHW.bcut/checks/check-mveldqjl.json');shutil.copy2(p,R/'sources/project-strict-check.json')
print('sealed',len(images),'images;',len(c['states']),'candidates;',len(chunks),'chunks')
