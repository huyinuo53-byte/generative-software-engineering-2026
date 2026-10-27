import json,urllib.request,urllib.parse,pathlib,sys,time,hashlib
root=pathlib.Path(__file__).resolve().parent;target=sys.argv[1]
def req(route,data=None):
 return json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:3456/'+route,data=data.encode() if data else None),timeout=60))
def ev(js):
 x=req('eval?target='+target,js)
 if 'error' in x:raise RuntimeError(x)
 return x.get('value')
for lesson in sys.argv[2:]:
 r=root/lesson;out={'method':'Actual Chrome iframe viewport; complete inline artifact in srcdoc; monitor added before scripts','html_sha256':hashlib.sha256((r/'课堂笔记.html').read_bytes()).hexdigest(),'viewports':{}}
 for mode in ['mobile','desktop']:
  req('navigate?target='+target+'&url='+urllib.parse.quote((r/'qa'/f'{mode}.html').as_uri()));time.sleep(.3)
  count=ev("document.querySelector('iframe').contentDocument.querySelectorAll('main img').length")
  for image_index in range(count):
   ev(f"document.querySelector('iframe').contentDocument.querySelectorAll('main img')[{image_index}].scrollIntoView()")
   req('screenshot?target='+target+'&file=/tmp/gse-qa-paint.png')
  ev("document.querySelector('iframe').contentWindow.scrollTo(0,0)")
  state=ev("""(()=>{let w=document.querySelector('iframe').contentWindow,d=w.document;let imgs=Array.from(d.querySelectorAll('main img'));let ids=Array.from(d.querySelectorAll('[id]'),x=>x.id);return {width:w.innerWidth,scrollWidth:d.documentElement.scrollWidth,images:imgs.length,brokenImages:imgs.filter(x=>!x.naturalWidth).length,duplicateIds:ids.filter((x,i)=>ids.indexOf(x)!==i),badAnchors:Array.from(d.querySelectorAll('a[href^="#"]')).filter(a=>!d.getElementById(a.getAttribute('href').slice(1))).length,errors:w.__qaErrors||[],title:d.title};})()""")
  req('screenshot?target='+target+'&file='+urllib.parse.quote(str(r/'qa'/f'{mode}-top.png')))
  interactive=ev('''(()=>{let w=document.querySelector('iframe').contentWindow,d=w.document;let toc=d.querySelector('.course-toc');toc.querySelector('summary').click();let opened=toc.open;d.querySelector('nav a[href="#s1"]').click();let jumped=w.location.hash==='#s1';toc.open=false;d.querySelector('#s1').scrollIntoView();return {tocOpened:opened,anchorJump:jumped,bodyWidth:d.documentElement.scrollWidth}})()''')
  req('screenshot?target='+target+'&file='+urllib.parse.quote(str(r/'qa'/f'{mode}-body.png')))
  zoom=ev('''(()=>{let d=document.querySelector('iframe').contentDocument;d.querySelector('.zoom').click();let q=d.querySelector('dialog');return {open:q.open,imageLoaded:q.querySelector('img').naturalWidth>0,width:q.getBoundingClientRect().width}})()''')
  req('screenshot?target='+target+'&file='+urllib.parse.quote(str(r/'qa'/f'{mode}-zoom.png')))
  scales=[]
  for step in range(3):
   scales.append(ev("(()=>{let d=document.querySelector('iframe').contentDocument;d.querySelector('#zoom-scale').click();let img=d.querySelector('dialog img');return {style:img.style.width,actualWidth:img.getBoundingClientRect().width,dialogWidth:d.querySelector('dialog').clientWidth}})()"))
   if step==1:req('screenshot?target='+target+'&file='+urllib.parse.quote(str(r/'qa'/f'{mode}-zoom3.png')))
  zoom['scales']=scales
  close=ev('''(()=>{let w=document.querySelector('iframe').contentWindow,d=w.document;d.querySelector('#close').click();return {closed:!d.querySelector('dialog').open,errors:w.__qaErrors||[]}})()''')
  out['viewports'][mode]={'state':state,'interaction':interactive,'zoom':zoom,'close':close}
 (r/'qa'/'browser.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(lesson,json.dumps(out['viewports'],ensure_ascii=False),flush=True)
