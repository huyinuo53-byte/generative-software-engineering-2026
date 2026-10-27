#!/usr/bin/env python3
"""Read-only recovery plan; recorded passes never replace content review or a writer lease."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

TRACE_TOOL = Path.home()/'.codex/skills/baocut-course-notes/scripts/trace_artifacts.py'
HTML_CHECKS = {'structure','html_static','html','desktop','narrow_screen','zoom_pan_close','console','print','ui','adversarial_review','adversarial_content'}
REQUIRED = ['content','structure','images','desktop','narrow_screen']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def plan(run):
    run=run.resolve()
    result={'run_dir':str(run),'read_only':True,'scope':'recorded evidence and hashes; no semantic re-review or execution',
            'writer_state':'unverified','can_execute':False,'stale':[],'stages':{},'blockers':[]}
    if not run.is_dir():raise ValueError('run directory does not exist')
    if (run/'ownership.json').exists():
        result['writer_state']='ownership_record_present'
        result['blockers'].append('Confirm the recorded writer/session and its agents have stopped; this command does not acquire ownership.')
    if not (run/'review.json').exists():
        transcript=(run/'transcript.json').exists() or (run/'transcript/transcript.json').exists()
        result.update(status='PENDING',first_pending='content' if transcript else 'source_acquisition',
                      next_action='Reuse the existing transcript and read it in chunks; do not rerun ASR.' if transcript else 'Inspect existing source/media/transcript evidence first.')
        return result
    review=load(run/'review.json')
    recorded={**review.get('checks',{}),**review.get('validation',{})}
    for key,value in recorded.items():
        key='narrow_screen' if key=='narrow' else key
        result['stages'][key]=value.get('status','pending') if isinstance(value,dict) else value
    for key in REQUIRED:result['stages'].setdefault(key,'pending')
    def invalidate(name):
        # HTML-only changes require export/reader review, not rereading unchanged transcripts/materials.
        keys=HTML_CHECKS if Path(name).suffix in ['.html','.css','.js'] or 'ui-review' in name else set(result['stages'])
        for key in keys & result['stages'].keys():
            if str(result['stages'][key]).startswith('passed'):result['stages'][key]='stale'
    hashes=dict(review.get('source_hashes',{}))
    transcript_name='transcript.json' if (run/'transcript.json').exists() else 'transcript/transcript.json'
    html_name=review.get('delivery_path','课堂笔记.html')
    for field,name in [('notes_sha256','notes.json'),('transcript_sha256',transcript_name),('html_sha256',html_name)]:
        if review.get(field):hashes[name]=review[field]
    snapshot_ref=review.get('trace_snapshot') or review.get('delivery_snapshot')
    snapshot=load((run/snapshot_ref).resolve()) if snapshot_ref and (run/snapshot_ref).resolve().is_relative_to(run) and (run/snapshot_ref).is_file() else None
    if snapshot:
        for item in snapshot.get('artifacts',[]):
            target=(Path(snapshot['root'])/item['path']).resolve()
            if target.is_relative_to(run):hashes.setdefault(str(target.relative_to(run)),item['sha256'])
    for name in ['notes.json',transcript_name,html_name]:
        if name not in hashes:result['stale'].append({'path':name,'reason':'no recorded fingerprint'})
    for name,digest in hashes.items():
        target=(run/name).resolve()
        if not target.is_relative_to(run):
            result['stale'].append({'path':name,'reason':'external fingerprint not checked by this planner'});continue
        if not target.is_file() or sha(target)!=digest:result['stale'].append({'path':name,'reason':'missing or changed'})
    for item in result['stale']:invalidate(item['path'])
    dependency_blocked=False
    if snapshot_ref:
        if not snapshot or not TRACE_TOOL.is_file():
            result['blockers'].append('Restore the declared dependency snapshot/checker, then replan before reusing evidence.')
            dependency_blocked=True
        else:
            checked=subprocess.run([sys.executable,str(TRACE_TOOL),'check','--snapshot',str((run/snapshot_ref).resolve())],capture_output=True,text=True)
            result['trace_exit_code']=checked.returncode
            try:trace=json.loads(checked.stdout)
            except ValueError:trace={}
            result['trace_result']=trace
            if checked.returncode!=0:
                if trace.get('status')=='changed':
                    paths={item['id']:item['path'] for item in snapshot['artifacts']}
                    for ident in trace.get('changed_files',[])+trace.get('unavailable_files',[]):
                        name=paths.get(ident,'unknown dependency')
                        result['stale'].append({'path':name,'reason':'native trace dependency changed/unavailable'})
                        invalidate(name)
                else:
                    result['blockers'].append('Dependency checker could not validate the declared snapshot; restore it before reuse.')
                    dependency_blocked=True
    if dependency_blocked:
        for key in result['stages']:
            if str(result['stages'][key]).startswith('passed'):result['stages'][key]='unverified_dependency'
    ordered=list(dict.fromkeys(REQUIRED+list(result['stages'])))
    def done(key):
        value=result['stages'][key]
        return value in ['passed','passed_for_declared_scope'] or (key not in REQUIRED and value=='not_requested')
    pending=[key for key in ordered if not done(key)]
    result.update(status='BLOCKED' if result['blockers'] else 'STALE' if result['stale'] else 'PENDING' if pending else 'RECORDED_CHECKS_CURRENT',
                  first_pending='dependency_evidence' if dependency_blocked else pending[0] if pending else None,pending=pending,
                  reusable_recorded_checks=[key for key in ordered if result['stages'][key] in ['passed','passed_for_declared_scope']],
                  not_required=[key for key in ordered if key not in REQUIRED and result['stages'][key]=='not_requested'],
                  next_action='Restore dependency snapshot/checker and replan.' if dependency_blocked else 'Confirm one writer, then resume first_pending; retain unchanged media/transcript/materials and rerun only invalidated checks.')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-dir',required=True,type=Path);args=parser.parse_args()
    try:result=plan(args.run_dir)
    except (OSError,ValueError,TypeError,KeyError) as error:
        print(json.dumps({'status':'BLOCKED','reason':str(error)},ensure_ascii=False));return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='RECORDED_CHECKS_CURRENT' else 2
if __name__=='__main__':sys.exit(main())
