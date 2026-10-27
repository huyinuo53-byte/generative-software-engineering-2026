from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self):super().__init__();self.t=[];self.ignore=0
 def handle_starttag(self,t,a):
  if t in ('script','style','svg','noscript'):self.ignore+=1
  if t in ('h1','h2','h3','h4','p','li','pre','section','article','div','tr'):self.t.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','svg','noscript'):self.ignore-=1
 def handle_data(self,d):
  if not self.ignore:self.t.append(d)
for f in Path('/tmp/gse08-materials').glob('*.html'):
 p=P();p.feed(f.read_text());s='\n'.join(l.strip() for l in ''.join(p.t).splitlines() if l.strip());f.with_suffix('.txt').write_text(s)
