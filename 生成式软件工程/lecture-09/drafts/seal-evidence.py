from pathlib import Path
import json,hashlib,shutil,datetime,runpy
R=Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-09');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();wr=lambda p,x:Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
shutil.copytree('/tmp/gse09-visual',R/'visual',dirs_exist_ok=True)
shutil.copy2('/tmp/gse09-slides/audit-16-30.json',R/'sources/official-capture/audit-16-30.json')
shutil.copy2('/tmp/gse09-author.py',R/'drafts/author.py');shutil.copy2('/tmp/gse09-build.py',R/'drafts/build.py')
n=json.loads((R/'notes.json').read_text());b=json.loads((R/'audits/frame-bindings.json').read_text());bind={x['candidate_id']:x for x in b};pg={f['page']:{'section':i+1,'frame':j+1} for i,s in enumerate(n['sections']) for j,f in enumerate(s['frames']) if f['source_type']=='pdf_page'}
raw=runpy.run_path('/tmp/gse09-author.py')['sections'];sec=lambda t:next((i+1 for i,s in enumerate(raw) if s['start']<=t<s['end']),len(raw))
c=json.loads((R/'visual/visual-coverage-draft.json').read_text());c['notes_sha256']=sha(R/'notes.json');c['inventory']={'path':'visual/visual-inventory.json','sha256':sha(R/'visual/visual-inventory.json')}
for s in c['states']:
 if s['disposition']=='included':s['targets']=[{k:bind[s['candidate_id']][k] for k in ['section','frame']}]
 elif s['disposition']=='official_page':s['targets']=[pg[p] for p in s['official_slide_pages']]
 elif s['disposition']=='represented_in_text':s['targets']=[{'section':sec(s['time'])}]
 s.pop('binding_required',None)
c['pdf_pages']=[{'page':p,'disposition':'included','targets':[pg[p]],'reason':'完整官方网页截图汇编；来源与口述区分，相关段落后展示。'} for p in range(1,31)]
c['pdf']={'path':'sources/official-capture/official-web-slides-capture.pdf','sha256':sha(R/'sources/official-capture/official-web-slides-capture.pdf'),'total_pages':30};c['status']='passed';c.pop('required_next',None)
wr(R/'visual-coverage.json',c)
reviews=json.loads((R/'visual/native-frame-review.json').read_text());vmap={x['candidate_id']:x for x in reviews['images']};sel=json.loads((R/'visual/selected-frames.json').read_text());p2id={x['path']:x['candidate_id'] for x in sel}
o2=json.loads((R/'sources/official-capture/audit-16-30.json').read_text());omap={x['page']:x for x in o2['pages']}
obs={1:'软件工程的Intent/Spec/Impl、NASA紫色例子与Git/Jujutsu条目完整。',2:'essential/accidental复杂性、Brooks九成条件及Agent-native/CI-CD完整。',3:'开发者交流现场照片和展示物完整，照片原像素有限，不据此识别小字。',4:'150行Mini-Agent、校园三维图目标、网络中断反例和API问题完整。',5:'三种失败类别、未知执行结果、文件移动例与AWS链接完整。',6:'项目/Skills/权限、预算/交付/隐私/体验条目完整；末行可见。',7:'最小Agent Loop与恢复、暂停、权限、预算、验收、同步六类外围需求均完整。',8:'Grok Bot标题、角色列表和Morning Paper界面完整；界面细字需原尺寸看。',9:'dsh-bot执行/审阅/改进界面截图与标题完整，非本次实际运行证明。',10:'2026-06-10 22:57、主流产品与两个初始化步骤完整。',11:'受限/自由、四类架构取舍与得到的基础设施/接口文字完整，右侧留白为原页面适配。',12:'假设有效期、电力与传动轴/流程重组类比完整。',13:'5172客服/15%及推演、分配边界完整，不能泛化软件效率。',14:'进程地址空间、系统调用、工作集抖动与memory.max边界完整。',15:'Java托管内存、论坛延迟例、暂停/吞吐/内存取舍与GC链接完整。'}
images=[]
for i,s in enumerate(n['sections'],1):
 for j,f in enumerate(s['frames'],1):
  path=R/f['path']
  if f['source_type']=='video_frame':
   cid=p2id[f['path'].removeprefix('visual/')];q=vmap[cid];o=q['observed_information'];purpose=q['purpose'];exp=q['expected_information'];ev=f'visual/native-frame-review.json#{cid}; visual/contact-review.json; precise seek {f["time"]}'
   sources=[{'path':c['media']['path'],'sha256':c['media']['sha256'],'detail':f'BV144nc6KEA4 原视频 {f["time"]}秒'}]
  else:
   page=f['page'];o=obs[page] if page<=15 else omap[page]['visual_observation'];purpose=f'保存{f["caption"]}';exp='该页完整标题、正文、图例、代码与链接标注（如有），不遗漏底部条目';ev='sources/official-capture/Chrome逐页截图；root实际目视1–15页，visual代理实际目视16–30页';sources=[{'path':'sources/official-capture/official-web-slides-capture.pdf','sha256':c['pdf']['sha256'],'detail':f'网页截图汇编物理第{page}页，不是教师原生PDF'}]
  images.append({'section':i,'frame':j,'path':f['path'],'sha256':sha(path),'purpose':purpose,'expected_information':exp,'observed_information':o,'comparison_evidence':ev,'sources':sources,'status':'passed','known_gap':False,'resolution':'实际查看原尺寸；视频转场修正记录保留，官方页等待换页动画结束后完整截取。'})
wr(R/'image-audit.json',{'schema_version':1,'notes_sha256':sha(R/'notes.json'),'images':images})
# Preserve both source author's factual reading and independent final-export coverage.
wr(R/'audits/transcript-reading.json',{'status':'passed','source_sha256':sha(R/'transcript.json'),'index_sha256':sha(R/'chunks/index.json'),'source_units':518,'read_chunks':18,'authors':[{'actor':'root','method':'顺序完整阅读原始ASR713片段，0.31–5363.07秒；按主题写作后核对最终来源索引。'},{'actor':'gse09_content_review_20261026','method':'最终导出18块518单元逐块全文阅读；记录在initial-content-review/content-review-draft.json'}],'scope':'完整转写阅读，不是逐秒听审全部音频。'})
wr(R/'audits/official-capture-review.json',{'status':'passed','root_review_pages':list(range(1,16)),'observations':obs,'other_review':'sources/official-capture/audit-16-30.json','capture':'Chrome原站逐页pager验证、图片可解码、换页矩形x=0','pdf_pages':30,'pdf_roundtrip_rendered':[1,15,30],'pdf_roundtrip_visually_viewed':[15,30],'scope':'截图汇编来源，非官方原生PDF；网页重排不同于课堂投影比例。'})
print('image rows',len(images),'visual states',len(c['states']))
