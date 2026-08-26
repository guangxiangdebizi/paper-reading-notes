# Color Overlap Multiplexing 文献分支索引

完成日期：2026-08-25

状态：顶会顶刊主链、最近邻与技术路线首轮审计完成。

## 当前判断

- 单 RGB 多图隐藏已有 DeepMIH（TPAMI）、ISN（CVPR 2021）、InvMIHNet（ICASSP 2024）等直接先例。
- 可防御方向不是“首次多图压单图”，而是强预训练 VLM 上的 lightweight semantic demultiplex、clean-conditional retention、query-conditioned layer reveal 与真实 cost Pareto。
- LaSt-ViT 只提供 selective aggregation / anti-shortcut 思路，不是 layer decoder 或 token compressor。
- 现有真实图像和自然视频结果未证明颜色 overlap 优于 contact sheet；后续从 base competence gate 与 post-processor probe 开始。

## 阅读入口

| 文件/项目 | 内容 | 状态 |
|---|---|---|
| [`../../../颜色重叠多图复用分支阅读路线图.md`](../../../颜色重叠多图复用分支阅读路线图.md) | 图形学到 LaSt-ViT 的阅读顺序与失败触发支线 | 已完成 |
| [`../last-vit/精读笔记/README.md`](../last-vit/精读笔记/README.md) | LaSt-ViT 四站精读 | 已完成 |
| `D:/Myproject/chromatic-superposition-vlm/docs/LAST_VIT_COLOR_OVERLAP_ROUTE.md` | 系统架构、operator、capacity、成本与实验 gate | source of truth |
| `D:/Myproject/chromatic-superposition-vlm/docs/SEMANTIC_PRIOR_AND_BASE_COMPETENCE.md` | 强 base prior 假设、clean competence cohort 与指标 | source of truth |
| `D:/Myproject/chromatic-superposition-vlm/docs/NOVELTY_AUDIT_20260825.md` | 直接近邻矩阵、可防御与禁止主张 | source of truth |
| `D:/Myproject/chromatic-superposition-vlm/literature/COLOR_OVERLAP_TOP_VENUE_CHAIN.md` | 完整一手文献链 | source of truth |
| `D:/Myproject/chromatic-superposition-vlm/literature/evidence-register-20260825.csv` | 结构化证据登记 | source of truth |

独立私有项目分支：[`research/last-vit-color-overlap-20260825`](https://github.com/guangxiangdebizi/chromatic-superposition-vlm/tree/research/last-vit-color-overlap-20260825)。本仓库不复制方法文档和证据表，以避免两个 source of truth。

## 下一站

先执行 `K=2` 的 Base-Competence-Gated Carrier Retention：P0 operator audit -> G0 clean competence -> G1 processor 后 layer probe/条件保留 -> G2 causal test -> G3 A0 demux adapter -> G4/G5 contact/token-compression 与成本 gate。未过 probe 时不得用更大 LoRA 掩盖 carrier 信息损失。
