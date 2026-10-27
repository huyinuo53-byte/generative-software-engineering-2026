import json
import sys
from pathlib import Path

skill = Path('/Users/yjzhao/.codex/skills/baocut-course-notes')
sys.path.insert(0,str(skill/'scripts'))
import trace_artifacts as trace
run = Path(__file__).resolve().parent
root = run.parents[1]
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def read(p): return json.loads(p.read_text())

skill_files = ['scripts/course_notes.py','scripts/reading_layout.py','assets/template.html','assets/editorial.html','assets/editorial.css','assets/editorial.js']
checks = []
for p in sorted(root.glob('*/reading-layout.json')):
    d = p.parent
    out = d/'revisions/20261008-scale'
    artifacts = []
    def add(ident,path,deps=()):
        artifacts.append({'id':ident,'path':str(path),'depends_on':list(deps)})
    add('transcript','transcript.json')
    add('index','chunks/index.json',['transcript'])
    frame_ids=[]
    for i,s in enumerate(read(d/'notes.json')['sections']):
        for j,f in enumerate(s.get('frames', [])):
            ident=f'frame-{i}-{j}';add(ident,f['path']);frame_ids.append(ident)
    add('notes','notes.json',['index']+frame_ids)
    add('layout','reading-layout.json',['notes'])
    build_ids=[]
    for i,f in enumerate(skill_files):
        ident=f'build-{i}';add(ident,skill/f);build_ids.append(ident)
    add('html','课堂笔记.html',['layout','notes','index']+build_ids)
    prefix='revisions/20261008-scale/'
    add('layout-check',prefix+'layout-validation.json',['notes','layout'])
    add('browser',prefix+'browser.json',['html'])
    add('pdf',prefix+'print-check.pdf',['html'])
    add('print',prefix+'print.json',['pdf','html','notes'])
    add('preservation',prefix+'preservation.json',['html','notes','layout']+frame_ids)
    screenshot_ids=[]
    for i,img in enumerate(sorted(out.glob('*.png'))):
        ident=f'visual-{i}';add(ident,str(img.resolve()),['pdf' if img.name=='print-last-page.png' else 'html']);screenshot_ids.append(ident)
    add('review','review.json',['browser','print','layout-check','preservation']+screenshot_ids)
    spec={'schema_version':1,'run_id':d.name+'-20261008-editorial-scale','basis':'observed_build','root':str(d.resolve()),'artifacts':artifacts}
    save(out/'trace-spec.json',spec);trace.capture(out/'trace-spec.json',out/'trace.json');result=trace.check(out/'trace.json');save(out/'trace-check.json',result);assert not result['changed_files'] and not result['unavailable_files'];checks.append(result)

artifacts=[]
def add(ident,path,deps=()): artifacts.append({'id':ident,'path':str(path),'depends_on':list(deps)})
for i,d in enumerate(sorted(root.glob('*/reading-layout.json'))):
    add('lesson-'+str(i),str((d.parent/'revisions/20261008-scale/trace.json').resolve()))
lesson_ids=[x['id'] for x in artifacts]
add('approved-pilot',str((root/'lecture-05/课堂笔记.html').resolve()))
add('index-generator',str((root/'build_index.py').resolve()))
add('course-index',str((root/'课程索引.html').resolve()),lesson_ids+['approved-pilot','index-generator'])
add('index-qa','index-browser.json',['course-index'])
for name in ['independent-layout-review.json','forward-test-review.json','visual-review.json','print-visual-review.json','preservation.json','installed-validation.json','skill-installation.json','review.json']:
    add(name,name,lesson_ids)
add('course-review',str((root/'review.json').resolve()),['review.json','index-qa'])
add('manifest',str((root/'manifest.json').resolve()),['course-review'])
save(run/'trace-spec.json',{'schema_version':1,'run_id':'gse-20261008-editorial-scale','basis':'observed_build','root':str(run),'artifacts':artifacts})
trace.capture(run/'trace-spec.json',run/'trace.json')
result=trace.check(run/'trace.json');save(run/'trace-check.json',{'course':result,'lessons':checks,'claim':'Dependency hashes, not proof of content quality; semantic and browser evidence recorded separately'})
assert not result['changed_files'] and not result['unavailable_files']
print('Course and seven new lesson snapshots sealed and checked')
