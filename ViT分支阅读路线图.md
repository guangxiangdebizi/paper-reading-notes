# ViT 分支阅读路线图

> 以 **Vision Transformer（ViT, ICLR 2021）** 为根的一条大分支：从"纯 Transformer 进入视觉"出发，沿四条主线把这条脉络读完。
> 本文档随精读进度维护：读完一篇就在状态列打勾，并在下方"精读记录"补一行链接。
> **下游拓展**：主线（A–D）之外的 ViT 家族后续演进（2022–2026）统一登记在《[ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)》，主线读完后按该图继续。
> **当前状态**：A–D 四条主线共 8 篇已全部精读完成。

---

## 🧭 四条主线

```
                          ViT (2021.01, ICLR 2021) ✅ 已读
                                │
   ┌──────────────────┬─────────┴──────────┬─────────────────────┐
   ▼                  ▼                    ▼                     ▼
 主线A：效率/数据      主线B：架构演进        主线C：自监督          主线D：行为诊断与修正
 民主化               （"怎么适配各种        （"不靠标签             （"CLS token 在
 （"没大数据也能用"）    视觉任务"）           预训练"）              搞什么名堂"）
   │                  │                    │                     │
 DeiT (2020.12)      Swin (2021.03)       MAE (2021.11)         Registers (2023.09)
   │                  │                                          LAST-ViT (CVPR 2026)
 ConvNeXt (2022.01)  DETR (2020.05)*
 （对照组：CNN 反击）  （下游任务：检测）
```

\* DETR 发表于 ViT 之前，但它是 Transformer 进视觉检测的开路者，读 Swin 后接它正好。

---

## 📋 阅读清单

### 主线 A：效率与数据民主化（ViT 最大短板的补全）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 0 | **ViT**：An Image is Worth 16×16 Words | ICLR 2021 | 纯 Transformer 做视觉；大数据战胜归纳偏置 | ✅ 已读（[笔记](./2026/08/vit-paper/精读笔记/README.md)） |
| 1 | **DeiT**：Training Data-Efficient Image Transformers & Distillation | ICML 2021 | 知识蒸馏 token，**只在 ImageNet 上**就把 ViT 教明白 | ✅ 已读（[笔记](./2026/08/deit-paper/精读笔记/README.md)） |
| 2 | **ConvNeXt**：A ConvNet for the 2020s | CVPR 2022 | 对照组：拿 ViT 的训练配方武装 CNN，"现代 CNN"的反击 | ✅ 已读（[笔记](./2026/08/convnext-paper/精读笔记/README.md)） |

### 主线 B：架构演进（从分类到通用骨干网）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 3 | **Swin**：Hierarchical Vision Transformer using Shifted Windows | ICCV 2021 | 窗口注意力 + 层次结构，ViT 变成通用骨干网 | ✅ 已读（[笔记](./2026/08/swin-paper/精读笔记/README.md)） |
| 4 | **DETR**：End-to-End Object Detection with Transformers | ECCV 2020 | 去掉 anchor/NMS，集合预测做检测 | ✅ 已读（[笔记](./2026/08/detr-paper/精读笔记/README.md)） |

### 主线 C：自监督（ViT §4.6 埋下的种子）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 5 | **MAE**：Masked Autoencoders Are Scalable Vision Learners | CVPR 2022 | 遮 75% 的 patch 重建像素，75% 算力省出来的自监督 | ✅ 已读（[笔记](./2026/08/mae/精读笔记/README.md)） |

### 主线 D：行为诊断与修正（CLS token 在搞什么名堂）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 6 | **Registers**：Vision Transformers Need Registers | ICLR 2024 | 大而且训练充分的 ViT 会把少数低信息 patch token 复用为高范数全局计算载体，牺牲局部空间信息；加入专用 register token 可隔离该行为 | ✅ 已读（[笔记](./2026/08/registers/精读笔记/README.md)） |
| 7 | **LAST-ViT**：Vision Transformers Need More Than Registers | CVPR 2026 | 上一问的续作：artifact 的根源是"懒惰聚合"——ViT 拿无关背景 patch 当全局语义的捷径；用频域 token 选择替代标准 CLS token，三种监督范式下 12 个 benchmark 全面提升 | ✅ 已读（[笔记](./2026/08/last-vit/精读笔记/README.md)） |

