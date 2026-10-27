# GSE 09 原始材料阅读交接

目标视频：BV144nc6KEA4，DeepSeek Harness (1)，2026-10-20。

## 可接入成果

- `materials-draft.json`：30 项来源；17 项本课 required，均已实际读完其声明范围。其余背景材料明确限定相关章节，NASA / Feature Interaction 未取得正文，RDD 原论文只有身份摘要页。
- `supplements-draft.json`：17 条有内容的补充，覆盖 PRD/重试/架构/Event Sourcing/MapReduce/Spark/Flink/Agent 输入/Session/插件生命周期/dsh-bot/复杂性/生产率/Creator Mode/GenUI。每条给材料 ID、原文定位、来源及边界；尚未写进最终 notes。
- `sources/slides9.html`：原官方 30 页完整 HTML；`sources/slides-pages/page-01.html` 至 `page-30.html` 为 slides-data 逐页原 HTML。
- `sources/slides9-pages.json`、`slides9-pages.clean.txt`：已完整阅读 30 页文字与代码；原始 5 张内嵌 WebP 已从官方页面解码在 `sources/assets/page-*.webp`。
- `sources/office-agent-prd.md`：第 6 页 data:text/markdown 链接解码原文，全文已读。产品预算、成功率等数字都是目标规格，不是 dsh 的已测结果。
- `sources/assets/`：除 5 张官方原图外，另有 AWS 幂等序列 PNG、MapReduce Figure 1 PNG、Flink 两张原 SVG及阅读渲染。`asset-manifest.json` 给当前文件哈希；相关材料记录实际目视细节。

## 与课堂的归因边界

当前讲义/幻灯片于 2026-10-26 获取。`.aigc` 是来源标记，不能据此判成课后内容。视觉代理已经证实 NASA/Brooks 紫色补注在录制开场就存在；主作者应按实际画面与转写区分“讲者口述”与“屏上/现行讲义补充”。主作者提供的 33:09 教师邀请自读 AI 补充、40:12 明确不讲 Cordis 部分的证据已纳入判断。因此没有把 Cordis 全论文升级成必读，只读与本课接口相关的官方 primer。

本代理不负责录制全程画面或最终 30 页浏览器截图，不声称那些阶段完成。

## 固定仓库版本

沿用第 08 讲的 DeepSeek Harness `687f282e8625c6b8d11ff58211a90524be2e4317`（2026-10-17）。本次重读已冻结 architecture.md 全文，另只取 core/session/system-prompt/cordis-primer 相关承重文档。继承的版本/真实阅读清单分别保存在 `sources/dsh-inherited-version.json` 和 `sources/dsh-inherited-read-scope.json`，本次下载文档的 hash 在 `sources/repo-retrieval.json`。不声称该 commit 就是第 09 讲录制 checkout；未执行、安装或测试被研究项目。

`dsh-bot` 锁定 `3acc759fc634d5d5c55792614b6bca03c630a345`（2026-10-02），README 全文已读。README 面向 Shell v0.2.0-rc.1；兼容性、运行行为未验证。其队列仅在内存，重启丢失，persona 编辑仅对新会话生效。

## 需要主作者接线后才能验收的部分

这两份 JSON 是独立阅读草稿，不是可直接宣告 passed 的最终账本。

1. 复制到课程时统一调整相对路径。所有源路径相对 `/tmp/gse09-materials`；保留 source 文件再更新 hash。
2. 将实际采用的补充放进对应正文附近。材料 `contributions` 只有 suggested_topic 和 draft_supplement_id，还没有伪造最终 section/note_target；必须由主作者绑定实际 notes.json 落点并运行材料校验。
3. 讲义 30 页原 HTML 不等于 30 张已查看渲染截图。最终截图、视频对应、手机展示仍由主作者/视觉代理负责。
4. 背景 NASA LLIS 只返回 1733 字节 SPA 壳，Feature Interaction HTTP403；不采用这两个未读来源的论文细节，不声称全文。RDD 原论文只有摘要页，不可当全文；本课 RDD persistence 由 Spark 官方链接相关节支撑。
5. QJE 通过官方站网页工具实际读了摘要/引言、样本、主效应表和结论前段；没有整篇 54 页论文或附录。台账明确 full 仅指这些声明范围，不能改成全篇阅读。

## 优先避免的事实越界

- MapReduce 原论文：worker 可重做；当时实现的 master 失败会中止计算。没有“所有故障都自动恢复”。
- `session.append` 的 commit 是内存日志提交，落盘异步；需要等待持久化时使用 flush。不是 UI 显示成功就已持久。
- 动态上下文 provider、inject/steer 不能追溯改写已发出的请求；生命周期卸载不自动撤销外部副作用。
- Flink checkpoint/exactly-once 不能直接保证任意外部工具动作只做一次；checkpoint 默认未开启。
- Apache 可以代理 WebSocket；课堂 LAMP 例子指典型短请求模型的假设变化。
- QJE 约 15% 是单家企业人工客服 issues resolved/hour，不能直接套到软件工程。
- Shneiderman 此篇扫描原文物理页 8 是四项原则；可交互卡片不自动等于合格直接操纵。

## 已做核对

- 30 个材料 ID 唯一，17 个 required 都为本次真实阅读声明范围 full；所有有 path 的原文件存在。
- 17 条 supplements 的材料 ID 均可回查；30 页 HTML 齐全；资产逐个哈希记录。
- 实际目视：MapReduce Figure1、AWS 幂等流程、Flink watermark/checkpoint、Toolkits 物理页12、Direct Manipulation物理页8。
- 没有运行 final validate_materials（最终 notes 尚未绑定）；没有最终 HTML 审查、真机、原生打印或运行时验证。
