from pathlib import Path
import hashlib,json,shutil,os,re,zipfile,datetime
BASE=Path('/private/tmp/gse-publication-20261027')
SRC=Path('/Users/yjzhao/Documents/ChatGPT/learning-machine')
REPO=BASE/'repo'; REPO.mkdir(exist_ok=False)
COURSE='生成式软件工程'; EXCLUDED=[]; COPIED=[]; CHANGED=[]

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def put(path,data):
 p=REPO/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding='utf-8')
def js(path,data):put(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def copytree(src,dest):
 for p in sorted(src.rglob('*')):
  if p.is_symlink():raise RuntimeError('symlink needs review: '+str(p))
  if not p.is_file():continue
  rel=p.relative_to(src)
  if p.name=='.DS_Store' or '__pycache__' in rel.parts or p.name=='.audit.lock' or (p.name=='lock' and p.parent.name=='.bcut'):
   EXCLUDED.append({'source':str(p),'reason':'OS/Python cache or ephemeral lock; not course evidence'});continue
  target=REPO/dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
  sha=digest(p);assert digest(target)==sha
  COPIED.append({'path':str(target.relative_to(REPO)),'source':str(p),'bytes':p.stat().st_size,'sha256':sha})
copytree(SRC/COURSE,Path(COURSE))
manifest=json.loads((SRC/COURSE/'manifest.json').read_text());videos=manifest['videos'];ids={v['id'] for v in videos}
# Scope a historical all-project inventory. Local original remains untouched.
p=REPO/COURSE/'sources/projects.json';old=digest(p);data=json.loads(p.read_text());items=data['data']['projects'];kept=[]
for x in items:
 s=json.dumps(x,ensure_ascii=False)
 if any(v in s for v in ids):kept.append(x)
data['data']['projects']=kept
for k in ['count','total']:
 if k in data['data']:data['data'][k]=len(kept)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
CHANGED.append({'path':str(p.relative_to(REPO)),'original_sha256':old,'archived_sha256':digest(p),'reason':'Historical inventory scoped to course videos; unrelated BaoCut project records omitted','original_project_count':len(items),'archived_project_count':len(kept)})
# Keep directly related research in its original relative-path structure.
copytree(SRC/'research/research_notes/pstack-skills-20261022',Path('research/research_notes/pstack-skills-20261022'))
p=SRC/'research/reports/pstack Skills 写法与生成式软件工程启发.html';t=REPO/p.relative_to(SRC);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);COPIED.append({'path':str(t.relative_to(REPO)),'source':str(p),'bytes':p.stat().st_size,'sha256':digest(p)})
# Older reused draft and its original frames remain distinct from current accepted notes.
copytree(Path('/Users/yjzhao/Downloads/课堂笔记/BV1Nyeq6qEt8/20261001T063030Z'),Path('legacy/BV1Nyeq6qEt8/20261001T063030Z'))
copytree(Path('/Users/yjzhao/Downloads/提示词工程-课堂笔记-assets'),Path('legacy/prompt-engineering-assets'))
# Freeze the workflow source used to understand/build/check this archive.
copytree(Path('/Users/yjzhao/.codex/skills/baocut-course-notes'),Path('tooling/baocut-course-notes'))
for name in ['audit-report.mjs','resume-course.py']:
 p=SRC/'scripts'/name;t=REPO/'tooling/learning-machine'/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);COPIED.append({'path':str(t.relative_to(REPO)),'source':str(p),'bytes':p.stat().st_size,'sha256':digest(p)})
# The 10 native projects are copied read-only, including ASR rows, history, waveform cache and tasks.
projects=[];media=[];assets=BASE/'release-assets';assets.mkdir()
for v in videos:
 show=json.loads((BASE/(v['id']+'-show.json')).read_text());sp=Path(show['project']);m=show['data']['manifest']['media'];target=Path('baocut/projects')/sp.name
 copytree(sp,target)
 projects.append({'video_id':v['id'],'title':v['title'],'path':str(target),'original_path':str(sp),'identity_basis':'media sourceMetadata.id' if m.get('sourceMetadata',{}).get('id')==v['id'] else 'original run video binding + exact media SHA256','metadata':m})
 raw=Path(m['path']);sha=digest(raw);assert sha==m['hash'].removeprefix('sha256-')
 asset=v['id']+'.mp4';dest=assets/asset;shutil.copy2(raw,dest);assert digest(dest)==sha
 media.append({'video_id':v['id'],'title':v['title'],'source_url':'https://www.bilibili.com/video/'+v['id'],'original_path':str(raw),'original_filename':raw.name,'asset':asset,'release_tag':'snapshot-2026-10-27','bytes':raw.stat().st_size,'sha256':sha,'duration_seconds':m.get('duration'),'width':m.get('width'),'height':m.get('height'),'storage':'GitHub Release; download separately from repository','availability':'present_and_hash_verified'})
 # Fresh status read contains only this project.
 js(Path('archive/project-status')/(v['id']+'.json'),show)
 print('copied project/media',v['id'],flush=True)
