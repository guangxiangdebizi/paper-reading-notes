# 论文知识图谱 · 单篇 YAML 片段规范（SCHEMA_SPEC）

本文件定义**一篇精读论文**对应一个 YAML 片段文件的写法。每个执行 subagent 只负责**一篇论文**：
读该论文的精读笔记原文 → 按本规范写出一个片段文件 → 只回传计数，不要把 YAML 内容贴回对话。

## 0. 铁律（忠实性，最高优先级）
1. **只写笔记里有的**：所有字段内容必须出自该论文的精读笔记原文。笔记没写的字段直接省略或留空，**严禁凭训练知识补全** venue / 年份 / arXiv / 数字 / 关系。
2. **原文优先、高信息密度**：problem / contributions / limitations / key_results 用笔记原句或紧贴原句的压缩，关键主张用引号标出笔记原句。不做二次演绎、不改变原始语义与方法论表述。
3. **每条可溯源**：尽量在每个条目末尾用括号注明来源文件（如 `（02_方法.md）` 或 `（V-03）`）。片段顶层 `source` 填该论文精读笔记目录的代表文件。
4. **关系必须有笔记依据**：relates 里的每条边，evidence 字段填笔记原句片段；笔记没明确写的关联不要建。
5. 禁止输出任何凭据类信息。

## 1. 输出位置与文件头
- 写到：`knowledge_graph/data/papers/<id>.yaml`（`<id>` 用下面 id 注册表里该论文的 id）。
- 文件第一行固定为 `paper:`（单篇），其下缩进 2 空格写字段。

## 2. 字段 schema（按此顺序，可选字段无内容则省略整行）
```yaml
paper:
  id: vit                      # 必填，见 id 注册表，ascii 小写下划线
  title: "英文原名标题"          # 必填，笔记记载的英文标题
  aliases: ["ViT", "Vision Transformer"]   # 可选，笔记出现的别名/简称
  authors: "Dosovitskiy et al."            # 可选，笔记记载的作者（简写即可）
  affiliation: "Google Brain"              # 可选
  year: 2021                   # 可选，笔记有才写（整数）
  venue: "ICLR 2021"           # 可选，笔记记载的发表 venue
  arxiv: "2010.11929"          # 可选
  status: "已读"                # 精读论文固定填 "已读"
  notes_path: "paper-reading-notes/2026/08/vit-paper/精读笔记"   # 该论文笔记目录（相对项目根）
  source: "paper-reading-notes/2026/08/vit-paper/精读笔记/01_摘要与引言.md"  # 代表来源文件
  problem: |                   # 必填，论文解决的核心痛点/前作缺陷，1-4句，忠实笔记，可含引号原句
    Transformer 在视觉中"应用受限"……核心主张："视觉根本不需要 CNN 这根拐杖"。
  contributions:               # 必填，逐条列出核心贡献/方法，用笔记术语，每条末尾注来源
    - "图像分词：16×16 patch 线性投影 + [class] token + 1D 可学习位置编码（02_方法.md）"
    - "贴着原版 Transformer 设计、最少修改，为 NLP 高效实现开箱即用（02_方法.md）"
  limitations:                 # 可选，笔记提到的局限/未解决问题；没有则省略整个字段
    - "小/中数据下泛化差，ImageNet 上低于同尺寸 ResNet（01/03）"
  key_results:                 # 可选，关键实验结论/数字，每条注来源
    - "ImageNet 88.55%（ViT-H/14, JFT）（03）"
  concepts:                    # 可选，本文【提出/定义】的方法概念 -> 建 PROPOSES 边
    - id: patch_embedding
      name: "Patch Embedding"
      detail: "把图像切 16×16 patch 线性投影成 token 序列"
      origin: "本文"            # 或 "借自 BERT" 等（笔记记载的来源）
      source: ".../02_方法.md"
  depends:                     # 可选，本文【依赖/借鉴的外部技术】-> 建 USES 边（也是 Concept 节点）
    - id: bert_cls_token
      name: "BERT [class] token"
      detail: "分类用的全局 token 借自 BERT"
      origin: "BERT"
      source: ".../02"
  datasets:                    # 可选，评测/训练数据集 -> 建 EVALUATES_ON 边
    - name: "ImageNet-1K"
      scale: "1.3M"            # 可选
      role: "pretrain+eval"    # 可选：pretrain/eval/downstream 等
      metrics: "88.55% (ViT-H/14, JFT)"   # 可选，本文在该集上的代表数字
      source: ".../03"
  problems:                    # 可选，比 paper.problem 更结构化的"痛点"节点 -> 建 ADDRESSES 边
    - id: vit_data_hunger
      description: "依赖私有 JFT-300M 大数据，公众无法复现"
      source: ".../03"
  relates:                     # 可选，论文间关系，【from 恒为本论文】，to 用 id 注册表
    - to: transformer
      rel_type: INHERITS        # 见下方关系类型词表
      detail: "贴着原版 Transformer 设计"
      evidence: "follow the original Transformer (Vaswani et al., 2017) as closely as possible"
      source: ".../02"
      confidence: high          # high/medium/low；证据是笔记原句直引=high，归纳=medium
  belongs_to:                  # 可选，本论文属于哪些阅读路线/家族 topic（id 见注册表）
    - topic: t_vit_line_a
      order: 0
      source: "paper-reading-notes/ViT分支阅读路线图.md"
```

