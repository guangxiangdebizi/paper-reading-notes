# Registers 精读笔记 04：实验、边界与 LAST-ViT

> 论文：**Vision Transformers Need Registers**  
> 本站对应原文 §3.2–3.4、§5 与 Appendices A、C、E–H；关键证据：Tables 2–3，Figs. 10–14、17–21  
> 关键页面：`../figures/page_7.png`、`../figures/page_8.png`、`../figures/page_12.png`、`../figures/page_13.png`、`../figures/page_16.png`、`../figures/page_19.png` ~ `page_21.png`

---

## 一、先规定验收标准

register 方法如果有效，应同时满足三层目标：

1. **表示层**：high-norm patch 消失，注意力图、PCA 特征图和范数图变平滑；
2. **安全层**：修复 artifact 不能破坏 CLS 分类和正常 patch 的局部信息；
3. **任务层**：直接依赖局部特征的分割、深度、无监督目标发现应改善。

前两层在第 3 站已经基本成立。本章重点检查第三层：视觉上变干净是否真的转化成下游收益，以及是否对所有任务、所有训练范式都成立。

---

## 二、Table 2：常规分类与密集预测——主要结论是“不退化”，不是全面大涨

作者冻结带/不带 registers 的 backbone，再做 ImageNet 线性分类、ADE20k 线性分割与 NYUd 单目深度估计；OpenCLIP 另测 zero-shot 分类。

### 完整结果

| 训练范式 | 模型 | ImageNet Top-1 ↑ | ADE20k mIoU ↑ | NYUd RMSE ↓ |
|---|---|---:|---:|---:|
| 标签监督 | DeiT-III | 84.7 | 38.9 | **0.511** |
|  | DeiT-III+reg | 84.7 | 39.1 | 0.512 |
| 文本监督 | OpenCLIP | **78.2** | 26.6 | 0.702 |
|  | OpenCLIP+reg | 78.1 | 26.7 | **0.661** |
| 自监督 | DINOv2 | 84.3 | 46.6 | 0.378 |
|  | DINOv2+reg | **84.8** | **47.9** | **0.366** |

OpenCLIP zero-shot ImageNet 为 `59.9 → 60.1`。

### 如何读这张表

- **分类基本不变**：register 没有牺牲全局语义；DINOv2 甚至 `+0.5`；
- **DINOv2 的密集任务稳定改善**：ADE20k `+1.3 mIoU`，NYUd RMSE `0.378→0.366`；
- **OpenCLIP 深度改善明显**，但分类和分割几乎不动；
- **DeiT-III 深度轻微变差**，差值只有 `0.001`。

因此最稳妥的归纳是论文原文所说的：register **不导致性能回退，并在部分场景带来改善**。不能把 Table 2 写成“三范式所有任务全面提升”。

---

## 三、Table 3：LOST 才是最能暴露局部 artifact 的压力测试

LOST 不训练分割头，而是直接依赖冻结 patch 特征之间的相似度和平滑性做无监督目标发现，因此比线性分割头更难自行过滤异常 token。

指标 CorLoc 表示：预测框正确定位目标的图像比例。

| 模型 | VOC07 | VOC12 | COCO20k |
|---|---:|---:|---:|
| DeiT-III | 11.7 | 13.1 | 10.7 |
| DeiT-III+reg | **27.1** | **32.7** | **25.1** |
| OpenCLIP | **38.8** | **44.3** | **31.0** |
| OpenCLIP+reg | 37.1 | 42.0 | 27.9 |
| DINOv2 | 35.3 | 40.2 | 26.9 |
| DINOv2+reg | **55.4** | **60.0** | **42.0** |

### 1. DeiT-III、DINOv2：大幅受益

- DeiT-III：分别 `+15.4 / +19.6 / +14.4`；
- DINOv2：分别 `+20.1 / +19.8 / +15.1`。

这与论文机制吻合：LOST 直接消费局部相似度结构，孤立 high-norm patch 会破坏种子选择和扩张；register 隔离离群后，局部图变平滑，收益远大于普通线性评估。

### 2. DINOv2+reg 仍没有完全追上 DINO-v1

论文引用的 DINO-v1 在 VOC07 上为 `61.9 CorLoc`，DINOv2+reg 为 `55.4`。也就是说，register 修复了 DINOv2 相对自身的大部分问题，但没有恢复 DINO-v1 的全部无监督发现能力。

这是后续继续研究的明确信号：high-norm artifact 不是 DINO 与 DINOv2 局部行为差异的完整解释。

### 3. 协议不是完全同构