js('archive/projects.json',projects);js('archive/media-manifest.json',media)
js('archive/exclusions.json',EXCLUDED);js('archive/transformations.json',CHANGED)
js('archive/source-copy-manifest.json',COPIED)
js('archive/jobs-check.json',{'checked_at':'2026-10-27','scope_video_ids':sorted(ids),'active_scoped_jobs':[],'basis':'BaoCut jobs list returned one completed unrelated project; record omitted from archive'})
# Do not make machine-specific historical QA appear portable or freshly revalidated.
put('archive/README.md','''# 制作档案与证据边界\n\n- `生成式软件工程/` 保存现有课程目录、转写分块、notes/layout、讲义、全部候选帧、逐图审核、浏览器截图、修订与失败记录。\n- `baocut/projects/` 保存 10 个原生 `.bcut` 目录：原始转写、ASR rows、Studio、历史对象、项目内 tasks/logs/cache 均保留。\n- `legacy/` 保存可识别的早期复用草稿及提示词工程截图，不替代现行笔记。\n- `media-manifest.json` 对应同仓库 Release 中 10 个源视频，记录平台 BV ID、原始路径、长度与 SHA-256。\n- `source-copy-manifest.json` 记录源文件与复制指纹；`transformations.json` 单独记录归档转换；`exclusions.json` 列出未复制的 OS/Python 缓存和临时锁。\n\n唯一内容范围转换是 `生成式软件工程/sources/projects.json`：从历史全机项目列表中去掉其他课程条目。历史 trace 仍保留原值，因此涉及该文件的旧快照不是归档副本的新验收结果。本次完整性以 `files.json` 和 `publication-review.json` 为准；不修改历史 passed/hash。\n\n历史审核是原制作时的证据，包含真实手机、原生打印、音频逐秒听审等未测边界。复制文件并不构成新的全文/来源/真机验收。历史绝对路径、工具路径和状态照存，跨机器不自动有效。不要执行旧 `ownership.json` 或临时脚本来覆盖当前目录。\n\n截至本次归档，在这 10 个 `.bcut` 项目和可识别的课程原件中未发现独立音视频 slices。存在的 `chunks/` 是转写阅读分块；`frames/`、`visual/` 是真实画面候选与审查资料；项目 `cache/` 中已有 waveform 文件也予以保存。没有为上传重新转码或制造 slices。\n''')
put('RESTORE.md','''# 阅读和恢复\n\n## 阅读\n\n克隆或下载仓库，使用浏览器打开 `生成式软件工程/课程索引.html`。10 篇现行笔记均内嵌图片，可离线阅读。GitHub 文件页只显示源码；下载后打开 HTML。也可下载 Release 的 `course-reading-2026-10-27.zip`，这是只含现行阅读成品的便携包。\n\n## 取得源视频\n\n```sh\ngh release download snapshot-2026-10-27 --repo zhao-d-r/generative-software-engineering-2026 --pattern '*.mp4' --dir media\npython3 tools/verify_archive.py --media-dir media\n```\n\n使用已授权访问这个私有仓库的 GitHub 账号。`archive/media-manifest.json` 将 Release 的 BV 文件名映射到原始视频名、来源 URL 和 SHA-256。\n\n## 恢复 BaoCut\n\n1. 先校验 `python3 tools/verify_archive.py`，把需要的 `.bcut` 目录复制到新的工作位置；不要直接编辑仓库中的档案。\n2. 下载对应原视频并按媒体清单核对哈希。\n3. 用兼容的 BaoCut 打开项目副本；原项目保留了旧机器的媒体绝对路径。若媒体离线，通过 BaoCut 的项目设置/重新关联媒体操作选择已下载文件，不手改 `.bcut` 内部 JSON。\n4. 检查转写、章节、Studio 与媒体能否正常工作。只有完成这些实际检查，才能声称跨机器原生恢复成功；本次未在第二台机器验证。\n\n工作流快照见 `tooling/baocut-course-notes/`；BaoCut App、模型和登录/密钥配置不分发。历史脚本可能仍引用原工作目录，应先审阅路径和依赖。完整重算会产生新版本及新审查记录，不能把归档中的旧 PASS 当作当前机器的 PASS。\n''')
put('ATTRIBUTION.md','''# 来源与权属\n\n课程由南京大学蒋炎岩老师讲授，官方网站：https://jyywiki.cn/GSE/2026/ ，视频合集：https://space.bilibili.com/202224425/lists/8942017?type=season 。每课笔记、manifest 和材料台账保留具体来源。\n\n这是个人学习、制作与审查档案。课堂画面、讲义、论文及源码快照保留各自原有权属与许可证；没有给第三方材料附加统一开源许可。相关 pstack 研究锁定的来源版本见其 source-manifest/source 文件。仓库保持私有；未启用公开站点。\n''')
put('.gitignore','''# Source videos are in GitHub Releases, not Git objects.\n/media/\n/.downloads/\n.DS_Store\n__pycache__/\n*.pyc\n''')
put('.gitattributes','''*.png binary\n*.jpg binary\n*.webp binary\n*.pdf binary\n*.mp4 binary\n*.bin binary\n''')
# Build a small reading-only archive with relative paths unchanged.
reading=assets/'course-reading-2026-10-27.zip'
with zipfile.ZipFile(reading,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for s in ['课程索引.html']+[v['output'] for v in videos]:z.write(REPO/COURSE/s,COURSE+'/'+s)
 z.writestr('请先阅读.txt','打开 生成式软件工程/课程索引.html。完整制作过程、转写、讲义与项目在 GitHub 仓库；源视频在同仓库 Release。\n')
js('archive/reading-package.json',{'asset':reading.name,'bytes':reading.stat().st_size,'sha256':digest(reading),'html_count':11,'embedded_images':472})
js('archive/repository.json',{'repository':'zhao-d-r/generative-software-engineering-2026','visibility':'private','release_tag':'snapshot-2026-10-27','created_for':'course notes and BaoCut production archive','original_course_root':str(SRC/COURSE)})
print(json.dumps({'copied_files':len(COPIED),'excluded':len(EXCLUDED),'transformations':len(CHANGED),'media_count':len(media),'media_bytes':sum(x['bytes'] for x in media),'repo_files':len([p for p in REPO.rglob('*') if p.is_file()])},ensure_ascii=False),flush=True)
