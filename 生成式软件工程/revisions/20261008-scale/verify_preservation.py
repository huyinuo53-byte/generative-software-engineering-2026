"""Verify this editorial revision against its frozen inputs and printed output."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent / 'skill-staging/scripts'))
from reading_layout import validate

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def diff(a, b, path=''):
    if type(a) != type(b):
        return [{'path': path, 'before': a, 'after': b}]
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        return [d for key in a for d in diff(a[key], b[key], path+'/'+str(key))]
    if isinstance(a, list):
        assert len(a) == len(b), path
        return [d for i in range(len(a)) for d in diff(a[i], b[i], path+'/'+str(i))]
    return [] if a == b else [{'path': path, 'before': a, 'after': b}]

baseline = json.loads((Path(__file__).parent/'baseline.json').read_text())
reports = []
allowed = {'lecture-01': ['/sections/10/editor_notes/0', '/sections/22/editor_notes/0'], 'lecture-03': ['/sections/24/paragraphs/4'], 'lecture-06': ['/sections/19/paragraphs/2']}
for name, files in baseline['lessons'].items():
    d = root/name
    for file in ['transcript.json', 'chunks/index.json']:
        assert sha(d/file) == files[file], (name, file)
    if name == 'lecture-05':
        assert sha(d/'notes.json') == files['notes.json']
        assert sha(d/'课堂笔记.html') == files['课堂笔记.html']
        reports.append({'lesson': name, 'approved_pilot_unchanged': True})
        continue
    out = d/'revisions/20261008-scale'
    note = json.loads((d/'notes.json').read_text())
    old = json.loads((out/'before/notes.json').read_text())
    changes = diff(old, note)
    assert sorted(c['path'] for c in changes) == sorted(allowed.get(name, [])), name
    layout = json.loads((d/'reading-layout.json').read_text())
    structure = validate(note, layout, (d/'notes.json').read_bytes())
    save(out/'layout-validation.json', structure)
    images = [f for s in note['sections'] for f in s.get('frames', [])]
    audit = json.loads((out/'before/image-audit.json').read_text())
    audited = {x['path']: x['sha256'] for x in audit['images']}
    for f in images:
        assert sha(d/f['path']) == audited[f['path']], (name, f['path'])
    text = subprocess.check_output(['pdftotext', '-layout', str(out/'print-check.pdf'), '-']).decode()
    normalize = lambda s: re.sub(r'\s+', '', s)
    blocks = note.get('summary', []) + note['limitations']
    for s in note['sections']:
        blocks += s['paragraphs'] + s.get('examples', []) + s.get('editor_notes', [])
    for x in note.get('supplements', note.get('official_slide_supplements', [])):
        blocks += [x['title'], x['text']]
    for q in note.get('self_test', []):
        blocks += [q['question'], q['answer']]
    blocks += [s['takeaway'] for s in layout['sections']]
    missing = [s for s in blocks if normalize(s) not in normalize(text)]
    assert not missing, (name, missing)
    image_list = subprocess.check_output(['pdfimages', '-list', str(out/'print-check.pdf')]).decode()
    count = sum(bool(re.match(r'\s*\d+\s+\d+\s+image\s', s)) for s in image_list.splitlines())
    assert count == len(images), (name, count, len(images))
    save(out/'print.json', {'status': 'passed', 'method': 'Chrome headless PDF; pdftotext -layout preserves literal end-of-line hyphens; whitespace-normalized exact blocks; pdfimages count; not native print dialog', 'blocks': len(blocks), 'missing': missing, 'images': count, 'html_sha256': sha(d/'课堂笔记.html'), 'pdf_sha256': sha(out/'print-check.pdf')})
    report = {'lesson': name, 'status': 'passed', 'changes': changes, 'all_other_notes_fields_unchanged': True, 'all_image_bytes_match_previous_audit': True, 'images': len(images), 'transcript_and_index_unchanged': True, 'html_sha256': sha(d/'课堂笔记.html'), 'layout_sha256': sha(d/'reading-layout.json')}
    save(out/'preservation.json', report)
    reports.append(report)
save(Path(__file__).parent/'preservation.json', {'status': 'passed', 'lessons': reports})
print(json.dumps({'status': 'passed', 'lessons': len(reports), 'navigation_copy_changes': sum(len(r.get('changes', [])) for r in reports)}, ensure_ascii=False))
