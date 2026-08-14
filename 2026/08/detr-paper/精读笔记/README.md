# DETR 精读笔记

> 论文：**End-to-End Object Detection with Transformers**（DETR）
> Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko（Facebook AI Research）
> ECCV 2020 · arXiv:2005.12872 · 代码：https://github.com/facebookresearch/detr

- 原稿：`../DETR_2005.12872.pdf`（arXiv v3，26 页）
- 全文文本：`../DETR_fulltext.txt`（pdftotext 提取，1367 行）
- 图片：`../figures/`（Figure 1–9 按整页渲染为 PNG，按仓库规则 7 选择性查阅）

## 在 ViT 分支中的位置

**主线 B（架构演进）第 2 站**。前序：Swin 解决了"ViT 怎么变成通用骨干网"；本篇回答"Transformer 怎么把检测任务本身改写掉"——去掉 anchor 与 NMS，用集合预测直接输出检测结果。Swin 骨干网 + DETR 式设计，即今天检测领域的主流形态。

## 讲解约定

全篇统一使用"**通讯社改组**"锚点：传统检测器 = 人海蹲点 + 事后筛重稿（anchor + NMS）的旧式通讯社；DETR = 固定编制 100 名在编记者（object queries）并行交稿，记者碰头会（decoder 自注意力）从源头消灭撞稿，总编一对一派稿（匈牙利匹配），筛稿工序（NMS）直接裁撤。锚点映射表见 [01 站第〇节](./01_摘要与引言.md)。

## 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | [01_摘要与引言.md](./01_摘要与引言.md) | 核心主张（检测 = 直接集合预测）、要拆掉的手工组件、与前人直接集合预测工作的差异（非自回归并行解码）、对 Faster R-CNN 的胜负预告 | ✅ |
| 2 | [02_方法_集合损失与架构拆解.md](./02_方法_集合损失与架构拆解.md) | 匈牙利匹配与匹配代价（公式 (1)）、匈牙利损失（公式 (2)）、∅ 类降权、GIoU+ℓ1 框损失；架构三件套：backbone / encoder / object queries decoder / 共享 FFN 与辅助解码损失 | ✅ |
| 3 | [03_实验与消融.md](./03_实验与消融.md) | Table 1 对加强版 Faster R-CNN 的打平（APL +7.8 / APS -5.5）、encoder/decoder 层数消融（NMS 探针实验）、FFN 与位置编码消融（Table 3）、损失消融（Table 4）、槽位特化与长颈鹿泛化 | ✅ |
| 4 | [04_拓展与结论.md](./04_拓展与结论.md) | 全景分割 mask head 与 Table 5（PQ 45.1 登顶、stuff 最强）、结论的功绩/痛点清单、附录精华：复杂度公式、超参清单、实例数压力测试、36 行 PyTorch 推理代码 | ✅ |

## 全文一句话总结

**DETR 把目标检测从"海量候选 + 手工规则（anchor、正负样本指派、NMS）"改写为"固定 N 个可学习 object queries 一次并行输出集合 + 匈牙利一对一匹配损失"，首次以真正端到端的方式在 COCO 上与被反复调优的 Faster R-CNN 打平（42.0 AP），大目标显著更强（APL +7.8）、小目标暂弱（APS -5.5）、训练慢（500 epoch）的代价换来了极简实现（推理 36 行 PyTorch）与统一的下游拓展（全景分割 PQ 登顶）——由此开启"Transformer 改写检测任务本身"的路线，其留下的痛点清单（收敛慢、小目标弱）被 Deformable DETR 等后续工作逐一攻克。**
