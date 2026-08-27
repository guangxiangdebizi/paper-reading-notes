# Registers 精读笔记 03：方法——给内部计算一个专用位置

> 论文：**Vision Transformers Need Registers**  
> 本站对应原文 §2.2、§3.2、Appendix B、D；关键证据：Fig. 6–8、12、15–16，Tables 4–5  
> 关键页面：`../figures/page_5.png`、`../figures/page_6.png`、`../figures/page_7.png`、`../figures/page_13.png`、`../figures/page_14.png`、`../figures/page_15.png`

---

## 一、方法本体：只给序列增加 K 个可学习向量

### 原文 1：插入与输出规则

> *"We add these tokens after the patch embedding layer, with a learnable value, similarly to the [CLS] token. At the end of the vision transformer, these tokens are discarded, and the [CLS] token and patch tokens are used as image representations, as usual."*

**直译：** 作者在 patch embedding 层之后加入这些 token，其值可学习，类似 CLS token。在 ViT 末端，这些 token 被丢弃，仍像通常一样使用 CLS token 与 patch token 作为图像表示。

设一张图得到 `N` 个 patch embeddings、隐藏维度为 `d`，新增参数为：

```text
R ∈ R^(K×d)
```

每张图共享同一组可学习初值 `R`。一次前向传播可写成：

```text
P = PatchEmbed(image) + positional_embedding
X0 = concat([CLS], [R1 ... RK], [P1 ... PN])

XL = TransformerBlocks(X0)

downstream_global = XL[CLS]
downstream_dense  = XL[P1 ... PN]
unused_output     = XL[R1 ... RK]
```

官方 DINOv2 实现先给 CLS/patch 加位置编码，再把 registers 插到 CLS 与 patch 之间，因此 register 本身没有图像空间位置编码。它们不对应某个像素块，正适合承担非空间的内部计算。

### 一个容易误读的地方：“末端丢弃”不等于“预训练后从模型中删除”

register token 在**训练和推理的每次前向传播中都必须存在**，并参与每一层 self-attention。“discarded”只表示最后不把它们交给分类、分割、深度等下游头使用。

错误理解：

```text
预训练时有 registers → 训练完把它们从序列中删掉 → 推理不再使用
```

正确理解：

```text
训练与推理都带 registers → Transformer 末端忽略 register 输出
```

如果推理时把 register 输入删掉，其他 token 的注意力上下文也会改变，这已不是论文评估的模型。

---

## 二、它没有直接监督，为什么还能学会

register 输出没有单独的标签、重建目标或辅助损失，但它们参与所有 self-attention：

```text
register → 影响后续 CLS / patch 表示 → 影响原训练损失
         ← 通过这条路径接收梯度
```

因此 registers 是**间接优化**的。模型只有在把它们作为中间计算空间能够降低原有损失时，才会形成有用行为。

这也是该方法论证力较强的地方：作者没有规定“哪个 register 存什么”，也没有对 register 范数、注意力区域或全局语义施加正则；如果它们训练后自动接走 high-norm 与全局分类信息，就支持“模型本来确实需要这种内部空间”。

---

## 三、它与其他特殊 token 有什么本质区别

| token | 输入时提供什么 | 输出是否被使用 | 主要角色 |
|---|---|---|---|
| CLS | 一个可学习查询 | 是，接分类/全局目标 | 聚合最终全局表示 |
| MAE/BERT MASK | “此处内容被遮挡”的结构信息 | 是，需重建/预测 | 表示待预测位置 |
| DETR object query | 可学习查询槽位 | 是，每个输出目标预测 | 产生检测结果 |
| Perceiver latent | 可学习潜变量 | 是，供 decoder 读取 | 压缩和解码输入 |
| memory token | 通常不对应输入位置 | 视方法而定 | 扩展内部工作记忆 |
| 本文 register | 不提供图像内容或空间位置 | **否** | 仅供 Transformer 中间存取信息 |

形式上它最接近 Memory Transformer 的 memory token，创新不在“第一次发明额外 token”，而在新的行为解释：**ViT 原本已经会把普通 patch 当 memory；显式 register 不是创造这种能力，而是把它从空间 token 中隔离出来。**

