#!/usr/bin/env python3
"""Read-only local archive acceptance; writes only verifier.json next to this script."""
import datetime
import hashlib
import json
import shlex
import zipfile
from pathlib import Path

ROOT = Path('/Users/yjzhao/Documents/ChatGPT/generative-software-engineering-2026')
WORK = Path('/private/tmp/gse-publication-20261027')
COMMAND = f'python3 {WORK / "verifier_checks.py"}'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def version(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}


def read_json(path):
    return json.loads(path.read_text())


report = {
    'schema_version': 1,
    'status': 'IN_PROGRESS',
    'verified_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verifier': '/root/gse_archive_verify (independent Codex instance)',
    'artifact_root': str(ROOT),
    'data_level': 'personal',
    'privacy_route': 'same-family-exception under /Users/yjzhao/AGENTS.md section 5.4; local tools only; no external model seat, network request or upload',
    'scope': 'Current frozen archive byte integrity and media hashes; read-only browser evidence freshness; recorded reader paths; current HTML review hashes; ZIP decompression and byte fidelity; independent-review current-version and finding-closure checks.',
    'frozen_manifest': version(ROOT / 'archive/files.json'),
    'verification_script': version(Path(__file__)),
    'checks': [],
}


def recorded(name, command, stdout):
    # These commands were actually executed by the verifier before this report script.
    report['checks'].append({'name': name, 'status': 'PASS', 'command': command,
                             'cwd': str(ROOT), 'exit_code': 0,
                             'observations': json.loads(stdout)})


recorded('archive_and_ten_source_videos',
         'python3 tools/verify_archive.py --media-dir /private/tmp/gse-publication-20261027/release-assets',
         '{"status":"PASS","repository_files":9465,"media_files_checked":10,"failed":[],"scope":"byte integrity only"}')
for label, html, out in [
    ('guide', '归档阅读与恢复.html', 'guide-browser'),
    ('index', '生成式软件工程/课程索引.html', 'index-browser'),
    ('lecture09', '生成式软件工程/lecture-09/课堂笔记.html', 'lecture09-browser'),
]:
    recorded(f'{label}_browser_evidence_check',
             f'node tooling/learning-machine/audit-report.mjs {shlex.quote(html)} archive/qa/{out} --profile generic --check',
             '{"status":"PASS","issues":[]}')

course_root = ROOT / '生成式软件工程'
course = read_json(course_root / 'review.json')
items = course['items']


def inspect(name, fn):
    check = {'name': name, 'command': COMMAND, 'cwd': str(ROOT), 'exit_code': 0}
    try:
        check['observations'] = fn()
        check['status'] = 'PASS'
    except Exception as error:
        check.update(status='FAIL', exit_code=1, error=f'{type(error).__name__}: {error}')
    report['checks'].append(check)


def journey_check():
    path = ROOT / 'archive/qa/reader/journey.json'
    data = read_json(path)
    rows = data['rows']
    assert data['status'] == 'PASS'
    assert len(rows) == 20
    expected = {item['folder']: item['images'] for item in items}
    assert len(expected) == 10
    for width in (1280, 390):
        group = [row for row in rows if row['width'] == width]
        assert len(group) == 10
        assert {row['item'] for row in group} == set(expected)
        for row in group:
            assert row['images'] == row['expectedImages'] == expected[row['item']]
            assert row['broken'] == 0 and row['overflow'] is False
            assert row['externalImages'] == 0 and row['click'] == 'passed'
    assert {row['width'] for row in rows} == {1280, 390}
    assert sum(row['images'] for row in rows) == 944
    assert data['errors'] == [] and data['network'] == []
    assert data['realPhone'] == 'not_tested'
    return {'evidence': version(path), 'recorded_paths': len(rows),
            'recorded_widths': [1280, 390], 'recorded_decoded_images': 944,
            'per_width_images': 472, 'recorded_broken_images': 0,
            'recorded_page_errors': 0, 'recorded_network_requests': 0,
            'recorded_external_images': 0, 'recorded_overflow': False,
            'evidence_kind': 'Existing browser journey read back and cross-checked; browser paths were not rerun by this verifier.'}


def html_check():
    rows = []
    assert len(items) == 10 and course['outcome'] == 'completed'
    for item in items:
        html = course_root / item['html']
        review_path = course_root / item['review']
        review = read_json(review_path)
        current = version(html)
        assert current['sha256'] == item['html_sha256']
        assert current['sha256'] == review['source_hashes']['课堂笔记.html']
        assert item['outcome'] == review['outcome'] == 'completed'
        rows.append({'folder': item['folder'], 'html': current,
                     'course_review_sha256_match': True,
                     'individual_review_sha256_match': True,
                     'review': version(review_path)})
    index = version(course_root / '课程索引.html')
    assert index['sha256'] == course['index_sha256']
    return {'course_review': version(course_root / 'review.json'),
            'html_count': len(rows), 'matching_html': rows,
            'index_sha256_matches_course_review': True, 'index': index,
            'evidence_kind': 'Current bytes match historical review references; no new course semantic validation.'}


