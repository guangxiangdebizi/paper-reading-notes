# paper-reading-notes · 论文精读笔记

> 我们自己的论文精读仓库。每篇论文 = 原稿 + 逐段精读笔记，按**精读完成的时间**归档。
> GitHub 端**公开**，GitLab 端内部备份（双远端同步）。

---

## 📁 目录结构规则（新增论文时必须遵守）

```
.
└── <精读年份>/                  # 如 2026
    └── <月份，两位数>/           # 如 08（按精读完成当月归档）
        └── <论文英文名-短横线连接>/   # 如 vit-paper、mae、detr
            ├── <原稿 PDF>          # 论文原文，文件名含 arXiv 编号
            ├── <论文名>_fulltext.txt  # 从 PDF 提取的纯文本（便于对照/检索）
            ├── figures/             # 从 PDF 抽取的图片（见规则 6）
            └── 精读笔记/
                ├── README.md        # 该篇的索引 + 全文一句话总结
                ├── 01_<章节主题>.md
                ├── 02_<章节主题>.md
                └── ...
```

**规则要点：**

1. **时间跨度文件夹**：`<年份>/<月份>` 两层，月份用两位数（`08` 不是 `8`）。归档时间 = 精读完成的日期。
2. **论文文件夹**：英文名、小写、短横线连接（`vit-paper`），不带空格和特殊字符。
3. **原稿 PDF**：必须入库，文件名尽量含 arXiv 编号（如 `ViT_2010.11929.pdf`），方便溯源。
4. **全文文本**：用工具从 PDF 提取的 txt，方便笔记里引用原文和全文搜索。
5. **笔记编号**：`01_`、`02_` 起按精读顺序编号，一个 md 对应论文的一"站"（如摘要+引言、方法、实验、分析）。
6. **图片抽取**：`figures/` 目录存放从 PDF 抽取的图片。矢量图按整页渲染为 PNG（命名 `fig<编号>_page<页码>.png`），嵌入的位图按原格式抽取（命名 `img_<序号>_p<页码>.<ext>`）。笔记中涉及关键图的应引用 `figures/` 中的文件。图片的**阅读策略见规则 7**。
7. **精读时的阅读策略（文本按需抽段，图片选择性看）**：
   - **文本**：`<论文名>_fulltext.txt` 禁止整份读入上下文，用 `grep -n` 定位行号、`sed -n '起,止p'` 只抽当前站点需要的段落；读到哪段看哪段。
   - **图片**：`figures/` 中的整页 PNG 体积大、进上下文的折算成本高，**不要求全部看**——只在当前站点的论证确实依赖某张图（如方法结构图、关键消融图）时才读取该张；一次会话内读取的图应克制，避免多张大图与全文同时进上下文。
   - **背景**：2026-08-13 一次 Swin 精读会话曾把整份 fulltext 与多张大图同时读入上下文，超过模型的输入长度上限，触发中转站 `400 InvalidParameter` 报错（`Range of input length should be [1, 983616]`）。本条规则即针对该事故设定。

---

## ✍️ 笔记撰写规范

- **逐段精读**：关键原文引用（英文原句）→ 解读 → 深意/写作技巧点评。
- **每个 md 结尾**附：小结表格 + 自检小问题。
- **论文 README**（`精读笔记/README.md`）包含：精读路线索引表（站次/文件/内容/状态）+ 全文一句话总结。
- 数字、公式、表格尽量忠实原文；自己的评论和原文严格区分（引用块 = 原文，正文 = 解读）。

---

## ➕ 新增一篇论文的流程（Checklist）

- [ ] 下载原稿 PDF（arXiv 优先），提取全文 txt
- [ ] 抽取 PDF 内图片到 `figures/`（矢量图整页渲染 PNG，位图原格式抽取）
- [ ] 在 `<年份>/<月份>/` 下建 `<论文名>/` 文件夹，放入 PDF + txt
- [ ] 建 `精读笔记/` 子目录，边精读边写编号 md
- [ ] 精读过程遵守规则 7：文本按需抽段，图片选择性读取
- [ ] 写该篇的 `README.md` 索引
- [ ] 提交并推送到 GitHub 与 GitLab 两个远端

---

## 📖 已精读论文

