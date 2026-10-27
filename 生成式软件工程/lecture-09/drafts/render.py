from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1]
S=Path('/Users/yjzhao/.codex/skills/baocut-course-notes/scripts/course_notes.py')
subprocess.run([sys.executable,str(S),'render','--notes',str(R/'notes.json'),'--index',str(R/'chunks/index.json'),'--layout',str(R/'reading-layout.json'),'--require-layout','--out',str(R/'课堂笔记.html')],check=True)
p=R/'课堂笔记.html';s=p.read_text();css='<style id="lecture09-reading-fixes">.course-toc>summary{pointer-events:auto;cursor:pointer}@media(min-width:1100px){.course-toc:not([open])>nav{display:none}}.inline-reading p[data-content]{white-space:pre-line}</style>'
p.write_text(s.replace('</head>',css+'</head>'))
