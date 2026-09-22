# Mamba 视觉链路阅读路线图

> 定位：Mamba（选择性状态空间模型，SSM）在 CV 侧的完整链路，自《ViT 家族拓展阅读路线图》支线五「挑战者·非注意力架构」（原仅登记 Vim / VMamba 两篇）展开为独立链路图。
> 本图只做清单登记与阅读排序，**不建精读笔记归档、不预插知识图谱**；某篇确定精读时，按仓库规则建 `<年份>/<月份>/<论文名>/` 归档目录，精读完成后再按 SCHEMA_SPEC 写入 `knowledge_graph/data/papers/<id>.yaml` 入图（2026-09-22 使用方确立：图谱内只放精读完成的论文，方便逐篇查看复核）。
> 表内 venue 与 arXiv 编号于 2026-09-22 经 arXiv API + 会议官方论文库（CVF / ECVA / MICCAI / OpenReview）双渠道核对；仅单渠道佐证或渠道间有分歧的，在表内显式标注「待核实」。
> **当前状态**：35 篇登记（含综述 3 篇、既有登记引用 2 篇），0 篇精读。

---

## 📜 来历说明

1. 《ViT 家族拓展阅读路线图》支线五仅登记 Vim、VMamba 两篇（2026-08-12 建）。2026-09-22 应使用方要求，将 Mamba 在 CV 侧的链路整理为独立路线图：上游源头 → 视觉骨干 → 视频 / 复原 / 分割 / 检测 / 多模态下游，后续逐篇精读、逐篇入图。
2. **既有登记衔接**：`vim`、`vmamba` 两条目已存在于 `knowledge_graph/data/catalog.yaml`（挂 `t_ext_challenger`，状态"选读"），本图 #5、#6 引用之，不重复登记；精读入图时再处理归属。
3. **检索澄清（如实记录，检索不到 ≠ 不存在）**：
   - 「VMamba v2」未检索到独立成文（arXiv 全文 + Semantic Scholar 双渠道 0 命中；VMamba 的 arXiv v4（2024-12）为扩展版稿件）。项目根目录 `vmsv2/` 文件夹经核实与 VMamba 无关（系视频 QA 课题独立仓库）。
   - 「SwinMamba」骨干论文未能定位，仅检索到 2025 年两篇同名细分应用（血管分割 2507.01323、遥感分割 2509.20918），未入清单。
4. **调研纠偏记录**（主 agent 复核，2026-09-22）：PlainMamba 实际 venue 为 **BMVC 2024**（非 ECCV）；LocalMamba 编号实为 2403.09338、VideoMamba（OpenGVLab）实为 2403.06977；MANTA 的 arXiv 编号经主 agent 用 arXiv API 复核为 **2501.08837**（调研初稿所记 2503.08675 实为一篇无关数学论文）。
5. Mamba 正刊 venue 经 OpenReview 官方记录核实为 **COLM 2024**；S2/DBLP 尚未关联该会议，属单一权威渠道佐证，如实标注。

---

## 🧭 链路总览

```
上游源头（序列建模，非 CV 专属）
S4 (ICLR 2022) ──► Mamba (COLM 2024) ──► Mamba-2 (ICML 2024) ──► Mamba-3 (ICLR 2026)
                        │
      ┌─────────────────┼───────────────────────────┐
      ▼                 ▼                           ▼
 主线一 视觉骨干      主线二 视频理解            主线三～五 下游任务
 Vim (plain 双向)    VideoMamba (OpenGVLab)     复原: MambaIR → MambaIRv2 / MambaLLIE
 VMamba (SS2D 层级)    └► VideoMambaPro         分割2D: ReMamber / Hybrid Mamba / Bridge
   ├ 扫描设计: MSVMamba / LocalMamba /          分割3D医学: SegMamba / U-Mamba* / Mamba-UNet*
   │            PlainMamba / PRISMamba          检测: WaveMamba / MambaDETR* / Mamba YOLO*
   ├ 混合架构: MambaVision / GroupMamba         多模态等: Cobra / MANTA
   ├ 轻量化: EfficientVMamba
   └ 对照组(批判): MambaOut ◄── 先立"何处需要 Mamba"的边界
                                             (* 为 arXiv 预印本或 venue 待核实)
 综述（背景，非精读主体）: 2405.04404 / 2410.03105 / 2502.07161
```

