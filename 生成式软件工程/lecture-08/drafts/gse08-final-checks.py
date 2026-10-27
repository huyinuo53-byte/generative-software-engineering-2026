import pathlib,json,hashlib,subprocess,sys,shutil,re,datetime
from html.parser import HTMLParser
R=pathlib.Path('/Users/yjzhao/Documents/ChatGPT/learning-machine/生成式软件工程/lecture-08');sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();write=lambda p,x:pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
shutil.copy2('/tmp/gse08-content-review-final.json',R/'audits/content-review.json')
assert json.loads((R/'audits/content-review.json').read_text())['notes_sha256']==sha(R/'notes.json')
S=pathlib.Path('/Users/yjzhao/.codex/skills/baocut-course-notes/scripts')
checks={}
for name,args in [('image', ['validate_image_audit.py','--notes',str(R/'notes.json'),'--audit',str(R/'image-audit.json')]),('visual-coverage',['validate_visual_coverage.py','--notes',str(R/'notes.json'),'--coverage',str(R/'visual-coverage.json')]),('materials',['validate_materials.py','--materials',str(R.parent/'materials.json'),'--course-root',str(R.parent)]),('layout',['validate_reading_layout.py','--notes',str(R/'notes.json'),'--layout',str(R/'reading-layout.json')])]:
 x=subprocess.run([sys.executable,str(S/args[0]),*args[1:]],capture_output=True,text=True);d=json.loads(x.stdout);write(R/'audits'/f'{name}-validation.json',d);assert x.returncode==0,(name,d);checks[name]=d['status']
class Content(HTMLParser):
 def __init__(self):super().__init__();self.all=[]
 def handle_data(self,d):self.all.append(d)
p=Content();p.feed((R/'课堂笔记.html').read_text());txt=''.join(p.all);norm=lambda t:re.sub(r'\s+','',t)
txt=norm(txt);n=json.loads((R/'notes.json').read_text());blocks=[]
for s in n['sections']:
 blocks.extend(s['paragraphs']+s['examples']+s['editor_notes']);blocks.extend(f['caption'] for f in s['frames'])
blocks+=n['summary']+[x['text'] for x in n['supplements']]+[x[k] for x in n['self_test'] for k in ('question','answer')]
missing=[x[:100] for x in blocks if norm(x) not in txt];assert not missing,missing
source_ids=[u for s in n['sections'] for u in s['source_ids']];idx=json.loads((R/'chunks/index.json').read_text());expected=[x['id'] for x in idx['sentences']];assert len(source_ids)==len(set(source_ids)) and set(source_ids)==set(expected)
write(R/'audits/html-content-preservation.json',{'status':'passed','html_sha256':sha(R/'课堂笔记.html'),'notes_sha256':sha(R/'notes.json'),'text_blocks_checked':len(blocks),'missing':missing,'source_units':len(expected),'unique_assignment':True,'scope':'All authored prose/example/editor notes/captions/supplements/questions/answers present in rendered HTML text; not semantic correctness.'})
j=json.loads((R/'qa/reader/journey.json').read_text());assert j['html_sha256']==sha(R/'课堂笔记.html') and not j['errors'] and not j['network']
for row in j['viewports']:
 assert all(row[k] for k in ['toc_jump','fit','closed','escape','answer_open','quiz_back','answer_closed','source_has_timestamp']);assert row['native']['scrollLeft']>0 and row['page']['width']==row['page']['scrollWidth'] and row['page']['inline']
viewed=['1280-top.png','390-bilingual.png','390-native-pan.png','320-fit.png','390-quiz.png','390-repo.png','320-top.png','1280-bilingual.png']
write(R/'qa/reader/visual-review.json',{'status':'passed','reviewer':'root','html_sha256':sha(R/'课堂笔记.html'),'journey_sha256':sha(R/'qa/reader/journey.json'),'screenshots_viewed':[{'path':x,'sha256':sha(R/'qa/reader'/x)} for x in viewed],'observations':['桌面标题和08期号比例正常，目录与正文两栏清晰','390/320窄屏标题、正文及自测可读，页面无横向溢出','原尺寸图在独立容器横向平移，关闭和适合屏幕始终可用','自测问题与展开答案颜色及层次区分，回查链接可用','仓库补充保留段落空行和当前版本标签；源码文件名按窄屏折行'],'scope':'8代表截图实际目视+3视口读者路径；不是每一屏逐页目视，不是真实手机或原生打印。'})
write(R/'audits/issue-closure.json',{'status':'passed','notes_sha256':sha(R/'notes.json'),'issues':[{'id':'board-gcc','resolution':'visual-coverage.json的compiler事件区分左右内容，event-binding-map纠正旧events误解释；正文21节及v0439图注已回读。','evidence':['visual-coverage.json','audits/gse08-event-binding-map.json','audits/content-review.json']},{'id':'historical-hash','resolution':'保留原始HANDOFF和纠错记录；更正复制来的最终HANDOFF，实际4350画面已分节hash。','evidence':['sources/harness-20261019/parent-correction.json','audits/gse08-final-visual-review.json']},{'id':'desktop-toc','resolution':'本课交付CSS启用桌面summary鼠标操作并真正折叠nav；复验PASS。共享skill与既有课程不改。','evidence':['audits/browser-first-failure.json','qa/browser/audit.json']},{'id':'hero-issue','resolution':'issue由日期长字符串改08，标题恢复正常宽度；桌面截图已目视。'},{'id':'final-typo','resolution':'文务改义务，独立审阅者已关闭。','evidence':['audits/content-review.json']}],'open_issues':[]})
write(R/'audits/material-integration.json',{'status':'passed','notes_sha256':sha(R/'notes.json'),'materials_sha256':sha(R.parent/'materials.json'),'materials':18,'supplements':27,'method':'原始材料读者按范围实际阅读；主作者完整回读交接与所有补充，按主题嵌入；独立终审复核关键数字、机制与归因。Lab2落第2节整理者说明，其他材料有note_target落点。','evidence':['audits/content-review.json','sources/official-20261019/materials-draft.json','sources/lab2-humanize-20261019/materials-draft.json','sources/harness-20261019/read-scope-and-source-manifest.json','audits/materials-validation.json'],'boundaries':['现行讲义与课后仓库提交未当课堂逐句口述','仓库仅34全文+3范围，并非全部产品源码；未执行门禁','历史旧8篇未重新认证来源阅读']})
print(json.dumps(checks));print('text_blocks',len(blocks),'source_units',len(expected),'reader checks passed')