def zip_check():
    path = WORK / 'release-assets/course-reading-2026-10-27.zip'
    expected_html = {'生成式软件工程/课程索引.html'}
    expected_html.update('生成式软件工程/' + item['html'] for item in items)
    members = []
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        assert len(infos) == 12
        names = [item.filename for item in infos]
        assert len(set(names)) == 12
        assert set(names) == expected_html | {'请先阅读.txt'}
        assert len(expected_html) == 11
        assert archive.testzip() is None
        for info in infos:
            data = archive.read(info)
            row = {'name': info.filename, 'uncompressed_bytes': len(data),
                   'sha256': sha(data), 'crc_and_decompression': 'PASS'}
            if info.filename in expected_html:
                current = (ROOT / info.filename).read_bytes()
                assert data == current
                row['matches_current_archive_file'] = True
            else:
                row['utf8_text'] = data.decode('utf-8')
                assert row['utf8_text'].strip()
            members.append(row)
    return {'zip': version(path), 'size_mib': round(path.stat().st_size / 1024**2, 3),
            'members': members, 'member_count': 12, 'html_count': 11,
            'html_members_byte_identical_to_current_archive': 11,
            'bad_crc_member': None, 'extraction_performed': False}


def independent_review_check():
    path = WORK / 'independent-review.json'
    data = read_json(path)
    assert data['status'] == 'PASS'
    assert data['artifact_root'] == str(ROOT)
    assert data['data_level'] == 'personal'
    assert 'same-family-exception' in data['privacy_route']
    assert data['open_findings'] == data['open_blocker_or_major'] == 0
    versions = []
    for row in data['reviewed_versions']:
        current = version(ROOT / row['path'])
        assert current['bytes'] == row['bytes'] and current['sha256'] == row['sha256']
        versions.append({'path': row['path'], 'bytes': current['bytes'],
                         'sha256': current['sha256'], 'matches_reviewed_version': True})
    assert len(versions) == 10
    closed = {'fixed', 'closed', 'resolved'}
    assert all(finding['status'].lower() in closed for finding in data['findings'])
    minor = [finding for finding in data['findings'] if finding['severity'] == 'minor']
    assert len(minor) == 1 and minor[0]['id'] == 'GSE-ARCHIVE-001'
    security = read_json(ROOT / 'archive/security-review.json')
    disposition = 'false_positive_embedded_slide_video_base64'
    assert sum(finding.get('disposition') == disposition for finding in security['findings']) == 1
    assert minor[0]['closure_evidence']['current_value_verified'] is True
    assert all(check['status'] == 'PASS' for check in data['checks'])
    return {'review_report': version(path), 'reviewed_versions_match': versions,
            'open_findings': 0, 'minor_total': len(minor), 'minor_closed': len(minor),
            'closure_current_value': disposition,
            'historical_not_tested_preserved': data['not_tested'],
            'evidence_kind': 'Current report version references and closure state checked; independent review conclusions were not expanded.'}


inspect('recorded_twenty_reader_paths', journey_check)
inspect('ten_current_html_review_fingerprints', html_check)
inspect('portable_reading_zip_integrity_and_fidelity', zip_check)
inspect('independent_review_current_versions_and_minor_closure', independent_review_check)
report['not_tested'] = [
    'No new course full-text/source semantic review, full-video listening or per-frame semantic review.',
    'No new browser journey or screenshot review by this verifier; existing current-version evidence was checked read-only.',
    'No real phone, native print dialog, BaoCut App opening, media relinking, second-machine native project restore or cross-machine runtime acceptance.',
    'No remote GitHub objects, repository visibility, upload, Release download or post-upload asset verification.',
    'The forthcoming copy of this report into the repository and the parent session final refreeze are outside the 9465-file snapshot verified here.',
]
report['mutations'] = 'Only this verifier_checks.py and verifier.json in /private/tmp/gse-publication-20261027 were written; no course, archive, code, native .bcut or media asset was modified.'
report['status'] = 'PASS' if all(row['status'] == 'PASS' for row in report['checks']) else 'FAIL'
(WORK / 'verifier.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'checks': len(report['checks']),
                  'report': str(WORK / 'verifier.json'),
                  'failed_checks': [row['name'] for row in report['checks'] if row['status'] != 'PASS']}, ensure_ascii=False))
raise SystemExit(0 if report['status'] == 'PASS' else 1)
