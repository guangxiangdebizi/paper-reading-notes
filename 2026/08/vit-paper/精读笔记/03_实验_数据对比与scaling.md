# ViT 精读笔记（三）：实验与结果 —— §4 逐段精读

> 论文：*An Image is Worth 16×16 Words: Transformers for Image Recognition at Scale*（ICLR 2021, arXiv:2010.11929）
> 原稿位置：`../ViT_2010.11929.pdf`（全文文本：`../ViT_fulltext.txt`）
> 本篇对应论文第 4 节（Experiments），回答的核心问题是：**ViT 到底行不行，凭什么说行？**

---

## 〇、§4 的论证结构：四道关卡

作者布了四道关卡，层层递进：

```
§4.1 实验设置     ——  先把擂台搭好（数据、模型、评测方式）
§4.2 对比 SOTA    ——  正面刚：我能不能打赢现役冠军？         【结论战】
§4.3 数据需求     ——  回应质疑：没有归纳偏置，数据到底多重要？ 【核心论点战】
§4.4 Scaling 研究 ——  控制变量：同等算力下，谁的性能曲线更陡？ 【效率战】
```

注意这个顺序的**论辩技巧**：先甩出最强结果震慑全场（4.2），再主动回应自己最大的软肋（4.3），最后用控制实验证明架构本身的优越（4.4）。这是一篇"带着假想敌写作"的论文。

---

## 一、§4.1 实验设置：擂台是怎么搭的

### 1. 三个预训练数据集（阶梯式）

| 数据集 | 规模 | 类别数 | 备注 |
|---|---|---|---|
| ImageNet | 1.3M 张 | 1k | 公开的"小"数据集 |
| ImageNet-21k | 14M 张 | 21k | 公开 |
| JFT-300M | **303M 张** | 18k | Google 内部数据，高分辨率 |

**🔑 解读：** 这不是随便选的三个数据集，而是一个**精心设计的梯度**——专门用来测"数据量"这个变量。全文中心思想是"大数据战胜归纳偏置"，那就必须展示从"数据不够"到"数据管够"的完整光谱。JFT-300M 是 Google 的私藏弹药（标签由 noisy 的自动管线生成），这也是当时其他团队难以复现 ViT 的原因之一。

下游评测转移到：ImageNet（含 ReaL 重标注版）、CIFAR-10/100、Oxford Pets、Flowers-102，外加 **VTAB**（19 个任务、每任务仅 1000 张训练样本的"低数据迁移"测试套件，分 Natural / Specialized / Structured 三组）。

> 一个细节：作者特意说他们**对预训练集做了去重**（剔除与下游测试集重复的样本），防止"背题"。这是大规模实验论文的基本诚信。

### 2. 模型规格（Table 1，必须记住）

| 模型 | 层数 | 宽度 D | MLP 宽度 | 头数 | 参数量 |
|---|---|---|---|---|---|
| ViT-Base | 12 | 768 | 3072 | 12 | 86M |
| ViT-Large | 24 | 1024 | 4096 | 16 | 307M |
| ViT-Huge | 32 | 1280 | 5120 | 16 | 632M |

**解读：** 这个配置表**几乎照抄 BERT**（Base/Large 直接沿用，Huge 是新加的）。命名法 `ViT-L/16` = Large 尺寸 + 16×16 patch。再次呼应设计哲学：用 NLP 验证过的配方，不自己发明。

### 3. 对照组（Baseline）的讲究

**原文：**
> *"For the baseline CNNs, we use ResNet, but replace the Batch Normalization layers with Group Normalization, and used standardized convolutions... we denote the modified model 'ResNet (BiT)'."*

**解读：** 作者没有拿一个随便训练的 ResNet 来凑数，而是用了当时**最强的 ResNet 迁移学习方案 BiT**（Big Transfer）作为 CNN 代表。这是"打最强的对手，赢才光彩"的思路。Hybrid 则从 ResNet50 的中层特征图接出。

### 4. 训练细节（藏着关键信息）

**原文：**
> *"We train all models, including ResNets, using Adam... batch size of 4096 and apply a high weight decay of 0.1"*

三个值得注意的点：

