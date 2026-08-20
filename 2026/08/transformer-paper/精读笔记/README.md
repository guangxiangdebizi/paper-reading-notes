# Transformer 精读笔记

> 论文：**Attention Is All You Need**（Transformer）
> Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin（Google Brain / Google Research / University of Toronto）
> NIPS 2017 · arXiv:1706.03762（v7，2023-08-02）· 代码：https://github.com/tensorflow/tensor2tensor

- 原稿：`../Transformer_1706.03762.pdf`（15 页，含附录 attention 可视化）
- 全文文本：`../Transformer_fulltext.txt`（pdftotext 提取，521 行）
- 图片：`../figures/`（Figure 1–5 与 Table 1–4 所在页整页渲染为 PNG，按仓库规则 7 选择性查阅）

## 在精读体系中的位置

**《经典地基阅读路线图》正式清单第 1 篇，经晋升后的四站精读**。仓库内 8 篇精读笔记（ViT / DeiT / RAFT / ConvNeXt / Swin / DETR / MAE / LAST-ViT）全部把 encoder/decoder 架构、self-attention 的 QKV 公式、multi-head、正弦位置编码当作已知前提直接使用、行文一律"贴着原版 Transformer"——而原版自身从未被精读，构成最大的地基缺口，故按晋升规则（多次造成卡点）升级为四站精读。

## 讲解约定

关键原文按 **英文原文 → 直译（忠实原义）→ 解读** 呈现；全文使用直白的技术剖析语言，不使用隐喻与类比。

## 精读路线

| 站次 | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | [01_摘要与引言.md](./01_摘要与引言.md) | 摘要逐句（三个实验主张、两个 BLEU 数字、泛化预告）、作者贡献脚注（各组件发明权）、引言论证链（RNN 串行瓶颈 → attention 只是配件 → 只用 attention） | ✅ |
| 2 | [02_背景与模型架构.md](./02_背景与模型架构.md) | §2 前人路线对比；§3 架构全解：encoder/decoder 定义、Figure 1 读图、N=6 层与残差+LayerNorm、缩放点积注意力（公式 (1) 与 √d_k 的方差论证）、多头（公式 (2) 与分辨率补偿）、注意力三用法（QKV 来源对照表）、position-wise FFN（公式 (3)）、embedding 三处共享与 √d_model 缩放、正弦位置编码（几何级数波长、相对位置线性可表示、长度外推）；§4 三条标准与 Table 1（复杂度/串行步数/路径长度对照） | ✅ |
| 3 | [03_训练设置与实验结果.md](./03_训练设置与实验结果.md) | §5 训练：BPE 词表与按 token 定 batch、8×P100 时长（base 12 小时/big 3.5 天）、Adam+warmup 学习率调度（公式 (3)）、残差 dropout 与 label smoothing（牺牲困惑度换 BLEU）；§6.1 Table 2（base 超所有集成、big 双登顶、训练成本低一到两个数量级）、checkpoint 平均与 beam search；§6.2 Table 3 五行消融（多头必要性、d_k、scale、dropout、位置编码可替换） | ✅ |
| 4 | [04_泛化实验_结论与附录精华.md](./04_泛化实验_结论与附录精华.md) | §6.3 成分句法分析（Table 4，半监督 92.7、WSJ only 91.3、泛化论断）、§7 结论三个未来方向（多模态/局部注意力/非自回归，后来全部兑现）、附录 Figure 3–5 注意力可视化（长距离依赖、指代消解、句法结构） | ✅ |

## 全文一句话总结

**Transformer 用"完全基于多头自注意力"取代循环与卷积，以 O(1) 串行步数与一步直达的路径长度换来训练的高度并行与长依赖建模，在 WMT 2014 英德/英法两个方向上以单机 8 卡（base 12 小时 / big 3.5 天）的双 SOTA（28.4 / 41.8 BLEU）证明了架构本身的优势，并在成分句法分析上以几乎未调参的配置验证了任务通用性——由此开启了从 BERT/GPT 到 ViT/DETR/MAE 的整个 Transformer 时代，其留下的三个未来方向（多模态、局部注意力、非自回归）也在后来逐一兑现。**
