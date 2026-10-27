import pathlib, json, hashlib, sys, subprocess, collections, datetime
from html.parser import HTMLParser

root = pathlib.Path(__file__).resolve().parent
skill = pathlib.Path('/Users/yjzhao/.codex/skills/baocut-course-notes/scripts')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.anchors, self.images, self.text = [], [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and a.get('href', '').startswith('#'): self.anchors.append(a['href'][1:])
        if tag == 'img' and a.get('src'): self.images.append(a['src'])
    def handle_data(self, data):
        self.text.append(data)

for name in sys.argv[1:]:
    run = root / name
    notes = json.loads((run / 'notes.json').read_text())
    index = json.loads((run / 'chunks/index.json').read_text())
    expected = {s['id']: s for s in index['sentences']}
    coverage = collections.Counter()
    for section in notes['sections']:
        for sid in section['source_ids']:
            assert sid in expected
            coverage[sid] += 1
            source = expected[sid]
            assert section['start'] <= source['start'] + .02 and section['end'] + .02 >= source['end'], sid
    for omitted in notes.get('omitted', []): coverage[omitted['id']] += 1
    assert set(coverage) == set(expected) and all(n == 1 for n in coverage.values())
    assert set(notes['read_chunks']) == {c['id'] for c in index['chunks']}
    result = subprocess.run(['python3', str(skill / 'validate_image_audit.py'), '--notes', str(run / 'notes.json'), '--audit', str(run / 'image-audit.json')], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    (run / 'qa/image-validator.txt').write_text(result.stdout)
    page = Page((run / '课堂笔记.html').read_text())
    assert len(page.ids) == len(set(page.ids))
    assert all(x in page.ids for x in page.anchors)
    assert all(x.startswith('data:image/') for x in page.images)
    image_count = sum(len(s.get('frames', [])) for s in notes['sections'])
    assert len(page.images) == image_count
    text = ''.join(page.text)
    blocks = notes['limitations'] + notes.get('summary', [])
    for section in notes['sections']:
        blocks += [section['title']] + section['paragraphs'] + section.get('examples', []) + section.get('editor_notes', [])
    for item in notes.get('supplements', []): blocks += [item['title'], item['text']]
    for item in notes.get('self_test', []):
        blocks += [item['question'], item['answer']]
        assert 1 <= item.get('section', 1) <= len(notes['sections'])
    assert all(b in text for b in blocks), 'missing HTML body block'
    html_hash = sha(run / '课堂笔记.html')
    browser = json.loads((run / 'qa/browser.json').read_text())
    assert browser['html_sha256'] == html_hash, 'browser QA is stale'
    for mode in ['mobile', 'desktop']:
        test = browser['viewports'][mode]
        state = test['state']
        assert state['scrollWidth'] <= state['width'] and not state['brokenImages'] and not state['errors']
        assert not state['badAnchors'] and not state['duplicateIds'] and state['images'] == image_count
        assert test['interaction']['tocOpened'] and test['interaction']['anchorJump']
        assert test['zoom']['open'] and test['zoom']['imageLoaded'] and test['close']['closed']
        assert [x['style'] for x in test['zoom']['scales']] == ['200%', '300%', '100%']
    printing = json.loads((run / 'qa/print.json').read_text())
    assert printing['html_sha256'] == html_hash and not printing['missing_blocks']
    assert printing['printed_images'] == image_count
    audits = [p.name for p in [run / 'audit.json', run / 'audit-independent07.json', run / 'cross-review.json'] if p.exists()]
    assert audits
    static = {'status': 'passed', 'source_units': len(expected), 'coverage_once': True, 'source_time_containment': True, 'html_text_blocks': len(blocks), 'all_text_present': True, 'inline_images': image_count, 'duplicate_ids': 0, 'broken_anchors': 0, 'html_sha256': html_hash}
    write(run / 'qa/final-static.json', static)
    review_path = run / 'review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else {'run_id': name + '-20261002', 'lessons': []}
    review.update({'outcome': 'completed', 'summary': f"完整阅读{len(index['chunks'])}块转写，{len(expected)}来源单元逐项覆盖；{len(notes['sections'])}节、{image_count}图。内容与逐图复核、最终HTML结构/桌面/390px窄屏/打印保真检查通过。未做真实手机或逐秒音频听审。", 'blocker': None, 'resume_condition': None, 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'delivered_files': ['课堂笔记.html'], 'audit': audits})
    validation = review.setdefault('validation', {})
    for check, evidence in {'content': audits, 'source_coverage': 'qa/final-static.json', 'image_integrity': 'image-audit.json', 'html_static': 'qa/final-static.json', 'desktop': 'qa/browser.json', 'narrow': 'qa/browser.json', 'html_print': 'qa/print.json'}.items():
        validation[check] = {'status': 'passed', 'evidence': evidence}
    validation['real_phone'] = {'status': 'not_requested', 'evidence': '未做真实手机设备实测；390px仅浏览器模拟'}
    validation['pdf'] = {'status': 'not_requested', 'evidence': '临时PDF只用于HTML打印检查，不作为完整PDF交付'}
    validation['package'] = {'status': 'not_requested', 'evidence': '逐视频独立单文件HTML'}
    checks = [p for p in [run / 'project-check.json', run / 'sources/project-check.json'] if p.exists()]
    if checks:
        check = json.loads(checks[0].read_text())
        assert check['data']['ready']
        validation['project_strict'] = {'status': 'passed', 'evidence': str(checks[0].relative_to(run))}
    metrics = review.setdefault('metrics', {})
    metrics.update({'sections': len(notes['sections']), 'source_units': len(expected), 'transcript_chunks': len(index['chunks']), 'selected_images': image_count, 'text_blocks': len(blocks), 'tokens': None, 'cost': None})
    review['source_hashes'] = {p: sha(run / p) for p in ['transcript.json', 'chunks/index.json', 'notes.json', '课堂笔记.html', 'image-audit.json', 'qa/browser.json', 'qa/print.json']}
    review['trace_snapshot'] = 'trace-final.json'
    write(review_path, review)
    if not (run / 'run.json').exists():
        write(run / 'run.json', {'schema_version': 2, 'run_id': review['run_id'], 'batch_id': 'GSE-20261002', 'item_id': name, 'scope_revision': 1, 'source_url': notes['source_url'], 'requested_outputs': ['complete_mobile_html', 'quality_review'], 'required_checks': ['content', 'source_coverage', 'image_integrity', 'html_static', 'desktop', 'narrow'], 'sources': [{'path': 'transcript.json', 'kind': 'original_export', 'transcript_origin': 'reused' if name in ['lecture-02','lecture-05','lecture-06','lecture-07'] else 'new'}]})
    subprocess.run(['python3', str(skill / 'course_notes.py'), 'record', '--run', str(run), '--stage', 'final_quality_review', '--status', 'completed', '--actor', 'coordinator', '--evidence', 'review.json', '--detail', review['summary']], check=True, stdout=subprocess.DEVNULL)
    paths = [p for p in run.rglob('*') if p.is_file() and p.suffix in ['.json', '.jsonl', '.png', '.jpg', '.jpeg', '.pdf', '.html'] and not p.name.startswith('trace-') and p.name not in ['desktop.html', 'mobile.html'] and p.name != 'pipeline.jsonl']
    ids = {str(p.relative_to(run)) for p in paths}
    artifacts = []
    for p in sorted(paths):
        rel = str(p.relative_to(run))
        deps = []
        if rel == 'notes.json': deps = ['transcript.json', 'chunks/index.json']
        if rel == '课堂笔记.html': deps = ['notes.json', 'chunks/index.json'] + [str(f['path']) for s in notes['sections'] for f in s.get('frames', [])]
        if rel.startswith('qa/') and rel.endswith('.json'): deps = ['课堂笔记.html']
        if rel == 'review.json': deps = ['notes.json', '课堂笔记.html', 'image-audit.json', 'qa/browser.json', 'qa/print.json']
        artifacts.append({'id': rel, 'path': rel, 'depends_on': [d for d in deps if d in ids]})
    write(run / 'trace-final-spec.json', {'schema_version': 1, 'run_id': review['run_id'], 'basis': 'observed_build', 'root': '.', 'artifacts': artifacts})
    subprocess.run(['python3', str(skill / 'trace_artifacts.py'), 'capture', '--spec', str(run / 'trace-final-spec.json'), '--out', str(run / 'trace-final.json')], check=True, stdout=subprocess.DEVNULL)
    print(name, 'sealed', len(expected), image_count, flush=True)
