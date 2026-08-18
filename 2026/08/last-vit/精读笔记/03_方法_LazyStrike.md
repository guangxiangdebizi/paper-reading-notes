# LAST-ViT 精读笔记 03：方法 LazyStrike

> 论文：**Vision Transformers Need More Than Registers**（CVPR 2026 · arXiv:2602.22394v2）
> 对应原文 §5（Method，含 §5.1 LaSt-ViT、§5.2 Transfer to Downstream Tasks）
> 图片：`../figures/page_5.png`（Eq.4-8 与 Fig 5 所在区域）、`../figures/page_6.png`（Fig 6 + Table 3）

本站讲 §5 的完整方法：设计动机（为什么选频域）、稳定度分数（Eq.4-5）、逐通道 Top-K 池化（Eq.6-7）、vote count（Eq.8）、聚合行为的可视化验证（Fig 5）、以及方法在下游任务上的三种使用方式（§5.2）。

---

## 一、设计动机：为什么用频域手段筛选 patch

### 原文 1（总览与原理）

> *"Overview and Rationale. To mitigate lazy aggregation, we reformulate CLS token aggregation as a frequency-aware process that distinguishes foreground patches from background ones. In natural images, foreground signals have more homogeneous semantic meaning, giving rise to less variations along the channel dimension of a feature map in a deep layer, whereas background often has higher semantic diversity; thus selecting tokens that are stable under low-pass filtering in the channel dimension can potentially anchor CLS tokens to foreground regions."*

**直译：** **总览与原理。** 为缓解懒惰聚合，我们把 CLS token 聚合重新表述为一个**频率感知的过程**，以区分前景 patch 与背景 patch。在自然图像中，前景信号具有更同质（homogeneous）的语义含义，在深层特征图沿**通道维**产生较少的变化；而背景往往具有更高的语义多样性。因此，选择在通道维低通滤波下保持稳定的 token，有望把 CLS token 锚定到前景区域。

**解读：** 方法的核心假设是一条可检验的前景/背景判别准则，拆开看：
1. **前景同构性**：一个目标的多个 patch（狗头的不同部位）在深层特征空间中语义接近——它们描述的是同一个东西，特征沿通道维的变化平缓；
2. **背景异构性**：背景由各种不相干的物体、纹理、区域拼成，单个 patch 与邻居之间语义跳跃大，特征沿通道维变化剧烈；
3. **判别手段**：低通滤波的作用是压制高频变化。一个 patch 若滤波前后几乎不变（低频主导、变化平缓），说明它处于语义同质的区域——判为前景候选；若滤波前后差异大（高频成分多），判为背景。

为什么沿**通道维**做滤波而不是沿空间维：每个 patch 是一个 D 维向量（ViT-B 为 768 维），把通道序列当作一维信号做 FFT，是对"单个 token 内部各通道响应的一致性"做频域刻画，不需要空间邻域结构，天然适配 ViT 的 token 序列形式（patch 在序列中的排列顺序与空间位置无直接卷积关系）。

这个准则与第 2 站的两条干预实验形成呼应：加大 patch 与窗口注意力都是通过**改变信息结构**来削弱背景捷径，代价是伤精度；频域筛选则不动 token 数量、不动注意力范围，只在**聚合环节**（CLS 的构造）做选择，把背景 patch 排除在 CLS 之外——背景 patch 依然存在、依然参与自注意力，只是不再被 CLS 读取。这是"保精度"的关键。

---

## 二、§5.1 LaSt-ViT：四步管线

记号：x_patch ∈ R^(N×D) 为 ViT encoder 输出的全部 patch 表示（丢弃 [CLS] 后），N 为 patch 数、D 为通道数。

### 步骤一：通道维低通滤波（Eq.4）

### 原文 2（滤波管线）