---

## 四、Fig. 7：跨三种训练范式，patch norm 离群都消失

作者分别训练：

- DeiT-III ViT-B：标签监督，ImageNet-22k；
- OpenCLIP ViT-B/16：图文监督，授权 Shutterstock 图文数据；
- DINOv2 ViT-L：自监督，ImageNet-22k。

每种方法都训练无 register 与有 register 两个版本。Fig. 7 比较最终 patch token 的范数分布：三种模型加入 registers 后都不再出现原来的高范数 patch 离群群体。

这说明方案并不依赖 DINOv2 的某个特定损失。但图中三种模型的纵轴范围不同，只能在每种训练方法内部比较前后变化，不能直接用绝对范数判断哪种范式“artifact 更严重”。

---

## 五、Fig. 8：需要几个 register

作者用 DINOv2 ViT-L/14 分别训练 `K = 0, 1, 2, 4, 8, 16`。

### 1. 消除可见 artifact：一个就够

Fig. 8 上半部分显示，从 `K=0` 到 `K=1`，原先孤立的尖锐 attention artifact 已基本消失。于是：

> “ViT 需要 registers”并不意味着必须有很多 register；对隔离离群行为而言，一个专用槽位已经能承担大部分作用。

### 2. 下游任务：最优数量不一致

- 分割、深度等密集任务：加入 1 个获得大部分收益，随后在少量 registers 附近出现任务相关甜点位；
- ImageNet 分类：随着 register 数量增加仍缓慢改善，16 个最高；
- 作者最终统一采用 `K=4`，是密集任务效果与成本之间的经验折中，不是理论推导出的常数。

因此不能把 `4 registers` 当作架构定律。分辨率、模型规模、训练目标变化时，最优 `K` 可能不同。

---

## 六、Appendix B：参数与计算成本

新增可学习参数只有 `K×d`；与 ViT 的投影矩阵和 FFN 参数相比通常可以忽略。计算增加来自序列从 `N+1` 变成 `N+1+K`：

- attention 部分近似随序列长度平方增长；
- FFN 等逐 token 计算近似线性增长；
- `K=4` 时，论文测得总 FLOPs 增量低于 `2%`；
- `K=16` 时 FLOPs 增量可到约 `6%`；
- 参数量增幅始终接近零。

这个比例依输入 patch 数量而变：图像分辨率越高、原序列越长，固定 4 个 register 的相对开销通常越小。

---

## 七、最关键的干预验证：行为是否真的迁移到 register

仅证明“加 token 后 patch 变干净”还可能有很多解释，例如额外参数带来正则化、优化轨迹改变。Appendix D 进一步检查 high-norm 和全局信息去了哪里。

### 1. Fig. 15：高范数从 patch 集合转移到 register 集合

无 register 的 DINOv2：

```text
CLS     : 低范数
patches : 主体低范数 + 少量高范数离群
```

带 4 个 registers 的 DINOv2：

```text
CLS      : 低范数
patches  : 全部回到低范数主体
registers: 不同 register 落在若干稳定的较高范数水平
```

这比 Fig. 7 更强：高范数行为没有凭空消失，而是完整地集中到不对应图像位置的 registers 中。四个 register 的范数还呈现近似量化的不同水平，作者未进一步解释。

### 2. Table 4：全局分类能力也迁移过去

在 Aircraft 数据集上用不同单 token 做线性分类：

| #registers | CLS | normal patch | outlier patch | register |
|---:|---:|---:|---:|---:|
| 0 | 84.6 | 15.5 | **73.3** | N/A |
| 1 | 85.2 | 14.5 | N/A | **71.1** |

加入一个 register 后：

- outlier patch 消失；
- register 单 token 获得 `71.1%` 分类准确率，接近原 outlier 的 `73.3%`；
- CLS 与 normal patch 基本不变。

这是全文最接近“功能接管”的证据：不仅范数位置迁移，outlier 原本异常强的全局语义也迁移到了 register。

### 3. Table 5：普通 patch 没有被整体重写

