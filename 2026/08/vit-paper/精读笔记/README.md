# ViT 精读笔记索引

> 论文：**An Image is Worth 16×16 Words: Transformers for Image Recognition at Scale**
> Dosovitskiy et al., Google Brain, ICLR 2021 · arXiv:2010.11929
>
> 原稿 PDF：`../ViT_2010.11929.pdf`（22 页，含附录）
> 全文文本：`../ViT_fulltext.txt`

## 📖 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 第 1 站 | [01_摘要与引言.md](./01_摘要与引言.md) | 论文动机、核心主张、inductive bias 论点 | ✅ 已完成 |
| 第 2 站 | [02_方法_ViT是怎么造出来的.md](./02_方法_ViT是怎么造出来的.md) | 切 patch、线性投影、[class] token、位置编码、4 个核心公式、微调技巧 | ✅ 已完成 |
| 第 3 站 | [03_实验_数据对比与scaling.md](./03_实验_数据对比与scaling.md) | 实验设置、数据集规模、主结果表、scaling 规律 | ✅ 已完成 |
| 第 4 站 | [04_分析与讨论.md](./04_分析与讨论.md) | 注意力可视化、位置编码学到啥、自监督、附录精华 | ✅ 已完成 |

## 🌟 全文一句话

> **大规模训练，能够战胜归纳偏置。**
> （只要数据够多，一张白纸——无归纳偏置的 Transformer——能画出让 CNN 都羡慕的图画。）
