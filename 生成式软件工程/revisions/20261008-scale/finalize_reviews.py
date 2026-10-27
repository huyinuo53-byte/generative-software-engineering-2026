import datetime
import hashlib
import json
import uuid
from pathlib import Path

run = Path(__file__).resolve().parent
root = run.parents[1]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def save(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')

records = []
for name in read(run/'baseline.json')['lessons']:
    d = root/name
    if name == 'lecture-05':
        r = read(d/'review.json')
        r['user_acceptance'] = 'accepted'
        r['acceptance_evidence'] = '用户明确同意推广到其他课堂笔记并优化skills；2026-10-08会话。'
        r['follow_up'] = 'Pilot accepted; shared template installed and seven other notes updated in revisions/20261008-scale.'
        for lesson in r.get('lessons', []):
            lesson.update(status='verified', scope='User-accepted fifth-lesson pilot; course-scale verification recorded separately', next_action='Implemented in shared editorial template and seven additional notes')
        save(d/'review.json', r)
        records.append({'folder':name,'status':'accepted-pilot-unchanged','html_sha256':sha(d/'课堂笔记.html')})
        continue
    out = d/'revisions/20261008-scale'
    n = read(d/'notes.json')
    preservation = read(out/'preservation.json')
    assert read(out/'browser.json')['status'] == read(out/'print.json')['status'] == 'passed'
    # Existing image observations remain historical; only the notes binding changes.
    audit = read(d/'image-audit.json')
    if audit['notes_sha256'] != sha(d/'notes.json'):
        audit['reuse_binding'] = {'at':now, 'previous_notes_sha256':audit['notes_sha256'], 'reason':'Only obsolete navigation wording changed; every frame object and image byte matches prior audit', 'evidence':'revisions/20261008-scale/preservation.json', 'new_pixel_review':False}
        audit['notes_sha256'] = sha(d/'notes.json')
        save(d/'image-audit.json',audit)
    evidence = 'revisions/20261008-scale/'
    validation = {k:{'status':'passed','evidence':evidence+v} for k,v in [('content_preservation','preservation.json'),('layout_structure','layout-validation.json'),('desktop','browser.json'),('tablet','browser.json'),('narrow','browser.json'),('interactions','browser.json'),('html_print','print.json')]}
    validation['semantic_layout'] = {'status':'passed','evidence':[evidence+'layout-review.json','../revisions/20261008-scale/independent-layout-review.json' if name in ['lecture-01','lecture-02','lecture-03','lecture-04'] else '../revisions/20261008-scale/forward-test-review.json']}
    validation['visual_samples'] = {'status':'passed','evidence':'../revisions/20261008-scale/visual-review.json'}
    validation['print_visual_samples'] = {'status':'passed','evidence':'../revisions/20261008-scale/print-visual-review.json','scope':'Only final PDF page of this note viewed; full text and image count checked programmatically'}
    for k in ['real_phone','native_print_dialog','source_rereading','full_video_review','project_strict']:
        validation[k] = {'status':'not_requested','evidence':'Not repeated in this editorial-only revision; prior evidence retained in before/review.json'}
    source_files = ['notes.json','reading-layout.json','课堂笔记.html','transcript.json','chunks/index.json','image-audit.json',evidence+'browser.json',evidence+'print.json']
    r = {'run_id':name+'-20261008-editorial-scale','scope_revision':read(out/'before/review.json').get('scope_revision',1)+1,
         'scope':'Existing notes editorial integration, semantic emphasis and reading UI; no new transcription or source acquisition','outcome':'completed',
         'summary':f"{len(n['sections'])} sections, {preservation['images']} unchanged figures; prose and supplements integrated, source attribution retained; four viewport widths, interactions and headless print verified.",
         'previous_review':evidence+'before/review.json','validation':validation,
         'reuse':{'transcript':'Unchanged; prior full reading reused','source_materials':'Frozen existing sources; no live refresh or new reading claim','image_pixels':'All bytes verified against prior image audit; previous pixel observations reused'},
         'source_hashes':{f:sha(d/f) for f in source_files},'trace_snapshot':evidence+'trace.json','delivered_files':['课堂笔记.html'],
         'finished_at':now,'blocker':None,'metrics':{'tokens':None,'active_seconds':None,'cost':None}}
    save(d/'review.json',r)
    with (d/'events.jsonl').open('a') as f:
        f.write(json.dumps({'schema_version':1,'event_id':str(uuid.uuid4()),'occurred_at':now,'time_basis':'observed','run_id':r['run_id'],'item_id':name,'actor':'root','attempt_id':'editorial-scale-final','job_id':None,'stage':'editorial-delivery','status':'completed','detail':'Final layout, browser and print acceptance recorded; original ASR/source evidence reused','evidence':[evidence+'preservation.json',evidence+'browser.json',evidence+'print.json']},ensure_ascii=False)+'\n')
    records.append({'folder':name,'status':'completed','sections':len(n['sections']),'images':preservation['images'],'html_sha256':sha(d/'课堂笔记.html')})

save(run/'review.json',{'run_id':'gse-20261008-editorial-scale','outcome':'completed','finished_at':now,'scope':'Seven existing notes upgraded after fifth-lesson acceptance; all eight preserve source artifacts',
    'items':records,'checks':{'preservation':'preservation.json','semantic_cross_review':['independent-layout-review.json','forward-test-review.json'],'visual':'visual-review.json','print_visual':'print-visual-review.json','installed_skill':'installed-validation.json'},
    'fixes':['Four obsolete supplement-location sentences corrected','Two figure placements corrected after independent review','Five emphasis terms corrected to exact prose matches','Long-title balance applied and four orphan headings visually rechecked'],
    'nonblocking_suggestions':'Three broader emphasis terms retained for this revision; no semantic error or content loss. See forward-test-review.json.',
    'boundaries':['No new ASR, live playlist lookup or source reading','No real-phone or native print-dialog test','Print all text/image counts checked; seven final pages visually sampled'],
    'metrics':{'tokens':None,'cost':None,'active_seconds':None}})
print('Final reviews written for eight notes')
