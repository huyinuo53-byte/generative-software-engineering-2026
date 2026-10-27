from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[];self.head=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','nav','header','footer']:self.skip+=1
  if t in ['h1','h2','h3','h4','p','li','pre','div','section','tr']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','nav','header','footer']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.out.append(s)
r=Path('/tmp/gse09-materials/sources')
for p in r.glob('*.html'):
 if p.stem in ['slides9','lect9']:continue
 x=P();x.feed(p.read_text(errors='replace'));text=''.join(x.out);(r/(p.stem+'.txt')).write_text(text)
 print(p.stem,len(text))
