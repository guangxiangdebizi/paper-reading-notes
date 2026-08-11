# DeiT 精读笔记 03：实验 §5 —— 蒸馏分析、SOTA 对比与迁移

> 对应论文 §5 Experiments（§5.2 蒸馏分析、§5.3 效率对比、§5.4 迁移学习）
> 三个问题依次推进：哪种蒸馏最好/老师该选谁 → 和顶级 CNN 正面刚 → 下游迁移行不行。

---

## 一、§5.2 蒸馏分析：三连问

### 问题 1：老师该选谁？—— Table 2（全文最有趣的表）

固定学生为 DeiT-B⚗，换不同的老师：

| 教师 | 教师自身精度 | 学生 pretrain | 学生 ↑384 |
|---|---|---|---|
| **DeiT-B**（Transformer） | 81.8 | 81.9 | 83.1 |
| RegNetY-4GF（CNN） | 80.0 | 82.7 | 83.6 |
| RegNetY-8GF（CNN） | 81.7 | 82.7 | 83.8 |
| RegNetY-12GF（CNN） | 82.4 | 83.1 | 84.1 |
| RegNetY-16GF（CNN） | 82.9 | 83.1 | **84.2** |

**🌟 看第一行和后面的对比：** Transformer 老师自己精度 81.8，教出来的学生只有 83.1；而**精度更低的 CNN 老师（RegNetY-4GF，才 80.0）教出来的学生反而有 83.6**——老师比学生**弱**，学生却更强。

**原文的解释：**
> *"The fact that the convnet is a better teacher is probably due to the **inductive bias inherited by the transformers through distillation**, as explained in Abnar et al."*

**解读：** CNN 的预测里带着它看待图像的方式（局部性、平移不变性的痕迹），学生模仿这些预测，等于**免费继承了一套视觉先验**。

**和 ViT 的关系（划重点）：** ViT 说"大数据战胜归纳偏置"，DeiT 说"没有大数据时，归纳偏置可以**借**"。两篇论文拼在一起，才是完整的故事。

默认老师定为 **RegNetY-16GF**（82.9%，84M 参数）——老师本身也是作者用同样的数据+配方训练的，公平。

### 问题 2：哪种蒸馏姿势最好？—— Table 3

固定老师 RegNetY-16GF，对比三种蒸馏（学生列从左到右：Ti / S / B / B↑384）：

| 监督方式 | 教师目标 | Ti | S | B | B↑384 |
|---|---|---|---|---|---|
| DeiT–（无蒸馏） | — | 72.2 | 79.8 | 81.8 | 83.1 |
| soft 蒸馏 | 软标签 | 72.2 | 79.8 | 81.8 | 83.2 |
| **hard 蒸馏** | 硬标签 | 74.3 | 80.9 | 83.0 | 84.0 |
| DeiT⚗ class 头 | 硬标签 | 73.9 | 80.9 | 83.0 | 84.2 |
| DeiT⚗ distil 头 | 硬标签 | 74.6 | 81.1 | 83.1 | 84.4 |
| **DeiT⚗ class+distil 融合** | 硬标签 | 74.5 | 81.2 | **83.4** | **84.5** |

**逐层读这张表：**

1. **soft 蒸馏约等于白做**：81.8 → 81.8/83.2。经典的 KL 软蒸馏对 Transformer 几乎没增益——反直觉（在 CNN 上它通常有效），说明照搬 NLP/CNN 的蒸馏配方到 Transformer 行不通。
2. **hard 蒸馏大幅领先**：+1.2（83.0 vs 81.8）。零超参的方法反而最好用。
3. **蒸馏 token 再上一层楼**：83.4 / 84.5，且**单看 distil 头（83.1）已经比 class 头（83.0）略强**——distil 头更贴近 CNN 教师，吃到了更多归纳偏置。
4. **融合最优**：两头相加再涨一截，证明两个头携带**互补信息**。

### 问题 3：学生真的"像"老师吗？—— Table 4（分歧分析）

作者算了一个很妙的指标：**两个模型对同一批图做出不同判断的比例**（disagreement rate）。

| | 真实标签 | CNN老师 | DeiT(无蒸馏) | DeiT⚗ class头 | DeiT⚗ distil头 | DeiT⚗ 融合 |
|---|---|---|---|---|---|---|
| **CNN老师** | 0.171 | 0.000 | 0.133 | 0.112 | **0.100** | 0.102 |
| **DeiT(无蒸馏)** | 0.182 | 0.133 | 0.000 | 0.109 | 0.110 | 0.107 |

**解读：** 蒸馏后的 **distil 头和 CNN 老师的分歧率只有 0.100**（全表最低），而**无蒸馏的 DeiT 和 CNN 分歧率是 0.133**。反过来，class 头则更贴近"无蒸馏的 DeiT"。

**结论：** 蒸馏 token 的输出**真的变成了 CNN 的"影子"**，class token 则保住了 Transformer 自己的判断。两个头一个继承先验、一个保持本色，融合起来两头占便宜。这张表是"蒸馏传递归纳偏置"这个论点的**机制级证据**。

### 补充发现：蒸馏模型越训越香（Figure 3）

**原文：**
> *"Increasing the number of epochs significantly improves the performance of training with distillation... while for the latter the performance saturates with longer schedules, our distilled network clearly benefits from a longer training time."*

**解读：** 无蒸馏的 DeiT-B 训到 ~400 epoch 就饱和了；蒸馏版**一路涨到 1000 epoch 还在涨**（1000-epoch 版本：84.2 / 85.2）。含义：教师监督提供了比真实标签**更丰富的信号**，模型能从里面持续"榨汁"。

---

## 二、§5.3 效率 vs 精度：和 EfficientNet 家族正面刚

