import pathlib, subprocess, time, json, hashlib, sys, re

root = pathlib.Path(__file__).resolve().parent
chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
for name in sys.argv[1:]:
    run = root / name
    output = pathlib.Path('/tmp') / ('gse-' + name + '-print.pdf')
    logfile = run / 'qa' / 'print.log'
    start = time.time()
    with logfile.open('w') as log:
        process = subprocess.Popen([chrome, '--headless', '--disable-gpu', '--disable-background-networking', '--no-first-run', '--no-default-browser-check', '--no-pdf-header-footer', '--user-data-dir=/tmp/gse-print-qa-profile', '--print-to-pdf=' + str(output), (run / '课堂笔记.html').as_uri()], stdout=log, stderr=log)
        try:
            for _ in range(60):
                if output.exists() and output.stat().st_mtime > start and output.stat().st_size > 1000:
                    time.sleep(1)
                    break
                if process.poll() is not None:
                    break
                time.sleep(.5)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    if not output.exists() or output.stat().st_mtime < start:
        raise RuntimeError('Print did not produce current output: ' + name)
    textfile = output.with_suffix('.txt')
    subprocess.run(['pdftotext', '-layout', str(output), str(textfile)], check=True)
    text = textfile.read_text()
    compact = lambda s: re.sub(r'\s+', '', s)
    notes = json.loads((run / 'notes.json').read_text())
    blocks = notes['limitations'] + notes.get('summary', [])
    for section in notes['sections']:
        blocks += [section['title']] + section['paragraphs'] + section.get('examples', []) + section.get('editor_notes', [])
    for section in notes.get('supplements', []):
        blocks += [section['title'], section['text']]
    for item in notes.get('self_test', []):
        blocks += [item['question'], item['answer']]
    missing = [b for b in blocks if compact(b) not in compact(text)]
    info = subprocess.check_output(['pdfinfo', str(output)], text=True)
    images = subprocess.check_output(['pdfimages', '-list', str(output)], text=True)
    image_count = sum(bool(re.match(r'\s*\d+\s+\d+\s+image\s', line)) for line in images.splitlines())
    evidence = {'html_sha256': hashlib.sha256((run / '课堂笔记.html').read_bytes()).hexdigest(), 'method': 'isolated Chrome headless print; all text blocks checked against pdftotext; representative page visual inspection recorded separately', 'temporary_pdf': str(output), 'pdf_sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'text_blocks': len(blocks), 'missing_blocks': missing, 'printed_images': image_count, 'expected_images': sum(len(s.get('frames', [])) for s in notes['sections']), 'pdfinfo': info, 'status': 'passed' if not missing else 'pending'}
    (run / 'qa' / 'print.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2))
    print(name, 'missing', len(missing), 'images', image_count, flush=True)