| 归档 | 论文 | 一句话总结 |
|---|---|---|
| 2026/08 | [ViT](./2026/08/vit-paper/精读笔记/README.md)（An Image is Worth 16×16 Words, ICLR 2021） | 大规模训练，能够战胜归纳偏置 |
| 2026/08 | [DeiT](./2026/08/deit-paper/精读笔记/README.md)（Training Data-Efficient Image Transformers, ICML 2021） | 没有大数据时：借配方（强增强）+ 借先验（蒸馏 token），单机 3 天训出能打的 ViT |
| 2026/08 | [RAFT](./2026/08/raft-paper/精读笔记/README.md)（Recurrent All-Pairs Field Transforms for Optical Flow, ECCV 2020 Best Paper） | 把经典光流优化翻译成端到端网络：特征、先验、下降方向全部学出来；循环查表，单一分辨率流场 |
| 2026/08 | [ConvNeXt](./2026/08/convnext-paper/精读笔记/README.md)（A ConvNet for the 2020s, CVPR 2022） | 不引入注意力，仅用 Transformer 时代的训练配方与设计逐项翻新 ResNet，得到的纯 ConvNet 反超 Swin：ViT 与 CNN 的差距里，配方与设计占大头 |
| 2026/08 | [Swin](./2026/08/swin-paper/精读笔记/README.md)（Hierarchical Vision Transformer using Shifted Windows, ICCV 2021 Marr Prize） | 窗口内局部注意力（线性复杂度）+ patch merging 层级化 + 移位窗口保流通：ViT 从分类样板间变成检测/分割通吃的通用骨干网，COCO/ADE20K 双 SOTA，且任务越密集优势越大 |
| 2026/08 | [DETR](./2026/08/detr-paper/精读笔记/README.md)（End-to-End Object Detection with Transformers, ECCV 2020） | 检测 = 直接集合预测：N 个可学习 object queries 并行输出 + 匈牙利一对一匹配损失，去 anchor/NMS，首次端到端打平加强版 Faster R-CNN（大目标 +7.8、小目标 -5.5），并顺手拿下全景分割 PQ 第一 |
| 2026/08 | [MAE](./2026/08/mae/精读笔记/README.md)（Masked Autoencoders Are Scalable Vision Learners, CVPR 2022） | 非对称 encoder-decoder + 75% 高掩码比例：遮随机 patch、重建像素，精度与效率双赢（加速 3×+）；vanilla ViT-Huge 仅 IN1K 无标签达 87.8%，检测/分割迁移全面超越监督预训练且随规模持续涨点 |
| 2026/08 | [Transformer](./2026/08/transformer-paper/精读笔记/README.md)（Attention Is All You Need, NIPS 2017） | 完全基于多头自注意力取代循环与卷积，O(1) 串行步数换高度并行，WMT14 英德/英法双 SOTA（28.4/41.8，单机 8 卡 12 小时/3.5 天），成分句法分析验证任务通用性——整个 Transformer 时代的起点（《经典地基阅读路线图》第 1 篇晋升四站精读） |

## 🗺️ 阅读路线图

- [ViT 分支阅读路线图](./ViT分支阅读路线图.md)：以 ViT 为根的整条脉络，四条主线（DeiT → ConvNeXt / Swin → DETR / MAE / Registers → LAST-ViT），含各篇因果链与进度。
- [ViT 家族拓展阅读路线图](./ViT家族拓展阅读路线图.md)：主线读完后的下游拓展（2022–2026），按架构演进/自监督/多模态基础模型/Scaling/挑战者五条支线登记，共 36 篇候选，仅登记清单、暂不精读。
- [视频抽帧压帧分支阅读路线图](./视频抽帧压帧分支阅读路线图.md)：把一整段视频变成几张有信息量的图片——镜头检测 → 光流 → 冗余剔除 → 关键帧/视频摘要 → 神经压缩 → VLM 帧采样，含顶会顶刊与阅读顺序。
- [小模型vs大模型阅读链路](./小模型vs大模型阅读链路.md)：源自"过拟合与数据规模"讨论的独立链路——scaling law / 双下降 → 蒸馏与合成数据 → 算力分配 → benchmark 幻觉 → 剪枝冗余，清单只收顶会顶刊（9 篇），预印本与 workshop 文献归入背景文献供查证；将"条件拉齐则大模型必赢"立为阅读假设，逐篇验证。
- [LLM 分支阅读路线图](./LLM分支阅读路线图.md)：以《LLMs can't jump》（Zahavy, Google DeepMind, 2026）为正主的"LLM 科学发现能力边界"链路——清单只收顶会顶刊（Si et al. ICLR 2025、Genie ICML 2024 两篇），正主与压力测试标本（AI Scientist、AlphaEvolve 等非顶会文献）归入背景文献供查证，附正主身份多渠道核查记录与 venue 复核记录。
- [经典地基阅读路线图](./经典地基阅读路线图.md)：把 8 篇已精读笔记当作已知前提使用、但从未展开讲解的概念回溯到奠基论文——encoder/decoder 完整架构（Transformer）、decoder 掩码与 [CLS]（BERT）、骨干网基线（ResNet）、RPN/RoI（Faster R-CNN）、focal loss（RetinaNet）、AdamW/cosine/warmup/label smoothing/RandAugment 等，共 13 篇顶会顶刊，只登记、按需查阅，同一篇多次卡点可晋升四站精读。

---

## 🔒 其他约定

- 双远端备份：`origin` = GitHub（公开），`gitlab` = GitLab（内部）。
- 提交信息格式：`<论文名>: <做了什么>`，如 `vit-paper: 完成第 3 站实验部分笔记`。
- 不在仓库里放任何密钥、token、大模型权重等敏感/超大文件。
- 仓库内论文原稿 PDF 版权归原作者/出版方所有，仅作个人学习研究存档；笔记为原创解读。
