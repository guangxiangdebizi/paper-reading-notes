# Registers 精读笔记 02：诊断——high-norm token 里有什么

> 论文：**Vision Transformers Need Registers**  
> 本站对应原文 §2.1 与 §2.2；关键证据：Fig. 3–5、Table 1，补充证据：Appendix G / Table 6  
> 关键页面：`../figures/page_3.png`、`../figures/page_4.png`、`../figures/page_5.png`

---

## 一、本站要验证的不是“范数很高”，而是“功能发生替换”

仅看到少数 patch token 的 L2 范数很高，最多能说明表示分布里有离群点，不能直接推出它们是内部寄存器。作者必须补齐下面这条证据链：

```text
输出范数离群
  → 不是固定输入噪声，而是训练过程中涌现
  → 模型优先挑选输入中冗余的 patch
  → 被挑中的 token 丢失原位置的局部信息
  → 同时获得与整张图有关的全局信息
  → “patch token 被改作全局计算空间”成为最简解释
```

其中前五项是实验观察，最后一项仍是**机制解释**。第 3 站的 register 干预才会进一步检验这个解释。

---

## 二、Fig. 3：先把视觉 artifact 变成数值事件

### 原文 1：用输出 token 范数检测 artifact

> *"We observe that an important difference between 'artifact' patches and other patches is the norm of their token embedding at the output of the model."*

**直译：** 作者观察到，artifact patch 与其他 patch 的一个重要差别，是它们在模型输出处 token embedding 的范数。

对最后一层第 `i` 个 patch 表示 `h_i`，诊断量就是：

```text
n_i = ||h_i||_2
```

Fig. 3 对同一张狗图比较 DINO ViT-B/16 与 DINOv2 ViT-g/14：

- DINO 的范数图平滑，统计分布集中在低值区；
- DINOv2 的少数位置突然变亮，范数分布形成第二个高值峰；
- DINOv2 多数 patch 的范数在 `0–100`，作者对该模型人工取 `150` 为阈值；
- 超过阈值的 token 比例为 `2.37%`。

**关键点：双峰比分布长尾更重要。** 如果只是所有 token 的范数随语义强弱连续变化，很难划定 artifact；两个明显群体使作者可以把 token 分为 normal / outlier，随后分别做 probing。

### 阈值的边界

论文明确说明 `150` 是手工选择且随模型而变。因此：

- `norm > 150` 不是可跨模型直接复用的判据；
- “约 10 倍”“约 2%”是所分析模型上的经验量级，不是 ViT 定律；
- 跨模型部署时应先检查各自的范数分布，再定阈值，或使用分位数/双峰拟合等相对标准。

---

## 三、Fig. 4：这种行为在哪里、何时、以什么规模出现

### 1. 沿网络深度：大约第 15/40 层开始分叉

> *"These high-norm patches seem to differentiate themselves from other patches around layer 15 of this 40-layer ViT."*

Fig. 4a 展示 DINOv2 ViT-g 的 token 范数沿层数演化。前十余层只有一个主体分布；大约到第 15 层，高范数支路开始与普通 token 分离，之后差距持续放大。

这排除了一个简单解释：artifact 不是 patch embedding 一开始就产生的异常尺度，而是 Transformer 中层以后形成的内部状态。

### 2. 沿训练时间：约三分之一训练后出现

Fig. 4b 中，训练初期 token 仍属于同一范数群体；约完成全程三分之一后才出现离群分支。这说明它：

- 不是随机初始化直接带来的结构；
- 不是第一次前向传播就必然存在的数值病态；
- 更像模型在优化过程中逐渐学到的一种计算策略。

“训练足够久”仍只是相关条件。论文没有定位到某个具体 loss term、数据阶段或优化事件使分支突然出现。

### 3. 沿模型规模：DINOv2-L/H/g 出现，T/S/B 不明显

Fig. 4c 比较 Tiny、Small、Base、Large、Huge、giant，只有 `L/H/g` 三个较大模型出现明显高范数群体。这支持标题所针对的是**大规模、充分训练的 ViT**，而不是任何尺寸的 ViT。