> *"Stability Score. Let x_patch ∈ R^(N×D) denote the collection of all patch representations generated from the ViT encoder (after dropping [CLS]) and let g ∈ [0,1]^D be a normalized vector of Gaussian weights duplicated to all patches:*
>
> *x_FFT = FFT1D(x_patch),*
> *x_LP = x_FFT ⊙ g,*
> *x̂_patch = Re{IFFT1D(x_LP)}, (4)*
>
> *where FFT1D and IFFT1D respectively represent the 1D Fourier transform and the 1D inverse Fourier transform in the channel dimension of every patch, ⊙ is element-wise multiplication, and Re{·} extracts the real part."*

**直译：** **稳定度分数。** 设 x_patch ∈ R^(N×D) 为 ViT encoder 生成的全部 patch 表示（丢弃 [CLS] 后），g ∈ [0,1]^D 为一个归一化的高斯权重向量，复制到所有 patch：x_FFT = FFT1D(x_patch)，x_LP = x_FFT ⊙ g，x̂_patch = Re{IFFT1D(x_LP)}。其中 FFT1D 与 IFFT1D 分别表示对每个 patch 沿通道维的一维傅里叶变换与一维逆傅里叶变换，⊙ 为逐元素乘法，Re{·} 取实部。

**解读：** Eq.4 是标准的"变换域乘积 = 低通滤波"三步管线：
1. **FFT1D**：把每个 patch 的 D 维通道向量变换到频域。每个 patch 独立做，互不干扰；
2. **⊙ g**：与一个固定的高斯型权重逐元素相乘。g 沿频率轴呈高斯形状（低频处接近 1、高频处衰减到接近 0），且**对全部 patch 使用同一个 g**（"duplicated to all patches"）——即滤波器不随内容自适应，所有 patch 用同一把尺子量；g 是归一化的（取值 [0,1]），保证低频成分不被放大、只衰减高频；
3. **IFFT1D + 取实部**：变换回通道域，得到滤波后的 x̂_patch。

滤波后，x̂_patch[i,:] 是 patch i 的"低频版本"——只保留其通道响应中变化平缓的成分。

### 步骤二：稳定度分数（Eq.5）

### 原文 3（逐通道稳定度）

> *"The channel-wise stability score compares individual channels of original and low-pass-filtered patch representations:*
>
> *S_{i,j} = x̂[i,j] / (|x̂[i,j] − x[i,j]| + ε), (5)*
>
> *where i is the patch index and j is the channel index."*

**直译：** 逐通道稳定度分数比较原始与低通滤波后 patch 表示的各个通道：S_{i,j} = x̂[i,j] / (|x̂[i,j] − x[i,j]| + ε)，其中 i 是 patch 索引、j 是通道索引。

**解读：** Eq.5 把"滤波前后差异"转化为分数，结构是**信号 / 失真**的形式：
- **分子 x̂[i,j]**：滤波后保留下来的低频成分幅值——patch i 在通道 j 上的"稳定部分"有多大；
- **分母 |x̂[i,j] − x[i,j]| + ε**：滤波去掉的那部分（高频失真）的绝对值加一个小常数 ε 防除零——patch i 在通道 j 上被滤掉的变化有多大；
- **分数的语义**：一个通道上，若 patch 的响应以低频为主（滤波几乎不改变它），分子大、分母小，分数高——该 patch 在该通道上"稳定"；若响应含大量高频成分（滤波前后差异大），分数低。

注意这是**逐通道**的分数（j 从 1 到 D 各自独立计算），不是把整个 patch 压成一个标量——这为下一步"每个通道各自选 patch"留下了结构。

### 步骤三：逐通道 Top-K 池化构造 CLS（Eq.6-7）

### 原文 4（选择性聚合）