- **所有模型（包括 ResNet）都用 Adam**——这很反常（ResNet 传统上用 SGD）。附录 D.1 专门做了消融证明在他们的设置下 Adam 更好。**这是"公平性"设计：统一优化器，免得赢了被说是优化器的功劳。**
- **weight decay 0.1**，很高——为迁移性能服务。
- 评测分两种：**fine-tuning 精度**（全量微调）和 **few-shot 线性精度**（冻结特征，只解一个带正则的岭回归，闭式解，快）。后者用于训练过程中快速评估——这本身也是个工程贡献：不用每次微调几小时，几秒钟就能估出模型好坏。

---

## 二、§4.2 对比 SOTA：主战场的胜利（Table 2 主表）

| 任务 | ViT-H/14 (JFT) | ViT-L/16 (JFT) | ViT-L/16 (I21k) | BiT-L (ResNet152x4) | Noisy Student (EfficientNet) |
|---|---|---|---|---|---|
| ImageNet | **88.55** | 87.76 | 85.30 | 87.54 | 88.4/88.5 |
| ImageNet ReaL | **90.72** | 90.54 | 88.62 | 90.54 | 90.55 |
| CIFAR-10 | **99.50** | 99.42 | 99.15 | 99.37 | – |
| CIFAR-100 | **94.55** | 93.90 | 93.25 | 93.51 | – |
| Pets | **97.56** | 97.32 | 94.67 | 96.62 | – |
| Flowers | 99.68 | **99.74** | 99.61 | 99.63 | – |
| VTAB (19 任务) | **77.63** | 76.28 | 72.72 | 76.29 | – |
| **TPUv3-core-days** | **2.5k** | 0.68k | 0.23k | 9.9k | 12.3k |

### 这张表的四条"潜台词"

1. **ViT-L/16（JFT）在所有任务上击败 BiT-L——而两者用的是同一个预训练数据集。** 这一条极其重要：控制了数据变量，赢的只能是架构（+训练方法）。
2. **ViT-H/14 进一步刷新高难度任务**（ImageNet、CIFAR-100、VTAB）。
3. **算力对比是真正的杀招**：ViT-H/14 用了 2.5k TPU-core-days，Noisy Student 用了 12.3k——**约 1/5 的算力，打出更高的精度**。BiT-L 是 9.9k，约 1/4。
4. **连"穷人版"也能打**：只用公开的 ImageNet-21k 预训练的 ViT-L/16，只花 0.23k core-days（**一张标准 8-core TPUv3 训练约 30 天就能复现**），在多数任务上依然有竞争力。

### 作者紧接着的自我打假（诚实声明）

> *"we note that pre-training efficiency may be affected not only by the architecture choice, but also other parameters, such as training schedule, optimizer, weight decay, etc."*

翻译：*先别急着说"Transformer 架构就是比 CNN 省算力"——训练配方也有影响，我下面 §4.4 做控制实验。* 这种"主动限制自己结论的适用范围"的写法，是严谨论文的典范。

### VTAB 分解（Figure 2）

VTAB 拆成三组对比历史 SOTA（BiT、VIVI、S4L）：
- **Natural（7 任务）**：ViT-H/14 领先
- **Structured（8 任务）**：ViT-H/14 领先
- **Specialized（4 任务）**：与 BiT 打平

---

## 三、§4.3 数据需求：直面软肋

这一节是回应引言里承认的"ImageNet 上打不过 ResNet"。作者做了**两组实验**，一组看"调正则化能不能救"，一组看"模型本质属性"。

### 实验一：换数据集大小，看各尺寸 ViT 的表现（Figure 3）

**原文：**
> *"When pre-trained on the smallest dataset, ImageNet, ViT-Large models underperform compared to ViT-Base models, despite (moderate) regularization. ... Only with JFT-300M, do we see the full benefit of larger models."*

**拆解这个"违反直觉"的现象：**

- 在 ImageNet 上：**大模型（ViT-L）反而不如小模型（ViT-B）**，而且**整个 ViT 家族不如 BiT ResNet**。
- 在 ImageNet-21k 上：大模型追平小模型。
- 到 JFT-300M：**大模型的潜力才完全释放，全面反超**。

**为什么？** 这就是经典的**过拟合-容量**关系：模型越大越容易过拟合小数据；ViT 没有归纳偏置这个"护栏"，过拟合比 CNN 更严重。数据不够时，容量是毒药；数据管够时，容量才是资产。

### 实验二：JFT 随机抽子集，不救场（Figure 4）

**原文：**
> *"we train our models on random subsets of 9M, 30M, and 90M as well as the full JFT-300M dataset. We do not perform additional regularization on the smaller subsets ... This way, we assess the intrinsic model properties"*

