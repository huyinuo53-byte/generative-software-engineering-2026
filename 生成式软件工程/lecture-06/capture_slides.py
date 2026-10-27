import urllib.request,urllib.parse,json,time
from pathlib import Path
p=Path(__file__).parent
base='http://localhost:3456';target='833A3ABFB11BAB4B0E683255AB7F8E81'
req=urllib.request.Request(base+'/eval?target='+target,data=b'let fix=document.createElement("style");fix.textContent="*{transition:none!important;animation:none!important}";document.head.append(fix);true'); json.load(urllib.request.urlopen(req))
for i in range(47):
 req=urllib.request.Request(base+'/eval?target='+target,data=f'show({i}); true'.encode())
 json.load(urllib.request.urlopen(req));time.sleep(.7)
 dest=p/'frames'/f'page-{i+1:03d}.png'
 url=base+'/screenshot?'+urllib.parse.urlencode({'target':target,'file':str(dest.resolve())})
 r=json.load(urllib.request.urlopen(url))
 if not dest.exists():raise RuntimeError(r)
print('captured',47)