> *"Channel-wise Top-K Pooling. Using channel-wise stability scores, we aggregate patch representations into the CLS token by selecting, for each channel, the K most stable patches (tokens) and averaging them:*
>
> *I_K(j) = TopK({S_{i,j}}_{i=1}^{N}, K), j = 1,...,D, (6)*
>
> *Q_CLS[j] = Pool_K(x_patch[:,j]; S[:,j]) ≜ (1/K) Σ_{i∈I_K(j)} x_patch[i,j], j = 1,...,D, (7)*
>
> *where I_K(j) represents the index set of the K patches with the highest stability scores in the j-th channel."*

**直译：** **逐通道 Top-K 池化。** 利用逐通道稳定度分数，我们通过为每个通道选择 K 个最稳定的 patch（token）并对其取平均，把 patch 表示聚合进 CLS token：I_K(j) = TopK({S_{i,j}}_{i=1}^{N}, K)，j = 1,...,D；Q_CLS[j] = Pool_K(x_patch[:,j]; S[:,j]) ≜ (1/K) Σ_{i∈I_K(j)} x_patch[i,j]，j = 1,...,D。其中 I_K(j) 表示第 j 个通道上稳定度分数最高的 K 个 patch 的索引集合。

**解读：** 这两式定义了新的 CLS token 构造规则，替换 ViT 原有的全局平均池化（式 1）或 CLS query（式 2）：
1. **每个通道独立选人**：对通道 j，在全部 N 个 patch 的稳定度分数 {S_{1,j}, ..., S_{N,j}} 中取 Top-K，得到索引集 I_K(j)。不同通道选出的 K 个 patch **可以不同**——通道 1 可能选中 patch {3, 17, 42}，通道 2 选中 {17, 42, 88}；
2. **聚合用原始特征**：注意 Eq.7 平均的是**原始** x_patch[i,j] 而不是滤波后的 x̂——滤波只用于"选人"（决定谁有资格进 CLS），进 CLS 的值仍是未失真的原始特征，表示的信息量不受低通压缩；
3. **对照标准做法**：GAP 是对全部 N 个 patch 无差别平均（K=N 且不看稳定度）；LazyStrike 是 K<N 且按稳定度筛选。K=N 时退化为对稳定度排序的全量平均——第 4 站 Table 8 的 K=196 (Full) 行正是这个退化情形，其下游表现跌回未筛选水平，证明收益来自"选择"而非"平均方式"本身；
4. **K 的取值**：第 4 站 Table 8 消融显示 K 取 N/2（选一半 token）时下游表现最好——选太少（K=1）信息量不足，选太多（接近 N）背景又混进来。

### 步骤四：vote count（Eq.8）

### 原文 5（票数统计）

> *"Vote Count. We define the vote count of token (patch) i as*
>
> *v_i ≜ Σ_{j=1}^{D} 1{i ∈ I_K(j)}, i = 1,...,N, (8)*
>
> *where 1{·} denotes the indicator function. A larger v_i indicates a greater importance of patch i among all patches."*

**直译：** **票数统计。** 我们把 token（patch）i 的票数定义为 v_i ≜ Σ_{j=1}^{D} 1{i ∈ I_K(j)}，i = 1,...,N，其中 1{·} 是指示函数。更大的 v_i 表示 patch i 在所有 patch 中更重要。

**解读：** vote count 是对"逐通道选人"结果的汇总视图：
- **构造**：patch i 每被一个通道选中就记一票，对全部 D 个通道求和。v_i 的取值范围是 [0, D]；
- **语义**：v_i 高意味着 patch i 在**许多通道上同时稳定**——它不是某个通道的偶然入选者，而是跨通道一致的前景候选。这比单看某个通道的入选与否稳健得多；
- **用途**：① 可视化（Fig 5 直接按 v_i 画前景掩码）；② 下游无监督定位（第 4 站 Table 7 的 DINO+LazyStrike 定位结果即基于此类 patch 级分数构造掩码）；③ 诊断工具——v_i 的空间分布就是"CLS 在看哪里"的直接读数。

---

## 三、聚合行为的可视化验证（Fig 5）

### 原文 6（CLS 看向哪里）

