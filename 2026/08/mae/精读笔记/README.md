# MAE 精读笔记

> 论文：**Masked Autoencoders Are Scalable Vision Learners**
> Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, Ross Girshick（Facebook AI Research）
> CVPR 2022 · arXiv:2111.06377 · 代码：https://github.com/facebookresearch/mae

- 原稿：`../MAE_2111.06377.pdf`（arXiv v3，14 页正文+附录）
- 全文文本：`../MAE_fulltext.txt`（pdftotext 提取，816 行）
- 图片：`../figures/`（Figure 1/5/6/7/8/9 按整页渲染为 PNG，按仓库规则 7 选择性查阅）

## 在 ViT 分支中的位置

**主线 C（自监督）第 1 站**。回到 ViT 论文 §4.6 那个"遮块自监督预训练达到 79.9%"的初步实验，把"遮块重建"做成可扩展的自监督范式：非对称 encoder-decoder + 75% 高掩码比例，让数据饥饿的大模型仅用公开 IN1K 无标签数据即可吃饱。主线 A 的 DeiT 在监督设定下做"数据民主化"，本篇在自监督路线上直接绕开标签——两条路线合起来回答了 ViT 留下的"数据依赖"根问题。

## 讲解约定

关键原文按 **英文原文 → 直译（忠实原义）→ 解读** 呈现；全文使用直白的技术剖析语言，不使用隐喻与类比。

## 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | [01_摘要与引言.md](./01_摘要与引言.md) | 核心主张（可扩展的自监督学习者）、两个核心设计、"视觉掩码自编码为何落后于 NLP"的三视角分析（架构差/信息密度差/decoder 角色差） | ✅ |
| 2 | [02_方法.md](./02_方法.md) | 掩码采样（均匀不放回随机）、encoder（标准 ViT 只看 25% 可见 patch、无 mask token）、轻量 decoder（mask token + 位置嵌入）、像素重建目标（MSE、只算被遮 patch、per-patch 归一化变体）、shuffle 无稀疏算子实现 | ✅ |
| 3 | [03_实验与消融.md](./03_实验与消融.md) | 掩码比例 75% 甜点位（Fig 5）、decoder 深宽消融、mask token 消融（lin -14% / 加速 3.7×）、重建目标与增广（零增广仍可用）、采样策略（重建锐利 ≠ 表示好）、1600 epoch 未饱和、Table 3 对比（ViT-H448 87.8%）、部分微调与 linear probing 的分裂 | ✅ |
| 4 | [04_迁移学习与结论.md](./04_迁移学习与结论.md) | COCO/ADE20K/iNat/Places 全面超越监督预训练、pixels vs tokens 终局判决（统计相似）、结论（"视觉自监督踏上 NLP 轨迹"）与诚实边界、附录精华（复现配方、ViT 检测骨干改造、鲁棒性 Table 13） | ✅ |

## 全文一句话总结

**MAE 用两个互为条件的设计——非对称 encoder-decoder（encoder 只处理可见 patch、decoder 轻量且训后即弃）与 75% 高掩码比例——把"遮随机 patch、重建像素"变成同时兑现精度与效率（加速 3× 以上）的自监督预训练范式，让 vanilla ViT-Huge 仅用 ImageNet-1K 无标签数据达到 87.8%，并在检测、分割、分类迁移上全面超越监督预训练且随规模持续涨点：视觉自监督由此踏上 NLP 式 scaling 轨迹，"像素重建逼出语义表示"的机理问题则留给了后续表示行为研究。**
