# DeiT 精读笔记 02：方法 §3 + §4 —— ViT 回顾与 ⚗ 蒸馏 token

> 对应论文 §3 Vision transformer: overview 与 §4 Distillation through attention
> §4 是全文的心脏：蒸馏的三种姿势 + 招牌贡献"蒸馏 token"。

---

## 一、§3 Vision Transformer 回顾：不只是复读，藏着一个洞察

DeiT 的 §3 名义上是"回顾 ViT"，但它是**用自己的话重讲一遍**，重讲的过程里塞了私货。只挑它**和 ViT 论文讲得不一样**的地方。

### 1. class token 的机制解读（比 ViT 原文更透）

ViT 原文只说"加一个可学习的 class token，它的输出当图像表示"。DeiT 补了一段机制分析：

**原文：**
> *"This architecture forces the self-attention to spread information between the patch tokens and the class token: at training time the supervision signal comes only from the class embedding, while the patch tokens are the model's only variable input."*

**解读：** 注意这个"forces（迫使）"。训练时损失函数**只挂在 class token 上**，而输入信息**全在 patch token 里**——那梯度想要流到 patch，就必须**借道自注意力**。所以这个架构天然逼着注意力学会"把 patch 的信息搬运到 class token"。

**🔑 为什么重要：** 这段话其实是在给 §4 的蒸馏 token **做理论铺垫**——既然监督信号只挂在一个 token 上就能让它吸走全图信息，那我再挂一个 token、换成"蒸馏损失"，它同样能吸走信息。蒸馏 token 的合法性，就建立在这段机制分析上。

### 2. 位置编码与变分辨率（呼应 ViT §3.2）

这段和 ViT 讲的一样：微调换高分辨率时 patch 大小不变、序列变长、位置编码要做插值。但 DeiT 补了一个**工程细节**（§6 中给出）：

> 插值要用 **bicubic（双三次）** 而不是 bilinear（双线性）——因为双线性插值会把向量的 ℓ2 范数插低，低范数向量和预训练的 Transformer 不匹配，直接掉点。双三次插值能近似保范数。

这种细节就是"真动手训过模型的人"才会写的。

---

## 二、§4 Distillation through attention：全文的心脏

这一节把蒸馏拆成**两个坐标轴**，一共摆出三种方法：

```
                        蒸馏目标用什么
                 ┌─────────────────┬─────────────────┐
                 │  soft（教师软标签）│  hard（教师硬标签）│
    ┌────────────┼─────────────────┼─────────────────┤
损失│ 传统姿势     │ ① soft 蒸馏      │ ② hard 蒸馏      │
形式│（改损失函数）│   （Hinton 经典）  │  （DeiT 新提）    │
    ├────────────┼─────────────────┴─────────────────┤
    │ 新姿势       │ ③ 蒸馏 token（⚗）                   │
    │（改模型结构）│   —— 本文核心贡献                     │
    └────────────┴───────────────────────────────────┘
```

### 方法 ①：soft 蒸馏（经典款）

**原文：**
> *"Soft distillation minimizes the Kullback-Leibler divergence between the softmax of the teacher and the softmax of the student model."*

损失函数（Eq. 2）：

```
L_global = (1−λ)·L_CE(ψ(Z_s), y)  +  λτ²·KL(ψ(Z_s/τ), ψ(Z_t/τ))
           └────────真实标签的交叉熵────┘   └────学生模仿教师软分布────┘
```

**解读：**
- `Z_t`、`Z_s`：教师和学生的 logits；`ψ` 是 softmax；
- `τ`（温度）：把教师的分布"烫软"，让学生学到"这个图 80% 是猫、15% 是虎、5% 是狗"这种**类间关系**；
- `λ`：平衡真实标签和教师监督的权重。

这就是 Hinton 2015 年的经典蒸馏，一字未改。DeiT 拿它当 baseline。

### 方法 ②：hard 蒸馏（DeiT 的小创新）

**原文：**
> *"We introduce a variant of distillation where we take the hard decision of the teacher as a true label."*

损失函数（Eq. 3）：

```
L_hardDistill = ½·L_CE(ψ(Z_s), y)  +  ½·L_CE(ψ(Z_s), y_t)
                └──对真实标签──┘     └──对教师的预测结果──┘
```

**解读：** 不要教师的软分布了，直接拿教师预测的**那个类别**（`y_t = argmax Z_t`）当"第二真值"，和真实标签各占一半权重。

**妙处**（原文自评）：
> *"this choice is better than the traditional one, while being **parameter-free and conceptually simpler**"*

没有 τ、没有 λ，零超参，概念上就是"老师说的也算一个标准答案"。而且它天然兼容数据增强——同一张图做不同增强时，教师的硬标签会跟着变（教师看的是增强后的图），相当于**教师替你实时改答案**。实验结果：hard 比 soft 在 DeiT-B 上高 **1.2 个点**（83.0 vs 81.8）。

---

### 方法 ③：蒸馏 token（⚗，本文的招牌）

**原文：**
> *"We add a new token, the distillation token, to the initial embeddings (patches and class token). Our distillation token is used similarly as the class token: it interacts with other embeddings through self-attention, and is output by the network after the last layer. Its target objective is given by the distillation component of the loss."*

