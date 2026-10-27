# BaoCut chapter metadata run — 2026-10-02

CLI: `/Users/yjzhao/Downloads/BaoCut.app/Contents/Resources/skills/baocut/bin/bcut-cli`  
App/spec: `2.1.0` / `1.249.0`; existing runtime reused (`started: false`).  
Project root: `/Users/yjzhao/Library/Application Support/BaoCut/projects/`.

Each project was inspected with `--json project show`, `--json task status`, and `--json review list` before starting. All had zero existing chapters, zero review candidates, and zero pending chapter calls. Exact preflight output is in the corresponding `*-before.json` files.

| Video ID | Producer command (project path abbreviated to `<project>`) | Task ID | Producer result | Accept result | Final state |
| --- | --- | --- | --- | --- | --- |
| BV1pb8o6yE8f | `chapters <project> --review --from-source --jsonl` | none (source path) | 5 source entries; 4 matched, 1 ambiguous; 5 chapters | accepted, 5 chapters | chapters fresh; strict check ready |
| BV1kybV6DE47 | `chapters <project> --review --from-source --jsonl` | none (source path) | 3 source entries; 3 matched; 3 chapters | accepted, 3 chapters | chapters fresh; strict check ready |
| BV1Q6en6NEUo | `chapters <project> --review --from-source --jsonl` | none (source path) | 3 source entries; 2 matched, 1 ambiguous; 3 chapters | accepted, 3 chapters | chapters fresh; strict check ready |
| BV1fKtN6DErG | `chapters <project> --review --llm agent --jsonl` | `t-mur4u87i`, call `c0001` | one `chapters` call, accepted first submission; 2 chapters, no outline fallback | accepted, 2 chapters | chapters fresh; strict check ready |

For all four projects, acceptance used `--json review accept <project> chapters`; final verification used `--json project show <project>` and `check <project> --strict --json`. All four strict checks exited 0 with `data.ready: true`. The `*-chapters-*.jsonl`, `*-accept.json`, `*-final-show.json`, and `*-strict-check.json` files preserve the command results. The short clip's `*-answer-c0001.html` preserves the submitted worker answer. No retries were needed.
