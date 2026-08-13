# LLM 分支阅读路线图

> 分支主题：**LLM 在科学发现上的能力边界**——归纳（从数据学规律）、演绎（从前提推结论）、溯因（为现象发明新解释框架）三种推理，当前大模型具备哪几种、缺哪一种。
> 正主为 Google DeepMind 研究员 Tom Zahavy 的立场论文《**LLMs can't jump**》（2026-01-27，PhilSci-Archive）。标题是双关："jump" 指爱因斯坦在致 Maurice Solovine 信中描述的、从感官经验（E）到公理体系（A）的直觉跳跃；论文论断是当前 LLM 在结构上无法完成这一步。
> 本文档随精读进度维护：读完一篇就在状态列打勾，并在下方"精读记录"补一行链接。
> 文末附**正主身份核查记录**：该文未被 arXiv API 索引，字面检索会得出"查无此文"的假象，身份确认经过多渠道交叉核实。

---

## 🧭 链路总览

```
被攻击的靶子                压力测试标本                  正主                      处方与检验
─────────────────     ─────────────────────────    ─────────────────    ─────────────────────────
Schmidhuber (2008)    AI Scientist (2024)          LLMs can't jump      Genie (ICML 2024)
"创造力=压缩进步"      全自动科学发现宣称            (2026-01-27)         动作可控的世界模型
        │             AlphaEvolve (2025)           Zahavy, DeepMind     ARC Prize 2024 TR
        │             固定框架内的进化搜索                               度量"溯因半边"的基准
        └──────────────────────┬───────────────────────────────────────────────┘
                               ▼
        正主的判决：归纳与演绎都不是瓶颈，缺的是溯因跳跃（E→A）；
        处方：可交互、物理一致、支持反事实干预的世界模型。
        另一侧的实证坐标：Si et al. (ICLR 2025) 的 100+ 研究者对照实验。
```

---

## 📋 阅读清单

| # | 论文 | 发表 | 一句话 | 状态 |
|---|---|---|---|---|
| 0 | **Schmidhuber**：Driven by Compression Progress | arXiv 0812.4360（2008；短版刊于 J. SICE 48(1), 2009） | 提出"创造力即压缩进步"：科学发现本质是寻找能压缩观测数据的短程序——正主正面攻击的靶子理论 | ⏳ 待读 |
| 1 | **ARC Prize 2024**: Technical Report（Chollet et al.） | arXiv 2412.04604（2024-12） | 度量"从稀疏样例猜出隐藏规则"的公开基准，正主引用的、当下最接近测量"溯因推理半边"的标尺 | ⏳ 待读 |
| 2 | **The AI Scientist**（Lu et al., Sakana AI） | arXiv 2408.06292（2024-08） | 全自动科学发现智能体（提出想法→跑实验→写论文）；正主判定其为既有概念的组合重排，而非框架发明 | ⏳ 待读 |
| 3 | **AlphaEvolve**（Novikov et al., Google DeepMind） | arXiv 2506.13131（2025-06） | 进化式编码智能体，在数学与算法发现上取得实质成果；正主判定其依赖预先给定的评价函数，属固定框架内优化 | ⏳ 待读 |
| 4 | **LLMs can't jump**（Tom Zahavy, Google DeepMind）⭐ | PhilSci-Archive #28024（2026-01-27），立场论文 | 以爱因斯坦发明广义相对论为案例，逐一排除归纳与演绎：科学发明的瓶颈是溯因跳跃 E→A；当前 LLM 在结构上无法完成该跳跃，处方为可交互、物理一致的世界模型 | ⏳ 待读 |
| 5 | **Genie**: Generative Interactive Environments（Bruce et al.） | ICML 2024，arXiv 2402.15391 | 从未标注视频训练的生成式交互环境，动作空间无监督学习、可由智能体操控——正主所开世界模型处方的代表工程谱系 | ⏳ 待读 |
| 6 | **Can LLMs Generate Novel Research Ideas?**（Si et al.） | ICLR 2025，arXiv 2409.04109 | 100+ NLP 研究者参与的大规模对照实验：LLM 产出的研究想法新颖度高于人类、可行性低于人类——正主先验论证另一侧的实证坐标 | ⏳ 待读 |

> 链路外的背景文献（不进表格，供精读时查证）：Ha & Schmidhuber《World Models》（NeurIPS 2018，arXiv 1803.10122，Genie 的概念前身）；Harnad《The Symbol Grounding Problem》（Physica D, 1990，正主"高维中文房间"论断的学理基础）；Peirce《Collected Papers》（1934，归纳/演绎/溯因三分法的出处）；Pearl & Mackenzie《The Book of Why》（2018，反事实干预的概念框架）。

