from pathlib import Path
import json,subprocess,hashlib,sys
R=Path('/Users/yjzhao/Documents/ChatGPT/generative-software-engineering-2026');REPO='zhao-d-r/generative-software-engineering-2026';BASE='https://api.github.com/repos/'+REPO

def get(url):
 p=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','60','--user-agent','GSE-Archive-Verification',url],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-500:])
 return p.stdout
repo=json.loads(get(BASE));assert repo['private'] is False and repo['visibility']=='public' and repo['default_branch']=='main'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R,text=True).strip()
branch=json.loads(get(BASE+'/branches/main'));assert branch['commit']['sha']==head
remote=json.loads(get(BASE+'/git/trees/'+tree+'?recursive=1'));assert remote['truncated'] is False
rfiles={x['path']:x['sha'] for x in remote['tree'] if x['type']=='blob'};local={}
for row in subprocess.check_output(['git','ls-tree','-r','-z','HEAD'],cwd=R).split(b'\0'):
 if not row:continue
 metadata,name=row.split(b'\t',1);local[name.decode()]=metadata.decode().split()[2]
assert local==rfiles
release=json.loads(get(BASE+'/releases/tags/snapshot-2026-10-27'));assert release['draft'] is False
expected={x['asset']:x for x in json.loads(Path('/private/tmp/gse-publication-20261027/release-expected.json').read_text())};observed={x['name']:x for x in release['assets']};assert set(expected)==set(observed)
for n,x in expected.items():assert observed[n]['state']=='uploaded' and observed[n]['size']==x['bytes'] and observed[n]['digest']=='sha256:'+x['sha256'],n
readme=get('https://raw.githubusercontent.com/'+REPO+'/main/README.md');assert hashlib.sha256(readme).hexdigest()==hashlib.sha256((R/'README.md').read_bytes()).hexdigest()
pack='https://github.com/'+REPO+'/releases/download/snapshot-2026-10-27/course-reading-2026-10-27.zip'
p=subprocess.run(['curl','--fail','--silent','--show-error','--location','--head','--max-time','60','--output','/dev/null','--write-out','%{http_code}',pack],capture_output=True,text=True);assert p.returncode==0 and p.stdout.strip()=='200',(p.stdout,p.stderr)
result={'status':'PASS','verification':'Unauthenticated HTTPS requests: repository, main branch, full Git tree, published Release, raw README and reading ZIP HEAD','repository':repo['html_url'],'visibility':'public','default_branch':'main','verified_content_commit':head,'tree_sha':tree,'remote_blob_count':len(rfiles),'all_git_blob_shas_match':True,'release_url':release['html_url'],'release_tag':release['tag_name'],'release_draft':False,'release_assets':[{'name':x['name'],'state':x['state'],'bytes':x['size'],'sha256':x['digest']} for x in release['assets']],'server_asset_digests_match':12,'anonymous_readme_sha256':hashlib.sha256(readme).hexdigest(),'anonymous_reading_zip_status':200,'reading_zip_url':pack,'note':'This record binds the indicated content commit. Later commits may add verification metadata; validate their Git head separately.'}
if '--write' in sys.argv:(R/'archive/remote-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='release_assets'},ensure_ascii=False))