> 🕳️ 先记在"未来再说"坑里的：BEiT（遮块预测离散 token）、Segmentation Transformer 系（SETR 等）、Scaling Law 系（ViT-22B 等）、多模态系（CLIP 等）。其中 BEiT、ViT-22B、CLIP 系已于 2026-08-12 纳入《[ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)》统一登记；核心八篇读完后按该图继续拓展。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| [2026/08/registers](./2026/08/registers/精读笔记/README.md) | Registers | 大而且训练充分的 ViT 会把少数输入冗余 patch 从局部空间表示复用为高范数全局计算载体（DINOv2-g 示例约 2.37%）；4 个无空间位置、无直接输出监督的 register token 以低于 2% FLOPs 隔离该行为，high-norm 与全局分类能力从 patch 迁移到 registers，DINOv2 LOST VOC07 `35.3→55.4`，但 OpenCLIP LOST 反而下降且训练根因未明 |
| [2026/08/vit-paper](./2026/08/vit-paper/精读笔记/README.md) | ViT | 大规模训练战胜归纳偏置；纯 Transformer 可行且算力效率高 |
| [2026/08/deit-paper](./2026/08/deit-paper/精读笔记/README.md) | DeiT | 架构不变，靠 CNN 时代配方（强增强）+ 蒸馏 token 借归纳偏置，单机 ImageNet 训出 85.2% |
| [2026/08/convnext-paper](./2026/08/convnext-paper/精读笔记/README.md) | ConvNeXt | 零注意力逐步翻新 ResNet（配方 +2.7、减法设计、7×7 即饱和），纯 ConvNet 反超 Swin：性能差距的大头在配方与设计，不在注意力 |
| [2026/08/swin-paper](./2026/08/swin-paper/精读笔记/README.md) | Swin | 窗口内局部注意力（线性复杂度）+ patch merging 层级化 + 移位窗口保流通，ViT 变成检测/分割通吃的通用骨干网；任务越密集优势越大（分割 +5.3 mIoU），组织方案输出给 all-MLP 也赢 |
| [2026/08/detr-paper](./2026/08/detr-paper/精读笔记/README.md) | DETR | 检测 = 直接集合预测：N=100 个可学习 object queries 并行输出 + 匈牙利一对一匹配损失，去 anchor/NMS 首次端到端打平加强版 Faster R-CNN（42.0 AP，大目标 +7.8、小目标 -5.5）；全景分割 PQ 登顶；留下收敛慢（500 epoch）与小目标两大痛点待后续攻克 |
| [2026/08/mae](./2026/08/mae/精读笔记/README.md) | MAE | 非对称 encoder-decoder（encoder 只看 25% 可见 patch、无 mask token；decoder 轻量训后即弃）+ 75% 高掩码比例，"遮块重建像素"同时兑现精度与效率（加速 3×+）；vanilla ViT-Huge 仅 IN1K 无标签达 87.8%，检测/分割/分类迁移全面超越监督预训练且随规模持续涨点 |
| [2026/08/last-vit](./2026/08/last-vit/精读笔记/README.md) | LAST-ViT | artifact 的根源是"懒惰聚合"（粗粒度监督 + 全局注意力 → 背景 patch 走捷径编码全局语义）；LazyStrike 用通道维频域稳定度筛选 patch、逐通道 Top-K 构造 CLS token，预训练期介入零架构改动，三种监督范式下 PiB 大幅修复（ViT +12.4 / DINO +25.2 / CLIP +10.3）、12 个 benchmark 一致提升（CLIP L/14 VOC 分割 17.1→72.4），顺带消除 high-norm 现象 |

---

## 🔑 各篇之间的因果链（为什么按这个顺序读）

1. **ViT** 证明纯 Transformer 可行，但留下最大短板：**要 JFT-300M 这种私有大数据**，普通人用不起。
2. **DeiT** 正面回答这个短板：用蒸馏 + 强数据增强，**只用公开 ImageNet** 就训出能打的 ViT —— 民主化。
3. **ConvNeXt** 是精彩的对照组：ViT 赢了，到底是"注意力机制"赢了，还是"训练配方"赢了？ConvNeXt 证明配方本身价值连城。主线 A 至此闭环：**数据民主化（DeiT）与归因澄清（ConvNeXt）双双完成**，下一篇回到主线 B 的 Swin。
4. **Swin** 回答另一个短板：ViT 的全局注意力又贵又只能做分类；Swin 用窗口+层次让它**便宜且能接检测/分割**。
5. **DETR** 展示 Transformer 改写检测任务本身（集合预测），与 Swin 骨干网结合就是今天的检测主流。读完确认：端到端的代价（500 epoch 收敛、小目标弱）被论文自己列成清单，后续 Deformable DETR 系工作逐一攻克——详见拓展阅读路线图。
6. **MAE** 回到 ViT §4.6 那个 79.9% 的初步实验，把"遮块重建"做成可扩展的自监督范式，闭环。读完确认：75% 掩码比例同时兑现任务难度与训练效率（encoder 只算 25% patch，加速 3×+）；迁移学习全面超越监督预训练且随模型规模持续涨点，视觉自监督自此走上 NLP 式 scaling 轨迹；"像素重建逼出语义表示"的机理问题留给主线 D 的表示行为研究。
7. **Registers** 提出主线 D 的起点问题：大规模预训练 ViT 的 patch token 是否仍可靠保留局部空间语义？论文发现，大而且训练充分的模型会优先挑中输入冗余的 patch，把它们从局部表示复用为高范数全局计算载体；位置/像素 probing 下降而整图分类 probing 大幅上升。加入若干不对应图像位置的 register token 后，高范数与全局分类能力转移到 registers，普通 patch 的局部信息基本不变，特征图与部分密集任务改善。这篇完成"发现症状 → 功能诊断 → 隔离修复"，但明确没有确定训练根因。
8. **LAST-ViT** 顺着 Registers 继续追问：register 只是把症状压住，**毛病的根源是什么**？答案是"懒惰聚合"——在全局注意力 + 粗粒度语义监督（一张图一个标签）下，ViT 学会了走捷径：把语义无关的背景 patch 当成表示全局语义的跳板，CLS token 因此被背景污染。解法是用频域 token 选择替代标准 CLS token，只让语义相关的 patch 参与全局聚合；标签、文本、自监督三种范式下 12 个 benchmark 一致提升。主线 D 至此完成"发现症状（Registers）→ 解释病因并对症修正（LAST-ViT）"的闭环。