---

## 🔑 各篇之间的因果链（为什么按这个顺序读）

1. **Schmidhuber（2008）** 给出被攻击的靶子：创造力与科学发现可以还原为压缩——谁找到了更短的数据解释程序，谁就完成了一次发现。这个等式若成立，擅长压缩的 LLM 天然就是科学发现的引擎。正主全文的第一任务即拆解该等式。
2. **ARC Prize 2024 Technical Report** 提供度量工具：ARC 任务要求从极少数样例中归纳出隐藏的变换规则，与"溯因"的结构同构。正主把 ARC 视为当下唯一接近测量"溯因推理半边"的基准，同时指出它测不了另一半——动手干预与反事实模拟。
3. **The AI Scientist（2024）** 是正主压力测试的第一个标本：一个宣称全自动、开放式科学发现的智能体。正主的判词是：它能写论文、跑实验、做评审，但全部工作都是对既有符号概念的组合重排；它缺少感官奠基，无法在没有符号先例的情况下发明公理——是"组合性的创造"，而非"诠释性的发明"。
4. **AlphaEvolve（2025）** 是第二个标本，且出自正主作者所在公司：进化式搜索在数学与算法发现上确有实质成果，但其运转依赖一个预先给定的评价函数。而爱因斯坦面对的局面的要害在于：牛顿力学并未提供任何误差信号来驱动发现。判据由此浮出——评价标准能否在探索过程中被共同改写，是"框架内优化"与"框架发明"的分界。
5. **LLMs can't jump（2026，正主）** 把论证推完：借助爱因斯坦的 E-J-A 循环（感官经验 →跳跃→ 公理体系 →演绎→ 定理 →回到经验检验），以广义相对论这一罕见的"理论先于数据"标本做排除法——归纳不成立（水星近日点的微小异常远不足以驱动范式更替，当时学界宁可假设存在"火神星"；验证性数据在理论成型多年后才出现），演绎也不成立（格罗斯曼曾摸到里奇张量，却因一个关于静态场的错误假设将其放弃——"致命错误"说明搜索到了正确答案也照样会被丢掉）。剩下唯一能解释发明的环节是溯因：爱因斯坦借自由落体与加速电梯的思想实验，把身体经验转化为等效原理这一新公理。正主称该机制为"操纵性溯因"，并断言纯文本模型缺少可供干预的物理世界，故无法执行这一步；处方是让 AI 拥有可交互、物理一致、支持反事实干预（"剪断缆绳"）的世界模型。需特别留意正主自带的范围限定：该处方专为物理科学量身定做；在数学等抽象领域，跳跃同样必要，但模拟基质需换为形式系统的抽象景观。标题是不加限定的全称判断，论证重心却在物理学——这一张力正是精读时最值得盯住的结构性弱点。
6. **Genie（ICML 2024）** 承接处方：从海量未标注视频中学习出可控的生成式交互环境，智能体能在其中执行动作——这正是"把模拟经验变成可干预实验"的工程雏形（概念前身可追溯至 Ha & Schmidhuber 的 World Models）。精读时的检验问题：此类环境学到的物理是否一致、能否承载反事实干预、离正主要求的"合成实验室"还差几步。
7. **Si et al.（ICLR 2025）** 提供实证对位：正主是先验论证（历史案例 + 排除法），该篇则是实证数据——让 LLM 与 100+ 位 NLP 研究者分别生成研究想法并由专家盲评，结果是新颖度更高、可行性更低。两篇并读，可以看清"LLM 不能发明框架"这一命题目前处于什么证据等级：既未被证明，也未被证伪。
8. **闭环判断**：该链路读完应得到一个降温后的结论——正主论证支持的是"仅靠文本预测、形式演绎与预设评价函数，不足以解释最困难的科学范式创新"，而非"AI 永远不能跳跃"。若世界模型路线日后成功把溯因机械化，那将是又一次"苦涩教训"式的换基质胜利。

---

## 🔎 正主身份核查记录（2026-08-13）

使用方提供的线索为口头转述"LLM cannot jump"。鉴于教训案例（LAST-ViT 事件：仓库名未出现在论文标题与摘要中，单一字面检索会误判为"查无此文"），本次核查按"arXiv API → cn.bing.com → GitHub → 关联线索"的顺序多渠道展开，并逐条记录如下。

