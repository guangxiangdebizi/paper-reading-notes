# ViT 精读笔记 02：方法 §3 —— ViT 是怎么造出来的

> 对应论文 §3 Method（含 §3.1 Vision Transformer、§3.2 Fine-Tuning and Higher Resolution）

这一节不长，但信息密度极高。

---

## 〇、开场白：设计哲学

**原文：**
> *"In model design we follow the original Transformer (Vaswani et al., 2017) as closely as possible. An advantage of this intentionally simple setup is that scalable NLP Transformer architectures – and their efﬁcient implementations – can be used almost out of the box."*

**解读：** 翻译过来就是——

> "我们**故意**贴着 2017 年原版 Transformer 来设计。这么做的目的是：NLP 圈那些高度优化的实现（GPU/TPU kernel、并行策略），我们**开箱即用（out of the box）**。"

这呼应了引言里"前人那些魔改的注意力模型没法在硬件上高效跑"的批评。ViT 的成功一半是**架构**的成功，一半是**工程**的成功——它站在了 NLP 生态的肩膀上。

记住这句话，它是理解"为什么 ViT 能赢"的钥匙之一：**不是 ViT 多巧妙，而是它足够标准，所以能蹭到整个 NLP 工业界的优化红利。**

---

## 一、§3.1 核心思想：把图像"翻译"成句子

先看论文给出的总览（Figure 1 的文字版）。整个流程是**一条流水线**：

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  原始图像 x ∈ R^(H×W×C)                                          │
│  (例如 224×224×3)                                                │
│       │                                                          │
│       │ ① 切 patch：切成 N = HW/P² 个小方块（如 16×16）           │
│       ▼                                                          │
│  x_p ∈ R^(N × (P²·C))     ← N 个被"压扁"的 patch                 │
│       │                                                          │
│       │ ② 线性投影 E：每个 patch 映射成 D 维向量（patch embedding）│
│       ▼                                                          │
│  N 个 D 维向量                                                   │
│       │                                                          │
│       │ ③ 在最前面插入一个可学习的 [class] token                  │
│       │ ④ 加上位置编码 E_pos                                     │
│       ▼                                                          │
│  z_0 ∈ R^((N+1) × D)      ← 一个标准的"句子"                     │
│       │                                                          │
│       │ ⑤ 丢进 L 层标准 Transformer Encoder                      │
│       ▼                                                          │
│  取出 [class] 位置的输出 z_L^0                                    │
│       │                                                          │
│       │ ⑥ 接分类头（MLP）                                         │
│       ▼                                                          │
│  类别预测（猫 / 鸟 / 车 …）                                       │
└─────────────────────────────────────────────────────────────────┘
```

我们一步一步拆。

---

### 步骤 ①：切 patch —— 图像的"分词"

**原文：**
> *"To handle 2D images, we reshape the image x ∈ R^(H×W×C) into a sequence of ﬂattened 2D patches x_p ∈ R^(N×(P²·C)), where (H,W) is the resolution of the original image, C is the number of channels, (P,P) is the resolution of each image patch, and N = HW/P² is the resulting number of patches."*

**拆解：**

- 输入图像：`H×W×C`，比如 `224×224×3`（RGB 三通道）。
- 把它切成一个个 `P×P` 的小方块。论文默认 `P=16` 或 `P=32`。
- 每个小方块**压扁（flatten）**成一个长向量，长度 = `P²·C = 16×16×3 = 768`。
- 一共切出 `N = HW/P²` 个 patch。以 224×224、P=16 为例：`N = 224×224/256 = 196` 个 patch。

**类比（这是全文最精妙的比喻，也是标题的来源）：**

| NLP | ViT |
|---|---|
| 一句话 | 一张图 |
| 一个单词（token） | 一个 16×16 的小方块（patch） |
| 词表 | 不存在！patch 是连续的像素块 |

标题 **"An Image is Worth 16×16 Words"** 就是这个意思：一张图 = 196 个"单词"。

**🔑 关键洞察：** 这一步是全文**唯一**用到"图像是二维的"这个先验知识的地方。切完之后，二维结构就被压扁成一维序列了，后面的 Transformer 完全不知道这些 patch 原本在图像里的行列位置——**这就是为什么必须加位置编码**（步骤④）。

---

### 步骤 ②：线性投影 —— 相当于 NLP 的"词嵌入层"

**原文：**
> *"The Transformer uses constant latent vector size D through all of its layers, so we ﬂatten the patches and map to D dimensions with a trainable linear projection. We refer to the output of this projection as the patch embeddings."*

**拆解：** Transformer 内部要求所有向量都是同一个维度 D。所以用一个**可训练的线性投影矩阵 E**（形状 `(P²·C) × D`）把每个 patch 映射成 D 维向量。

**为什么这一步意义深远：** 在实现上，这个"线性投影"**就是一个卷积核大小为 P×P、步长也为 P 的卷积**——一次性把图像切成块并投影。所以 ViT 的输入层本质上是"一层粗粒度的卷积"，但论文把它表述为线性投影，强调的是"我在做序列嵌入，不是在做卷积网络"。

---

### 步骤 ③+④：[class] token 和位置编码

**原文：**
> *"Similar to BERT's [class] token, we prepend a learnable embedding to the sequence of embedded patches (z⁰₀ = x_class), whose state at the output of the Transformer encoder (z⁰_L) serves as the image representation y."*

**解读：**

**[class] token**：在序列最前面**硬塞**一个额外的、可学习的向量。它自己不对应任何图像内容，而是在层层自注意力中不断"吸收"全图信息，最后它的输出状态 `z⁰_L` 就被当作**整张图的表示**，送去分类。

> 为什么要这么做？因为自注意力的输出是**每个 patch 一个向量**，而分类需要**一个**全局向量。有两种选择：把所有 patch 向量池化（像 CNN 的 global average pooling），或者学一个专门的"汇总员" token。ViT 选了后者，纯粹是为了**跟 BERT 保持一致**。（附录 D.3 证明两者其实效果差不多，只是需要不同的学习率——这是后话。）

**位置编码：**

**原文：**
> *"Position embeddings are added to the patch embeddings to retain positional information. We use standard learnable 1D position embeddings, since we have not observed signiﬁcant performance gains from using more advanced 2D-aware position embeddings."*

**解读：** 切 patch 时二维结构丢了，所以要加位置信息。有意思的是作者说：**用一维的就行，二维的没更好。** 这个反直觉的结论在附录 D.4 做了消融：不加位置编码掉点严重（61.4% → 64.2%），但 1D / 2D / 相对位置编码之间几乎无差别。原因：patch 网格很小（14×14），学空间关系对哪种方案都容易，而且模型会**自己**在 1D 编码里学出 2D 结构（后面第 4 站会看到证据）。

---

### 核心公式：四行字概括整个 ViT

论文把整个模型压缩成 4 个公式，这是全文**最值得背**的部分：

```
z⁰ = [x_class; x¹_p E; x²_p E; ··· ; xᴺ_p E] + E_pos          (1)

