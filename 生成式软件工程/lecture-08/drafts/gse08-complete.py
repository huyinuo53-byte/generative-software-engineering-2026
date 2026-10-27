import pathlib,json,hashlib,shutil,datetime
C=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程');R=C/'lecture-08';sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();write=lambda p,x:pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Prerequisites come from executed checks and actual independent review.
assert json.loads((R/'audits/content-review.json').read_text())['open_content_findings']==[]
assert json.loads((R/'qa/browser/audit.json').read_text())['status']=='PASS'
assert json.loads((R/'qa/reader/visual-review.json').read_text())['status']=='passed'
validation={}
for key,evidence in {'content':'audits/content-review.json','structure':'audits/layout-validation.json','source_coverage':'audits/transcript-reading.json','reading_materials':'audits/materials-validation.json','material_integration':'audits/material-integration.json','visual_coverage':'visual-coverage.json','images':'image-audit.json','html_static':'audits/html-content-preservation.json','desktop':'qa/browser/audit.json','narrow_screen':'qa/reader/journey.json','zoom_pan_close':'qa/reader/journey.json','console':'qa/browser/audit.json','print':'qa/reader/journey.json','visual_samples':'qa/reader/visual-review.json','project_strict':'sources/project-strict-check.json'}.items():validation[key]={'status':'passed','evidence':evidence}
validation['print']['scope']='Print media and before/after print events; 16 answers open and visible. No exported PDF or native print dialog.'
for key in ['real_phone','native_print','pdf','zip','full_audio_listening','repository_execution']:validation[key]={'status':'not_requested','evidence':'未执行；本次交付为离线HTML，按实际阅读/静态源代码审查范围记录。'}
files=['notes.json','reading-layout.json','课堂笔记.html','transcript.json','chunks/index.json','image-audit.json','visual-coverage.json',*[v['evidence'] for v in validation.values() if v['status']=='passed']]
review={'run_id':'BV11LWw6VEHW-20261019','scope_revision':1,'outcome':'completed','first_pending':None,'pending':[],'video_id':'BV11LWw6VEHW','title':'Agent-native 开发','summary':'97分钟完整转写阅读，30主题、69内嵌图、27原始材料补充、16自测；内容/逐图/画面覆盖/桌面与390及320窄屏复核通过。','validation':validation,'source_hashes':{p:sha(R/p) for p in dict.fromkeys(files)},'trace_snapshot':'trace-r01.json','delivered_files':['课堂笔记.html'],'delivery_path':'课堂笔记.html','finished_at':now,'blocker':None,'reuse':{'transcript':'66个已有BaoCut项目中未找到匹配BV的新课转写；经身份核对新建匹配项目并生成，失败下载未重复ASR。旧八课转写/正文/HTML保留。','images':'逐图原尺寸审阅和图片hash复用；最终仅修改文字笔误，图绑定与事件段落逐项比较未变。'},'limits':['未逐秒听审全部音频或逐帧播放视频','现行官方24页网页截图汇编非原生PDF，可能含课后补充','仓库固定commit晚于录制，仅34文件全文和3文件范围静态阅读','浏览器窄屏模拟不是真实手机；打印媒体模拟非原生打印'],'metrics':{'tokens':None,'cost':None,'media_seconds':5829.674667,'sections':30,'images':69,'supplements':27,'self_test':16,'source_units':394}}
write(R/'review.json',review)
shutil.copy2('/tmp/gse08-final-checks.py',R/'drafts/gse08-final-checks.py');shutil.copy2('/tmp/gse08-complete.py',R/'drafts/gse08-complete.py')
# Preserve prior root ledger/index files before incremental update.
rev=C/'revisions/20261019-new-08';before=rev/'before';before.mkdir(parents=True,exist_ok=True)
for name in ['manifest.json','review.json','build_index.py','课程索引.html']:
 dest=before/name
 if not dest.exists():shutil.copy2(C/name,dest)
old=json.loads((before/'review.json').read_text());unchanged=[]
for x in old['items']:
 assert sha(C/x['html'])==x['html_sha256'],x['folder'];unchanged.append({'path':x['html'],'sha256':x['html_sha256']})
write(rev/'preservation.json',{'status':'passed','scope':'原有八篇HTML逐一与上次交付hash比较，未重转写或重写。','files':unchanged,'checked_at':now})
m=json.loads((C/'manifest.json').read_text());check=json.loads((C/'checks/2026-10-19.json').read_text());ids=set(check['video_ids'])
for v in m['videos']:v['listed_on_last_check']=v['id'] in ids
if not any(v['id']=='BV11LWw6VEHW' for v in m['videos']):m['videos'].append({'id':'BV11LWw6VEHW','title':'Agent-native 开发 [08-Raw/26生成式软件工程/NJU]','url':'https://www.bilibili.com/video/BV11LWw6VEHW','published_at':'2026-10-13T17:10:24+08:00','status':{'transcript':'new','notes':'completed','ui':'passed'},'output':'lecture-08/课堂笔记.html','listed_on_last_check':True})
m.update(queried_at=check['checked_at'],last_check='checks/2026-10-19.json',current_playlist_ids=check['video_ids'],preserved_unlisted_ids=check['previous_not_listed']);write(C/'manifest.json',m)
shutil.copy2('/tmp/gse08-build-index-draft.py',C/'build_index.py')
print('lecture completed, old8 preserved, manifest extended, index generator adapted')