| # | 检索词 | 渠道 | 结果 | 来源 |
|---|---|---|---|---|
| 1 | `all:"LLMs Can't Jump"` | arXiv API | 0 命中 | https://export.arxiv.org/api/query?search_query=all:%22LLMs+Can%27t+Jump%22 |
| 2 | `all:"cannot jump"` | arXiv API | 6 条，均为数学（随机游走、机制设计等），无相关论文 | https://export.arxiv.org/api/query?search_query=all:%22cannot+jump%22 |
| 3 | `ti:"can't jump"` / `au:Zahavy AND ti:jump` | arXiv API | 均 0 命中 | https://export.arxiv.org/api/query?search_query=ti:%22can%27t+jump%22 |
| 4 | `ti:"jump" AND all:"large language"`（30 条）、`all:"jump" AND all:"language models"`（按提交时间倒序 40 条） | arXiv API | 均为 early exit、bandit、激活函数等无关主题 | https://export.arxiv.org/api/query?search_query=ti:%22jump%22+AND+all:%22large+language%22 |
| 5 | `au:Zahavy`（按提交时间倒序 40 条）、`au:Zahavy AND all:"invention"` | arXiv API | 作者名下无 jump/invention 相关论文——**正主未被 arXiv API 索引** | https://export.arxiv.org/api/query?search_query=au:Zahavy |
| 6 | `"LLM cannot jump"` / `"LLMs can't jump"` / `"Tom Zahavy" "LLMs can't jump"` | cn.bing.com | 无有效命中（结果为 LLM 科普页、无关百科词条等） | https://cn.bing.com/search?q=%22LLM+cannot+jump%22&mkt=zh-CN |
| 7 | 仓库检索 `"cant jump" llm`、`"cannot jump"` | GitHub API | **命中：`aaaron7/llms-cant-jump-report`**（一份单文件精读报告）；`"cannot jump"` 无相关仓库 | https://api.github.com/search/repositories?q=%22cant+jump%22+llm |
| 8 | 抓取该仓库唯一文件 `index.html` | raw.githubusercontent.com | 提取到论文原题《LLMs can't jump》、作者 Tom Zahavy（Google DeepMind）、成文日期 2026-01-27、OpenReview forum id `klU4737opt`、PhilSci-Archive PDF 链接 | https://raw.githubusercontent.com/aaaron7/llms-cant-jump-report/main/index.html |
| 9 | `notes?forum=klU4737opt`、`notes/search` | OpenReview API（v1/v2） | 检索接口可达但精确短语 0 命中；forum 详情接口被人机验证拦截（403 ChallengeRequiredError），收录 venue 无法确认 | https://api2.openreview.net/notes?forum=klU4737opt |
| 10 | `title.search:"LLMs can't jump"` | OpenAlex API | **唯一命中**：标题、作者（Tom Zahavy）、日期（2026-01-27）、收录库（PhilSci-Archive, University of Pittsburgh）齐全，无 DOI，摘要全文与第 8 步精读报告内容自洽 | https://api.openalex.org/works?filter=title.search:LLMs%20can%27t%20jump |
| 11 | 直接抓取条目页与 PDF | philsci-archive.pitt.edu/28024/ | 被站点 WAF 拦截（返回人机验证页），原文未能取得；身份改以 OpenAlex 元数据与第 8 步精读报告内容交叉互证 | https://philsci-archive.pitt.edu/28024/ |
| 12 | 链路各篇 venue 复核 | DBLP API | Genie = ICML 2024；Si et al. = ICLR 2025；AI Scientist / AlphaEvolve / World Models 仅收录为 CoRR 预印本 | https://dblp.org/search/publ/api?q=Genie+Generative+Interactive+Environments&format=json |

**核查结论：**

1. 正主身份确认为 **Tom Zahavy（Google DeepMind），《LLMs can't jump》，立场论文，成文日期 2026-01-27**，存档于 PhilSci-Archive（匹兹堡大学科学哲学档案库，条目号 28024），无 DOI、无 arXiv 编号；据第三方精读报告页，该文同时被 OpenReview 收录（forum id=klU4737opt），但 OpenReview 接口被人机验证拦截，**收录会议/venue 无法核实，标记为待确认**。
2. 检索教训与 LAST-ViT 事件同构：该文载体为 PhilSci-Archive 而非 arXiv，arXiv API（含按作者遍历）完全检索不到；仅凭"LLM cannot jump"字面检索必得"查无此文"。第 7 步的 GitHub 仓库检索是破局关键。
3. 核查范围限制（如实记录）：PhilSci-Archive 原文 PDF 未能打开，OpenAlex 亦无全文；身份确认依赖 OpenAlex 元数据与第三方精读报告页两个渠道的交叉一致（两者给出的标题、作者、日期、摘要内容相互印证）。若后续需要引用原文细节，应先取得 PhilSci-Archive 原文复核。

---

## 📖 精读记录（读完一篇加一行）

| 归档 | 论文 | 一句话收获 |
|---|---|---|
| | | |
