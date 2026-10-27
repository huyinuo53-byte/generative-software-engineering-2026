import json
from pathlib import Path
from collections import deque
nxt={'A':'B','B':'C','C':'A'}
def hanoi(n,src,dst,out):
 aux=({'A','B','C'}-{src,dst}).pop()
 if n==1:
  while src!=dst:
   out.append((src,nxt[src]));src=nxt[src]
 elif nxt[src]==dst:
  hanoi(n-1,src,aux,out);hanoi(1,src,dst,out);hanoi(n-1,aux,dst,out)
 else:
  hanoi(n-1,src,dst,out);hanoi(1,src,aux,out);hanoi(n-1,dst,src,out);hanoi(1,aux,dst,out);hanoi(n-1,src,dst,out)
def shortest(n,dst):
 start=('A',)*n;goal=(dst,)*n;q=deque([(start,0)]);seen={start}
 while q:
  st,d=q.popleft()
  if st==goal:return d
  top={x:st.index(x) for x in set(st)}
  for src,k in top.items():
   dest=nxt[src]
   if dest in top and top[dest]<k:continue
   a=list(st);a[k]=dest;a=tuple(a)
   if a not in seen:seen.add(a);q.append((a,d+1))
rows=[]
for n in range(1,8):
 for dst in ['B','C']:
  moves=[];hanoi(n,'A',dst,moves);piles={'A':list(range(n,0,-1)),'B':[],'C':[]}
  for src,dest in moves:
   assert nxt[src]==dest
   disk=piles[src].pop();assert not piles[dest] or piles[dest][-1]>disk;piles[dest].append(disk)
  assert piles[dst]==list(range(n,0,-1));opt=shortest(n,dst);assert opt==len(moves)
  rows.append({'n':n,'destination':dst,'moves':len(moves),'bfs_shortest':opt,'legal':True})
Path(__file__).with_name('sources').joinpath('hanoi-check.json').write_text(json.dumps({'basis':'Reconstructed displayed recursion from actual frame at 4320s; independent BFS checks directed legal moves for n1..7, not a general proof','results':rows},indent=2))
print(rows)
