# 小模型 vs 大模型阅读链路

> 定位：一条独立于 ViT 谱系的阅读链路，源自一次关于"过拟合与数据规模"的讨论，终点问题为：**小模型凭什么在 benchmark 上媲美乃至超越大模型？**
> 本图按因果链组织 **14 篇候选论文、五个站点**，并将链路终点结论立为"阅读假设"——后续每篇精读都是对该假设某一环节的验证或证伪。
> 本图只做清单登记与阅读排序，**不建精读笔记归档**；某篇确定精读时，再按仓库规则建 `<年份>/<月份>/<论文名>/` 归档目录，并把该条目从本图迁出、记入"精读记录"。
> 表内 arXiv 编号与发表 venue 已于 2026-08-13 逐条核对（检索过程与更正记录见文末"文献核查记录"）。

---

## 📜 链路来历

1. **讨论起点**：数据量小的时候过拟合致命；数据量巨大时，"充分拟合训练数据"从危险动作变成必要动作——矛盾的主要方面从"防过拟合"转移到"防欠拟合、拼数据质量、拼分布覆盖"。
2. **由此引出的问题**：既然小模型容量小、天然怕过拟合，为何仍有大量"小模型媲美大模型"的报告？是蒸馏？剪枝？还是别的机制？
3. **讨论得出的初步结论（立为阅读假设）**：小模型赢永远靠某个**不对称条件**——吃了大模型嚼过的知识（蒸馏）、专精评测窄分布（过拟合 benchmark）、算力预算内喂足数据更划算、或利用大模型的参数冗余。条件全部拉齐（同数据质量、同训练配方、同算力诚意、同通用性要求）时，容量差距是物理性的，大模型必赢。
4. **本图的任务**：为上述假设的每一条路径找顶会文献作锚，逐篇精读验证。

---

## 🧭 五站总览

```
讨论起点：过拟合的致命性随数据规模递增而递减；
          大数据时代的主旋律从"防过拟合"变为"防欠拟合 + 拼数据质量"
                                │
  ┌─────────────┬───────────────┼───────────────┬─────────────┐
  ▼             ▼               ▼               ▼             ▼
站 1 理论地基    站 2 蒸馏与      站 3 算力分配    站 4 评测      站 5 剪枝与
（容量与泛化     知识压缩         之争            幻觉           参数冗余
 到底怎么算）   （吃嚼过的知识）  （大模型欠训？） （benchmark   （雕刻出
 Scaling law /  Hinton →         Chinchilla →     是不是可被     稀疏子网络）
 Double descent DistilBERT →     LLaMA →          定向过拟合？）  Lottery Ticket
                Phi-1            数据受限 scaling  GSM-Symbolic → → Renda
                                                  BenBench
```

**站点间的因果链**：

1. **站 1** 先立地基：loss 随参数量、数据量、算力幂律下降（Kaplan）；但"拟合得越好泛化越差"的经典直觉在插值区域失效，出现 double descent（Nakkiran、Belkin）——这是整条链路讨论"充分拟合何时安全"的理论前提。
2. **站 2** 回答"小模型的知识从哪来"：软标签蒸馏（Hinton）→ 工程落地（DistilBERT）→ LLM 时代把"蒸馏"升级为"用大模型生成教科书级合成数据"（Phi-1、phi-1.5）。这条路径的代价是知识源头即大模型，学生上限被老师锁死。
3. **站 3** 处理"大模型自己没喂饱"的反例：Chinchilla 证明参数量与 token 数应 1:1 同扩、此前大模型普遍欠训练；LLaMA 用小模型配足 token 实践该结论；数据受限 scaling（Muennighoff）进一步给出数据质量与重复次数的权衡。
4. **站 4** 处理"假赢"：GSM-Symbolic 证明仅改写题目表面措辞即可大幅拉低数学基准分数——高分里有多少是对评测分布的过拟合？BenBench 系统检测训练语料对 benchmark 的泄漏。
5. **站 5** 处理"剪枝逆袭"的猜想：彩票假说证明大网络中存在可从头训练的稀疏子网（冗余是真实的）；但 Renda 等的系统比较显示，剪枝后微调很少打赢同尺寸从头训练的模型——"小模型雕刻得更完美"这一直觉在剪枝方向上基本不成立。

---

## 📋 阅读清单

### 站 1：理论地基——scaling law 与 double descent

