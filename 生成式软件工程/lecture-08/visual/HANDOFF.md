# 第 08 课真实视频视觉盘点（待正文整合）

目标 BV11LWw6VEHW；本次仅视觉盘点，没有新增 ASR、没有读取 .bcut、没有修改课程成品。

## 文件与实际检查范围

- `visual-inventory.json`：同一完整媒体 SHA-256、音视频时长、检测参数、984 候选（基础 712 + 加密 272）。
- `scan-mapping.json`：全长 2915 张每 2 秒全幅原始帧的扫描/筛选映射。原帧保存在 `scan/`，1280×410。
- `dense-inventory.json`：34 个关键转场，各前后 2 秒、0.5 秒取样，272 张均实际查看。
- `contacts/`：26 张右侧屏幕代表联系表 + 10 张重复候选全幅联系表 + 5 张每 60 秒全幅复查表 + 12 张加密回查表，均实际查看。不是用文件存在推导通过。
- `events.json`：52 个连续视觉事件，0–5829.674667 秒。它记屏幕/板书事实，不生成课堂口述。
- `selected-frames.json`：45 张建议真实帧，均打开原始 1280×410 实际查看；`full/` 保存全幅，`crops/` 只提供同源右屏裁剪。所有笔记 targets 仍空。
- `native-frame-review.json`：额外关键帧原尺寸查看记录。部分板书小字仍不能逐字辨认，不能强行 OCR 后包装成准确转录。
- `visual-coverage-draft.json`：每个候选一个处置草稿。需要正文/配图的条目保持 `pending` + `proposed_disposition`、`pending_targets`；已看过的重复与过场才用相应处置。未运行最终 notes validator，未标 passed。
- `review-draft.json`：真实执行范围与未执行范围。

媒体 SHA-256：`dee8d8992246a868d973678ab85c152e3eaf3e07ccef70eb5a674556386552b7`。
视频 5829.666625 s，音频 5829.674667 s；流时长由本代理复查，尾部 30 s 解码通过是主代理提供的结果，尾帧 5828 s 本代理实际查看。

## 必须放进正文的独特画面链

1. **00:42–05:34 Lab2 Deeper Research 回顾**。00:56 是 Master Bot / Morning Paper 应用截图；02:00 是 effort / 算力换智力要求；04:04 的网页显示 Humanize 标题与运行框架；05:06 是 2.3 评估效果（固定输入/模型、直接求解 vs 低/高 effort、耗时 token 和预先确定指标、盲比）。页面 URL 栏未显示，不能从视频猜地址；可由主线已读官网作身份核对。
2. **15:22–21:14 MiniAgent**。代码依次是 key loader/system prompt/bash schema → `run_bash` → DeepSeek streaming → `read_reply` 收集工具调用 → `main` 内层工具循环。19:14 启动，19:16 输入 Hi 后模型自行检查目录，读取已有 HTML，生成 GSE 简介卡；20:18 完整页面见帧 1218。20:55 起 grim 截图 + Pillow 像素分析；21:06 报告红/黄/绿三个灯的像素结果。**这是模型用像素模式推断浏览器已显示，不是实际视觉理解，也不能写成完整 UI 验收。**
3. **33:40 `ralf-loop.sh`**。脚本要求每轮检查当前状态、只推进一个明确步骤、验证并把未完事项写文件；只有确认完成才输出 `<RALPH_DONE>`，shell 用 `grep -Fxq` 决定退出。不要把 `while true` 说成天然知道何时完成。
4. **34:44–38:04 语言研究的 Ralph 操作链**。首轮研究“世界上最好的编程语言”，curl 超时后继续读取 TIOBE/PYPL 等；35:46 `NEXT_STEPS.md`；35:48 出现新 Agent banner，重新读取状态；37:56 输出自评和 `<RALPH_DONE>`，38:02 回 shell。调查结果和数字只是现场 Agent 产物，不能当独立核实结论。
5. **36:01–37:44 两张 jyy 名片比较**。蓝紫页面（36:14）与橙色页面（37:00），与后台语言研究并行显示。不能把名片误写成“语言研究生成的页面”。
6. **38:30–40:58 第二次研究/结果比较**。加密帧显示 38:30 命令为 `./agent.py`，不是再次调用 `ralf-loop.sh`；请结合口述确认比较意图。39:00 的抓取曾返回 IEEE 会员/隐私内容、GitHub Page not found；40:40 最终 Agent 仍报告完成，两个交付文件 `编程语言调研报告.md` 和 `语言榜单原始数据.txt`。不要遗漏这个对比，也不要默认“宣称核验”即真的核验。
7. **47:52–52:16 Codex CI 现场查看**。Pi 在 `~/Projects/codex/.github` 读 workflows，右侧打开 `rust-ci-full.yml`、平台 matrix、format/cargo shear/argument lint/Python tests。左侧是 Agent 的架构摘要。随后追问 Lint，AI 区分工程卫生与功能正确；正文里应写这是现场问答/生成结果。
8. **61:34–62:58 再看 Codex CI**。PR 门禁、main 全量、发布三层，用餐厅试吃员/深度质检/端菜类比；62:58 对照表为清晰真实帧 3778。这段不在单独静态讲义全文里，值得保留。
9. **67:24–69:56 DeepSeek Harness 文档浏览**。目录与 `docs/architecture.md`：Cordis 插件、profile、bundle、启动形态。69:28 完整顶部可读。只引用屏幕实际出现字段；无须把目录每个文件都列进正文。
10. **69:56–74:26 双语一致性**。现场 AI 读仓库，有 `No such file` 探路；说明 `foo.md`、`foo.zh.md`、`foo.i18n.yaml` 三件套；`README.i18n.yaml` 展示每节 heading slug 的 en/zh 哈希。**哈希/结构配对保证约定内变化被确认，不代表翻译忠实。**
11. **74:26–77:46 翻译品味**。`style-samples.md` 是人工校准段落，`terminology.md` 限定首现、缩写、不译项；机器门禁与人类文本判断不同；AI 屏幕还说明原作者/译者两遍改写策略。对应 74:40、75:30、76:30 原帧。
12. **77:46–81:10 机制历史考古**。AI 读 git log/show 与 archived process notes，报告六阶段演进；右侧打开初始提交。这里看到的作者/日期/归因是 Agent 的现场分析，未经本代理独立 repo 核验，不能直接升级为已证实贡献归属。
13. **81:10–88:03 Harness 机制盘点**。AGENTS 分层、Agent Notes 生命周期、skills 与调用元数据、verify 脚本/run-gates、文档分层与 slop checklist、schema/状态、snapshots、先验证再落盘、model-visible vs logged、prototype API、去除思考痕迹、归档和简化；83:24 新开 Pi 追问 skills，84:26 左右再问 code review，说明本地自证→CI→人工审查。不能只放“Deepseek Harness 人物图”代替这 20 分钟演示。
14. **96:48–结尾**。回源码 `agent.py`，main tool loop 清楚；5828 秒仍同画面，不是早已课程结束后黑屏。