> *"Where does the CLS token in LaSt-ViT look at? After the application of LaSt-ViT, the highly voted patches are better aligned with the foreground regions and the number of such patches increases or decreases with the amount of foreground evidence (see Fig. 5), indicating that the model has learned to anchor the CLS token to the foreground patches."*

**直译：** LaSt-ViT 中的 CLS token 看向哪里？应用 LaSt-ViT 后，高票 patch 与前景区域更好地对齐，且此类 patch 的数量随前景证据的多少而增减（见图 5），表明模型已经学会把 CLS token 锚定到前景 patch。

**解读：** Fig 5 的可视化协议：对每张图，把 vote count 超过**该图内最大票数的 50% / 30% / 20%** 的 patch 分别标红（左、中、右三档阈值）。验证包含两层：
1. **空间对齐**：标红的 patch 落在前景目标上——对照第 2 站 Fig 2a（高分由背景主导），聚合对象发生了翻转；
2. **数量随内容自适应**：目标占画面比例大的图，高票 patch 多；目标小的图，高票 patch 少——筛选不是固定数量地选，而是跟随图中真实的前景证据量变化。这一点说明稳定度分数确实编码了"内容属性"（前景/背景），而不是位置先验。

这组可视化在论证结构中的地位：它是方法有效性的**机制级证据**——不仅下游指标涨了（第 4 站），而且涨的原因确实是"CLS 重新锚定前景"这一预期机制在起作用。

---

## 四、方法的三项"无需"与训练期介入

方法的设计约束可以概括为三项"无需"（对应引言相关工作段的对照定位）：

1. **无需架构改动**：encoder、patch embedding、注意力层全部保持标准 ViT 形式；改变的只有 CLS token 的构造规则（从 GAP/CLS query 换成 Eq.6-7 的选择性聚合）。Eq.4-5 的 FFT/IFFT 与逐元素运算是无参数的前向算子；
2. **无需后训练（post-hoc fine-tuning）**：方法在预训练期启用——模型从一开始就在新聚合规则下学习，监督信号（分类头/文本对比/自蒸馏）直接作用于选择性聚合产生的 Q_CLS，梯度回传迫使 encoder 学会"把前景 patch 变得稳定、把语义集中进前景"；
3. **无需测试期干预**：不存在推理时的激活编辑、注意力重算或额外 token 管理。

对照第 1 站相关工作：CLIP 系三类修补（改注意力层 = 架构改动；对齐训练 = 后训练；激活编辑 = 测试期干预）各占一条，Registers 的 register token 属架构改动。LazyStrike 的差异在于**干预发生在聚合规则的层面、且在训练期内生效**——lazy behavior 没有被事后清理，而是在优化起点就没有形成条件（背景 patch 无法通过进入 CLS 来兑现分类收益，捷径不再成立）。

训练期的介入方式还有一个重要性质：Eq.6-7 的选择操作使 CLS 对入选 patch 的子集敏感，入选标准（稳定度）又依赖 encoder 输出，因此 encoder 收到了一种隐式的结构化压力——要让全局损失下降，它需要让真正的前景 patch 在稳定度排序中占据高位。Fig 5 的"自动转向"就是这一压力下的学习结果。

---

## 五、high-norm 现象的顺带消除（Fig 6）

### 原文 7（特征范数分析）

> *"Tab. 3 presents the results under different training methods, demonstrating that LazyStrike not only eliminates the high-norm phenomenon but also enhances Point-in-Box score. With LazyStrike applied, ViT's Point-in-Box score approaches that of ResNet [11]. Fig. 6 provides a detailed analysis of feature norms under fully supervised training [34], revealing that LazyStrike reduces the maximum feature values, thereby mitigating the high-norm phenomenon."*