| # | 论文 | 发表 | arXiv | 一句话 | 状态 |
|---|---|---|---|---|---|
| 1 | **Scaling Laws for Neural Language Models**（Kaplan et al.） | arXiv 2020 | [2001.08361](https://arxiv.org/abs/2001.08361)（已核对） | loss 随参数量、数据量、算力呈幂律下降——"条件拉齐后大模型必赢"的定量基础 | ⏳ 待读 |
| 2 | **Deep Double Descent: Where Bigger Models and More Data Hurt**（Nakkiran et al.） | ICLR 2020 | [1912.02292](https://arxiv.org/abs/1912.02292)（已核对） | 插值区域里"充分拟合"反而安全：过拟合致命性随容量/数据变化的完整曲线 | ⏳ 待读 |
| 3 | **Reconciling modern machine learning practice and the classical bias-variance trade-off**（Belkin et al.） | PNAS 2019 | [1812.11118](https://arxiv.org/abs/1812.11118)（已核对） | 用偏差-方差框架重述双下降，给出"充分拟合何时安全"的经典统计解释 | ⏳ 待读 |

### 站 2：蒸馏与知识压缩（"吃大模型嚼过的知识"）

| # | 论文 | 发表 | arXiv | 一句话 | 状态 |
|---|---|---|---|---|---|
| 4 | **Distilling the Knowledge in a Neural Network**（Hinton, Vinyals & Dean） | NIPS 2014 Workshop | [1503.02531](https://arxiv.org/abs/1503.02531)（已核对） | 蒸馏开山：大模型的软输出（概率分布）信息密度远高于 one-hot 标签 | ⏳ 待读 |
| 5 | **DistilBERT**（Sanh et al.） | NeurIPS 2019 Workshop | [1910.01108](https://arxiv.org/abs/1910.01108)（已核对） | 蒸馏的工程落地范本：BERT 体积减 40%、速度提 60%，保留 97% 能力 | ⏳ 待读 |
| 6 | **Textbooks Are All You Need**（Phi-1，Gunasekar et al.） | arXiv 2023 | [2306.11644](https://arxiv.org/abs/2306.11644)（已核对） | 1.3B 模型靠 GPT-3.5 生成的"教科书级"合成数据训练，HumanEval 50.6%、MBPP 55.5%；摘要已核对该分数 | ⏳ 待读 |
| 7 | **Textbooks Are All You Need II**（phi-1.5） | arXiv 2023 | [2309.05463](https://arxiv.org/abs/2309.05463)（已核对） | Phi-1 续作，合成数据配方扩展到通用推理 | ⏳ 待读 |

### 站 3：算力分配之争（"大模型欠训练，小模型喂饱更划算"）

| # | 论文 | 发表 | arXiv | 一句话 | 状态 |
|---|---|---|---|---|---|
| 8 | **Training Compute-Optimal Large Language Models**（Chinchilla，Hoffmann et al.） | arXiv 2022 | [2203.15556](https://arxiv.org/abs/2203.15556)（已核对） | 参数量与训练 token 应 1:1 同扩；此前大模型普遍 token 喂不够 | ⏳ 待读 |
| 9 | **LLaMA: Open and Efficient Foundation Language Models**（Touvron et al.） | arXiv 2023 | [2302.13971](https://arxiv.org/abs/2302.13971)（已核对） | Chinchilla 结论的直接实践：小模型配远超常规的 token 量打赢大模型 | ⏳ 待读 |
| 10 | **Scaling Data-Constrained Language Models**（Muennighoff et al.） | NeurIPS 2023 | [2305.16264](https://arxiv.org/abs/2305.16264)（已核对） | 数据量有限时重复数据有边际递减，高质量数据比重复堆量更重要 | ⏳ 待读 |

### 站 4：评测幻觉（"benchmark 是不是可以被定向过拟合"）

| # | 论文 | 发表 | arXiv | 一句话 | 状态 |
|---|---|---|---|---|---|
| 11 | **GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in LLMs**（Mirzadeh et al.） | ICLR 2025 | [2410.05229](https://arxiv.org/abs/2410.05229)（已核对） | 仅改写题目表面措辞，各模型准确率即大幅下滑——高分里有相当部分是对评测分布的过拟合 | ⏳ 待读 |
| 12 | **Benchmarking Benchmark Leakage in Large Language Models**（Xu et al.） | arXiv 2024 | [2404.18824](https://arxiv.org/abs/2404.18824)（已核对） | 系统检测训练语料对 benchmark 的泄漏："媲美"里有多少是原题记忆 | ⏳ 待读 |

### 站 5：剪枝与参数冗余（"大模型里确实有莫名其妙的神经元"）

| # | 论文 | 发表 | arXiv | 一句话 | 状态 |
|---|---|---|---|---|---|
| 13 | **The Lottery Ticket Hypothesis**（Frankle & Carbin，ICLR 2019 最佳论文） | ICLR 2019 | [1803.03635](https://arxiv.org/abs/1803.03635)（已核对） | 大网络中存在稀疏子网络，从头训练能达到原网络精度——参数冗余是真实的 | ⏳ 待读 |
| 14 | **Comparing Rewinding and Fine-tuning in Neural Network Pruning**（Renda, Frankle & Carbin） | ICLR 2020 | [2003.02389](https://arxiv.org/abs/2003.02389)（已核对） | 系统比较剪枝后微调与等规模从头训练——"剪枝逆袭同尺寸模型"的猜想基本不成立 | ⏳ 待读 |

---

## 🔑 阅读假设（链路终点结论，待逐篇验证）

1. 过拟合的致命性随数据规模增加而递减；数据足够时，"充分拟合训练数据"从危险动作变为必要动作。（站 1 验证）
2. 小模型在 benchmark 上打赢大模型，永远依赖某个不对称条件：
   - **知识不对称**：吃了大模型蒸馏/合成的浓缩知识，上限被老师锁死（站 2）；
   - **分布不对称**：把全部容量砸在评测窄分布上，分布内赢、分布外输，属于"假赢"（站 4）；
   - **算力不对称**：预算固定时，小模型配足 token 比大模型欠训练更划算（站 3）；
   - **冗余不对称**：大模型存在可剪除的冗余，但剪枝模型很少打赢同尺寸从头训练的模型（站 5）。
3. 条件全部拉齐时，容量差距是物理性的，大模型必赢——scaling law 的幂律没有给小模型留反超的口子（站 1 + 站 3 联合验证）。
4. 小模型研究的真实动机不是"赢"，而是**用 1/10 的成本拿到 90% 的效果**；benchmark 是可以被针对性优化的窄目标，小模型恰好便宜到值得为每个窄目标单独优化一个。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| — | — | （尚未开始精读） |

---

## 🔍 文献核查记录（2026-08-13）

按全局规则记录核查过程（检索词、检索源、结果、结论）。

**第一轮：文献清单初拟（2026-08-13）**
- 方式：基于讨论内容列出 13 篇候选文献。当时 WebSearch 工具返回空结果，全部标注"待验证"。

**第二轮：arXiv 编号与标题逐篇核对（curl，2026-08-13）**
- 检索源：`arxiv.org/abs/<编号>` 页面逐一抓取标题与作者元数据。
- 结果：13/13 标题、作者与原文一致；Phi-1 摘要确认 HumanEval 50.6%、MBPP 55.5%、phi-1-small（350M）45%。
- **更正一处编号错误**：Belkin 双下降论文初稿误写为 `1803.08823`（该编号实为同组的《A high-bias, low-variance introduction to Machine Learning for physicists》）；经 arXiv API 按标题检索，正确编号为 [1812.11118](https://arxiv.org/abs/1812.11118)。

**第三轮：发表 venue 核对（curl，2026-08-13）**
- 检索源：arXiv API 的 `arxiv:comment` / `arxiv:journal_ref` 字段、dblp、Semantic Scholar API、NeurIPS 2022 官方目录（papers.nips.cc）、ICML 2024 官方目录（proceedings.mlr.press/v235）。
- 结果与 **两处更正**：
  1. **Chinchilla**（2203.15556）：初稿曾标"NeurIPS 2022"。经核查，NeurIPS 2022 官方目录中检索作者 Hoffmann 命中 0 条，arXiv 无 journal_ref，dblp 仅 CoRR 记录——**该篇实为 arXiv 预印本**，已更正。
  2. **BenBench**（2404.18824）：初稿曾标"ICML 2024"。经核查，ICML 2024 官方目录（v235）无此文，dblp 仅 CoRR 记录——**该篇实为 arXiv 预印本**，已更正。
  3. 其余确认：GSM-Symbolic = ICLR 2025（dblp）、Scaling Data-Constrained = NeurIPS 2023（dblp，另有 JMLR 2025 版）、Belkin = PNAS（Semantic Scholar，正式发表年 2019）、Hinton 蒸馏 = NIPS 2014 Workshop（arXiv comment）、DistilBERT = NeurIPS 2019 Workshop（arXiv comment）、彩票假说 = ICLR 2019、Renda = ICLR 2020（均为 arXiv comment）、Double Descent = ICLR 2020（Semantic Scholar）。
  4. Phi-1 / phi-1.5 / Kaplan / LLaMA 四篇无正式会议发表记录，均为 arXiv 技术报告。
- **留待精读时核对的细节**：Chinchilla 的具体数字（70B / 1.4T token 打赢 Gopher 280B / 300B token）、LLaMA 的 token 量（7B / 1T）等，本轮仅核对标题与 venue，未逐字核对正文数字。

---

## 🔗 与其他路线图的关联

- **DeiT**（[2026/08/deit-paper](./2026/08/deit-paper/精读笔记/README.md)，已读）：蒸馏 token 是站 2 在视觉侧的实践案例，可与 Hinton、DistilBERT 对照阅读。
- **《[ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)》支线四（Scaling 与训练配方）**：与本图站 1/站 3 有交集，但支线四聚焦视觉模型的规模化（ViT-22B、DeiT III），本图聚焦 LLM 的 scaling 理论与小模型逆袭机制，两边不重复登记。