**解读实验设计的巧妙：** 这组实验**故意不调正则化**，所有子集用同一套超参，只加 early-stopping。目的是测量模型的**内在属性**，而不是"调参水平"。评测用便宜的 few-shot 线性精度。

**结果：**
> *"Vision Transformers overfit more than ResNets with comparable computational cost on smaller datasets. For example, ViT-B/32 is slightly faster than ResNet50; it performs much worse on the 9M subset, but better on 90M+ subsets."*

**关键结论——Figure 4 曲线形状：**

- **小数据区**：ResNet 赢（归纳偏置占优）
- **大数据区**：ViT 赢，而且——**ResNet 更早进入平台期（plateau），ViT 的曲线还在往上走**

**🌟 作者给出的总结句，是全文中心思想的实验版：**

> *"the convolutional inductive bias is useful for smaller datasets, but for larger ones, learning the relevant patterns directly from the data is sufficient, even beneficial."*
>
> 卷积归纳偏置在**小数据**下有用；在**大数据**下，直接从数据中学规律不仅**够用**，而且**更好**。

注意 "even beneficial" 这个措辞——不只是"追平"，是"**更好**"。没有归纳偏置反而成了优点：因为先天假设既是捷径也是天花板，白纸模型能学到 CNN 结构里根本表达不出的模式。

---

## 四、§4.4 Scaling 研究：同等算力下的控制对决

**实验设计：** 数据固定为 JFT-300M（消除数据瓶颈），训练 7 个 ResNet、6 个 ViT、5 个 Hybrid，横轴是**总预训练算力（exaFLOPs）**，纵轴是迁移精度。这是"拿算力当尺子"量架构效率。

### Figure 5 的三个发现

**发现 1：ViT 统治"性能/算力"性价比曲线。**
> *"ViT uses approximately 2–4× less compute to attain the same performance"*

达到同样的迁移精度，ViT 只需 ResNet **1/2 到 1/4** 的算力。

**发现 2：Hybrid 只在低算力区略胜，大模型时优势消失。**
> *"hybrids slightly outperform ViT at small computational budgets, but the difference vanishes for larger models"*

作者说这有点意外（"somewhat surprising"）——本以为卷积的局部特征处理在任何规模都有帮助，结果大 ViT 自己就把这活干了。**潜台词：CNN 的那点先验，大 ViT 用数据就能学会，不需要外挂。**

**发现 3（最让人兴奋的）：**
> *"Vision Transformers appear not to saturate within the range tried, motivating future scaling efforts."*

在试验范围内，**ViT 的性能曲线没有饱和迹象**。这句话在 2020 年读起来，等于在说："继续把模型做大，还能继续涨点。"——后来的一切（Swin、MAE、直到今天的大模型时代）都验证了这一点。

---

## 🧠 本站小结

### 四道关卡，四个结论

| 关卡 | 回答的问题 | 结论 |
|---|---|---|
| §4.2 | 打得赢 SOTA 吗？ | ✅ 全面打赢 BiT-L，算力省 4-5 倍 |
| §4.3 | 归纳偏置缺失致命吗？ | ❌ 不致命——**数据规模够大时反而更好**；但小数据下确实吃亏 |
| §4.4 | 架构本身效率高吗？ | ✅ 同等算力性能碾压 ResNet，且看不到饱和 |

### 三个必须带走的数字

- ViT-H/14：ImageNet **88.55%**，只用 Noisy Student **约 1/5** 的算力
- 同等性能下 ViT 比 ResNet 省 **2-4×** 算力
- **300M 张图**是 ViT 彻底反超 CNN 的数据临界点

### 一个思维框架

这组实验本质上在回答一个关于机器学习的元问题——

> **"先验知识（归纳偏置）和数据，谁更值钱？"**
>
> ViT 的答案：**数据足够多时，先验一文不值，甚至碍事。**

---

## ✏️ 自检问题

1. 为什么作者要用"同数据集下的 BiT-L"作对比，而不只是拿 Noisy Student 比？
2. Figure 4 里，ViT-B/32 在 9M 子集上输给 ResNet50，在 90M+ 上反超——这说明了什么？
3. 作者为什么在 §4.2 赢了之后，还要"多此一举"做 §4.4？
4. 为什么说 JFT-300M 的"私有性"既是 ViT 成功的助力，也是它当时被质疑的原因？
