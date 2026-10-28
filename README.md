# 生成式软件工程 · 2026

南京大学《生成式软件工程》个人学习笔记与 BaoCut 制作档案。归档日期：2026-10-27。

现有 **9 课 + 1 个补充视频，190 节正文，96 张手绘图解，359 幅原帧（其中 249 张官方 slides 页），166 条推荐材料补充，5,087 个转写来源单元**（2026-10-28 v3 重写版）。各课 `课堂笔记.html` 已按精简版 baocut-course-notes skill 从原始转写与原视频重写，再增量补入官方讲义、slides 和推荐材料（台账见各课 `v3-rewrite/materials.json`），图解为手绘信息图，并由另一家模型做精度/召回评测；审计材料在各课 `v3-rewrite/`。此前版本的制作档案与审查历史原样保留在各课目录和 git 历史中。

- **归档指南**：[阅读与恢复 HTML](归档阅读与恢复.html)，也可直接读本页。
- **阅读入口**：[课程索引](生成式软件工程/课程索引.html)。GitHub 显示 HTML 源码，下载后用浏览器打开。
- **只读笔记（推荐）**：[下载 course-reading-2026-10-27.zip](https://github.com/zhao-d-r/generative-software-engineering-2026/releases/download/snapshot-2026-10-27/course-reading-2026-10-27.zip)（约 86 MB）；解压后打开 `生成式软件工程/课程索引.html`。
- **10 个原视频**：[snapshot-2026-10-27 Release](https://github.com/zhao-d-r/generative-software-engineering-2026/releases/tag/snapshot-2026-10-27)，按 BV ID 选择需要的 `.mp4`。
- **恢复项目**：[RESTORE.md](RESTORE.md)；**制作记录说明**：[archive/README.md](archive/README.md)。
- **延伸分析**：[pstack Skills 写法与生成式软件工程启发](research/reports/pstack%20Skills%20写法与生成式软件工程启发.html)。其来源快照和审查资料保存在相邻 research/research_notes 目录。

| 课次 | 笔记 | 视频 ID |
|---|---|---|
| 第01课 | [欢迎来到未来](生成式软件工程/lecture-01/课堂笔记.html) | `BV1pb8o6yE8f` |
| 补充 | [失败的AI Slop数字永生尝试](生成式软件工程/extra-ai-slop/课堂笔记.html) | `BV1fKtN6DErG` |
| 第02课 | [提示词工程](生成式软件工程/lecture-02/课堂笔记.html) | `BV1CQt365EzW` |
| 第03课 | [软件仓库管理](生成式软件工程/lecture-03/课堂笔记.html) | `BV1kybV6DE47` |
| 第04课 | [软件仓库管理 (2)](生成式软件工程/lecture-04/课堂笔记.html) | `BV1Q6en6NEUo` |
| 第05课 | [软件工程的来龙去脉](生成式软件工程/lecture-05/课堂笔记.html) | `BV1Nyeq6qEt8` |
| 第06课 | [需求和架构 (1)](生成式软件工程/lecture-06/课堂笔记.html) | `BV1Rch76WEfQ` |
| 第07课 | [需求和架构 (2)](生成式软件工程/lecture-07/课堂笔记.html) | `BV1JGap6LE74` |
| 第08课 | [Agent-native 开发](生成式软件工程/lecture-08/课堂笔记.html) | `BV11LWw6VEHW` |
| 第09课 | [DeepSeek Harness (1)](生成式软件工程/lecture-09/课堂笔记.html) | `BV144nc6KEA4` |

## 档案结构

```text
生成式软件工程/          现行 HTML、notes/layout、原始转写和 chunks、讲义/论文、帧、QA、修订
baocut/projects/         10 个原生 .bcut 目录，含 ASR、Studio、历史、任务日志、已有缓存
legacy/                  可识别的早期复用成果与原截图
research/                pstack Skills 对照分析及固定版本来源
tooling/                 本次冻结的课程 skill 与检查器源码
archive/                 项目/视频映射、逐文件 SHA-256、转换与排除说明、归档复核
tools/verify_archive.py   无第三方依赖的完整性检查
```

## 下载与校验

```sh
gh repo clone zhao-d-r/generative-software-engineering-2026
cd generative-software-engineering-2026
python3 tools/verify_archive.py
```

源视频约 2.44 GB，放在同仓库 Release，不进入 Git 历史；转写分块和全部候选帧保存在仓库。GitHub 对普通 Git 大文件的限制见[官方说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。本次没有找到另存的音视频 slices；没有为上传重新切片。已有 waveform 等项目缓存予以保留。

## 质量与范围

原笔记中的内容/逐图/来源/浏览器复核记录随档保存。本次检查复制完整性、媒体指纹、现行 HTML 与索引、上传后的远端对象和 Release 资产；不等于重新听完整课程，也不把旧历史 QA 当成跨机器新验收。真实手机、部分原生打印与第二台机器原生项目恢复未测，逐课限制见各自 review。

本机原始课程、项目和媒体未改动。课程目录中一份历史全机项目清单只保留了本课程条目；OS/Python 缓存与临时锁不归档，详见 archive/transformations.json 与 exclusions.json。历史绝对路径原样保留，执行旧脚本前先核对环境。仓库公开供课程学习分享，未启用 Pages，未分发 App、模型、账户登录或密钥配置。第三方材料权属见 [ATTRIBUTION.md](ATTRIBUTION.md)。