z′_ℓ = MSA(LN(z_{ℓ−1})) + z_{ℓ−1},   ℓ = 1...L                 (2)

z_ℓ  = MLP(LN(z′_ℓ)) + z′_ℓ,          ℓ = 1...L                 (3)

y    = LN(z⁰_L)                                                  (4)
```

**逐条解读：**

**(1) 输入构造**：把 `[class]` 嵌入和 N 个 patch 嵌入拼成一个序列，加上位置编码。这就是"造句"。

**(2) 注意力子层**：第 ℓ 层的第一个操作。注意顺序 —— 先 **LayerNorm**，再做**多头自注意力（MSA）**，然后**残差连接**。这个"先归一化再计算"的顺序叫 **Pre-LN**（原论文是 Post-LN，这里是个不易察觉的改动，Pre-LN 训练更稳）。

**(3) MLP 子层**：同样的结构套在两层 MLP 上（中间用 GELU 激活，MLP 隐藏层宽度通常是 4D）。

**(4) 输出**：最后一层 `[class]` 位置的输出再过一次 LayerNorm，就是最终的图像表示 y，送去分类头。

**一个细节很多人会漏：** 分类头在**预训练**时是一个带隐藏层的 MLP，在**微调**时会换成**单层线性层**（§3.2 提到）。

---

### 📐 顺手算一笔账：ViT-B/16 的序列是什么样的？

用 Table 1（实验部分的配置表）的配置，输入 224×224：

- patch 大小 P=16 → 每个 patch 768 维 → N = 196 个 patch
- 加 1 个 [class] → 序列长度 197
- 隐藏维度 D = 768，12 层，12 个注意力头

所以 ViT-B/16 处理一张图 = 处理一个**197 个 token、每个 768 维**的"句子"。

**⚠️ 顺便记住一个重要规律**（论文特别强调的）：
> *"the Transformer's sequence length is inversely proportional to the square of the patch size"*

序列长度和 patch 面积的**平方**成反比——patch 从 32 减到 16，序列长度变成 **4 倍**，注意力的计算量（约 O(N²)）暴涨。这就是为什么 ViT-B/16 比 ViT-B/32 贵得多，也是 ViT 的根本计算瓶颈。

---

### 关于归纳偏置（Inductive Bias）的专段

这段是引言论点的**技术版重述**：

**原文：**
> *"Vision Transformer has much less image-speciﬁc inductive bias than CNNs. In CNNs, locality, two-dimensional neighborhood structure, and translation equivariance are baked into each layer throughout the whole model."*

**拆解：** CNN 每一层都"内置"三个图像假设：
1. **局部性**：卷积核只看小邻域
2. **二维邻域结构**：按 2D 网格组织
3. **平移等变性**：猫在左上角和右下角，特征一样

而 ViT 呢？作者诚实地盘点了一遍：
- **MLP 层**：局部 + 平移等变（逐 patch 独立作用）
- **自注意力层**：完全是**全局的**，没有任何局部假设
- **二维结构**：只在两处用到——① 开头切 patch，② 微调时换分辨率对位置编码做 2D 插值
- 位置编码初始化时**不含任何 2D 信息**，空间关系全靠学

> 💡 你可以这么理解：**CNN 是"带着答案进考场"（先天假设），ViT 是"空手进考场但允许先读完整个图书馆"（大数据）。**

---

### Hybrid 混合架构

**原文：**
> *"As an alternative to raw image patches, the input sequence can be formed from feature maps of a CNN."*

**解读：** 输入也可以不是原始像素，而是先用 CNN 提取特征图，再把特征图切块喂给 Transformer。极端情况下 patch 取 1×1，就等于直接把 CNN 特征图摊平。这是给"不相信纯 Transformer"的人留的台阶，实验里也确实有用（小算力下 hybrid 略优，大模型时差距消失）。

---

## 二、§3.2 微调与高分辨率

这一小节短，但藏着一个**工程上非常实用的技巧**。

**原文：**
> *"we remove the pre-trained prediction head and attach a zero-initialized D×K feedforward layer, where K is the number of downstream classes."*

**要点 1：分类头替换**。微调时扔掉预训练的分类头，换成新的 `D×K` 线性层（K = 下游类别数），并且**用 0 初始化**——附录说这比随机初始化更稳（训练初期输出全 0，不会乱扰动）。

**原文：**
> *"When feeding images of higher resolution, we keep the patch size the same, which results in a larger effective sequence length ... the pre-trained position embeddings may no longer be meaningful. We therefore perform 2D interpolation of the pre-trained position embeddings."*

**要点 2：高分辨率微调技巧**。微调时常用更高分辨率（比如预训练 224 → 微调 384）：
- **patch 大小不变**（还是 16×16），于是序列变长：224→197 个 token，384→577 个 token
- 问题来了：预训练学的位置编码是 196 组，现在要 576 组，**对不上**！
- 解法：把预训练的位置编码**还原成 2D 网格，做双线性插值**，"放大"到新网格尺寸。

**要点 3（呼应主题）：**
> *"this resolution adjustment and patch extraction are the only points at which an inductive bias about the 2D structure of the images is manually injected"*

作者再次强调：**切 patch + 位置编码插值，是整个人工注入 2D 先验的仅有的两处。** 这种反复强调是论文写作上的刻意设计——在不断强化"pure transformer"的卖点。

---

## 🧠 小结

| 组件 | 作用 | NLP 对应物 |
|---|---|---|
| 切 patch + 线性投影 | 图像 → token 序列 | 分词 + 词嵌入 |
| [class] token | 汇总全图信息供分类 | BERT 的 [CLS] |
| 位置编码（1D 可学习） | 补回空间信息 | 位置编码 |
| L 层 Encoder（Pre-LN + MSA + MLP + 残差） | 特征提取主体 | 原版 Transformer |
| 分类头 | 输出类别 | 分类层 |

**三个必须带走的结论：**
1. ViT = **"图像分词" + 标准 NLP Transformer**，刻意不魔改，为的是吃 NLP 工程红利。
2. 序列长度 ∝ 1/P²，**patch 越小越贵**，这是 ViT 的成本命门。
3. 2D 先验只在**切 patch** 和 **位置编码插值**两处人工注入，其余全靠学。

---

## 自检小问题

1. 为什么输入 224×224 的图、patch=16 时，序列长度是 197 而不是 196？
2. 公式 (2) 里 `LN` 放在 `MSA` 之前，这个细节叫什么？有什么意义？
3. 微调换成 384 分辨率时，位置编码是怎么"变多"的？