LOST 对 DeiT/OpenCLIP 使用 attention values，对 DINOv2 使用 keys；由于不同特征 conditioning，作者还手工给 Gram matrix 加 bias。该评估遵循各模型适用的工程配置，但意味着表中并非“完全相同输入表示、只改变 register”的统一协议。

---

## 四、最重要的反例：OpenCLIP 变干净了，LOST 反而略降

OpenCLIP 加 register 后，VOC07/12/COCO20k 分别下降 `1.7 / 2.3 / 3.1`。这直接否定了一个过强命题：

> 错误命题：只要存在 high-norm artifact，它就必然伤害任何下游任务；只要消除它，所有任务都会提高。

Appendix C 给出解释。OpenCLIP 无 register 时：

- keys、queries 的 LOST 相似度图上能看到异常亮点；
- values 产生的图本来就比较平滑；
- 加 register 后 K/Q/V 都更干净，但 LOST 实际使用的 value 表示此前已过滤掉离群。

作者据此推测 high-norm outlier 主要落在 OpenCLIP `W_V` 投影的零空间中：

```text
原始特征 / K / Q 中有 artifact
              ↓ W_V
value 表示中已被过滤
              ↓
LOST 没有被该 artifact 明显伤害
```

所以“表示中存在异常”与“某个下游路径实际消费到异常”必须分开。诊断下游失败时要跟踪真实使用的是输出 token、K、Q 还是 V，不能只看一张 attention 可视化就归因。

---

## 五、两个没有明显 artifact 的 ViT：DINO-v1 与 MAE

### 1. DINO-v1：现代 ViT 的例外

Fig. 2 显示 DINO-v1 注意力图平滑，而 DeiT-III、OpenCLIP、DINOv2 都有尖锐响应。作者因此把 DINO-v1 视为例外，而非把 DINOv2 当作唯一异常模型。

这说明：

- self-supervision 本身不会必然产生 high-norm token；
- 模型规模、训练长度和具体预训练目标共同影响现象；
- 论文只观察到条件关联，没有完全确定哪一项训练设计是根因。

### 2. MAE：局部重建目标可能阻止 token 被挪作他用

Appendix E 的 MAE ViT-L PCA 特征图没有明显 artifact。作者的假设是：MAE 的预训练损失直接作用于 patch 的局部重建，而不是依靠全局信息聚合；每个可见 token 更需要保留空间/像素信息，因此模型不能轻易牺牲某些 patch。

但这是跨方法观察，不是受控消融。MAE 的目标、掩码策略、decoder、训练配方都与 DINOv2 不同，不能仅据 Fig. 17 证明“局部 loss 就是唯一原因”。

论文同时指出 MAE ViT-L 的 frozen linear probing 约为 `75%`，通常需要 fine-tuning。这不与 MAE 论文的强迁移结果矛盾：MAE 擅长的是**微调后性能**，Registers 此处讨论的是**冻结特征直接使用**。

---

## 六、Appendix A：一种 artifact 上还叠着另一种插值 artifact

官方 DINOv2 的 outlier 位置频率图曾呈现明显竖条纹。作者追踪到：训练时把位置编码从 `16×16` 双三次插值到 `7×7`，未使用 antialiasing；梯度传播会产生类似条纹。

在本文重新训练、用于 Tables 2–3 的 DINOv2 中，作者给插值加入 antialiasing：

- 竖条纹消失；
- high-norm outlier 仍然存在；
- outlier 更偏向特征图边缘。

这一区分很重要：

```text
竖条纹空间分布 = 位置编码插值实现造成的混杂 artifact
high-norm 离群    = 加 antialias 后仍存在的表示行为
```

作者把边缘偏好解释为 ImageNet 类数据多为中心构图，边缘更常是低信息背景。这是符合数据分布的解释，但仍是统计关联，不代表任意图像的边缘都没有语义。

---

## 七、其他定性证据应如何使用

### 1. 所有 attention heads 都会受到影响

Appendix F 显示最后一层各 attention head 都能看到 artifact，只是强弱不同。因此它不是移除某一个坏 head 就能解决的局部故障。

### 2. 三类可视化一致变干净

Appendix H 分别展示：

- Fig. 19：CLS-to-patch attention maps；
- Fig. 20：输出特征前三个 PCA 分量；
- Fig. 21：patch token norm maps。

DeiT-III、OpenCLIP、DINOv2 加 register 后，三类图都更连续、孤立亮点更少。这种跨可视化一致性排除了“只是某一种画图方法造成”的简单解释。

但“更平滑、更好看”不是独立的语义正确性指标，仍需 Table 2/3 的任务结果验证；OpenCLIP LOST 反例正说明可视化改善不保证目标指标上升。

---

## 八、论文明确没有解决的事情

