# DeiT 精读笔记索引

> 论文：**Training Data-Efficient Image Transformers & Distillation through Attention**
> Touvron et al., Facebook AI, ICML 2021 · arXiv:2012.12877
>
> 原稿 PDF：`../DeiT_2012.12877.pdf`（22 页，含附录）
> 全文文本：`../DeiT_fulltext.txt`
>
> 在 ViT 分支中的位置：**第 2 篇**。ViT 说"没大数据不行"，DeiT 说"那是配方问题"。

## 📖 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 第 1 站 | [01_摘要与引言.md](./01_摘要与引言.md) | 动机（ViT 的大数据门槛）、四大贡献、蒸馏 token 预告 | ✅ 已完成 |
| 第 2 站 | 02_方法_ViT回顾与蒸馏token.md | §3 ViT 回顾（含 class token 洞察）、§4 蒸馏三种姿势 + 蒸馏 token | ⏳ 待续 |
| 第 3 站 | 03_实验_蒸馏分析与SOTA对比.md | 教师选择（CNN > Transformer）、蒸馏方法对比、Table 5 主表、迁移学习 | ⏳ 待续 |
| 第 4 站 | 04_训练配方与消融_结论.md | §6 训练细节大消融（Table 8/9）、与 ViT 训练配方逐项对比、结论 | ⏳ 待续 |

## 🌟 全文一句话

> **架构一个字不改（DeiT-B ≡ ViT-B），靠 CNN 时代攒下的训练秘方 + 一个蒸馏 token，只用公开 ImageNet、单机 8 卡训 3 天，就能把 Vision Transformer 训到和顶级 CNN 掰手腕（85.2%）。**
