import urllib.request,urllib.parse,json,time
from pathlib import Path
p=Path(__file__).parent
base='http://localhost:3456';target='EB7BEFAAF4D2D7D6DE8CE3EA2F6BE52D'
req=urllib.request.Request(base+'/eval?target='+target,data=b'(()=>{let fix=document.createElement("style");fix.textContent="*{transition:none!important;animation:none!important}.slide:not(.active){display:none!important}.slide.active{transform:none!important;opacity:1!important}";document.head.append(fix);return true})()'); json.load(urllib.request.urlopen(req))
for i in range(25):
 req=urllib.request.Request(base+'/eval?target='+target,data=f'show({i}); true'.encode())
 json.load(urllib.request.urlopen(req));time.sleep(.7)
 dest=p/'frames'/f'page-{i+1:03d}.png'
 url=base+'/screenshot?'+urllib.parse.urlencode({'target':target,'file':str(dest.resolve())})
 r=json.load(urllib.request.urlopen(url))
 if not dest.exists():raise RuntimeError(r)
print('captured',25)