**图解（Figure 2 的文字版）：**

```
输入序列：[distil] [class] [patch 1] [patch 2] ... [patch 196]
             │        │        │          │             │
             ▼        ▼        ▼          ▼             ▼
        ┌──────────────────────────────────────────────────┐
        │            L 层 Transformer Encoder               │
        │   （两个特殊 token 和所有 patch 自由互相注意）        │
        └──────────────────────────────────────────────────┘
             │        │
             ▼        ▼
        蒸馏损失    分类损失
     （模仿教师）  （真实标签）
```

**解读：** 把"蒸馏"这件事从**损失函数**层面挪到了**模型结构**层面——不再让学生最后输出的分布去模仿教师，而是**专门派一个 token 深入网络内部，从头到尾盯着教师的信号**。class token 继续负责真实标签，两个头各司其职。

### 一个漂亮的实证细节：两个 token 真的学到了不同的东西

**原文：**
> *"the learned class and distillation tokens converge towards different vectors: the average cosine similarity between these tokens equal to 0.06. ... through the network, all the way through the last layer at which their similarity is high (cos=0.93), but still lower than 1."*

**解读：** 输入端两个 token 的余弦相似度只有 **0.06**（几乎正交，各干各的），逐层上升，到最后一层是 **0.93**（趋同但不重合——因为两个目标相似但不相同）。这组数字证明蒸馏 token 不是 class token 的复制品，而是**功能互补**的第二通道。

### 一个严谨的对照实验：排除"多一个 token"的偶然性

**原文：**
> *"instead of a teacher pseudo-label, we experimented with a transformer with two class tokens. Even if we initialize them randomly and independently, during training they converge towards the same vector (cos=0.999)... This additional class token does not bring anything."*

**解读：** 有人可能会杠："多一个 token 性能涨，说不定只是多了点参数/容量？"作者堵死这个杠点：把第二个 token 也设成 class token（同样目标），结果两个 token 训着训着**完全重合（cos=0.999）**，性能毫无增益。所以增益来自**蒸馏目标**，不是 token 本身。——这是非常干净的消融。

### 推理时怎么用这两个头

**原文：**
> *"our referent method is the late fusion of these two separate heads, for which we add the softmax output by the two classifiers to make the prediction."*

**解读：** 测试时两个头都能独立分类，但默认做法是**晚期融合**——把两个分类器的 softmax 输出**直接相加**再预测。简单粗暴，但实验显示它比单用任何一个头都好（84.5 vs 84.2/84.4，B↑384）。

### 微调阶段也要蒸馏

**原文：**
> *"We use both the true label and teacher prediction during the fine-tuning stage at higher resolution. ... We have also tested with true labels only but this reduces the benefit of the teacher."*

**解读：** 高分辨率微调时**继续用教师**（教师也要换成同分辨率版本）。只用真实标签微调反而掉点——教师的作用贯穿始终。

---

## 三、§5.1 顺手交代的模型家族（Table 1）

| 模型 | 对应 ViT | 宽度 D | 头数 | 层数 | 参数量 | 吞吐量(im/s) |
|---|---|---|---|---|---|---|
| DeiT-Ti | 无 | 192 | 3 | 12 | **5M** | 2536 |
| DeiT-S | 无 | 384 | 6 | 12 | **22M** | 940 |
| DeiT-B | ViT-B | 768 | 12 | 12 | **86M** | 292 |

**解读：** DeiT-B ≡ ViT-B（原文原话："Our architecture design is identical to the one proposed by Dosovitskiy et al. with no convolutions. Our only differences are the training strategies, and the distillation token."）。Ti（Tiny）和 S（Small）是新造的轻量型号，对标 ResNet-18/50 的生态位——**让 ViT 家族第一次有了"平民型号"**。

命名规则（后文常用）：
- `DeiT-B`：基础模型；`DeiT-B↑384`：384 分辨率微调版
- `DeiT-B⚗`：蒸馏版（那个烧瓶符号）

---

## 🧠 小结

| 方法 | 改动位置 | 核心思想 | 效果定位 |
|---|---|---|---|
| ① soft 蒸馏 | 损失函数 | 学生模仿教师的软分布 | baseline |
| ② hard 蒸馏 | 损失函数 | 教师预测当"第二真值"，零超参 | 比 soft 好（83.0 vs 81.8） |
| ③ 蒸馏 token ⚗ | **模型结构** | 专设一个 token 负责学教师，与 class token 分工 | **最好**（84.5，配合融合） |

**三个必须带走的结论：**
1. 蒸馏 token 的合法性来自 class token 的机制——"监督信号挂哪个 token，哪个 token 就吸走全图信息"。
2. 两个 token 输入端 cos=0.06、输出端 cos=0.93：**分工明确又目标趋同**。
3. "两个 class token"的对照实验证明：增益来自蒸馏目标，不是 token 数量。

---

## 自检小问题

1. 蒸馏 token 和 class token 在结构上几乎一样，它们的本质区别是什么？
2. hard 蒸馏比 soft 蒸馏好，作者给的解释和哪个因素有关？（提示：数据增强）
3. 为什么推理时把两个头的 softmax 相加（late fusion）比只用一个头好？
