# 阅读和恢复

## 阅读

克隆或下载仓库，使用浏览器打开 `生成式软件工程/课程索引.html`。10 篇现行笔记均内嵌图片，可离线阅读。GitHub 文件页只显示源码；下载后打开 HTML。也可下载 Release 的 `course-reading-2026-10-27.zip`，这是只含现行阅读成品的便携包。

## 取得源视频

```sh
gh release download snapshot-2026-10-27 --repo zhao-d-r/generative-software-engineering-2026 --pattern '*.mp4' --dir media
python3 tools/verify_archive.py --media-dir media
```

仓库和 Release 公开可读；gh 命令需要可用的 GitHub CLI 环境，也可直接从网页下载。`archive/media-manifest.json` 将 Release 的 BV 文件名映射到原始视频名、来源 URL 和 SHA-256。

## 恢复 BaoCut

1. 先校验 `python3 tools/verify_archive.py`，把需要的 `.bcut` 目录复制到新的工作位置；不要直接编辑仓库中的档案。
2. 下载对应原视频并按媒体清单核对哈希。
3. 用兼容的 BaoCut 打开项目副本；原项目保留了旧机器的媒体绝对路径。若媒体离线，通过 BaoCut 的项目设置/重新关联媒体操作选择已下载文件，不手改 `.bcut` 内部 JSON。
4. 检查转写、章节、Studio 与媒体能否正常工作。只有完成这些实际检查，才能声称跨机器原生恢复成功；本次未在第二台机器验证。

工作流快照见 `tooling/baocut-course-notes/`；BaoCut App、模型和登录/密钥配置不分发。历史脚本可能仍引用原工作目录，应先审阅路径和依赖。完整重算会产生新版本及新审查记录，不能把归档中的旧 PASS 当作当前机器的 PASS。