## 3. 关系类型词表（rel_type 取值，大写）
- `INHERITS` 继承/采用架构（DETR 采用 Transformer）
- `IMPROVES` 改进（Swin 改进 ViT）
- `CONTINUES` 续作/解释根因（LAST-ViT 续 Registers）
- `SUPERSEDES` 对比超越/终结其时代（RAFT 终结 PWC-Net）
- `CONTRAST` 对比（不分胜负的对照，ConvNeXt 对照 Swin）
- `REFUTES` 反驳/回应其论点（ConvNeXt 反驳 ViT 大数据论点）
- `INSPIRES` 启发/思想源头（ViT §4.6 启发 MAE）
- `BORROWS` 借鉴技巧（RAFT 借鉴 FlowNet2 梯度截断）
- `PROVIDES_RECIPE` 提供配方/基座（DeiT 提供配方给 ConvNeXt）
- `CORROBORATES` 立场呼应（弱关系，Swin↔ConvNeXt）
- `USES_AS_TOOL` 作为工具/验证手段引用（Registers 用 LOST）
- `DISTINGUISHES` 角色区分/对比表（Registers vs DETR object query）
（`FOLLOWS` 仅由 catalog 的路线承接使用，精读片段一般不用）

## 4. id 注册表（cross-paper 边的 to / concept 的 origin 引用请优先复用这些 id）
**10 篇精读论文（本批要建片段的）**：
`vit` `deit` `convnext` `swin` `detr` `mae` `registers` `last_vit` `raft` `transformer`

**常被引用的其他论文/工作（to 或 origin 用到时用这些 id；没有合适的就自拟 ascii slug）**：
`bert` `gpt` `gpt2` `gpt3` `resnet` `resnext` `mobilenet` `mobilenetv2` `xception`
`efficientnet` `noisy_student` `bit` `regnety` `timm` `abnar`
`flownet` `flownet2` `pwc_net` `irr` `horn_schunck` `flowformer` `cotracker` `hsm_net` `deep_equilibrium` `vcn`
`beit` `dino` `dinov2` `dinov3` `moco_v3` `simclr` `byol` `ibot` `ijepa`
`lost` `memory_transformer` `dino_detector`（注意：LAST-ViT 笔记里 "DINO[43]" 是 DETR-DETR 检测器，与自监督 `dino` 不是同一篇，用 `dino_detector`）
`clip` `metaclip` `evaclip` `maskclip` `s_clip` `clipself` `siglip`
`deformable_detr` `dab_detr` `dino_detr` `faster_rcnn` `mask_rcnn` `panopticfpn` `upsnet`
`setr` `mlp_mixer` `resmlp` `efficientnetv2` `rvt` `convmixer`
`hinton_distill` `adamw` `sgdr` `cosine_annealing` `label_smoothing` `randaugment` `mixup` `cutmix`

**topic id（belongs_to 用，来自 catalog 的路线/家族）**：
`t_vit_branch` `t_vit_line_a` `t_vit_line_b` `t_vit_line_c` `t_vit_line_d`
`t_vit_extension` `t_ext_arch` `t_ext_ssl` `t_ext_multimodal` `t_ext_scaling` `t_ext_challenger`
`t_video_frame` `t_color_overlap` `t_small_vs_large` `t_llm_branch` `t_classic_foundation` `t_vmsv2`
（精读论文的 belongs_to：ViT/DeiT/ConvNeXt→t_vit_line_a；Swin/DETR→t_vit_line_b；MAE→t_vit_line_c；Registers/LAST-ViT→t_vit_line_d；RAFT→t_video_frame；Transformer→t_classic_foundation。order 填该论文在路线中的序号，笔记/路线图有则填，无则省略。）

## 5. 注意
- `concepts`（本文提出）与 `depends`（借鉴外部）都建成 Concept 节点，区别只在边类型（PROPOSES vs USES）。同一概念若多篇都涉及，用相同 id 即可（loader 会去重）。
- datasets 的 `name` 用笔记里的写法（如 `ImageNet-1K` `ImageNet-21k` `JFT-300M` `COCO 2017` `ADE20K` `Sintel` `KITTI` `WMT 2014 EN-DE` 等）。
- YAML 语法：含冒号/特殊字符的字符串用引号；多行用 `|` 块标量；中文 UTF-8 正常写。写完后该文件必须能被 pyyaml 安全解析。

## 6. 回传格式（只回这些，不要贴 YAML 全文）
```
写入: knowledge_graph/data/papers/<id>.yaml
计数: contributions=N, limitations=N, key_results=N, concepts=N, depends=N, datasets=N, problems=N, relates=N, belongs_to=N
异常: <笔记缺失/字段留空/id 不确定等，一句话；无则写"无">
```
