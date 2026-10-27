import pathlib,sys,html
for arg in sys.argv[1:]:
 r=pathlib.Path(arg);p=r/'课堂笔记.html';s=p.read_text()
 if 'class="course-toc"' not in s:
  s=s.replace('<nav>','<details class="course-toc"><summary>目录 · 点击展开</summary><nav>',1).replace('</nav>','</nav></details>',1)
  s=s.replace('</style>','\n.course-toc{margin-top:18px}.course-toc summary{cursor:pointer;font-weight:600;padding:8px 0}.course-toc nav{display:grid;grid-template-columns:1fr;gap:7px;margin-top:12px;font-size:16px;line-height:1.6}.course-toc nav a{padding:5px 0}dialog button{position:sticky;top:0;z-index:1;background:white;border:1px solid #bbb}dialog img{max-width:none}@media(max-width:600px){h1{font-size:30px}h2{font-size:24px}dialog{padding:10px;width:98vw}}@media print{.course-toc{display:none}}\n</style>',1)
  p.write_text(s)
 if 'id="zoom-scale"' not in s:
  s=s.replace('<main><aside>','<main><details class="reading-scope"><summary>阅读说明与核验范围</summary><aside>',1).replace('</aside>','</aside></details>',1)
  s=s.replace('<button id="close">关闭</button>','<div class="zoom-tools"><button id="close">关闭</button><button id="zoom-scale">放大至 2×</button></div>',1)
  s=s.replace('</style>','\n.reading-scope{margin-bottom:24px}.reading-scope summary{cursor:pointer;font-size:15px;color:#756c60}.zoom-tools{position:sticky;top:0;left:0;z-index:2;display:flex;gap:8px;width:max-content;background:white;padding-bottom:8px}dialog .zoom-tools button{position:static;white-space:nowrap}dialog img{max-width:none}@media print{.reading-scope{display:block}.reading-scope>aside{display:block}.reading-scope>summary{display:none}}\n</style>',1)
  s=s.replace('</body>', '<script>(()=>{const dialog=document.querySelector("dialog"),button=document.querySelector("#zoom-scale"),img=dialog.querySelector("img");let scale=1;const reset=()=>{scale=1;img.style.width="100%";button.textContent="放大至 2×";dialog.scrollLeft=0;};document.querySelectorAll(".zoom").forEach(b=>b.addEventListener("click",reset));button.addEventListener("click",()=>{scale=scale===3?1:scale+1;img.style.width=(100*scale)+"%";button.textContent=scale===3?"适应宽度":"放大至 "+(scale+1)+"×";});})();</script></body>',1)
  p.write_text(s)
 if 'id="print-reading-fix"' not in s:
  s=s.replace('</head>','<style id="print-reading-fix">@media print{section>small{display:block;break-after:avoid}figure{break-inside:avoid}figure img{max-height:650px;object-fit:contain}}</style></head>',1)
  s=s.replace('</body>','<script>(()=>{const scope=document.querySelector(".reading-scope");let wasOpen=false;addEventListener("beforeprint",()=>{wasOpen=scope.open;scope.open=true;});addEventListener("afterprint",()=>{scope.open=wasOpen;});})();</script></body>',1)
  p.write_text(s)
 q=r/'qa';q.mkdir(exist_ok=True)
 monitor='<base href="about:srcdoc"><script>window.__qaErrors=[];window.addEventListener("error",e=>__qaErrors.push(e.message));window.addEventListener("unhandledrejection",e=>__qaErrors.push(String(e.reason)));</script>'
 s=s.replace('<head>','<head>'+monitor,1)
 for name,w in [('mobile',390),('desktop',900)]:
  (q/(name+'.html')).write_text('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#ddd}iframe{border:0;display:block;height:760px;width:'+str(w)+'px}</style><iframe id="test" srcdoc="'+html.escape(s,quote=True)+'"></iframe>')
 print(p)