## 板书与去重纠正

初筛只比较右侧屏幕，发现这种做法会把新增板书误判重复。本代理实际看了全部 194 个“重复”候选的全幅图，并用全长每 60 秒全幅复查；板书书写区间的 screen-only duplicate 已提升为待映射状态，不自动丢弃。

关键板书阶段：

- 02:30–04:00：设计空间搜索、breadth-first/depth-first 与原型。
- 06:00–08:30：intent/spec/impl 三层及落差箭头（510 s 帧可见）。
- 22:00–23:30：token/history 路径补画（1410 s）。
- 28:00–32:00：Workspace/State、Agent/Transition 的圈和分支（1920 s 全幅）。
- 54:00–57:00：检查/CI 门禁与两个泳道（3330 s）。
- 64:30–66:30：文件/编译产物/任务分解示意（3990 s）。
- 71:50–73:30：双语文件/输出配对（4380 s 下板）。
- 76:30–77:00：文本/术语与流程补画（4590/4620 s）。
- 93:00–94:00：需求实现图加连线、划叉（5610 s）。

原媒体左侧板书本来只有 550×410，有些手写词无法可靠辨认。保留全幅图和课堂转写解释，不能用放大/锐化假装恢复未采到的字。

## 整合步骤与边界

1. 主线把 `events.json` 与完整转写对齐，决定正文小节及对话层次。
2. 优先静态页使用已交付当前官方 24 页完整图；真实帧用于操作、板书、现场 AI 回答与比较。视频原帧能确认多张紫色补充文字确实显示在录制中，但显示 ≠ 教师逐条口述；不要把所有补充都默认算课堂说过。
3. 给每项待处理状态填 notes targets；同一动态操作中间滚动/生成状态可由明确正文解释覆盖，不能以最终结果笼统抹掉流程。
4. 选入正文的其他原帧若不在 `native-frame-review.json`，仍需打开原尺寸查看；本代理只做列出的关键帧原尺寸复核，联系表不替代这个动作。
5. 最终写 `visual-coverage.json`，绑定最终 notes 和 inventory 的 hash，补 `pdf_pages`，执行 skill validator；只有主线确实整合完成后才可去掉 pending。当前草稿不是通过证明。
