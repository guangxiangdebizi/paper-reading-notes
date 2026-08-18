# LAST-ViT 精读笔记

> 论文：**Vision Transformers Need More Than Registers**
> Cheng Shi, Yizhou Yu（香港大学计算与数据科学学院），Sibei Yang（中山大学）
> CVPR 2026 · arXiv:2602.22394v2（2026-04-14）· 代码：https://github.com/ChengShiest/LAST-ViT

- 原稿：`../LAST-ViT_2602.22394.pdf`（arXiv v2，正文 8 页 + 参考文献 2 页，无附录）
- 全文文本：`../LAST-ViT_fulltext.txt`（pdftotext -layout 提取，597 行）
- 图片：`../figures/page_1.png` ~ `page_10.png`（pymupdf 按页渲染，110 dpi）

## 在 ViT 分支中的位置

**主线 D（行为诊断与修正）第 2 站、Registers 的直接续作**。Registers（ICLR 2024）发现大规模预训练 ViT 的 patch 特征图中存在 artifact 高响应区，模型把少数高范数 token 当作注意力的"垃圾桶"，加入可学习的 register token 即可缓解症状。本篇继续追问：**症状压住之后，毛病的根源是什么？** 答案是"懒惰聚合"（lazy aggregation）——在全局注意力 + 粗粒度语义监督（一张图一个标签）的共同驱动下，ViT 学会走捷径：把语义无关的背景 patch 当作表示全局语义的载体，CLS token 因此被背景污染，得到"高分类精度 + 差 patch 级对齐"的分裂表现。解法 LazyStrike 用频域感知的选择性聚合替代标准 CLS token 池化，只让最稳定的 patch 参与全局聚合；标签、文本、自监督三种范式下 12 个 benchmark 一致提升，并顺带消除 high-norm 现象。主线 D 至此完成"发现症状（Registers）→ 解释病因并对症修正（LAST-ViT）"的闭环。

## 讲解约定

关键原文按 **英文原文 → 直译（忠实原义）→ 解读** 呈现；全文使用直白的技术剖析语言，不使用隐喻与类比。

## 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | [01_摘要与引言.md](./01_摘要与引言.md) | 问题定性（三种监督范式下的 artifact 是同一根源）、统一度量 Patch Score 与 Point-in-Box（PiB）的提出、"懒惰聚合"假设的两因素表述、四条贡献、相关工作定位（CLIP 系三类既有解法 vs 本文预训练期介入；DINO 系 Registers 只是症状缓解） | ✅ |
| 2 | [02_分析与假设.md](./02_分析与假设.md) | Patch Score（Eq.3）与 PiB 的正式定义；Table 1（ViT 各范式 PiB 全面低于 ResNet、加 Register 不改善）；Fig 2（前景集中在低分区、背景主导高分尾部；移除 70% 高分 patch 不伤精度）；Fig 3（PiB 训练全程平坦且恒低于 ResNet、早期即出现背景偏向）；两因素验证——粗粒度监督（patch 16→28，PiB 0.44→0.52，top-1 62%→55%）与全局依赖（窗口注意力逐层替换，Table 2） | ✅ |
| 3 | [03_方法_LazyStrike.md](./03_方法_LazyStrike.md) | 频域感知选择性聚合：通道维 1D FFT + 归一化高斯低通（Eq.4）、稳定度分数（Eq.5）、逐通道 Top-K 池化构造 CLS（Eq.6-7）、vote count（Eq.8）；Fig 5 高票 patch 对齐前景；无需架构改动、无后训练、无测试期干预；Fig 6 顺带消除 high-norm 现象 | ✅ |
| 4 | [04_实验与结论.md](./04_实验与结论.md) | Table 3（PiB：ViT +12.4、DINO-v1 +25.2、CLIP +10.3，逼近 ResNet）；Table 4（六个语义分割基准，CLIP/MetaCLIP/EVACLIP × B/L 全部提升，CLIP L/14 VOC 17.1→72.4）；Table 5（OV 检测/分割，novel 类 +15.8/+14.4）；Table 6（粗分割涌现：监督 ViT 也涌现、接近 DINO）；Table 7（CorLoc 超 LOST 且 55.9 FPS）；Tables 8-9（K 消融：选一半 token 最优；Max-Pool 对照）；结论与局限 | ✅ |

## 全文一句话总结

**LAST-ViT 用 Patch Score（patch 与 CLS token 的余弦相似度）与 Point-in-Box（最高分 patch 是否落在前景框内）两个统一度量，系统证明 ViT 在三种监督范式下共有的 artifact 源于同一种"懒惰聚合"行为——全局注意力叠加图像级粗粒度监督，使模型把语义无关的背景 patch 当作编码全局语义的捷径（移除 70% 高分背景 patch 不伤分类精度、背景偏向从训练初期即出现并贯穿全程），并以两个受控实验分别验证粗粒度监督与全局依赖各自的贡献；据此提出 LazyStrike——对 patch 特征做通道维一维傅里叶低通滤波、以滤波前后比值作稳定度分数、逐通道取 Top-K 最稳定 patch 平均生成 CLS token——在预训练期介入、零架构改动，使 CLS token 重新锚定前景区域，在标签/文本/自监督三种范式的 12 个 benchmark（PiB、六个语义分割、开放词汇检测与实例分割、粗分割、无监督目标发现、K 消融）上一致提升，同时消除 high-norm 现象：Vision Transformer 需要的不只是 Registers（症状缓解），而是对聚合行为本身的修正。**