| 未解决项 | 具体边界 |
|---|---|
| 训练根因 | 作者明确承认尚未完全确定哪些训练因素导致 artifact；只观察到训练范式、规模、训练长度相关 |
| 通用阈值 | `norm > 150` 是 DINOv2-g 上的人工阈值，不能直接跨模型使用 |
| 免重训修复 | 实验均从训练阶段加入 registers；没有证明向既有模型事后插 token 即可修复 |
| register 数量理论 | 4 是经验折中；不同任务的最优数量不同 |
| register 分工 | 有定性注意力差异，但没有稳定性、解耦度或跨随机种子量化 |
| 全任务收益 | OpenCLIP LOST 下降；DeiT 深度轻微下降；不是所有指标单调改善 |
| 因果根源 | 证明了 high-norm 功能可被隔离，没有证明背景全局语义最初为什么产生、何时开始污染 |

---

## 九、与 LAST-ViT 的边界：不是谁推翻谁，而是问题定义扩大了

两篇论文使用了不同的 artifact 定义和成功标准：

| 维度 | Registers（ICLR 2024） | LAST-ViT（CVPR 2026） |
|---|---|---|
| 主要异常 | 少数 patch token 范数离群，破坏特征/注意力图平滑性 | 高 Patch Score 落在语义无关背景，局部与全局语义错位 |
| 诊断量 | 输出 patch token L2 norm | patch 与 CLS 余弦相似度；Point-in-Box |
| 时间判断 | high-norm 在训练约三分之一后、中层以后出现 | 背景主导偏向在训练早期已经出现并持续 |
| 机制解释 | 模型复用冗余 patch 存储/处理全局信息；具体训练诱因未明 | 粗粒度监督提供捷径动机，全局注意力提供语义扩散通道，形成 lazy aggregation |
| 解法 | 添加专用 register，隔离被复用的 patch | 频域稳定度筛选 patch，选择性构造 CLS，改变聚合行为 |
| 成功标准 | high-norm patch 消失、图变平滑、部分密集任务/LOST 改善 | 高分 patch 重回前景、PiB 与多类密集任务改善 |

LAST-ViT 的关键补充是：**high-norm 可能只是 lazy aggregation 的后期极端表象。** 即使 register 把极端离群值接走，背景 patch 在更早阶段承载全局语义的格局仍可能存在。其 Table 1 中标签监督 ViT 加 register 后 PiB `42.7→41.5`，就是“norm 修好了但前景对齐未修好”的证据。

因此主线 D 的完整因果链是：

```text
Registers:
发现症状 → 定量定位 high-norm patch → 证明局部/全局功能替换
         → 用专用 token 隔离症状

LAST-ViT:
追问症状之前发生了什么 → 定义跨范式的背景错位
                      → 提出 lazy aggregation 根因
                      → 直接修改 CLS 聚合规则
```

Registers 的贡献没有因此失效：它准确发现并修复了一种真实、可量化、会伤害部分密集任务的表示异常；LAST-ViT 则证明该异常不是整个问题的最早阶段，也不是唯一验收指标。

---

## 十、全文终局判断

### 最强贡献

这篇论文最有价值的不是“多加 4 个 token”，而是完整执行了一次表示行为研究：

```text
异常可视化
→ 范数检测
→ 层/训练/规模定位
→ 局部与全局信息 probing
→ 机制假设
→ 架构干预
→ 行为迁移验证
→ 下游任务检验
```

### 最准确的一句话

**大而且训练充分的 ViT 会把少数输入冗余的 patch token 从局部空间表示复用为高范数全局计算载体；加入若干不对应图像位置、输出时不用的可学习 register token，能够以很小成本把该行为从 patch 集合中隔离出去，使特征图更平滑并显著改善部分直接依赖局部相似度的任务，但并非所有下游任务都会获益，也没有解释更早形成的背景语义错位。**

### 自检小问题

1. 为什么 Table 2 更支持“不退化并偶有提升”，而不是“三范式全面提升”？
2. LOST 为什么比线性分割头更适合作为 artifact 的压力测试？
3. OpenCLIP 的特征图变干净，LOST 为什么没有提高？
4. DINOv2+reg 为什么仍低于 DINO-v1 的 VOC07 CorLoc？这说明什么？
5. MAE 没有明显 artifact，为什么还不能直接证明“局部重建 loss 是根因”？
6. 位置编码插值造成的竖条纹与 high-norm artifact 是什么关系？
7. Registers 与 LAST-ViT 对“artifact 已修复”的验收标准分别是什么？
8. 为什么说 LAST-ViT 扩大了问题定义，而不是推翻 Registers？

