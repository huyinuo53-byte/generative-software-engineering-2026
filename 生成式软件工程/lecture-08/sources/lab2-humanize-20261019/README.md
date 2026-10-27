# 第08课 Lab2 材料交接

仅为材料代理的阅读及补充草稿；未写共享课程状态，也未宣布第08课完成。主代理须把材料复制到持久课程目录，并将台账 path、贡献的实际 notes 落点与依赖 hash 更新后验收。

## 已完成

- 加载 baocut-course-notes、web-access 及 reading-materials 参考；PDF原页视觉复核使用PDF skill。
- 核对官方 Lab2 原链接指向 `Humanize: Judgement Engineering for Agentic Coding`。arXiv版本页显示 v1 2026-10-06，当前v2 2026-10-08；PDF首页v2、标题作者匹配。
- 顺序完整阅读14个物理页，含摘要、方法、应用、发现、局限、致谢/参考文献、附录A/B。顺序文字读取1–220、221–465、466–715、716–957行覆盖全部导出，不是搜索摘要。
- 实际目视物理页2/3/4/5/7/8/14：全部六张正文图和两张附录表；图2概率与图6公式、图5对数轴及48h/one-kernel/team-reported脚注已核对。
- 没有递归追读论文参考文献；未独立重跑作者实验。AlphaZero只是官方Lab2类比背景，登记为out_of_scope而非已读。

## 文件

- `humanize-v2.pdf`、`humanize-v2-abs.html`：冻结原文与版本页。
- `humanize-v2.txt`：带换页符的完整layout文字。
- `materials-draft.json`：身份、页码、图表核验、文件hash、已读范围和边界；reading full，但integration pending。
- `supplements-draft.json`：五组可嵌入对应课堂知识点的增量补充；不要直接把 `id/suggested_placement/related_time` 自定义字段混入renderer不支持的notes正文。
- `page-XX.png`：完整原页阅读截图；`key-page-05.png`、`key-page-07.png`是较清晰2400px的完整页，可作为最终内嵌备选，原PDF永远留存。

## 建议采用的图

1. 物理页5 图4（key-page-05.png）：对应“求解→检查→反馈修改”的具体协议。图示四步：code/contract/summary → hook → fresh reviewer → findings/verdict。清楚说明COMPLETE后仍进入代码review。可以只采用图4的完整区域，但必须留标题与所有箭头/注释；本交接提供原完整页，没有裁切。
2. 物理页7 图5（key-page-07.png）：解释知识库、profiling反馈、验证harness各自作用。图右为单个DSA TopK indexer、48小时、团队自报、相对FlashInfer基线；3.71/6.14/8.58均非全赛道通用增益。

采用原页时 frame 应为 `pdf_page`，page 5 或7，source_label应写“论文补充 Humanize v2，非课堂视频帧”，source_url使用固定v2；不得伪造截图时间。related_time等主代理核对转写后填写。

## 关键复核与边界

- 论文不是受控实验。118复盘自选择、113由分析代理模板产生，四名报告者贡献一半；没有同预算builder +/- reviewer对照；无每轮token成本遥测。
- 27份区分阶段报告：364/541轮=67.3%在实现验收后的review；不是“所有运行67.3%时间/成本被浪费”。
- 概率公式的 m_R 是条件漏检因素，不能误写为两个模型独立错误相乘的实证结论。
- KDA比赛DSA indexer19.08倍与后续48h消融8.58倍口径不同；五个kernel两个慢于基线。
- 论文gem5案例PR未通过upstream CI、待maintainer接受；不要写为已合并交付。自然语言奥赛成绩自评，IBO代理可见答案；不建议在Lab2补充中堆这些成就数字。
- 固定v2介绍的旧插件与后继Humanize runtime不同，不把论文当现行软件文档。
- 未核实课堂是否口述Humanize或展示论文哪个版本。当前材料全部标“现行官方Lab2材料/论文补充”，由主代理按转写最终决定归属。

## 自测建议（整理者题目）

- 两个模型互相review，为什么仍可能接受同一个错误？答：共同盲点、证据不足、验证范围不覆盖需求；模型数不是质量证明。
- effort加倍后答案变好一次，能否认定框架有效？答：先固定输入和指标，比直接求解/低/高effort，记录质量与成本，重复或盲评，避免只挑成功例。
- 图5的8.58倍意味着什么？答：论文团队在指定48h、单个DSA TopK indexer消融中，相对FlashInfer基线的平均加速比，不能当所有代码或任务的一般提升。