**直译：** 表 3 给出了不同训练方法下的结果，表明 LazyStrike 不仅消除了 high-norm 现象，还提升了 Point-in-Box 分数。应用 LazyStrike 后，ViT 的 Point-in-Box 分数逼近 ResNet [11]。图 6 提供了全监督训练 [34] 下特征范数的详细分析，揭示 LazyStrike 降低了特征的最大值，从而缓解 high-norm 现象。

**解读：** Fig 6 在全监督 ViT 上对比有无 LazyStrike 的特征范数分布：应用后，特征最大范数显著下降，high-norm token 消失。这在论证链上是**根因-表象关系的直接检验**：
- 第 1 站的论断是"high-norm 只是 lazy behavior 的后期表象"；
- Table 1 的反证是"消除 high-norm（加 register）不能修复 PiB"（表象没了、病还在）；
- Fig 6 提供正向证据："修复根因（聚合行为）后，high-norm 自动消失"（病好了、表象随之没了）。

两个方向的证据合起来，"Vision Transformer requires more than just Registers" 的论证闭合：register 治表象不治病，LazyStrike 治病后表象自愈。

---

## 六、§5.2 下游任务的使用方式

### 原文 8（三种下游用法）

> *"Unsupervised Object Discovery. Since LazyStrike guides the CLS token to focus on foreground objects, we can achieve unsupervised object localization using patch scores. This expansion is independent of the training method--typically a privilege of self-supervised approaches like DINO in earlier works--allowing any training objective to accomplish this. We construct the mask by applying a threshold defined as the mean score plus one standard deviation. Patches with scores above this threshold are classified as foreground."*

**直译：** **无监督目标发现。** 由于 LazyStrike 引导 CLS token 聚焦前景目标，我们可以用 patch score 实现无监督目标定位。这一扩展独立于训练方法——在先前工作中通常是 DINO 等自监督方法的特权——使任何训练目标都能完成该任务。我们通过施加一个定义为均值分数加一个标准差的阈值来构造掩码。分数高于该阈值的 patch 被归为前景。

**解读：** 第一个用法：无监督目标定位。技术细节——阈值 = 全图 patch score 的均值 + 1 倍标准差，超过阈值的 patch 判为前景。这个规则零训练、零标注，只依赖"前景 patch 分数显著高于背景"这一分布形状；而该分布形状正是 LazyStrike 修复的对象（修复前高分尾部被背景占据，此规则会失效）。"先前是自监督方法的特权"指 DINO 论文（[1]）首次展示的目标发现涌现性质——本文把它扩展到任意监督范式（第 4 站 Table 6/7 的实验对象包含监督 ViT）。

> *"Zero-shot Open-Vocabulary Tasks. Since LazyStrike ensures that the CLS feature aggregates information from the correct patch features, and the CLS feature itself is directly supervised by the learning signal, this effectively leads to an implicit alignment between patch features and the supervision signal. For text-supervised ViTs, we can obtain zero-shot semantic segmentation results by computing the similarity between patch features and arbitrary text features, thereby enabling applications across various open-vocabulary tasks."*

**直译：** **零样本开放词汇任务。** 由于 LazyStrike 保证 CLS 特征从正确的 patch 特征聚合信息，而 CLS 特征本身又直接受学习信号监督，这实际上导致了 patch 特征与监督信号之间的**隐式对齐**。对文本监督的 ViT，我们可以通过计算 patch 特征与任意文本特征的相似度获得零样本语义分割结果，从而支持各种开放词汇任务的应用。

**解读：** 第二个用法：零样本开放词汇分割。推理链是一个三段传递：
1. 训练时，CLIP 式对比损失直接监督 Q_CLS 与文本嵌入对齐——Q_CLS 是与文本"官方对齐"的特征；
2. LazyStrike 下，Q_CLS = 被选中的前景 patch 特征的平均——即这些 patch 的特征**平均意义上等于**与文本对齐的那个向量；
3. 因此，即使没有任何 patch 级监督，被选中的 patch 特征也继承了与文本的可比性——直接拿单个 patch 特征与文本嵌入算相似度，即可得到逐 patch 的类别响应图，实现零样本分割。