---

## 📋 主线零：上游源头（序列建模）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 1 | **S4**：Efficiently Modeling Long Sequences with Structured State Spaces | ICLR 2022（Outstanding Paper HM） | [2111.00396](https://arxiv.org/abs/2111.00396)（已核对） | HiPPO + 低秩修正使 SSM 可高效训练，整条链路的数学源头 | 必读 |
| 2 | **Mamba**：Linear-Time Sequence Modeling with Selective State Spaces | COLM 2024（OpenReview 核实；S2/DBLP 未挂 venue，单权威渠道） | [2312.00752](https://arxiv.org/abs/2312.00752)（已核对） | 选择性 SSM（参数随输入变化）+ 硬件感知并行扫描，线性复杂度替代注意力的奠基作 | 必读 |
| 3 | **Mamba-2**：Transformers are SSMs | ICML 2024 | [2405.21060](https://arxiv.org/abs/2405.21060)（已核对） | SSD 理论框架证明 SSM 与注意力变体对偶，核心层比 Mamba 快 2–8 倍 | 选读 |
| 4 | **Mamba-3**：Improved Sequence Modeling using State Space Principles | ICLR 2026（arXiv 自述 + 官方仓库双证） | [2603.15569](https://arxiv.org/abs/2603.15569)（已核对） | Mamba 系 2026 年最新上游迭代，链路上游终点候选 | 选读 |

---

## 📋 主线一：视觉骨干（图像分类 / 通用骨干网）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 5 | **Vim**：Vision Mamba, Efficient Visual Representation Learning with Bidirectional SSM | ICML 2024 | [2401.09417](https://arxiv.org/abs/2401.09417)（已核对） | 首批纯 SSM 视觉骨干：双向 Mamba + 位置嵌入的 plain 架构，对标 DeiT（既有登记，见来历说明第 2 条） | 必读 |
| 6 | **VMamba**：Visual State Space Model | NeurIPS 2024 spotlight | [2401.10166](https://arxiv.org/abs/2401.10166)（已核对） | SS2D 四方向 2D 选择性扫描 + 层级式骨干，检测/分割全面验证，与 Vim 并列两大主干（既有登记） | 必读 |
| 7 | **MSVMamba**：Multi-Scale VMamba | NeurIPS 2024 | [2405.14174](https://arxiv.org/abs/2405.14174)（已核对） | 多尺度 2D 扫描 + ConvFFN，削减 VMamba 多路扫描冗余 | 选读 |
| 8 | **LocalMamba** | ECCV 2024（主会/Workshop 归属渠道分歧，待核实） | [2403.09338](https://arxiv.org/abs/2403.09338)（已核对） | 窗口化局部扫描 + 逐层搜索扫描方向，修补展平扫描破坏 2D 局部依赖的问题 | 选读 |
| 9 | **PlainMamba** | BMVC 2024（注意：非 ECCV） | [2403.17695](https://arxiv.org/abs/2403.17695)（已核对） | 非层级 plain 骨干：连续 2D 扫描保空间邻接 + 方向感知更新，对照 Vim（plain 线）与 VMamba（层级线） | 选读 |
| 10 | **EfficientVMamba** | AAAI（届次待核实，推断 AAAI 2025；DBLP 仅 arXiv 记录） | [2403.09977](https://arxiv.org/abs/2403.09977)（已核对） | 空洞选择性扫描（skip sampling）轻量化骨干 | 备查 |
| 11 | **MambaVision** | CVPR 2025 | [2407.08083](https://arxiv.org/abs/2407.08083)（已核对） | Mamba-Transformer 混合：末段叠 self-attention 补长程依赖，层级式，混合路线代表作（NVIDIA） | 选读 |
| 12 | **GroupMamba** | CVPR 2025 | [2407.13772](https://arxiv.org/abs/2407.13772)（已核对） | 通道分组 + 四方向 VSSS 块 + 调制算子，解决纯 SSM 大模型训练不稳 | 选读 |
| 13 | **MambaOut**：Do We Really Need Mamba for Vision? | CVPR 2025 | [2405.07992](https://arxiv.org/abs/2405.07992)（已核对） | 批判性对照组：去掉 SSM 的 MambaOut 在 ImageNet 分类反超视觉 Mamba，论证 Mamba 只对长序列/自回归任务必要——链路必备反方证据 | 必读 |
| 14 | **PRISMamba**：Partial Ring Scan | ICML 2026 | [2602.04170](https://arxiv.org/abs/2602.04170)（已核对） | 同心环顺序无关聚合，重审扫描顺序对性能/旋转鲁棒性的影响，精度吞吐双超 VMamba | 备查 |

---

## 📋 主线二：视频理解

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 15 | **VideoMamba**（OpenGVLab）：State Space Model for Efficient Video Understanding | ECCV 2024 | [2403.06977](https://arxiv.org/abs/2403.06977)（已核对） | 时空双向扫描 + 自蒸馏，长视频线性复杂度；视频子链底座，下游工作普遍以它为基座 | 选读 |
| 16 | **VideoMambaPro**：Snakes and Ladders, Two Steps Up for VideoMamba | ICCV 2025 | [2406.19006](https://arxiv.org/abs/2406.19006)（已核对） | 理论分析 Mamba 历史衰减/元素矛盾，masked backward + 元素残差修复 | 备查 |
| 17 | **VideoMamba**（SNU，同名异文）：Spatio-Temporal Selective State Space Model | ECCV 2024 | [2407.08476](https://arxiv.org/abs/2407.08476)（已核对） | 与 #15 同名不同文（两篇同在 ECCV 2024），检索引用时注意区分 | 备查 |
| 18 | **VFIMamba**：Video Frame Interpolation with State Space Models | NeurIPS 2024 | [2407.02315](https://arxiv.org/abs/2407.02315)（已核对） | 下游应用向：视频插帧 | 备查 |

---

## 📋 主线三：低层视觉 / 图像复原（下游最厚一族）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 19 | **MambaIR**：A Simple Baseline for Image Restoration with State-Space Model | ECCV 2024 | [2402.15648](https://arxiv.org/abs/2402.15648)（已核对） | Mamba 复原基线：去雨/去噪/超分等 5 类复原任务 | 选读 |
| 20 | **MambaIRv2**：Attentive State Space Restoration | CVPR 2025 | [2411.15269](https://arxiv.org/abs/2411.15269)（已核对） | 注意力引导的扫描，缓解全局感受野与因果扫描的矛盾 | 选读 |
| 21 | **MambaLLIE**：Implicit Retinex-Aware Low Light Enhancement with Global-Local State Space | NeurIPS 2024 | [2405.16105](https://arxiv.org/abs/2405.16105)（已核对） | Retinex 先验 + 全局-局部状态空间的低光增强 | 备查 |

---

## 📋 主线四：分割（2D 自然图像 + 3D 医学）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 22 | **SegMamba**：Long-range Sequential Modeling Mamba For 3D Medical Image Segmentation | MICCAI 2024 | [2401.13560](https://arxiv.org/abs/2401.13560)（已核对） | 3D 医学分割全序列建模，速度与显存优势突出 | 选读 |
| 23 | **U-Mamba**：Enhancing Long-range Dependency for Biomedical Image Segmentation | 仅 arXiv 预印本（已核实无正式收录） | [2401.04722](https://arxiv.org/abs/2401.04722)（已核对） | nnU-Net 骨架内嵌 Mamba，引用量最高的医学 Mamba 之一 | 备查 |
| 24 | **Mamba-UNet**：UNet-Like Pure Visual Mamba for Medical Image Segmentation | 仅 arXiv 预印本（已核实无正式收录） | [2402.05079](https://arxiv.org/abs/2402.05079)（已核对） | 纯 VMamba 的 U 形 2D 医学分割 | 备查 |
| 25 | **ReMamber**：Referring Image Segmentation with Mamba Twister | ECCV 2024 | [2403.17839](https://arxiv.org/abs/2403.17839)（已核对） | Mamba 首批引用图像分割：Twister 结构对齐视觉与语言序列 | 备查 |
| 26 | **Hybrid Mamba for Few-Shot Segmentation** | NeurIPS 2024 | [2409.19613](https://arxiv.org/abs/2409.19613)（已核对） | Mamba + Transformer 混合做少样本分割 | 备查 |
| 27 | **Mamba as a Bridge**：Where VFM Meet VLM for Domain-Generalized Semantic Segmentation | CVPR 2025 Highlight | [2504.03193](https://arxiv.org/abs/2504.03193)（已核对） | 用 Mamba 桥接视觉基础模型与 VLM 做域泛化语义分割（本质是"Mamba 当桥"而非分割网络创新） | 备查 |

---

## 📋 主线五：检测与多模态（顶会成果稀薄，如实呈现）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 28 | **WaveMamba**：Wavelet-Driven Mamba Fusion for RGB-Infrared Object Detection | ICCV 2025（arXiv journal_ref + CVF 双渠道） | [2507.18173](https://arxiv.org/abs/2507.18173)（已核对） | RGB-红外小目标定向检测（遥感/多光谱，非自然图像 2D） | 备查 |
| 29 | **MambaDETR**：Query-based Temporal Modeling for Multi-View 3D Object Detection | 仅 arXiv（已确认无 venue comment） | [2411.13628](https://arxiv.org/abs/2411.13628)（已核对） | 多视角 3D 检测的时序建模，非 2D 自然图像 | 备查 |
| 30 | **Mamba YOLO**：A Simple Baseline for Object Detection with State Space Model | 未见正式收录（核查范围有限：DBLP 当时不可用） | [2406.05835](https://arxiv.org/abs/2406.05835)（已核对） | Mamba 版 YOLO 基线；无官方代码、无 venue 证据 | 备查 |
| 31 | **Cobra**：Extending Mamba to Multi-Modal LLM for Efficient Inference | AAAI 2025 | [2403.14520](https://arxiv.org/abs/2403.14520)（已核对） | Mamba 多模态大模型，推理效率对标 LLaVA | 备查 |
| 32 | **MANTA**：Diffusion Mamba for Efficient and Effective Stochastic Long-Term Dense Anticipation | CVPR 2025（CVF 列表单渠道，待核实） | [2501.08837](https://arxiv.org/abs/2501.08837)（已核对，编号经主 agent 复核更正） | 扩散 + Mamba 做长时密集动作预判 | 备查 |

---

## 📋 综述（背景文献，非精读主体）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 33 | **Vision Mamba: A Comprehensive Survey and Taxonomy** | 仅 arXiv（S2/DBLP 无会议记录） | [2405.04404](https://arxiv.org/abs/2405.04404)（已核对） | 视觉 Mamba 综述与分类学 | 备查 |
| 34 | **Mamba in Vision: A Comprehensive Survey** | 仅 arXiv（comment: Under Review） | [2410.03105](https://arxiv.org/abs/2410.03105)（已核对） | 视觉 Mamba 综述（含 GitHub 论文列表仓库） | 备查 |
| 35 | **A Survey on Mamba Architecture for Vision Applications** | 仅 arXiv | [2502.07161](https://arxiv.org/abs/2502.07161)（已核对） | 2025 年视觉 Mamba 架构综述 | 备查 |

> 同类预印本综述另有 A Survey on Visual Mamba（2404.15956）、Visual Mamba: A Survey and New Outlooks（2404.18861）、Mamba-360（2404.16112），均未核到正式 venue，不单独列行。

---

## 🩺 链路厚薄评估（2026-09-22 调研结论，如实记录）

1. **低层视觉/复原与 3D 医学分割最厚**：MambaIR → MambaIRv2 已成体系（ECCV 2024 → CVPR 2025）；医学方向 SegMamba（MICCAI 2024）正式发表，U-Mamba / Mamba-UNet 引用高但均为预印本；医学顶刊（TMI/MedIA）后续未在本轮核查范围内。
2. **目标检测（2D 自然图像）最薄**：CVPR 2025 / ICCV 2025 / ECCV 2024 三届官方列表中，2D 自然图像检测的 Mamba 论文为零（仅显著目标、遥感/红外、LiDAR 3D 各 1–2 篇）；该方向暂无被顶会检验的代表工作。
3. **语义/实例分割（2D 自然图像）偏薄**：无独立的 Mamba 全监督语义分割顶会代表作，现有工作均为细分设定（引用分割/少样本/域泛化）。
4. **视频理解**：顶会主力是两条 VideoMamba 骨干（归主线二），下游应用仅插帧、动作预判等点状成果。
5. **与 ViT 链路的关系**：截至 2026-09，Mamba 系在长序列、高分辨率场景有成本优势，但尚未撼动 ViT 主流地位（与《ViT 家族拓展》支线五结论一致）；MambaOut（#13）提供了"分类任务未必需要 SSM"的顶会级反方证据，精读时应先立边界再看骨干。

---

## 🔗 推荐精读链（启动精读时的顺序）

1. **Mamba**（#2）：选择性 SSM 机制 + 硬件感知并行扫描，全链路的前置知识；S4（#1）作数学源头，可先读或随读随查。
2. **Vim**（#5）：SSM 进视觉的最小改动路线（plain 架构），与 ViT 直接对照。
3. **VMamba**（#6）：2D 扫描路线（SS2D），与 Vim 构成方法论对照——"展平序列怎么保住 2D 结构"是本链路的核心张力。
4. **MambaOut**（#13）：批判性对照组，先立"Mamba 在何处必要/不必要"的边界，避免链路叙事一边倒。
5. **MambaIR**（#19）：下游最厚一族（复原）的代表。
6. **SegMamba**（#22）：3D 医学代表，长序列线性复杂度优势最显著的场景。
7. **VideoMamba**（#15）：视频长序列延伸。
8. **MambaVision**（#11）：混合架构（Mamba + attention），与 ViT 链路汇合的对照点。

按需扩展：Mamba-2（#3，理论统一）→ MSVMamba / LocalMamba / PlainMamba（#7–9，扫描设计细节）→ Mamba-3 / PRISMamba（#4、#14，2026 最新）。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| （暂无） | | |

---

## 📌 维护约定

1. **精读一篇的流程**：建归档 `<年份>/<月份>/<论文名>/`（PDF + fulltext + figures + 精读笔记四站）→ 本图对应行状态改为 `✅ 已读（[笔记](链接)）` → 精读记录表加一行。
2. **入图时机（2026-09-22 使用方确立）**：登记阶段**不预插** `catalog.yaml`；每篇精读完成后按 `knowledge_graph/data/SCHEMA_SPEC.md` 写 `knowledge_graph/data/papers/<id>.yaml`，首次入图时一并在 catalog.yaml 补本链路的 topic（建议 `t_mamba_branch` + 各主线 subline，届时按实际精读范围定），重跑 `build_graph.py --reset` 并用 `query.py --paper <id>` 验证。
3. **精读笔记要求**：保留论文原生实际完整信息——原文真实数字、真实实验设置、真实表述与结论；不做艺术加工与逻辑加工（规则见全局 CLAUDE.md「论文讲解风格」，派发精读 subagent 时任务说明须原样包含）。
4. **待核实项跟踪**（下次动本图时顺手复核）：① Mamba 在 COLM 2024 的接收等级；② LocalMamba 主会 vs Workshop；③ EfficientVMamba 的 AAAI 届次；④ MANTA 的 CVPR 2025 venue（当前单渠道）；⑤ Mamba YOLO 是否被期刊收录（当时 DBLP 不可用，核查范围有限）。
