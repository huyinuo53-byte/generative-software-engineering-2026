from pathlib import Path
import json, hashlib, datetime
from PIL import Image
root=Path('/tmp/gse09-slides');vr=Path('/tmp/gse09-visual')
texts=json.loads(Path('/tmp/gse09-materials/sources/slides9-pages.json').read_text())
notes={
16:('两组五项约束/收益/新需求的文字与文档链接均完整。无公式或代码块。','录制33:14.8 LAMP稳定状态可辨识HTTP→PHP→MySQL、PHP-FPM、WebSocket与外部支付边界。未发现实质差异；当前图为窄版重排。','/tmp/gse09-visual/slide-comparison/rapid-1994.8.png'),
17:('校园卡100→12→12例子、回放副作用、历史汇率/版本上下文三项均完整。无代码块。','录制快速翻页已出现同样紫色历史/副作用/汇率文字。未发现实质差异；不能把紫色段落自动认定为课后新增。','/tmp/gse09-visual/scan/sample-01000.jpg'),
18:('map→按key分组→reduce与热门key/幂等副作用/重算约束全文完整。末句“上。”靠近页底但在原图仍完整，额外查看底部裁片确认。','录制快速翻页及原论文返回段已出现同样MapReduce约束和§4.5原子/幂等注释。未发现实质差异。','/tmp/gse09-visual/scan/sample-01001.jpg'),
19:('Spark/RDD与Flink/水位线/状态检查点两部分完整，末句性能与语义也完整。无公式代码块。','录制33:30附近该页含同样紫色缓存、乱序/迟到、Kafka/检查点文字。未发现实质差异。','/tmp/gse09-visual/scan/sample-01006.jpg'),
20:('Everything Is a Plugin、Cordis四项和协同两结论均完整。无公式代码块。','录制38:34内容与当前页一致；仅版式/字号与层级分页显示不同。','/tmp/gse09-visual/slide-comparison/page-20-t2314.png'),
21:('Session=list[Event]、投影、Pacioli历史类比、Agent和UI slots两项均完整。','录制47:24明确已含Pacioli 1494紫色历史类比；当前页未观察到实质差异。','/tmp/gse09-visual/slide-comparison/page-21-t2844.png'),
22:('两块代码完整：append/on回调闭合；deriveMessages/register/stateOf三行含行尾中文注释完整。代码超出浅灰容器背景但未出截图边界。','录制50:00可见同样API及两组解释，当前窄版换行/代码背景宽度不同，未发现语义变化。','/tmp/gse09-visual/slide-comparison/page-22-t3000.png'),
23:('followup/inject/steer三行代码与末行ctx.systemPrompt.context调用（含闭合括号）完整。','录制50:30同样区分唤醒/等待后续step及动态text；当前页未观察到实质差异。','/tmp/gse09-visual/slide-comparison/page-23-t3030.png'),
24:('pre-step hook四行代码含async签名、await next、return及闭合完整；session/event与agent/pre-step紫色区别说明完整。','录制51:20明确已出现同样两条紫色说明；当前页未观察到实质差异。','/tmp/gse09-visual/slide-comparison/page-24-t3080.png'),
25:('总线图完整：业务插件、Agent/Loop、LLM/Tools、Session、模型投影、业务投影、UI和Cordis底座，所有框与箭头未裁断；图内字较正文小但原尺寸可读。','录制52:44总线图结构/文字和当前原图一致。当前图没有包含左侧课堂板书，须与独立视频帧区分。','selected:v0296'),
26:('TUI、pdf-reader inject、Cordis生命周期、sidebar、Creator Mode热插拔各段完整。无公式/长代码块。','录制53:28内容一致。原录制Creator现场操作另由连续视频帧证明，本页本身只说明机制。','/tmp/gse09-visual/slide-comparison/page-26-t3208.png'),
27:('Feature Interaction、插件依赖和10次压缩说明完整；公式(1/2)^10=1/1024上下标/分数线均正常完整。','录制63:20已出现电话系统Feature Interaction紫色类比、公式及组合合理性紫色结论；当前页未观察到实质差异。','/tmp/gse09-visual/slide-comparison/page-27-t3800.png'),
28:('低复杂度/vibe、社区观点与von Hippel 2001工具包整段完整。无代码公式。','录制66:08已出现von Hippel工具包紫色说明，与当前页一致。社区判断应归教师观点。','/tmp/gse09-visual/slide-comparison/page-28-t3968.png'),
29:('lock objects+serialize objects+UI和VBA复用能力整段完整，无源码代码块。','录制67:32已出现VBA紫色说明，与当前页一致。实现能否达成须由后续Excalidraw现场链另证。','/tmp/gse09-visual/slide-comparison/page-29-t4052.png'),
30:('HTML+JS双向通道、下棋与两段紫色流程/直接操纵说明完整。无公式代码块。','录制72:36已出现棋局→上下文→应手→卡片更新和直接操纵紫色段落。当前页未观察到实质差异；课堂演示的中间失败仍须保留，不能用此页倒推五子棋全流程成功。','/tmp/gse09-visual/slide-comparison/page-30-t4356.png')}
sel={x['candidate_id']:x for x in json.loads((vr/'selected-frames.json').read_text())}
pages=[]
for n in range(16,31):
 f=root/f'page-{n:02d}.png'; a,b,e=notes[n]
 if e.startswith('selected:'):
  s=sel[e.split(':')[1]]; e=str(vr/s['path']) if not s['path'].startswith('/') else s['path']
 pages.append({'page':n,'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'dimensions':list(Image.open(f).size),'native_image_actually_viewed':True,'source_text_cross_check':texts[n-1]['text'].split('\n')[0],'information_complete_in_capture':True,'formula_or_code_clipping_observed':False,'visual_observation':a,'recording_comparison':b,'recording_evidence':e,'comparison_limit':'人工语义与可辨文字比对，不是逐字像素同一性证明；当前独立讲义截图不是该秒视频帧。'})
out={'status':'native_visual_review_complete','reviewer':'gse09_visual_20261026','scope':'official_current_slides_16_to_30_only','source':'parent Chrome capture /tmp/gse09-slides/page-*.png; local source extraction /tmp/gse09-materials/sources/slides9-pages.json','reviewed_at':'2026-10-26','page_count':15,'pages':pages,'recapture_required_pages':[],'conclusion':'15页截图信息均完整，未见代码/公式裁断。录制中可辨识的主体与紫色注释与现行页相符，未识别实质课后新增。aigc class仅标注来源，不证明后补时间。','limits':['没有据此证明全文每个字与录制逐字相同；录制1280x410且右屏细字受限。','当前官方页为1080x1742窄版重排，录制投屏为横版且分页器采用分节计数；不能逐像素比较或混作视频同秒画面。','本检查不替代最终HTML配图/图注/手机交互审核。']}
(root/'audit-16-30.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# Resolve a default detection-stage field using the actual completed human screening.
p=vr/'visual-inventory.json';x=json.loads(p.read_text())
for c in x['candidates']:
 c['manual_status']='visually_reviewed'
 c['visual_review_evidence']='contact-review.json; visual-coverage-draft.json states; native-frame-review.json for selected'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
p=vr/'visual-coverage-draft.json';x=json.loads(p.read_text());x['inventory']['sha256']=hashlib.sha256((vr/'visual-inventory.json').read_bytes()).hexdigest()
x['additional_comparison_review']='slide-comparison/: 21 exact-seek reference frames viewed individually while auditing official pages16-30; these are comparison evidence, not additional selected deliverable frames. audit-16-30.json kept in /tmp/gse09-slides.'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
p=vr/'HANDOFF.md';s=p.read_text();s+='\n## 官方16–30页额外原尺寸复核\n\n/tmp/gse09-slides/audit-16-30.json 已输出，15页均完整、代码/公式未裁断，无需重截。另取21张对照帧并逐张看过，包含33:14.8的LAMP快速稳定状态。没有识别实质课后新增；图注应继续区分现行独立讲义与录制同秒。inventory每项manual_status已从检测阶段默认pending改为实际visually_reviewed，coverage中的inventory hash同步更新。\n\n说明：extract_selected.py是初版选图脚本，初始caption包含后来已纠正的导航误读；最终使用selected-frames.json、native-frame-review.json和full/当前图，不单独重跑初版脚本。events.json实际包含48个语义窗口。\n';p.write_text(s)
print(json.dumps({'audit_path':str(root/'audit-16-30.json'),'pages':len(pages),'recapture_required':[],'inventory_sha256':x['inventory']['sha256'],'selected':len(sel)},ensure_ascii=False))
