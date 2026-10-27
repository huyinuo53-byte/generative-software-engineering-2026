import json
from pathlib import Path
results=[]
for n in range(1,11):
 pegs=[list(range(n,0,-1)),[],[]]; pos=[0]*(n+1); steps=[]
 for step in range(1,1<<n):
  disk=(step&-step).bit_length(); direction=-1 if (n-disk)%2==0 else 1
  a=pos[disk];b=(a+direction+3)%3
  assert pegs[a] and pegs[a][-1]==disk
  assert not pegs[b] or pegs[b][-1]>disk
  pegs[a].pop();pegs[b].append(disk);pos[disk]=b;steps.append((disk,a,b))
 expected=[]
 def rec(n,a,b,c):
  if not n:return
  rec(n-1,a,c,b);expected.append((n,a,b));rec(n-1,c,b,a)
 rec(n,0,2,1)
 assert steps==expected and pegs[2]==list(range(n,0,-1))
 results.append({'n':n,'moves':len(steps),'legal':True,'matches_recursive':True})
Path(__file__).with_name('sources').joinpath('hanoi-check.json').write_text(json.dumps(results,indent=2))
print('PASS n=1..10; legal and recursive-equivalent')
