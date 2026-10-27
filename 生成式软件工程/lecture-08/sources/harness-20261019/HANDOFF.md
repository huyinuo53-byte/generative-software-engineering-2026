# 第 08 课：DeepSeek Harness 原始仓库补读

已完成课堂相关机制的原始文件阅读：34 个文件全文、3 个文件的明确行范围。完整阅读清单、原文件 SHA-256、Git blob ID 和 commit permalink 见 `read-scope-and-source-manifest.json`；源文件只读副本在 `source-snapshot/`，不含 `.git`。这不是对整个仓库的全文阅读或产品验收。

## 身份与版本边界

- 仓库：https://github.com/deepseek-ai/deepseek-harness
- URL 依据：真实视频 70:30（4230 秒）的 README 源文可见 clone 地址，证据 `repository-url-at-70m30s.jpg`。保存的官方 lect8/slides8 HTML 没有该仓库 href，不能写成“官网讲义链接到此仓库”。
- 固定读取 commit：`687f282e8625c6b8d11ff58211a90524be2e4317`，提交时间 `2026-10-17T15:22:43+08:00`，本次读取日期 2026-10-19。
- 课堂视频日期是 2026-10-13。当前 commit 晚于课堂，**未确认录制时 checkout 的 commit**。以下都是“当前原始仓库补充”，不得写成“老师当时演示的代码已验证如此”。课堂口述引用和时间段来自主代理完整转写；本子任务独立核对的是真实帧及当前源码。
- 只读源码：未安装依赖，未执行仓库脚本、测试或应用，未验证远端分支保护配置。

## 可直接整合的补充及出处

### 1. 三件套把“需要重新确认”变成可检测状态，不能替代翻译审查

当前配对由同目录 `foo.md`、`foo.zh.md` 和 `foo.i18n.yaml` 组成；中英文同等权威，可从任意一侧发起修改。当前 sidecar 按英文标题路径划分，分别记录每节两侧文本的 hash；脚本采用 SHA-256 的前 16 个十六进制字符。围栏代码和生成区另做一致性检查，不计入这份分节 hash。不同章节的改动因此能改变不同记录行，减少无关合并冲突。

**绿色的准确含义是：这些内容被记录为已确认一致，结构也符合约束；它不证明确认者判断正确。** 脚本没有翻译语义模型。把意思错误的译文重录 sidecar，仍可能通过机械门禁。因此术语、条件、否定、例外、警告及是否增删含义依然要逐条审查。`--write <pair>` 是明确确认指定配对的动作；无参数 `--write` 被拒绝，以免悄悄认可其他未读文件。`--list` 只是清单，退出 0 也可能列出 missing/out-of-sync，不能当验收通过。

出处：`docs/i18n/README.md` 全文，尤其 7–44；`scripts/translation-pairing-record.ts` 144–232、275–299；`scripts/translation-pairing.ts` 233–287；`scripts/verify-translation-pairing.ts` 全文。样本 `README.md` / `README.zh.md` / `README.i18n.yaml` 已分别全文阅读。

### 2. 文风样例、术语表与现行算法各有权威范围

`translation-rules.md` 要求完整保留原文的命题和约束，同时用自然中文/英文表达；术语表规定正文译法、首次出现形式、禁用译法以及概念边界。例：capability 与 feature 分别译“能力”“功能”，Agent Note 保持英文作为特定文档类型，seam 也不随意译作“接缝”。`style-samples.md` 用架构叙述、测试政策、机制、决策等七类双语样例校准写法，而不是列一组抽象“写得自然”的口号。

**实读发现一个版本陷阱：当前 `style-samples.md` 53–69 的机制/政策样例仍讲整文件 Git blob hash 与 `git cat-file`，而当前配对合同及实现已经使用分节 hash。** 应将它当文风样例，不应照抄为当前配对算法。当前 Agent Notes 的 frozen archive 检查确实仍保留整文件 Git blob hash sidecar，并另用 SHA-256 封存每个文件；这是独立档案机制，不能与活动文档算法混成一种。

出处：`docs/i18n/translation-rules.md`、`terminology.md`、`style-samples.md` 全文；`scripts/translation-pairing-record.ts` 176–232；`scripts/archived-agent-notes.ts` 全文。不要仅因文件位于官方仓库就断言其每个例子都描述现行实现。

