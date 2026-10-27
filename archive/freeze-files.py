from pathlib import Path
import hashlib,json
R=Path('/Users/yjzhao/Documents/ChatGPT/generative-software-engineering-2026')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
files=[]
for p in sorted(R.rglob('*')):
 rel=p.relative_to(R)
 if not p.is_file() or '.git' in rel.parts or str(rel)=='archive/files.json':continue
 files.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p)})
(R/'archive/files.json').write_text(json.dumps({'schema_version':1,'scope':'all repository files except this self-referential manifest and .git internals','files':files,'bytes':sum(x['bytes'] for x in files)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':sum(x['bytes'] for x in files),'largest':max(x['bytes'] for x in files)}))
