import json,urllib.request,urllib.parse,time,pathlib,sys
run=pathlib.Path(sys.argv[1]);target=sys.argv[2];count=int(sys.argv[3]);(run/'frames').mkdir(exist_ok=True)
def req(route,data=None):
 return json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3456/'+route,data=data.encode() if data else None),timeout=30))
audit=[]
for page in range(1,count+1):
 expr=f'''(async()=>{{show({page-1});await document.fonts.ready;if(window.MathJax?.typesetPromise)await MathJax.typesetPromise();fitSlides();await new Promise(r=>setTimeout(r,350));const s=document.querySelector('.slide.active');return {{page:document.querySelector('#cur').textContent,text:s.innerText,images:Array.from(s.querySelectorAll('img')).map(x=>({{complete:x.complete,w:x.naturalWidth}})),rect:s.getBoundingClientRect().toJSON()}}}})()'''
 state=req('eval?target='+target,expr);audit.append(state)
 path=str((run/'frames'/f'slide-{page:03}.png').resolve())
 req('screenshot?target='+target+'&file='+urllib.parse.quote(path))
(run/'slide-capture.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('captured',count,run)