### 战场设定（Figure 1）

横轴**吞吐量**（V100 上每秒处理多少图），纵轴 ImageNet top-1。对手选的是 **EfficientNet 家族**——CNN 十年进化的结晶（架构搜索+数年调优），也是当时"精度/效率"性价比之王。

### 结论（分三层）

**第一层：不蒸馏的 DeiT 已经基本追平。**
> *"Our method DeiT is slightly below EfficientNet, which shows that we have almost closed the gap between vision transformers and convnets when training with Imagenet only. These results are a major improvement (**+6.3% top-1** in a comparable setting) over previous ViT models trained on Imagenet1k only."*

对比的锚点：ViT 论文里 ViT-B 只用 ImageNet 训是 77.9%；DeiT-B 是 81.8%——**同架构、同数据，训练配方带来大幅提升**。

**第二层：蒸馏后反超。**
> *"when DeiT benefits from the distillation from a relatively weaker RegNetY to produce DeiT⚗, it **outperforms EfficientNet**. It also outperforms by 1% the Vit-B model pre-trained on JFT300M at resolution 384 (**85.2% vs 84.15%**)"*

两个"以下克上"：
- 学生（87M）**打败了老师** RegNetY-16GF 的性价比；
- **只用 ImageNet** 的 DeiT-B⚗↑384（85.2%）打败了**用 300M 张图**训的 ViT-B（84.15%）——数据量差 230 倍，还赢了 1 个点。

**第三层：Table 5 主表（挑关键行）**

| 模型 | 参数 | 吞吐(im/s) | ImageNet top-1 |
|---|---|---|---|
| EfficientNet-B7 | 66M | 55.1 | 84.3 |
| ViT-B/16（JFT-300M） | 86M | 85.9 | 77.9 |
| DeiT-B | 86M | 292.3 | 81.8 |
| DeiT-B⚗ | 87M | 290.9 | 83.4 |
| DeiT-B⚗ / 1000 epochs | 87M | 290.9 | 84.2 |
| **DeiT-B⚗↑384 / 1000 epochs** | 87M | 85.8 | **85.2** |

**读表要点：** 吞吐量列——EfficientNet-B7 只有 55 im/s（600px 输入），DeiT-B 家族在 224/384 分辨率下 290/86 im/s。作者比的是"同吞吐量下谁精度高"，结论是 DeiT⚗ 全面压过 EfficientNet 曲线。

诚实的注脚：吞吐量统一用 timm 的实现来测，"为了尽可能公平"——连测速都要声明口径。

---

## 三、§5.4 迁移学习：下游任务检验

**Table 7（挑关键对比）：**

| 模型 | CIFAR-10 | CIFAR-100 | Flowers | Cars | iNat-18 |
|---|---|---|---|---|---|
| EfficientNet-B7 | 98.9 | 91.7 | 98.8 | 94.7 | — |
| ViT-B/16（JFT） | 98.1 | 87.1 | — | 89.5 | — |
| DeiT-B | 99.1 | 90.8 | 98.4 | 92.1 | 73.2 |
| DeiT-B⚗↑384 | **99.2** | **91.4** | **98.9** | **93.9** | **80.1** |

**解读：** 只用 ImageNet 预训练的 DeiT，迁移到 7 个下游任务后**和顶级 CNN 打平**，全面超过用 JFT-300M 的 ViT-B。这堵住了一个可能的质疑："你 ImageNet 高是不是过拟合 ImageNet 了？"——迁移能力证明特征是真学到了。

### 彩蛋实验：CIFAR-10 从头训（不预训练）

| 方法 | RegNetY-16GF | DeiT-B | DeiT-B⚗ |
|---|---|---|---|
| CIFAR-10 top-1 | 98.0 | 97.5 | **98.5** |

**解读：** 训练时长按 ImageNet 等比拉长（7200 epoch），直接在 CIFAR-10 上从头训。结果：**蒸馏版 DeiT 小胜 CNN**。哪怕在"CNN 主场"（小数据集），拿到蒸馏加持的 Transformer 也不虚。

---

## 🧠 小结

| 问题 | 答案 | 证据 |
|---|---|---|
| 哪种蒸馏好？ | hard > soft；蒸馏 token > 两者；融合最优 | Table 3 |
| 老师选谁？ | **CNN 老师 > 同级 Transformer 老师** | Table 2 |
| 为什么 CNN 老师好？ | 蒸馏把归纳偏置"软传递"给了学生 | Table 4（distil 头与 CNN 分歧率最低） |
| 打赢 CNN 了吗？ | 性价比曲线反超 EfficientNet；85.2% > ViT-B(JFT) 的 84.15% | Figure 1 + Table 5 |
| 迁移行吗？ | 7 个下游任务与顶级 CNN 打平 | Table 7 |

**三个必须带走的数字：**
- **85.2%**：DeiT-B⚗↑384（1000 epochs），只用 ImageNet，超过 JFT-300M 的 ViT-B 一个点
- **0.100**：distil 头与 CNN 老师的分歧率（Table 4），归纳偏置传递的机制证据
- **+6.3%**：相对 ViT 原论文的 ImageNet-only 结果，纯训练配方带来的提升

**一个思维升级：** 这一站把"归纳偏置"从二元对立（有/无）变成了**可流动的资产**——CNN 有，可以通过蒸馏**流**给 Transformer。后面 ConvNeXt 还会再反转一次这个概念。

---

## 自检小问题

1. RegNetY-4GF 自己只有 80.0%，教出的学生却有 83.6%——"弱师出高徒"为什么可能？
2. soft 蒸馏对 Transformer 几乎无效，你觉得可能是什么原因？（开放题）
3. 为什么说 Table 4 比 Table 2 更能证明"归纳偏置被传递了"？