### 3. AGENTS 的层级是在分配知识归属与读取成本

根 `AGENTS.md` 放共同约束，`docs/AGENTS.md` 放文档规则，`packages/AGENTS.md` 放包目录规则，Agent Notes 子树再加生命周期规则。文档标准明确“一种事实一个归属”：架构页讲组合结构，子系统/包参考讲可使用的契约，Agent Notes 留下为什么这么选、放弃什么、要怎么验证，skill 保存复用工作流。它不要求所有事实都塞进一个根提示文件。

字数门禁只计 manifest 指定的常驻文档，超过预算要先搬到合适的归属，再压缩；确实需要扩预算时要解释。检查实现是按空白分隔的 `wc -w` 风格计数，不应写成 token 预算或整个仓库总字数限制。根规则还要求把能机械检查的不变量接到实际执行的顶层门禁，并用非法样本证明拒绝路径，而不只写“请遵守”。

出处：`AGENTS.md` 129–181；`docs/AGENTS.md` 15–59；`packages/AGENTS.md`；`scripts/verify-doc-budgets.ts` 与 `doc-budgets.manifest.json`。当前具体预算会变；不沿用视频旧数字作为现行事实。

### 4. Agent Notes 是有生命周期的决策记忆，不是聊天记录

当前活动路径是 `{proposed|implemented|rejected}/{feature|bug-fix|simplification|architecture|process|testing}/日期-题目.md`。proposed 写问题、方案、备选、验收与风险；implemented 写已交付决策及后果；rejected 在状态行给出拒绝理由。格式脚本核对路径与状态、必需标题，且拒绝 implemented 中残留 Proposal/Plan/Migration plan/Acceptance criteria 等计划标题。中文对应侧保持 machine tokens，格式门禁跳过 `.zh.md`，其结构一致性由配对门禁负责。

implemented 要随代码变化更新路径、符号、默认值等实现事实；若决策反转，应新建决策记录并互链，不能把旧文件改成相反结论。是否归档以未来决策价值判断，不能按年龄或字数一刀切。完整被替代且理由已被新归属吸收可按规则合并；仍有兼容性、安全、负面保证或重引入条件的记录继续活动。归档仅适用于已实现的记录，保留历史价值而冻结内容；归档后的外链可以过时，不能当当前行为权威。归档检查用独立封存清单阻止历史静默变更。

出处：`.agents/notes/README.md` 全文；该子树三个 `AGENTS.md`；`agent-note-tree.ts`、`verify-agent-note-format.ts`、`verify-agent-note-classification.ts`、`verify-archived-agent-notes.ts`、`archived-agent-notes.ts`；归档政策 Agent Note 与 `dsh-archive-agent-notes/SKILL.md` 全文。脚本可核对格式与封存，不能判断替代理由是否充分。

### 5. 类型文档有两种不同检查，不能合称“证明文档正确”

普通 `ts` 文档代码块由 `doc-typecheck` 作为 TypeScript 示例编译，检查其能否使用当前 workspace API。`ts ignore-check` 是显式豁免；当 eligible 示例至少 4 个且超过一半豁免，脚本会失败。生成目录及 source-equivalence fence 由其他门禁负责。

`verify-type-equiv` 则处理标记为 `ts type-equiv` / `ts public-api` 的复制声明，通过 manifest 的 doc + symbol + projection 找源码。它要求文档块和 manifest 一一对应，拒绝孤立块、孤立条目、重复映射或声明漂移。对比忽略空白与非 JSDoc 注释，但保留声明结构及原始 JSDoc；public-api 投影移除方法体、属性初值、private/protected 等，保留公开签名和文档。显式列出的 interface augmentation 也可合并比对。

**检查覆盖的是已标注/已登记的声明，不证明新增类型一定写了文档，更不证明自然语言解释、实现行为或示例运行效果正确。** 当前 docs/AGENTS 本身明确说它抓得到已复制内容漂移，抓不到从未被文档记录的新类型。

出处：`docs/AGENTS.md` 43–44；`scripts/verify-type-equiv.ts` 全文；`scripts/doc-typecheck.ts` 全文；`type-equiv.manifest.json` 仅阅读注释/schema 与首批映射例子（1–32），未逐条读整个 catalog。

### 6. Markdown 链接门禁具体查什么

