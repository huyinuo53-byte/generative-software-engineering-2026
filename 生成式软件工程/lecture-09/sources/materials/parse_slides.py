from pathlib import Path
from html.parser import HTMLParser
import json,re
class S(HTMLParser):
 def __init__(self):super().__init__();self.on=False;self.arr=''
 def handle_starttag(self,t,a):
  if t=='script' and dict(a).get('id')=='slides-data':self.on=True
 def handle_endtag(self,t):
  if t=='script':self.on=False
 def handle_data(self,s):
  if self.on:self.arr+=s
class T(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.links=[];self.img=[];self.aigc=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a':self.links.append(d.get('href'))
  if t=='img':self.img.append(d.get('src',''))
  if 'aigc' in d.get('class',''):self.aigc+=1
  if t in ['h1','h2','p','li','pre']:self.out.append('\n')
 def handle_data(self,s):self.out.append(s)
x=S();x.feed(Path('/tmp/gse09-materials/sources/slides9.html').read_text());arr=json.loads(x.arr); rows=[];out=[]
for i,s in enumerate(arr,1):
 t=T();t.feed(s);text=''.join(t.out).strip();rows.append({'page':i,'text':text,'links':t.links,'aigc_annotations':t.aigc,'images':len(t.img)})
 out.append(f'\n\nPAGE {i}\n{text}\nLINKS {t.links}\nAIGC annotations {t.aigc}')
Path('/tmp/gse09-materials/sources/slides9-pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
Path('/tmp/gse09-materials/sources/slides9-pages.txt').write_text(''.join(out))
print('pages',len(arr));print(''.join(out))
