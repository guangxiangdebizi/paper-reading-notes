# Registers 精读笔记

> 论文：**Vision Transformers Need Registers**  
> Timothée Darcet, Maxime Oquab, Julien Mairal, Piotr Bojanowski（FAIR / Inria）  
> ICLR 2024 · arXiv:2309.16588v2（2024-04-12）· 代码与模型：https://github.com/facebookresearch/dinov2

- 原稿：`../Vision_Transformers_Need_Registers_2309.16588.pdf`（arXiv v2，21 页，含附录）
- 全文文本：`../Vision_Transformers_Need_Registers_fulltext.txt`（PyMuPDF 提取）
- 图片：`../figures/`（Fig. 1–21 所需页面选择性渲染，110 dpi）

## 在 ViT 分支中的位置

**主线 D（行为诊断与修正）第 1 站**。前面的 ViT、DeiT、Swin、MAE 主要回答模型如何训练、扩展和迁移；本篇开始检查大规模预训练 ViT 的内部表示是否仍保留可靠的空间语义。论文从一个反常现象出发：DINOv2 的冻结特征在分割和深度估计上很强，却让依赖平滑局部特征的无监督目标发现方法 LOST 明显退化。作者发现，大而且训练充分的 ViT 会把少量低信息 patch token 改作内部全局计算空间，导致其范数异常升高、局部信息丢失，并在特征图和注意力图上形成 artifact。解决办法是在输入序列中显式加入若干可学习 register token，让模型把这种计算行为迁移到不对应图像位置的专用 token 上。

下一篇 LAST-ViT 将继续追问：Registers 虽然隔离了 high-norm 行为，是否真正解释并消除了背景 patch 承载全局语义的根因？

## 讲解约定

关键原文按 **英文原文 → 直译 → 解读** 呈现；把论文已经验证的观察、作者的机制解释和我们据后续工作作出的判断分开。

## 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | [01_摘要与引言_问题是怎么发现的.md](./01_摘要与引言_问题是怎么发现的.md) | DINO → DINOv2 的反常退化；artifact 的操作性定义；约 10× 范数、约 2% token；“垃圾 token”说法的准确修正；论文的假设—证据—干预链 | ✅ |
| 2 | [02_诊断_high-norm_token里有什么.md](./02_诊断_high-norm_token里有什么.md) | Fig. 3–5 与 Table 1：出现层数、训练时刻、模型规模；邻域冗余；位置预测/像素重建；全局分类 probing；为什么称为被复用的内部寄存器 | ✅ |
| 3 | [03_方法_register_token.md](./03_方法_register_token.md) | register token 的插入与丢弃；与 CLS / memory token / object query 的区别；1/2/4/8/16 个 token 消融；计算开销；register 是否真的接走原行为 | ✅ |
| 4 | [04_实验_边界与LAST-ViT.md](./04_实验_边界与LAST-ViT.md) | DeiT-III / OpenCLIP / DINOv2 三范式实验；分类、分割、深度与 LOST；反例和边界（DINO、MAE、OpenCLIP value null space、位置插值 artifact）；与 LAST-ViT 的结论边界 | ✅ |

## 全文一句话总结

**大而且训练充分的 ViT 会识别出约 2% 的低信息 patch，将这些本应保留局部空间语义的 token 改作全局内部计算空间，表现为约 10 倍范数离群、局部信息丢失而全局分类信息增强；在 patch 序列中加入 4 个可学习、无输入内容且输出时丢弃的 register token，可用低于 2% 的额外 FLOPs 把这种行为从 patch token 中隔离出去，使特征图更平滑并改善密集预测和无监督目标发现，但该论文尚未确定 artifact 的训练根因。**
