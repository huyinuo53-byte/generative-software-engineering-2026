# pstack 新增形式验证 skills：写法启发与边界

本次独立只读核对主作者提供的 commit `eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10`，本地根目录 `research/research_notes/pstack-skills-20261022/source/pstack`；`plugin.json` 自报版本 v0.15.30。三个目标目录在旧 v0.15.21 快照中均不存在。未执行脚本、未安装 Java/TLC、未改项目；以下是源码和 Markdown 规范审查，不是运行实测。此前 web-access 已读。

## 1. Skill 不只告诉 AI“做什么”，还设计人与 AI 怎样就“对不对”达成一致

`statechart` 开头就指定实际读者是 PM：状态写“正在支付”，箭头写“点支付”“扣款成功”，变量名和动作函数名不进入读者标签。UI 画面相同却有不同业务后果时，要把隐藏后果写进状态，如“正在支付，已经扣了两次款”。这比“请生成技术流程图”强，因为它规定了谁作判断、据什么判断。

**面向用户的借鉴：** 写 skill 时先定“谁看产物，能据它做什么判断”，再规定产物格式。即便不懂 TLA+，你也能明确“用户重试两次也不能收两次款”。AI 才负责把这句话映射成技术检查。

证据：[statechart SKILL 9–26 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/SKILL.md#L9-L26)。这里的能力是**规范设计**，并不说明脚本已自动理解真实用户意图。

## 2. 从“建议怎么干”升级到“可以交付的合同”：输入、动作、失败、证据、复用都要写

`create-formal-verification-skill` 指定：先从真实代码选高损害、测试难覆盖的承诺；工具随问题选择；每项模型变量/动作要指向代码；每条性质必须能失败；边界和假设必须声明；命令和工具版本可复现；覆盖文件/函数和最后同步 commit 必须记录。交付还要给下一位冷启动 Agent 可直接用的 skill，不能留下占位符。

**借鉴模板：** “何时用 → 从哪里拿事实 → 按什么步骤处理 → 什么情况算失败 → 保留什么证据 → 下一次如何重跑”。例如课程笔记 skill 不写“保证完整”，而写“逐块读取转写；每张图标来源；来源更改后哪些核验要重做；有缺口不得标完成”。这是可迁移的写法，不要求你先学形式验证。

证据：[create-formal SKILL 11–37 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/create-formal-verification-skill/SKILL.md#L11-L37)。

## 3. 要验证“验证器会抓错”，否则绿色可能没有信息量

create skill 不是只要求正常版本通过；还要求在真实代码上做临时破坏，如去掉检查或换执行顺序，按生成 skill 重跑，必须能抓到，然后撤销临时破坏。维护 skill 也要求更新后通过时，再做一轮反例，确认新检查没有失去失败能力。

**面向用户的例子：** 如果你让 AI 写一个“所有配图可打开”的检查，主动放入一条坏图片路径，它应该报错。若依然通过，先修检查器。这里的提升是“检查检查器”，比添加更多口头质量要求更有效。

证据：[create-formal SKILL 23–29、35–37 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/create-formal-verification-skill/SKILL.md#L23-L37)；[maintain-formal SKILL 40–44 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/maintain-formal-verification-skill/SKILL.md#L40-L44)。这是**生成 skill 的验收规范**，不是三个目录里已有一套通用脚本会自动篡改任意项目并证明验收器有效。

## 4. “资料过期”要成为正式状态，不能把旧的通过当新的通过

维护 skill 单独设 `in sync / updated / bug / blocked`，并明确“更新了模型”和“发现真实 bug”可以同时成立。流程是：先跑旧检查，读取从 sync commit 到现在覆盖代码的每次变化（包括函数搬家和新写入同一状态的路径），按代码改模型，再跑、解释结果、更新同步点。不能因为一跑红了就改小范围或弱化承诺直到绿；只有产品承诺确实有意改变并有证据，才能修改性质。

**面向用户的借鉴：** 完成状态应附“对哪个版本、查了什么、哪些没查”。如果课程讲义已更新，旧笔记校验“仍通过”最多证明旧描述内部一致，不能证明它仍对应新讲义。最危险的不是红灯，而是检查对象已变、旧检查仍绿。

证据：[maintain-formal SKILL 9–24 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/maintain-formal-verification-skill/SKILL.md#L9-L24)；[maintain-formal SKILL 28–44 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/maintain-formal-verification-skill/SKILL.md#L28-L44)。规范要求人工/Agent 查证 sync，并非脚本自动证明模型与代码等价。

## 5. Skills 可以成为“自然语言承诺 ↔ 可检查模型 ↔ 实际复现”的桥，但桥的每一段都要验

`statechart` 有两个方向：先有代码/模型，画出真实用户看见的状态供 PM 判断；或先让 PM 同意状态图，再生成 TLA+ 骨架。后续添加真实代码的 guard/变量后，重新导出的图要与约定图比较。发现的每条坏路径必须在真实代码上逐步复现；不能复现时优先怀疑模型。

**软件工程启发：** AI 降低了写模型和解释反例的成本，PM 可以参与“永远不应发生什么”和“失败后应该到哪”的设计。它可能减少“需求文字说清了但边界行为没想清”的落差。不过只画漂亮图仍然没有跨过实现正确性的那一关。

证据：[statechart SKILL 15–36 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/SKILL.md#L15-L36)。

## 脚本真实做了什么

- `statechart.mjs` 通过 Java 启动 TLC，输出日志和状态图。每个 INVARIANT 单独运行，并用同一规则作 CONSTRAINT，使路径在首次破坏该规则处停止。不是只让模型在回答中声称“已验证”。[247–281 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L247-L281)、[320–355 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L320-L355)。
- from-chart 首次生成 `.tla/.cfg/.map.mjs`，已有 spec 就保留；然后运行 TLC、出图、调用 compare-charts。成功要求规则结果符合预期且图比较成功。[697–734 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L697-L734)。
- 图比较针对可达状态、初始状态和带标签转移；并行区域转成组合状态机比较。**不比较不改变显示状态的步**，且有标签规范限制。[compare-charts 9–24 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/compare-charts.mjs#L9-L24)、[84–104 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/compare-charts.mjs#L84-L104)。

## 不能声称的事项（请主作者保留关键边界）

1. **TLC 通过不等于真实软件被证明正确。** 本工具检查人为建立的 TLA+ 模型、既定性质与边界；源码到模型的真实性靠规范要求的代码对照与复现，不是自动编译任意代码得到形式等价证明。create SKILL:23–29 明说 scope；maintain:9 明说旧模型能继续绿。
2. **不是所有界面都可无损自动转模型。** from-chart 支持受限 Mermaid stateDiagram-v2 子集，拒绝 final/choice/fork/history 和更深嵌套区域；同标签会同步移动各区域。这些是转换语义，不应任意套在不同原子性实现上。[statechart.mjs 54–62 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L54-L62)。
3. **“after N s”之类时间标签不是 TLC 自动证明的时间事实。** 本脚本的 guard()/timer() 映射标签由 reviewer 对照代码，帮助文本明确说 TLC 不检查这些、无该展示意义上的时钟。不要扩大为“TLA+ 无法建模时间”。[statechart.mjs 107–110 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L107-L110)。
4. **exit 0 不总是没有 bug。** `--expect-broken` 模式精确匹配已知坏规则也返回 0；它证明结果符合期待，而非无缺陷。没有 INVARIANT 时只打印“no rule is checked”。[statechart.mjs 141–149 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L141-L149)、[320–355 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L320-L355)。
5. **--fixed 图上绿色不一定是“已在产品修复并复现通过”。** 绿还包含仅修复模型里存在的新状态；真实复现是 skill 的另一个必要步骤。[statechart.mjs 111–115 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L111-L115)、statechart SKILL:26。
6. **不要泛称本工具默认证明不存在死锁。** TLC 调用明确带 `-deadlock`，源码注释解释 UI 静止可能被误报，所以关闭常规死锁检查。它主要围绕给定不变量和图表达；要检查进展/时间性质应明确建模及具体设置。[statechart.mjs 254–266 行](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/statechart/scripts/statechart.mjs#L254-L266)。
7. 本次没有跑 TLC，也没有验证生产应用；不能将以上规范或静态代码检查写成实际用户项目已经得到数学证明。
