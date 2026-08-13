# Swin 精读笔记索引

> 论文：**Swin Transformer: Hierarchical Vision Transformer using Shifted Windows**
> Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, Baining Guo（Microsoft Research Asia），ICCV 2021（Marr Prize）· arXiv:2103.14030
>
> 原稿 PDF：`../Swin_2103.14030.pdf`
> 全文文本：`../Swin_fulltext.txt`
> 图片：`../figures/`（Figure 1–4 整页渲染 + 抽出的位图；按仓库规则 7 选择性查阅）
>
> 在 ViT 分支中的位置：**主线 B（架构演进：从分类到通用骨干网）第 1 站**——ViT / DeiT / ConvNeXt 之后，回答"ViT 怎么从分类样板间变成检测/分割都能接的通用骨干网"。
>
> 讲解约定：全篇统一使用"**公司组织改革**"锚点（ViT 全局注意力 = 董事长一言堂；窗口 = 部门；移位 = 重划部门；patch merging = 晋升设管理层）；关键原文按 **英文原文 → 直译 → 解读** 三层展开。

## 📖 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 第 1 站 | [01_摘要与引言.md](./01_摘要与引言.md) | 立题（两道坎：尺度差异与高分辨率）、三件法宝的摘要预告、引言逐句精读、锚点声明 | ✅ 已完成 |
| 第 2 站 | [02_方法.md](./02_方法.md) | §2 相关工作四派点评 + §3 方法：四级架构与 patch merging、复杂度公式 (1)(2)、移位实现（循环移位+掩码）、相对位置偏置、T/S/B/L 变体 | ✅ 已完成 |
| 第 3 站 | [03_实验与消融.md](./03_实验与消融.md) | §4：ImageNet（1K/22K）+ COCO 四框架横扫与 SOTA + ADE20K + 消融（移位 +1.1/+2.8/+2.8、相对偏置、Table 5/6 延迟判决） | ✅ 已完成 |
| 第 4 站 | [04_结论与附录精华.md](./04_结论与附录精华.md) | §5 结论 + 附录精华（stage 4 恰为全员大会、GAP 替代 class token、给 CNN 对手换 AdamW、Swin-Mixer 输出组织方案） | ✅ 已完成 |

## 🌟 全文一句话

> **把 ViT 的"董事长一言堂"改造成层级制公司——注意力只在部门内开（线性复杂度）、逐级设管理层（层次化特征图）、每轮会议后重划部门（移位窗口保流通）——Swin 由此成为分类/检测/分割通吃的通用骨干网，在 COCO 与 ADE20K 同时刷新 SOTA，并证明真正值钱的是窗口的组织方式而非注意力本身。**