| 模型 | patch 范围 | 位置 Top-1 ↑ | 重建误差 ↓ |
|---|---|---:|---:|
| 0 register | 只看 non-outliers | 66.3 | 15.9 |
| 4 registers | 所有 patch（已无 outlier） | 65.8 | 16.0 |

普通 patch 的位置预测和像素重建几乎不变。因此 registers 主要隔离 outlier 行为，并没有靠全面改变剩余 patch 的局部编码来制造“更干净”的表象。

### 严格边界

两行结果来自**分别重新训练**的模型，不是向同一组已训练权重临时插入一个 token 后逐样本追踪信息搬运。因此“迁移”是跨训练条件的功能对应关系，而不是对单个 outlier 内容迁移路径的直接观测。

---

## 八、Fig. 9 / 16：register 会不会发生分工

作者没有对各 register 施加分工约束，但可视化显示：

- 不同 register 有不同注意力模式，有时关注场景中的不同物体；
- 平均位置图中，reg3 更偏图像边缘，reg2 略偏上方；
- registers 的注意力支持范围较大，接近 CLS；
- 普通 patch token 的平均注意力则明显更局部。

这与“register 携带全局信息”的 probing 结果一致，也显示多个 register 可能自发专门化。但这是定性证据，论文没有给出分工稳定性、跨随机种子一致性或显式的解耦指标。

---

## 九、方法的完整因果链

```text
观察：冗余 patch 被改作高范数全局载体
  ↓
干预：从训练开始提供不对应空间位置的可学习 token
  ↓
结果 1：三种监督范式的 high-norm patch 全部消失
  ↓
结果 2：高范数集中到 registers
  ↓
结果 3：register 继承 outlier 的全局分类能力
  ↓
结果 4：普通 patch 的局部信息几乎不变
  ↓
支持解释：模型确实需要内部全局计算槽位；显式槽位避免牺牲空间 patch
```

这个干预验证支持“register”功能解释，但还没有回答：**模型为什么要把全局语义写入背景、这种聚合策略在 high-norm 形成前是否已经损害了空间对齐。** 这正是 LAST-ViT 后来继续追问的部分。

---

## 十、第三站小结

| 维度 | 结论 |
|---|---|
| 参数化 | `K×d` 个可学习参数；跨所有图像共享；不编码输入内容 |
| 位置 | patch embedding 后插入；官方实现中无图像位置编码 |
| 优化 | 无直接输出损失，通过影响 CLS/patch 间接接收梯度 |
| 推理 | 必须继续参与前向；仅在 Transformer 输出端不交给下游头 |
| 数量 | 1 个已能消除可见 artifact；4 个是经验折中，不是理论常数 |
| 成本 | 4 个 register 增加低于 2% FLOPs，参数增量可忽略 |
| 跨范式 | DeiT-III、OpenCLIP、DINOv2 的 patch norm 离群均消失 |
| 功能迁移 | Aircraft：outlier `73.3%` 消失，单 register 达 `71.1%` |
| 局部保持 | 普通 patch 位置 probing `66.3→65.8`、重建误差 `15.9→16.0`，基本不变 |
| 未决问题 | register 的数量理论、分工稳定性、artifact 的训练根因和更早期背景语义扩散 |

### 自检小问题

1. “register 输出被丢弃”为什么不等于推理时可以删除 register 输入？
2. register 没有直接 loss，梯度从哪里来？
3. register 与 CLS、DETR object query 的核心区别是什么？
4. 为什么一个 register 就能消除 artifact，却仍可能需要多个 register？
5. Fig. 15 与 Table 4 分别证明了哪两种“迁移”？
6. Table 5 为什么能够反驳“register 只是全面重写了所有 patch 表示”的解释？
7. 当前因果链支持“专用内部计算槽位”后，仍没有解释的根因是什么？

---

> 下一站：`04_实验_边界与LAST-ViT.md`——检查 Table 2–3 的真实收益、OpenCLIP 反例、DINO/MAE 例外、位置插值混杂因素，以及为什么 LAST-ViT 认为“需要的不只是 Registers”。

