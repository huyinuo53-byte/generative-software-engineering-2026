from pathlib import Path
import json
R=Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-08')
p=R/'课堂笔记.html';s=p.read_text()
css='''<style id="lecture08-reading-fixes">
/* Keep desktop navigation operable; preserve source supplement paragraph breaks. */
.course-toc>summary{pointer-events:auto;cursor:pointer}
@media(min-width:1100px){.course-toc:not([open])>nav{display:none}}
.inline-reading p[data-content]{white-space:pre-line}
</style>'''
assert 'id="lecture08-reading-fixes"' not in s
s=s.replace('</head>',css+'</head>');p.write_text(s)