但这里也不要过度作因果解读：模型规模变化同时改变了深度、宽度、优化动力学和容量。该图证明“artifact 与规模相关”，没有单独证明“参数量本身是根因”。此外 DeiT-III、OpenCLIP 在 B/L 尺寸也会出现离群，说明训练范式会改变门槛。

---

## 四、Fig. 5a：模型为什么挑中这些位置

### 原文 2：outlier 对应输入中高度冗余的 patch

> *"We observe that high-norm tokens appear on patches that are very similar to their neighbors."*

作者先在**最终输出**用 `norm > 150` 找到 outlier 的位置，再回到 Transformer 的入口，在 patch embedding 刚完成时，计算该位置与上下左右 4 个邻居的余弦相似度。

Fig. 5a 的结果：

- normal patch 的邻域相似度分布很宽；
- 最终会成为 artifact 的 patch，在输入端就几乎都与邻居高度相似，分布尖锐集中在 `1` 附近。

这项设计很关键：它测的是 token 尚未经过 Transformer 全局混合时的局部冗余度。因此支持如下时间顺序：

```text
某个输入区域本来就高度均匀/冗余
  → 模型在后续层识别出它的局部内容可以牺牲
  → 对应 token 被改作其他用途
```

可视化中这些位置常是天空、地面、图像边缘等背景，但论文真正量化的是**邻域冗余**，不是依赖人工语义标签证明“它一定是背景”。

---

## 五、Fig. 5b：它们丢掉了什么——局部信息

作者冻结 DINOv2 表示，分别在 normal 与 outlier patch token 上训练简单线性模型，执行两个任务。

### 1. 位置预测

绝对位置 embedding 在第一层前已经加进 token。若最终表示仍保留原 patch 的空间身份，一个线性分类器应能反推出它位于 patch grid 的哪个坐标。

| token | 位置 Top-1 ↑ | 平均坐标距离 ↓ |
|---|---:|---:|
| normal | **41.7** | **0.79** |
| outlier | 22.8 | 5.09 |

outlier 的分类准确率几乎减半，预测坐标平均误差从 `0.79` 增至 `5.09`。这说明原本显式注入的位置线索在 outlier 中已经很难线性读出。

### 2. 输入 patch 像素重建

作者用线性模型从最终 patch embedding 重建其对应的输入像素：

| token | 重建 L2 error ↓ |
|---|---:|
| normal | **18.38** |
| outlier | 25.23 |

outlier 的误差明显更高，说明对应局部外观同样保留得更差。

### 严格措辞

这两个实验能证明的是：**局部位置和像素信息在 outlier 表示中更少线性可读**。它们不能严格证明信息在信息论意义上被彻底删除；一个更强的非线性 decoder 可能仍能恢复部分信息。论文采用线性 probing，是因为研究目标是检查冻结特征能否被轻量下游任务直接使用。

---

## 六、Table 1：它们又获得了什么——全局图像信息

### 实验设计

对每张分类图像：

1. 用 DINOv2-g 提取所有 patch embeddings；
2. 从 normal 或 outlier 集合中随机取**一个** token；
3. 把这个单 token 当作整张图的表示；
4. 训练 logistic regression 预测图像类别；
5. 与 CLS token 的线性分类结果对照。

如果 outlier 仍只表示一小块无信息背景，单靠它不应预测整张图的类别。

### 代表性结果

| 数据集 | normal patch | outlier patch | CLS |
|---|---:|---:|---:|
| ImageNet-1k | 65.8 | **69.0** | 86.0 |
| Aircraft | 17.1 | **79.1** | 87.3 |
| CUB | 18.6 | **84.9** | 91.3 |
| Cars | 10.8 | **85.2** | 91.5 |
| Flowers | 59.5 | **99.6** | 99.7 |
| Pets | 47.8 | **94.1** | 96.9 |
| SUN | 37.7 | **78.5** | 78.6 |
| VOC | 70.8 | **89.7** | 89.1 |

Table 1 的 14 个数据集上，outlier 单 token 的分类准确率都高于 normal 单 token；在 Aircraft、CUB、Cars、Pets、SUN 等数据集上差距极大，部分结果接近 CLS，VOC 上甚至略高于 CLS。

