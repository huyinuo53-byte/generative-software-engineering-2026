"""Fifth-lecture pilot: validate notes v2, then place evidence beside its argument.

Run with Python 3. This local renderer deliberately does not modify the shared skill.
The token sequences reference the current notes.json, with zero-based prose indices.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = Path('/Users/yjzhao/.codex/skills/baocut-course-notes')
NOTE = json.loads((ROOT / 'notes.json').read_text())
MAP = {x['page']: x for x in json.loads((ROOT / 'revisions/20261008-integrated/integration-map.json').read_text())}
# p: paragraph; e: example; n: editorial note; f: figure page (v1/v2: video);
# x: integrated extension, including its explanation and source figure.
ORDER = [
 'p0 p1 p4 n0 f1 p2 p3 p5 f2 e0 e1',
 'p0 p1 p7 f3 p2 f4 p5 p6 p3 p4 n0 e0 e1 e2 f5',
 'p0 f6 p1 p2 p3 p4 e0 x38',
 'p0 p1 e0 p4 fv1 p5 p2 p6 e1 p3 n1 n0',
 'p0 p1 p2 e0 e1 p3 n0 f8',
 'p0 f9 p1 p4 e0 f10 p2 p3 p5 e1 n0 f11',
 'p0 f12 p1 p4 e0 p2 p5 p3 e1',
 'p0 p4 f13 p1 p5 e0 f14 p2 p6 p3 e1 f15',
 'p0 f16 f17 p1 p4 p5 e0 e1 f19 p2 p3',
 'p0 p1 e0 f20 p3 p6 e1 p2 p5 f18 p4 f23 n0',
 'p0 p1 n0 f21 p2 p4 fv2 p3 p5 e0 e1 f22',
 'p0 p1 p4 e0 e1 f24 p2 p5 p3 p6',
 'p0 p1 p4 p5 e0 f25 p2 p6 e1 x39 p3',
 'p0 p1 p4 e0 f26 x33 p5 f27 p2 p3 p6 p7 e1',
 'p0 p1 p4 e0 f28 x31 x32 p2 x35 p5 e1 x36 x37 p3 n0',
 'p0 p4 e0 p5 f29 p1 p2 e1 f30 x34 p3 p6 n0',
]

CSS = '''
body{color:#292a28}main{max-width:980px}section>h2{max-width:850px}
.course-toc{margin-top:18px}.course-toc summary,.reading-scope summary{cursor:pointer;font-weight:600}
.course-toc nav{display:grid;grid-template-columns:1fr;gap:6px;margin-top:14px;font-size:16px}
.reading-scope{margin-bottom:24px}.reading-scope summary{font-size:15px;color:#635b50}
.inline-reading{margin:32px 0;padding:4px 0 4px 20px;border-left:3px solid #8b72a0}
.inline-reading h3{font-size:23px;color:#393047;margin:6px 0 12px;line-height:1.5}
.source-tag{font:600 12px/1.6 system-ui,sans-serif;color:#655078;letter-spacing:.03em}
.inline-reading .bridge{color:#53574f}.inline-reading figure{margin:18px 0 6px}
.inline-note{border-left:2px solid #b6b0a4;padding-left:16px;color:#565448;font-size:16px}
.example{padding-left:16px;border-left:2px solid #b4c6ba}.example-label{font:600 12px system-ui,sans-serif;color:#536b5d;margin-right:8px}
figure{margin:22px 0 32px}figcaption{line-height:1.65;margin-top:8px}
.quiz-intro{color:#586259}.quiz-card{margin:22px 0;background:#fffdf8;border:1px solid #bbc8be;border-radius:12px;overflow:hidden}
.quiz-question{padding:23px 24px;background:#edf2ed;border-bottom:1px solid #d4ded4}
.quiz-kicker{font:700 12px/1.4 system-ui,sans-serif;letter-spacing:.08em;color:#345b48}
.quiz-question h3{color:#203e30;font-size:22px;line-height:1.6;margin:10px 0 0}
.quiz-answer summary{cursor:pointer;padding:15px 24px;font:600 15px/1.7 system-ui,sans-serif;color:#375844}
.answer-body{padding:20px 24px 24px;background:#fff8e9;border-top:1px dashed #d6be88}
.answer-label{font:700 12px/1.4 system-ui,sans-serif;letter-spacing:.08em;color:#785513}
.answer-body p{margin:12px 0}.answer-body a{font-size:15px;text-underline-offset:3px}
.answer-action-close{display:none}.quiz-answer[open] .answer-action-open{display:none}.quiz-answer[open] .answer-action-close{display:inline}
button:focus-visible,summary:focus-visible,a:focus-visible{outline:3px solid #3f775b;outline-offset:4px}
@media(max-width:600px){h1{font-size:32px}h2{font-size:25px}.inline-reading{padding-left:12px}.inline-reading h3{font-size:21px}.quiz-question,.answer-body{padding:18px}.quiz-question h3{font-size:20px}.quiz-answer summary{padding:15px 18px}}
@media print{.course-toc,.quiz-answer summary,.reading-scope>summary{display:none}.reading-scope>aside{display:block}.quiz-card{break-inside:avoid}.quiz-question,.answer-body{padding:12px}.inline-reading{border-left-width:1px}section>small{break-after:avoid}figure img{max-height:650px;object-fit:contain}.source-tag,h3{break-after:avoid}}
'''

def esc(s):
    return html.escape(s, quote=True)


def main():
    with tempfile.TemporaryDirectory(prefix='gse5-render-') as work:
        base = Path(work) / 'base.html'
        subprocess.run([sys.executable, str(SKILL / 'scripts/course_notes.py'), 'render', '--notes', str(ROOT / 'notes.json'), '--index', str(ROOT / 'chunks/index.json'), '--out', str(base)], check=True)
        page = base.read_text()
    for number, (section, order) in enumerate(zip(NOTE['sections'], ORDER), 1):
        pattern = rf'<section id="s{number}">.*?</section>'
        old = re.search(pattern, page, re.S).group()
        figures = re.findall(r'<figure>.*?</figure>', old, re.S)
        assert len(figures) == len(section['frames'])
        images = {}
        for frame, figure in zip(section['frames'], figures):
            key = str(frame['page']) if 'page' in frame else ('v1' if frame['time'] == 1274.79 else 'v2')
            images[key] = figure
        used = {k: set() for k in ['p', 'e', 'n', 'f']}
        body = re.match(r'.*?</h2>', old, re.S).group()
        for token in order.split():
            kind, key = token[0], token[1:]
            if kind == 'x':
                entry = MAP[int(key)]
                assert entry['section'] == number
                index = entry['editor_note_index']
                text = section['editor_notes'][index].split('）：', 1)[1]
                used['n'].add(index)
                used['f'].add(key)
                body += f'<div class="inline-reading" id="slide-{key}"><div class="source-tag">讲义延伸 · 课堂未展开 · <a href="https://jyywiki.cn/GSE/2026/slides5.html">原讲义第 {key} 页</a></div><h3>{esc(entry["title"])}</h3><p class="bridge">{esc(entry["bridge"])}</p><p>{esc(text)}</p>{images[key]}</div>'
            elif kind == 'f':
                assert key not in used['f']
                used['f'].add(key)
                body += images[key]
            else:
                index = int(key)
                assert index not in used[kind]
                used[kind].add(index)
                field = {'p': 'paragraphs', 'e': 'examples', 'n': 'editor_notes'}[kind]
                text = esc(section[field][index])
                if kind == 'n':
                    body += f'<p class="inline-note"><span class="source-tag">整理者说明</span><br>{text}</p>'
                elif kind == 'e':
                    body += f'<p class="example"><span class="example-label">案例回扣</span>{text}</p>'
                else:
                    body += f'<p>{text}</p>'
        for kind, field in [('p', 'paragraphs'), ('e', 'examples'), ('n', 'editor_notes')]:
            assert used[kind] == set(range(len(section.get(field, [])))), (number, field)
        assert used['f'] == set(images), number
        page = page.replace(old, body + '</section>', 1)
    quiz = '<section id="self-test"><h2>自测：先回答，再核对</h2><p class="quiz-intro">先用自己的话回答，再展开参考答案。答不清楚时，沿回查链接回到对应知识点。</p>'
    for i, item in enumerate(NOTE['self_test'], 1):
        quiz += f'<article class="quiz-card"><div class="quiz-question"><div class="quiz-kicker">问题 {i:02d}</div><h3 id="q{i}">{esc(item["question"])}</h3></div><details class="quiz-answer"><summary aria-describedby="q{i}"><span class="answer-action-open">查看参考答案</span><span class="answer-action-close">收起参考答案</span></summary><div class="answer-body"><div class="answer-label">参考答案 · 核对思路</div><p>{esc(item["answer"])}</p><a href="#s{item["section"]}">回查第 {item["section"]} 节 →</a></div></details></article>'
    page = re.sub(r'<section id="self-test">.*?</section>', lambda _: quiz + '</section>', page, flags=re.S)
    page = page.replace('<nav>', '<details class="course-toc"><summary>课程目录 · 展开跳转</summary><nav>', 1).replace('</nav>', '</nav></details>', 1)
    page = page.replace('<main><aside>', '<main><details class="reading-scope"><summary>来源与阅读范围</summary><aside>', 1).replace('</aside>', '</aside></details>', 1)
    page = page.replace('</head>', f'<style id="integrated-pilot">{CSS}</style></head>', 1)
    # Print contains answers and limitations; after printing restore the reader's state.
    page = page.replace('</body>', '''<script>
let printState=[];addEventListener('beforeprint',()=>{printState=[...document.querySelectorAll('.quiz-answer,.reading-scope')].map(el=>[el,el.open]);printState.forEach(([el])=>el.open=true)});addEventListener('afterprint',()=>printState.forEach(([el,open])=>el.open=open));
</script></body>''', 1)
    (ROOT / '课堂笔记.html').write_text(page)
    print('Integrated pilot rendered; all prose and 40 figures accounted for.')


if __name__ == '__main__':
    main()