`verify-md-links` 在选定 Markdown 范围解析链接、图片与 definition，检查相对目标是否存在；目标是 Markdown 时，还检查 `#fragment` 是否对应标题 slug 或实际 HTML `<a id>`。同页锚点也检查，代码样例和注释里的伪锚点不算。

它明确跳过带 URL scheme 的外部链接、协议相对链接、根绝对路径；非 Markdown 文件的片段（如代码 `#L10`）也不验证。档案文件不作为外链扫描源，但活动文档指向档案仍可检查。所以准确表述是“防止本地文档相对引用断裂”，不能说“自动验证了网上每个链接和内容”。

出处：`scripts/verify-md-links.ts` 全文。双语的语义目标及 locale 一致性另由配对门禁负责；它和目标存在性检查是不同工作。

### 7. doc-sync 是接线后的检查集合，skill 是可重用操作规范

已核对 `package.json` 到 `scripts/run-gates.ts` 的静态接线：`doc-sync` 分派到 `docSyncLeafGates()`，列出 doc-typecheck、type-equivalence、markdown-links、translation-pairing、Agent Note 分类/格式/档案检查、文档预算、网站构建、生成目录新鲜度等。`test:docs` 只取 quick 标记子集，明确排除 build 与 doc-typecheck 等重检查；不能用 quick 成功代替完整 doc-sync。聚合入口对阻断检查失败或 skipped 返回非零。这里验证的是源码接线，不是本次真实跑绿或远端必需状态检查已启用。

`dsh-doc` 定义读者起点、可观察结果、失败与恢复、知识归属、同次更新双语和证据流程；要求运行所描述的实际操作才可以写操作结论。`dsh-archive-agent-notes` 定义逐项保留/归档/删除的判断和完整 triplet 迁移流程。当前日常翻译是术语引导的一次直接更新；`dsh-translate-docs` 的 briefing、委派与双遍审校仅供用户显式调用。不要因为看到该 skill 文件，就把重流程写成每次翻译必经步骤。本次只是把这些 skill 当研究材料阅读，没有按它们发起执行、委派或仓库改动。

出处：`package.json` 104–139、198；`run-gates.ts` 103–139、359–362、805–883；三个 skill 入口全文。

## 可以做的小自测（整理者设计）

1. 修改中文术语后，直接重录 `.i18n.yaml` 并通过 pairing，是否已证明翻译忠实？为什么？（未证明；只记录内容与结构，语义仍须审查。）
2. 某接口实现变了，文档里的 type-equiv 绿了，能否说明新 API 已被完整说明？（不能；既有块对应不等于覆盖全面。）
3. 已实现决策改了包路径，应新建 Note 还是更新旧 Note？若决策反转又如何？（事实实现更新旧记录；反转另立决策并互链。）
4. verify-md-links 通过后，一个外部网页 404 能否仍存在？（可以；它明确不检查外部 URL。）

## 尚未确认与问题清单

- 录制时仓库 commit 未确定；但真实视频 72:30（4350 秒，v0499）已经展示按 heading section 分节的 YAML，左侧说明为 heading path 与 SHA-256 前 16 位。不得把当前 style-samples 残留的整文件 blob 描述倒推为课堂当时的算法。
- 当前 style-samples 机制段是旧算法描述；知识归属应优先当前 pairing README 与实现，保留这个差异作为阅读原始仓库的版本判断练习。
- 活动配对的分节 hash 与档案 sidecar 的旧整文件 blob 格式独立存在；不把一种直接套用另一种。
- 未跑任何门禁，不声称 commit 当前全部 green；未执行 README 操作，不给运行成功结论。
- 未核对远端 branch-protection / CI 必需检查设置，也未读完整 gate scheduler、全量类型清单、所有产品代码和 skill 引用材料。
- 源快照的 SHA 验证只证明引用的版本字节可追溯，不证明语义阅读完成；阅读完成由上面的声明范围与实际逐文件阅读记录承担。

## 纠错记录（2026-10-19）

原问题清单误写“课堂当时展示整文件 hash”；该推断未经视频支持，现已删除并改为真实帧 v0499 所示分节机制。主作者原尺寸回看提供了纠错，视觉绑定复核已再次原尺寸查看该帧，确认两侧均展示分节机制。当前仓库样例与现行算法存在差异的发现仍成立；这一差异不能用来断言课堂演示版本。源文件快照保持不变。