Appendix G / Table 6 对随机选择 token 的过程重复实验并报告标准差，多数标准差较小；这降低了“刚好抽到一个特殊 token”的担忧。

### 该实验支持什么

它强烈支持：outlier 已经不再只编码原来的局部 patch，而包含整张图的语义。结合 Fig. 5b，得到功能替换：

```text
local position / pixels  ↓
global class semantics   ↑
```

但“分类信息多”仍不等于直接观察到了具体的 store/process/retrieve 算法。它也可能来自全局语义被注意力广播到某些 token。作者把这些可能性统一解释为“内部计算寄存器”，其更强验证要看加入专用 token 后行为是否迁移。

---

## 七、从证据到作者假设：哪些已证明，哪些尚未证明

### 原文 3：完整假设

> *"Large, sufficiently trained models learn to recognize redundant tokens, and to use them as places to store, process and retrieve global information."*

**直译：** 大而且训练充分的模型学会识别冗余 token，并把它们用作存储、处理和取回全局信息的位置。

把这句话拆开：

| 命题 | 证据强度 | 理由 |
|---|---|---|
| outlier 是范数离群 | 已直接证明 | Fig. 3 |
| 行为在训练中、网络中层以后涌现 | 已直接证明 | Fig. 4a-b |
| 大模型更容易出现 | 有相关性证据 | Fig. 4c，但规模因素未隔离 |
| 模型优先占用冗余 patch | 有较强证据 | 最终 outlier 的输入邻域相似度接近 1 |
| outlier 丢失局部信息 | 有线性可读性证据 | 位置预测、像素重建 |
| outlier 聚合全局信息 | 有较强线性分类证据 | 14 个数据集 Table 1 / 6 |
| 它们执行“存储、处理、取回”全过程 | 合理解释，未直接跟踪 | 没有逐层因果 tracing 或读写操作识别 |
| 训练为什么产生这种策略 | 未解决 | 作者在 §2.2 明确承认 |

所以本篇最严谨的表述不是“作者证明了 ViT 内部存在某种具体 CPU 式寄存器”，而是：**多组互补探针表明少数空间 patch token 发生了从局部表征到全局计算载体的功能替换；“register”是对这一功能最简洁的命名。**

---

## 八、第二站小结

| 诊断维度 | 结果 |
|---|---|
| 数值形态 | DINOv2 patch token 范数呈双峰；示例中 2.37% 超过人工阈值 150 |
| 网络时间 | 40 层 ViT-g 约第 15 层开始分叉 |
| 训练时间 | 约训练三分之一后涌现 |
| 模型规模 | DINOv2-L/H/g 明显，T/S/B 不明显；仅为相关性证据 |
| 输入位置 | 最终 outlier 对应的输入 patch 与四邻域余弦相似度接近 1，内容高度冗余 |
| 局部信息 | 位置 Top-1 `41.7→22.8`、平均距离 `0.79→5.09`、像素重建误差 `18.38→25.23` |
| 全局信息 | 14 个数据集上，随机单个 outlier token 分类均优于随机 normal token，常接近 CLS |
| 最强结论 | 少数 patch token 发生“局部空间表示 → 全局计算载体”的功能替换 |
| 未决问题 | 具体训练诱因，以及 token 内部如何执行 store/process/retrieve 尚未被直接证明 |

### 自检小问题

1. 为什么 Fig. 3 的双峰分布比一条普通长尾更有诊断价值？
2. Fig. 4 能否证明参数量是 artifact 的根因？为什么？
3. Fig. 5a 为什么要回到 patch embedding 后、Transformer 处理前测邻域相似度？
4. 位置预测和像素重建变差，严格来说证明的是“信息消失”还是“线性可读性下降”？
5. Table 1 为什么只用一个随机 patch token 做图像分类？
6. 从 Table 1 能否直接推出 outlier 执行了明确的“写入—处理—读取”算法？
7. 到此为止，“内部寄存器”解释还缺哪一个最关键的干预证据？

---

> 下一站：[03_方法_register_token.md](./03_方法_register_token.md)——把 register 的插入位置、训练与推理行为、数量消融和计算开销拆开，并检查 Fig. 15 / Table 4 是否真的证明 high-norm 与全局信息被专用 token 接走。

