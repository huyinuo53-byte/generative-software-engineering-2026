# 生成式软件工程 补充｜失败的AI Slop数字永生尝试 · v3 重写版

- 依据：BaoCut 原始转写 `../transcript.json` 与原视频 BV1fKtN6DErG（Release snapshot-2026-10-27），加上课程官网讲义页、slides 和推荐材料原文（见 `materials.json`）；未参考旧版笔记和旧 materials 记录。
- 推荐材料：10 项，阅读状态 {'full': 6, 'blocked': 1, 'out_of_scope': 3}。slides 上 AIGC 批注里的链接标为“官方 slides AIGC 批注推荐，非课堂口述”，不算老师明确推荐。下载的第三方原文不入库。
- 未读全的材料：gse-slides1-cv（blocked）。
- 写作：Cursor + grok-4.7-high；保真评测：Codex + gpt-6.1-sol（独立进程）。评测方式：只复核改动条目。
- 评测：精度 1.0，召回 1.0，状态 passed；页面检查 passed（headless Chrome 390/1280），页面 8.7MB。
- skill：baocut-course-notes `28981d8`（lean-rewrite-pipeline）。
- 结构：6 节 · 7 张图解（含课程地图）· 9 幅原帧（其中 1 张官方 slides 页）· 6 条材料补充 · 7 道自测。

重新渲染：`python3 <skill>/scripts/course_notes.py render --notes notes.json --index chunks/index.json --out 课堂笔记.html`
