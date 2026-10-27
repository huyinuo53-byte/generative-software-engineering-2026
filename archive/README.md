# 制作档案与证据边界

- `生成式软件工程/` 保存现有课程目录、转写分块、notes/layout、讲义、全部候选帧、逐图审核、浏览器截图、修订与失败记录。
- `baocut/projects/` 保存 10 个原生 `.bcut` 目录：原始转写、ASR rows、Studio、历史对象、项目内 tasks/logs/cache 均保留。
- `legacy/` 保存可识别的早期复用草稿及提示词工程截图，不替代现行笔记。
- `media-manifest.json` 对应同仓库 Release 中 10 个源视频，记录平台 BV ID、原始路径、长度与 SHA-256。
- `source-copy-manifest.json` 记录源文件与复制指纹；`transformations.json` 单独记录归档转换；`exclusions.json` 列出未复制的 OS/Python 缓存和临时锁。

唯一内容范围转换是 `生成式软件工程/sources/projects.json`：从历史全机项目列表中去掉其他课程条目。历史 trace 仍保留原值，因此涉及该文件的旧快照不是归档副本的新验收结果。本次完整性以 `files.json` 和 `publication-review.json` 为准；不修改历史 passed/hash。

历史审核是原制作时的证据，包含真实手机、原生打印、音频逐秒听审等未测边界。复制文件并不构成新的全文/来源/真机验收。历史绝对路径、工具路径和状态照存，跨机器不自动有效。不要执行旧 `ownership.json` 或临时脚本来覆盖当前目录。

截至本次归档，在这 10 个 `.bcut` 项目和可识别的课程原件中未发现独立音视频 slices。存在的 `chunks/` 是转写阅读分块；`frames/`、`visual/` 是真实画面候选与审查资料；项目 `cache/` 中已有 waveform 文件也予以保存。没有为上传重新转码或制造 slices。