这个"隐式对齐"论证是文本监督实验（第 4 站 Table 4/5）的理论支撑：修复聚合 → patch 特征继承 CLS 的文本对齐性 → 密集任务受益。第 4 站将看到 VOC 上 mIoU 从 49.0 跳到 75.0（CLIP B/16）等大幅增益，其机制根源就是这条传递链。

---

## 七、第 3 站小结

| 维度 | 内容 |
|---|---|
| 设计动机 | 前景语义同质（通道维变化平缓）、背景语义多样（变化剧烈）→ 用通道维低通滤波下的稳定性区分前景/背景 |
| Eq.4 滤波 | 每个 patch 独立做通道维 1D FFT，与固定归一化高斯权重 g 逐元素相乘（全 patch 共用同一个 g），IFFT 取实部得 x̂_patch |
| Eq.5 稳定度 | S_{i,j} = x̂[i,j] / (|x̂[i,j] − x[i,j]| + ε)：低频保留量 / 高频失真量，逐 patch 逐通道 |
| Eq.6-7 聚合 | 每个通道独立取稳定度 Top-K 的 patch 索引集 I_K(j)，对这些 patch 的**原始**特征取平均得 Q_CLS[j]；不同通道选中的 patch 可不同 |
| Eq.8 vote count | v_i = patch i 被各通道选中的总次数；跨通道一致的前景候选度量；用于可视化与下游定位 |
| K 的取值 | K = N/2（选一半 token）最优（第 4 站 Table 8）；K=N 退化为全量平均、收益消失 |
| 机制验证 | Fig 5：高票 patch 对齐前景、数量随图中前景证据量自适应 → CLS 确实重新锚定前景 |
| 三项无需 | 无架构改动、无后训练、无测试期干预；介入发生在预训练期的聚合规则层面 |
| 与 high-norm 的关系 | Fig 6：修复聚合后 high-norm 自动消失 → high-norm 是表象、lazy aggregation 是根因（与 Table 1 的反证合拢） |
| 下游用法 | ① 无监督目标发现（阈值 = 均值 + 1σ，任意监督范式可用）；② 零样本开放词汇分割（隐式对齐：patch 特征继承 CLS 的文本对齐性） |

### 自检小问题

1. 为什么选择沿通道维做一维傅里叶滤波，而不是沿空间维做二维滤波？这与 ViT 的 token 结构有什么关系？
2. Eq.5 的分子与分母分别度量什么？为什么一个"滤波前后几乎不变"的 patch 会得高分？
3. Eq.7 为什么用**原始**特征 x_patch 而不是滤波后特征 x̂_patch 来计算 Q_CLS？滤波在管线中的角色是什么？
4. "每个通道独立选 Top-K"与"先给每个 patch 打一个总分再选 Top-K"相比，结构上的差异是什么？vote count 在两者之间起什么作用？
5. LazyStrike 与第 2 站两种干预（加大 patch、窗口注意力）相比，保精度的关键差异在哪里？（提示：token 数量与注意力范围是否被改变）
6. 方法在训练期介入后，encoder 接收到什么样的隐式优化压力？Fig 5 的哪个观察结果证实了这一压力的效果？
7. "修复聚合 → high-norm 消失"与"消除 high-norm（register）→ PiB 不变"这两条证据合起来证明了什么？
8. 文本监督 ViT 应用 LazyStrike 后，为什么单个 patch 特征可以直接与文本算相似度做零样本分割？（写出三步传递链）

---

> 下一站：[04_实验与结论.md](./04_实验与结论.md)——§6 实验：Table 3（PiB 修复）、Table 4（六个语义分割基准 × 三个 CLIP × 两种规模）、Table 5（OV 检测/分割）、Table 6（粗分割涌现）、Table 7（CorLoc 与 FPS）、Tables 8-9（K 消融与池化方式对照）、§7 结论。
