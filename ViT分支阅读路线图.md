# ViT 分支阅读路线图

> 以 **Vision Transformer（ViT, ICLR 2021）** 为根的一条大分支：从"纯 Transformer 进入视觉"出发，沿三条主线把这条脉络读完。
> 本文档随精读进度维护：读完一篇就在状态列打勾，并在下方"精读记录"补一行链接。
> **下游拓展**：核心六篇之外的 ViT 家族后续演进（2022–2026）统一登记在《[ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)》，主线六篇读完后按该图继续。

---

## 🧭 三条主线

```
                          ViT (2021.01, ICLR 2021) ✅ 已读
                                │
        ┌───────────────────────┼───────────────────────────┐
        ▼                       ▼                           ▼
  主线A：效率/数据民主化      主线B：架构演进              主线C：自监督
  （"没大数据也能用"）       （"怎么适配各种视觉任务"）    （"不靠标签预训练"）
        │                       │                           │
      DeiT (2020.12)          Swin (2021.03)              MAE (2021.11)
        │                       │
   ConvNeXt (2022.01)      DETR (2020.05)*
   （对照组：CNN 反击）     （下游任务：检测）
```

\* DETR 发表于 ViT 之前，但它是 Transformer 进视觉检测的开路者，读 Swin 后接它正好。

---

## 📋 阅读清单

### 主线 A：效率与数据民主化（ViT 最大短板的补全）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 0 | **ViT**：An Image is Worth 16×16 Words | ICLR 2021 | 纯 Transformer 做视觉；大数据战胜归纳偏置 | ✅ 已读（[笔记](./2026/08/vit-paper/精读笔记/README.md)） |
| 1 | **DeiT**：Training Data-Efficient Image Transformers & Distillation | ICML 2021 | 知识蒸馏 token，**只在 ImageNet 上**就把 ViT 教明白 | ✅ 已读（[笔记](./2026/08/deit-paper/精读笔记/README.md)） |
| 2 | **ConvNeXt**：A ConvNet for the 2020s | CVPR 2022 | 对照组：拿 ViT 的训练配方武装 CNN，"现代 CNN"的反击 | ⏳ 待读 |

### 主线 B：架构演进（从分类到通用骨干网）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 3 | **Swin**：Hierarchical Vision Transformer using Shifted Windows | ICCV 2021 | 窗口注意力 + 层次结构，ViT 变成通用骨干网 | ⏳ 待读 |
| 4 | **DETR**：End-to-End Object Detection with Transformers | ECCV 2020 | 去掉 anchor/NMS，集合预测做检测 | ⏳ 待读 |

### 主线 C：自监督（ViT §4.6 埋下的种子）

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 5 | **MAE**：Masked Autoencoders Are Scalable Vision Learners | CVPR 2022 | 遮 75% 的 patch 重建像素，75% 算力省出来的自监督 | ⏳ 待读 |

> 🕳️ 先记在"未来再说"坑里的：BEiT（遮块预测离散 token）、Segmentation Transformer 系（SETR 等）、Scaling Law 系（ViT-22B 等）、多模态系（CLIP 等）。其中 BEiT、ViT-22B、CLIP 系已于 2026-08-12 纳入《[ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)》统一登记；这条主线六篇读完后按该图继续拓展。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| [2026/08/vit-paper](./2026/08/vit-paper/精读笔记/README.md) | ViT | 大规模训练战胜归纳偏置；纯 Transformer 可行且算力效率高 |
| [2026/08/deit-paper](./2026/08/deit-paper/精读笔记/README.md) | DeiT | 架构不变，靠 CNN 时代配方（强增强）+ 蒸馏 token 借归纳偏置，单机 ImageNet 训出 85.2% |

---

## 🔑 各篇之间的因果链（为什么按这个顺序读）

1. **ViT** 证明纯 Transformer 可行，但留下最大短板：**要 JFT-300M 这种私有大数据**，普通人用不起。
2. **DeiT** 正面回答这个短板：用蒸馏 + 强数据增强，**只用公开 ImageNet** 就训出能打的 ViT —— 民主化。
3. **ConvNeXt** 是精彩的对照组：ViT 赢了，到底是"注意力机制"赢了，还是"训练配方"赢了？ConvNeXt 证明配方本身价值连城。
4. **Swin** 回答另一个短板：ViT 的全局注意力又贵又只能做分类；Swin 用窗口+层次让它**便宜且能接检测/分割**。
5. **DETR** 展示 Transformer 改写检测任务本身（集合预测），与 Swin 骨干网结合就是今天的检测主流。
6. **MAE** 回到 ViT §4.6 那个 79.9% 的初步实验，把"遮块重建"做成可扩展的自监督范式，闭环。
