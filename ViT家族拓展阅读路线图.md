# ViT 家族拓展阅读路线图

> 定位：《ViT 分支阅读路线图》的下游拓展图。主线（A–D，即 ViT → DeiT → ConvNeXt / Swin → DETR / MAE / Registers → LAST-ViT）精读完成后，沿本图继续拓展 2022–2026 年 ViT 家族的演进。
> 本图只做清单登记与阅读排序，**不建精读笔记归档**；某篇确定精读时，再按仓库规则建 `<年份>/<月份>/<论文名>/` 归档目录，并把该条目从本图迁出、记入对应路线图的"精读记录"。
> 表内 arXiv 编号已于 2026-08-12 经 arXiv 官方 API / abs 页面逐条按标题核对，标注「已核对」；未能核对的在表中显式注明。

---

## 📜 来历说明

1. 《ViT 分支阅读路线图》建立于 2026-08-07，围绕经典六篇的因果链组织，止于 MAE（2021.11）；BEiT、CLIP、ViT-22B、SETR 等方向当时被记入"未来再说"坑。这是该图未覆盖近两年新论文的直接原因——属于有意收窄，而非遗漏。
2. 2022–2026 年 ViT 方向研究密度很高：架构简化、自监督特征、多模态基础模型、scaling law、非注意力挑战者各自成线。本图把"未来再说"坑展开为**五条支线**，并收拢这一时期的关键工作。
3. 关于「LastViT」的核查结论（2026-08-12 更正）：**确实存在，真名为 LAST-ViT**——《Vision Transformers Need More Than Registers》（CVPR 2026，arXiv [2602.22394](https://arxiv.org/abs/2602.22394)，官方代码 [ChengShiest/LAST-ViT](https://github.com/ChengShiest/LAST-ViT)）。初次核查时用 "LastViT" 作关键词检索 arXiv API 得到 0 条结果——原因是该词的 arXiv 论文标题与摘要中不含 "LAST-ViT" 字样（它只是官方代码仓库名），检索策略未覆盖 GitHub 来源，据此下过"查无此文"的错误结论，现已更正。
4. 2026-08-12 调整：**Registers**（arXiv 2309.16588）与 **LAST-ViT**（arXiv 2602.22394）从本图支线一**晋升**至《ViT 分支阅读路线图》主线 D「行为诊断与修正」。理由：该图主线收录标准为"对 ViT 基本设计的直接回应"，Registers 回答"CLS token 的聚合行为有毛病"、LAST-ViT 回答"毛病的根源与修正"，两篇构成完整因果链，且 LAST-ViT 的贡献点（解释 lazy aggregation、替换 CLS token）属于 ViT 基础架构层面的行为学，而非单纯工程优化。
5. 此前按名称相似度猜测的候选（FastViT / NaViT / FlexiViT）仍保留在支线一，但非正主。

---

## 🧭 五条支线总览

```
主线（见《ViT 分支阅读路线图》，A–D 四条主线八篇）
   │
   ├─ 支线一：架构演进续集（承接主线 B：Swin）
   │     Swin V2 / ConvNeXt V2 / Hiera / FastViT / FlexiViT / NaViT
   │     推理侧：ToMe；移动端：MobileViT 系 / EdgeNeXt / EfficientViT 系
   │     （Registers、LAST-ViT 已晋升主线 D，见上"来历说明"第 4 条）
   │
   ├─ 支线二：自监督续集（承接主线 C：MAE）
   │     遮块预测系：BEiT → BEiT v2 / BEiT-3 / iBOT
   │     自蒸馏系：DINO → DINOv2 → DINOv3
   │     表征预测系：I-JEPA；规模探索系：EVA / EVA-02
   │
   ├─ 支线三：多模态与视觉基础模型（原"未来再说"坑的 CLIP 系）
   │     CLIP → SigLIP → SigLIP 2；AIM / AIMv2
   │     InternVL（InternViT-6B）；SAM（应用侧证据）
   │
   ├─ 支线四：Scaling 与训练配方（原"未来再说"坑的 Scaling Law 系）
   │     ViT-22B；DeiT III；FlashAttention 1/2/3
   │
   └─ 支线五：挑战者——非注意力架构
        Vim / VMamba（状态空间模型进视觉）
```

---

## 📋 支线一：架构演进续集（承接主线 B：Swin）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 1 | **Swin V2**：Scaling Up Capacity and Resolution | CVPR 2022 | [2111.09883](https://arxiv.org/abs/2111.09883)（已核对） | Swin 的规模化续作：postnorm→prenorm、对数窗口注意力，把容量推到 190M 参数、3B 预训练图像 | 必读 |
| 2 | **ConvNeXt V2**：Co-designing and Scaling ConvNets with MAE | CVPR 2023 | [2301.00808](https://arxiv.org/abs/2301.00808)（已核对） | 现代 CNN 对"自监督时代"的回答：与 MAE 协同设计 + GRN 层，证明配方红利同样属于 CNN | 必读 |
| 3 | **Hiera**：A Hierarchical Vision Transformer without the Bells-and-Whistles | ICML 2023 | [2306.00989](https://arxiv.org/abs/2306.00989)（已核对） | 极简层级 ViT：去掉大部分工程花活，用强预训练（MAE）补齐，更简单更快 | 选读 |
| 4 | **FastViT**：A Fast Hybrid Vision Transformer using Structural Reparameterization | ICCV 2023 | [2303.14189](https://arxiv.org/abs/2303.14189)（已核对） | 结构重参数化 + 注意力/卷积混合分支，移动端高效骨干 | 选读 |
| 5 | **FlexiViT**：One Model for All Patch Sizes | CVPR 2023 | [2212.08013](https://arxiv.org/abs/2212.08013)（已核对） | 一套权重适配多种 patch size，推理时任意切换速度/精度档位 | 选读 |
| 6 | **NaViT**：Patch n' Pack, a ViT for any Aspect Ratio and Resolution | arXiv 2023.07 | [2307.06304](https://arxiv.org/abs/2307.06304)（已核对） | 原生分辨率 + 任意长宽比输入，同一 batch 打包不同尺寸图像，告别暴力 resize | 选读 |
| 7 | **ToMe**：Token Merging, Your ViT But Faster | ICLR 2023 | [2210.09461](https://arxiv.org/abs/2210.09461)（已核对） | 渐进合并相似 token，不训练、不加参数，ViT 推理吞吐翻倍级提升 | 选读 |
| 8 | **MobileViT**：Light-weight, General-purpose, Mobile-friendly ViT | ICLR 2022 | [2110.02178](https://arxiv.org/abs/2110.02178)（已核对） | CNN 局部性 + Transformer 全局性的移动端混合骨干开山 | 备查 |
| 9 | **MobileViTv2**：Separable Self-attention for Mobile ViTs | ICLR 2023 | [2206.02680](https://arxiv.org/abs/2206.02680)（已核对） | 线性复杂度的可分离自注意力替代 softmax 注意力，移动端再提速 | 备查 |
| 10 | **EdgeNeXt**：Efficiently Amalgamated CNN-Transformer for Mobile Vision | ECCV 2022 | [2206.10589](https://arxiv.org/abs/2206.10589)（已核对） | 边缘设备向的 CNN-Transformer 融合骨干 | 备查 |
| 11 | **EfficientViT**（MIT Han Lab 版）：Multi-Scale Linear Attention | CVPR 2023 | [2205.14756](https://arxiv.org/abs/2205.14756)（已核对） | 多尺度线性注意力做高分辨率密集预测；注意与 #12 同名不同文 | 备查 |
| 12 | **EfficientViT**（MSRA 版）：Memory Efficient ViT with Cascaded Group Attention | ICCV 2023 | [2305.07027](https://arxiv.org/abs/2305.07027)（已核对） | 级联分组注意力降低内存开销，同名论文的另一支 | 备查 |

---

## 📋 支线二：自监督续集（承接主线 C：MAE）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 13 | **DINO**：Emerging Properties in Self-Supervised ViTs | ICCV 2021 | [2104.14294](https://arxiv.org/abs/2104.14294)（已核对） | 自蒸馏 + 无标签预训练，ViT 特征自发出现目标分割能力，自监督特征线的源头之一 | 必读 |
| 14 | **BEiT**：BERT Pre-Training of Image Transformers | ICLR 2022 | [2106.08254](https://arxiv.org/abs/2106.08254)（已核对） | 遮块预测离散视觉 token，把 BERT 范式完整搬到图像，ViT 原文 §4.6 设想的正式答卷 | 选读 |
| 15 | **iBOT**：Image BERT Pre-Training with Online Tokenizer | ICLR 2022 | [2111.07832](https://arxiv.org/abs/2111.07832)（已核对） | 在线 tokenizer + 遮块建模，融合 BEiT 与 DINO 两条线 | 选读 |
| 16 | **BEiT v2**：Masked Image Modeling with VQ Visual Tokenizers | arXiv 2022.08 | [2208.06366](https://arxiv.org/abs/2208.06366)（已核对） | 用 VQ-KD 强教师 tokenizer 改进遮块预测目标 | 备查 |
| 17 | **BEiT-3**：Image as a Foreign Language | arXiv 2022.08 | [2208.10442](https://arxiv.org/abs/2208.10442)（已核对） | 把图像视作外语，统一视觉与视觉-语言任务的预训练框架 | 备查 |
| 18 | **I-JEPA**：Self-Supervised Learning From Images with a Joint-Embedding Predictive Architecture | CVPR 2023 | [2301.08243](https://arxiv.org/abs/2301.08243)（已核对） | LeCun 路线：在抽象表征空间做预测而非重建像素，训练算力大幅降低 | 选读 |
| 19 | **DINOv2**：Learning Robust Visual Features without Supervision | arXiv 2023.04 | [2304.07193](https://arxiv.org/abs/2304.07193)（已核对） | 精细数据工程 + 规模化自蒸馏，无需微调即得通用视觉特征，成为下游事实标准骨干 | 必读 |
| 20 | **DINOv3** | arXiv 2025.08 | [2508.10104](https://arxiv.org/abs/2508.10104)（已核对） | 引入 Gram anchoring 保持特征多样性，冻结特征全面超越微调，跨模态迁移能力显著增强 | 必读 |
| 21 | **EVA**：Exploring the Limits of Masked Visual Representation Learning at Scale | CVPR 2023 | [2211.07636](https://arxiv.org/abs/2211.07636)（已核对） | CLIP 教师 + MAE 学生的组合，探索遮块表征学习的规模极限 | 选读 |
| 22 | **EVA-02**：A Visual Representation for Neon Genesis | arXiv 2023.03 | [2303.11331](https://arxiv.org/abs/2303.11331)（已核对） | 用 EVA-CLIP 教师重训学生，更小模型取得更强表征 | 备查 |

---

## 📋 支线三：多模态与视觉基础模型（原"未来再说"坑的 CLIP 系）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 23 | **CLIP**：Learning Transferable Visual Models From Natural Language Supervision | ICML 2021 | [2103.00020](https://arxiv.org/abs/2103.00020)（已核对） | 图文对比预训练 + zero-shot 迁移，ViT 家族的另一条分水岭，一切多模态基础模型的起点 | 必读 |
| 24 | **SigLIP**：Sigmoid Loss for Language Image Pre-Training | ICCV 2023 | [2303.15343](https://arxiv.org/abs/2303.15343)（已核对） | sigmoid 逐对损失替代 softmax 全局对比，去掉跨卡负样本同步，训练可扩展性大增 | 选读 |
| 25 | **SigLIP 2**：Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features | arXiv 2025.02 | [2502.14786](https://arxiv.org/abs/2502.14786)（已核对） | 多语言 + 定位 + 密集特征全面改进，当前 VLM 视觉前端的主流选择之一 | 选读 |
| 26 | **AIM**：Better and Faster Large Vision Models via Multi-resolution Pretraining | ECCV 2022 | arXiv 编号待核对（API 检索未命中，读原文前需手工确认） | Apple：ViT-g 在约 5 亿图像上自回归预训练，多分辨率课程式训练 | 备查 |
| 27 | **AIMv2**：Multimodal Autoregressive Pre-training of Large Vision Encoders | arXiv 2024.11 | [2411.14402](https://arxiv.org/abs/2411.14402)（已核对） | 自回归预训练产出的视觉编码器直接作为多模态大模型底座 | 备查 |
| 28 | **InternVL**：Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks | CVPR 2024 | [2312.14238](https://arxiv.org/abs/2312.14238)（已核对） | InternViT-6B：开源 6B 级视觉编码器与语言模型的对齐方案 | 备查 |
| 29 | **SAM**：Segment Anything | ICCV 2023 | [2304.02643](https://arxiv.org/abs/2304.02643)（已核对） | ViT-H 骨干 + prompt 式分割，"ViT 成为通用视觉底座"的应用侧证据（应用向，精读可选） | 备查 |

---

## 📋 支线四：Scaling 与训练配方（原"未来再说"坑的 Scaling Law 系）

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 30 | **ViT-22B**：Scaling Vision Transformers to 22 Billion Parameters | ICML 2023 | [2302.05442](https://arxiv.org/abs/2302.05442)（已核对） | Google 把 ViT 推到 220 亿参数，验证视觉域的 scaling law，回答"ViT 的天花板在哪" | 选读 |
| 31 | **DeiT III**：Revenge of the ViT | NeurIPS 2022 | [2204.07118](https://arxiv.org/abs/2204.07118)（已核对） | 训练配方集大成：弱化增强、强化蒸馏教师，与 ConvNeXt 的"配方 vs 架构"之争互为注脚 | 选读 |
| 32 | **FlashAttention**：Fast and Memory-Efficient Exact Attention with IO-Awareness | NeurIPS 2022 | [2205.14135](https://arxiv.org/abs/2205.14135)（已核对） | IO-aware 精确注意力，ViT（及一切 Transformer）训练推理的底层基础设施 | 备查 |
| 33 | **FlashAttention-2** | ICLR 2024 | [2307.08691](https://arxiv.org/abs/2307.08691)（已核对） | 更优并行划分与工作分区，注意力再提速 | 备查 |
| 34 | **FlashAttention-3** | NeurIPS 2024 | [2407.08608](https://arxiv.org/abs/2407.08608)（已核对） | Hopper 架构异步执行 + 低精度，面向新一代 GPU | 备查 |

---

## 📋 支线五：挑战者——非注意力架构

| # | 论文 | 发表 | arXiv | 一句话 | 层级 |
|---|---|---|---|---|---|
| 35 | **Vim**：Vision Mamba, Efficient Visual Representation Learning with Bidirectional SSM | ICML 2024 | [2401.09417](https://arxiv.org/abs/2401.09417)（已核对） | 双向状态空间模型进视觉分类，线性复杂度挑战注意力 | 选读 |
| 36 | **VMamba**：Visual State Space Model | NeurIPS 2024 | [2401.10166](https://arxiv.org/abs/2401.10166)（已核对） | 2D 交叉扫描 + 状态空间骨干，覆盖分类到密集预测 | 选读 |

> 截至 2026-08：Mamba 系在长序列、高分辨率场景展现成本优势，但尚未撼动 ViT 的主流地位（预训练生态、基础模型权重仍以 ViT 系为主）。本支线结论随后续对比研究更新。

---

## 🔗 推荐精读链（核心八篇的因果链）

1. **Swin V2**：主线 B 的直接续作，看窗口注意力如何扩容、如何承接 3B 级预训练。
2. **ConvNeXt V2**：主线 A 的收官——ConvNeXt 与 MAE 协同设计，回答"配方红利归 CNN 还是 ViT"。
3. **DINO**：自蒸馏路线的源头，理解 DINOv2/v3 之前必读。
4. **DINOv2**：数据工程 + 规模化训练造就"免微调通用特征"，当前下游任务的默认骨干。
5. **DINOv3**：2025 年的最新一代，Gram anchoring 解决特征坍缩，冻结即超越微调。
6. **CLIP**：多模态线的分水岭，ViT 家族的第二个起点。
7. **SigLIP**：对比损失的可扩展化改造，理解当代 VLM 视觉前端的关键一步。
8. **ViT-22B**：scaling 线的顶点，与 ViT 原文 §4 的 scaling 讨论首尾呼应。

核心八篇之外，按兴趣自由取用：NaViT / FlexiViT / ToMe（工程实用）、BEiT / iBOT / I-JEPA（自监督理论线）、EVA / DeiT III（训练配方）、Vim / VMamba（挑战者视野）。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| （暂无） | | |

---

## 📌 维护约定

- 本表 arXiv 编号的核对方式为 arXiv 官方 API / abs 页面标题匹配；新纳入论文时需同样核对，无法核对的显式标注「待核对」。
- 读完某篇并在仓库建好精读归档后，从本图删除该条目，同时在《ViT 分支阅读路线图》或本图"精读记录"补链接。
- 领域演进较快（尤其支线二、三、五），每半年复查一次是否有新增必读项。
