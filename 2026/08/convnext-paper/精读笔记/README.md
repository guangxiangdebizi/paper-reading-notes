# ConvNeXt 精读笔记索引

> 论文：**A ConvNet for the 2020s**
> Zhuang Liu, Hanzi Mao, Chao-Yuan Wu, Christoph Feichtenhofer, Trevor Darrell, Saining Xie（FAIR + UC Berkeley），CVPR 2022 · arXiv:2201.03545
>
> 原稿 PDF：`../ConvNeXt_2201.03545.pdf`（15 页）
> 全文文本：`../ConvNeXt_fulltext.txt`
> 图片：`../figures/`（Figure 1–4 整页渲染，含翻新轨迹图 fig2、块结构对比图 fig4）
>
> 在 ViT 分支中的位置：**主线 A（效率/数据民主化）第 3 站**——ViT、DeiT 之后的"对照组"（CNN 的反击）。
>
> 讲解约定：全篇统一使用"**老房翻新**"锚点（ResNet = 老房子，Swin = 新豪宅，注意力 = 电梯，训练配方 = 施工工艺）；每处原文按 **英文原文 → 直译 → 隐喻解读** 三层展开。

## 📖 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 第 1 站 | [01_摘要与引言.md](./01_摘要与引言.md) | 归因问题（混杂变量）、"现代化"方法论、锚点声明、摘要与引言逐句精读、训练配方第一笔涨分 | ✅ 已完成 |
| 第 2 站 | [02_现代化路线图.md](./02_现代化路线图.md) | §2：训练配方 → 宏观设计（stage ratio、patchify stem）→ ResNeXt-ify → 倒瓶颈 → 大卷积核 → 微观设计，每步动机与涨分 | ✅ 已完成 |
| 第 3 站 | [03_实验与消融.md](./03_实验与消融.md) | §3–4：ConvNeXt 家族列装（T/S/B/L/XL）、ImageNet-1K/22K 全档位对 Swin、同构 ConvNeXt vs ViT、COCO/ADE20K 下游验证 | ✅ 已完成 |
| 第 4 站 | [04_结论与附录精华.md](./04_结论与附录精华.md) | §5–6 结论与相关工作 + 附录精华（EMA 与 BN 冲突、鲁棒性裸考、大档位轨迹、A100 吞吐 +46~49%、局限性边界） | ✅ 已完成 |

## 🌟 全文一句话

> **不给老房子装"注意力"这部电梯，只用 Transformer 时代的训练配方与设计理念逐项翻新 ResNet——得到的纯 ConvNet（ConvNeXt）在精度上反超 Swin，证明 ViT 与 CNN 的性能差距里，配方与设计占了大头，注意力并非唯一解释。**
