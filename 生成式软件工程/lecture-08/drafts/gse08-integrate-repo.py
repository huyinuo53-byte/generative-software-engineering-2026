import pathlib,json,re,shutil,hashlib
R=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-08')
src=pathlib.Path('/tmp/gse08-harness-reading/delivery');dest=R/'sources/harness-20261019'
shutil.copytree(src,dest,dirs_exist_ok=True)
h=(src/'HANDOFF.md').read_text();parts=re.split(r'\n### [1-7]\. ',h)[1:]
keys=['bilingual','translation','inventory','inventory','review-gates','review-gates','review-gates']
m=json.loads((src/'materials-draft.json').read_text())['materials'][0]
m.update(original_kind=m['kind'],kind='web',identity_status='verified',identity_note='仓库URL由视频4230秒确认；固定当前commit晚于录制，录制时commit未确定。',recommendation_kind='explicit_recommendation',reading_status='full',source_files=m['scope_sections'],scope_limitations=m['known_gaps'],known_gaps=[],integration_status='integrated_pending_semantic_review')
m['scope_sections']=[f"{x['path']} lines {x['read_ranges']}" for x in m['source_files']];m['read_sections']=m['scope_sections']
m['path']='lecture-08/sources/harness-20261019/read-scope-and-source-manifest.json';m['related_items']=['lecture-08']
s=[]
for key,p in zip(keys,parts):
 p=p.split('\n## ')[0].strip();title,body=p.split('\n',1)
 body=re.sub(r'\*\*','',body.strip())
 s.append({'section_key':key,'title':title.strip(),'text':'[gse08-deepseek-harness-repository；当前源码补充，commit 687f282，2026-10-17，晚于课堂] '+body,'source_label':'当前原始仓库补充；34文件全文、3文件明确范围，只读静态核验，未执行门禁','source_url':m['source_url']})
(dest/'integration.json').write_text(json.dumps({'materials':[m],'supplements':s},ensure_ascii=False,indent=2)+'\n')
# 原报告保存，纠错作为可追溯记录，不改任何原始源码。
(dest/'parent-correction.json').write_text(json.dumps({'claim_corrected':'课堂当时展示整文件hash','evidence':'visual/full/v0499-4350.jpg','observation':'实际画面已为per heading section，SHA256前16位；不要将现行算法误说成课后才出现。','source_sample_version_difference':'style-samples.md仍含旧整文件Git blob样例，现行配对按标题分节；两者权威范围不同。'},ensure_ascii=False,indent=2))
