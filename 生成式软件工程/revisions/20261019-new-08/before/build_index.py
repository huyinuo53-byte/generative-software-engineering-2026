# -*- coding: utf-8 -*-
import pathlib, json, html, hashlib, datetime

root = pathlib.Path(__file__).resolve().parent
items = [
    ('lecture-01', '01', '欢迎来到未来', 'Agent 如何进入生活、学习和工程；qrgen 的失败与架构转折。'),
    ('lecture-02', '02', '提示词工程', '上下文、可验证规格、分解与反馈，以及读论文和开放探索。'),
    ('lecture-03', '03', '软件仓库管理', '从项目快照到真实 Git 对象、冲突、提交与协作。'),
    ('lecture-04', '04', '软件仓库管理（2）', '修改与历史、Jujutsu、并发控制、工作区和个人助手实验。'),
    ('lecture-05', '05', '软件工程的来龙去脉', '需求与实现之间的距离、设计流程、契约、UML 与可靠反馈。'),
    ('lecture-06', '06', '需求和架构（1）', '教务系统需求、汉诺塔架构、时间、事件与可追溯的变化。'),
    ('lecture-07', '07', '需求和架构（2）', '经典抽象、可生长的接口、MVC/MVVM，以及事实与派生状态。'),
    ('extra-ai-slop', '短片', '失败的 AI Slop 数字永生尝试', 'AI 改编中的教育焦虑与图文偏移；约 2 分 49 秒的独立短片。'),
]
cards, reports = [], []
for folder, number, title, description in items:
    run = root / folder
    notes = json.loads((run / 'notes.json').read_text())
    review = json.loads((run / 'review.json').read_text())
    images = sum(len(s.get('frames', [])) for s in notes['sections'])
    latest = False
    label = ''
    cards.append(f'<a class="card {"latest" if latest else ""}" href="{folder}/课堂笔记.html"><div class="number">{number}</div><div><h2>{html.escape(title)}</h2>{label}<p>{html.escape(description)}</p><small>{len(notes["sections"])} 节 · {images} 幅配图 · {len(notes.get("self_test", []))} 道自测</small></div><span aria-hidden="true">↗</span></a>')
    reports.append({'folder': folder, 'title': title, 'html': folder + '/课堂笔记.html', 'html_sha256': hashlib.sha256((run / '课堂笔记.html').read_bytes()).hexdigest(), 'review': folder + '/review.json', 'outcome': review['outcome'], 'sections': len(notes['sections']), 'images': images, 'source_units': len(json.loads((run / 'chunks/index.json').read_text())['sentences']), 'transcript': 'reused' if number in ['02','05','06','07'] else 'new'})
sections = sum(x['sections'] for x in reports)
images = sum(x['images'] for x in reports)
page = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>生成式软件工程｜逐课完整笔记</title><style>
*{box-sizing:border-box}body{margin:0;background:#faf8f2;color:#29332e;font:17px/1.8 -apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif}main{max-width:920px;margin:auto;padding:48px 24px}header{border-bottom:2px solid #315345;margin-bottom:28px;padding-bottom:20px}h1{font:600 clamp(30px,5vw,46px)/1.25 'Songti SC',serif;margin:15px 0}h2{font:600 22px/1.4 'Songti SC',serif;margin:0}.eyebrow,small{color:#766a5a}header p{max-width:740px}.card{display:grid;grid-template-columns:44px 1fr 22px;gap:16px;padding:25px 0;border-bottom:1px solid #d7cdbb;text-decoration:none;color:inherit}.card:hover h2{text-decoration:underline}.number{color:#ab4930;font-size:18px}.card p{margin:9px 0;color:#5f594f}.badge{display:inline-block;color:#365d47;background:#e1e7db;font-size:12px;padding:1px 7px;margin-top:9px;border-radius:3px}footer{margin-top:32px;color:#756c60;font-size:14px}a{color:#365d47}a:focus-visible{outline:3px solid #718b77;outline-offset:4px}details{margin:24px 0}summary{cursor:pointer}p,h1,h2,a{overflow-wrap:anywhere}h1,h2{text-wrap:balance}@media(max-width:600px){main{padding:28px 18px}.card{grid-template-columns:32px 1fr 16px;gap:10px}h2{font-size:21px}body{font-size:16px}}@media print{body{background:white}.card{break-inside:avoid}}
</style></head><body><main><header><div class="eyebrow">NJU · 2026 · 课程阅读索引</div><h1>生成式软件工程</h1><p>围绕课堂问题阅读：讲述、相关讲义与补充说明就地衔接，保留时间码和来源。每节提供关键判断，正文强调重点，自测先作答再核对。</p><strong>7 堂课程 + 1 个改编短片 · SECTIONS 节 · IMAGES 幅图</strong></header>
CARDS
<details><summary>阅读方式与核验范围</summary><p>每课为独立 HTML，正文和图片均内嵌，可单独保存到手机离线阅读。点击目录定位章节；点击图片放大，并可切换原尺寸查看细节。视频及原始网页链接需要联网。</p><p>复用第 02、05、06、07 课已有转写；第 01、03、04 课和短片补做转写。全部导出转写按块读完，逐句归属到正文小节；画面按讲义页及重点演示检查，没有逐秒听审整套视频。</p><p>本次在已有内容与逐图审核基础上重排图文，完成 1440/768/390/320px 浏览器测试及打印正文与配图检查；没有重新转写、逐秒回看或重新读取外部材料。未在真实手机设备上测试。官网讲义为本次获取的版本，可能含课后补注；原视频分辨率、音频问题和其他来源边界在各课开头说明。</p></details><footer><a href="https://space.bilibili.com/202224425/lists/8942017?type=season">Bilibili 原合集</a> · <a href="https://jyywiki.cn/GSE/2026/">官方课程网站</a><p>资料获取：2026-10-02。每课附独立的 review.json、图像审核和来源索引；本索引与单课文件置于同一目录树时可完整跳转。</p></footer></main></body></html>'''.replace('CARDS', ''.join(cards)).replace('SECTIONS', str(sections)).replace('IMAGES', str(images))
(root / '课程索引.html').write_text(page)
report = {'course': '生成式软件工程', 'outcome': 'completed' if all(x['outcome'] == 'completed' for x in reports) else 'partial', 'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'items': reports, 'totals': {'videos': len(reports), 'sections': sections, 'images': images, 'source_units': sum(x['source_units'] for x in reports), 'reused_transcripts': 4, 'new_transcripts': 4}, 'scope': '全部转写全文读取；逐张入选图检查；重点演示抽帧；未逐秒听审，未真实手机测试'}
previous = json.loads((root / 'review.json').read_text()) if (root / 'review.json').exists() else {}
old_items = {x['folder']: x for x in previous.get('items', [])}
report['items'] = [{**old_items.get(x['folder'], {}), **x} for x in reports]
report = {**previous, **report}
(root / 'review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
manifest = json.loads((root / 'manifest.json').read_text())
by_id = {json.loads((root / x['folder'] / 'notes.json').read_text())['source_url'].split('/video/')[1].split('/')[0]: x for x in reports}
for video in manifest['videos']:
    item = by_id[video['id']]
    video['status'] = {'transcript': item['transcript'], 'notes': item['outcome'], 'ui': 'passed'}
    video['output'] = item['html']
manifest['outcome'] = report['outcome']
(root / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print(json.dumps(report['totals'], ensure_ascii=False))
