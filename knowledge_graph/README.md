# 论文知识图谱（Kùzu + Cypher）

把本项目读过的论文整理成可查询的知识图谱：论文之间的关联（继承/改进/续作/反驳/启发/对比…）、
解决了什么、没解决什么、提出了什么概念、用了哪些数据集、属于哪条阅读路线。
后续新读论文以「追加一个 YAML 片段 + 重跑构建脚本」的方式并入图谱。

## 一、技术选型

- **Kùzu**（`kuzu==0.11.3`，装在项目 `venv/`）：嵌入式图数据库（相当于图数据库界的 SQLite），
  原生支持 **Cypher** 查询，无服务、无端口、pip 装完即用。语法与 Neo4j 高度相似，日后要迁移成本低。
- 为什么不是 Neo4j：Neo4j 需要 Java 运行时 + 常驻服务（或 Docker 容器），对本机使用场景过重；
  Kùzu 满足「Cypher 查询 + 本地轻量」两个核心诉求。

## 二、目录结构

```
knowledge_graph/
├── build_graph.py        # 建库脚本：读 data/ 下 YAML → 建 schema → 灌数据（--reset 全量重建）
├── query.py              # 查询工具：任意 Cypher / --demo 示例 / --paper <id> 单篇全景
├── data/
│   ├── SCHEMA_SPEC.md    # 单篇 YAML 片段规范（subagent 照此产出，人工追加也照此写）
│   ├── catalog.yaml      # 待读/登记论文目录（185 篇 + 21 条路线/家族 + 25 条路线承接边）
│   └── papers/           # 精读论文单篇 YAML 片段（每篇一个文件，忠实笔记原文）
│       ├── vit.yaml  deit.yaml  convnext.yaml  swin.yaml
│       ├── detr.yaml  mae.yaml  registers.yaml
│       └── last_vit.yaml  raft.yaml  transformer.yaml
└── db -> C:\Users\26214\paperreading_kgdb   # junction，数据库实体（见下方"路径说明"）
```

**路径说明（重要）**：Kùzu 0.11.3 在 Windows 上无法打开含中文的路径（实测缺陷，已记录到项目根
`平台问题记录.md`）。数据库实体存放在纯 ASCII 路径 `C:\Users\26214\paperreading_kgdb`，
项目内 `knowledge_graph/db` 是指向它的目录联接（junction），两边看到的是同一份数据。
脚本内部一律使用 ASCII 实体路径。

## 三、图谱 Schema

**节点**
| 标签 | 主键 | 说明 |
|---|---|---|
| Paper | id | 论文。属性含 title/aliases/authors/affiliation/year/venue/arxiv/status（已读/待读/选读/备查/必读/登记/背景/待查）、notes_path（精读笔记目录）、problem（解决的问题，笔记原文）、contributions[]、limitations[]、key_results[]、source |
| Topic | id | 阅读路线/家族分支（t_vit_line_a…d、t_video_frame、t_color_overlap、t_small_vs_large、t_llm_branch、t_classic_foundation、t_vmsv2 等），parent 表达层级 |
| Concept | id | 方法/技术概念（patch_embedding、lazy_strike、匈牙利匹配、4D 相关体…），origin 记录出处 |
| Dataset | name | 数据集（ImageNet-1K/21k、JFT-300M、COCO、ADE20K、Sintel、KITTI…） |
| Problem | id | 结构化痛点节点（如"依赖私有 JFT-300M"） |

**关系**
| 类型 | 含义 |
|---|---|
| RELATES (Paper→Paper) | 论文间关系，用 rel_type 属性细分（见下），每条带 detail/evidence（笔记原句）/source（精确到站次文件）/confidence |
| PROPOSES (Paper→Concept) | 论文提出的概念 |
| USES (Paper→Concept) | 论文依赖/借鉴的外部技术 |
| EVALUATES_ON (Paper→Dataset) | 评测/训练数据集，role + metrics |
| ADDRESSES (Paper→Problem) | 论文解决的痛点 |
| BELONGS_TO (Paper→Topic) | 属于哪条路线/家族，seq 为路线内序号 |

**rel_type 词表**：INHERITS 继承架构 / IMPROVES 改进 / CONTINUES 续作·解释根因 / SUPERSEDES 对比超越·终结时代 / CONTRAST 对比 / REFUTES 反驳论点 / INSPIRES 启发·思想源头 / BORROWS 借鉴技巧 / PROVIDES_RECIPE 提供配方·基座 / CORROBORATES 立场呼应（弱边）/ USES_AS_TOOL 作为工具引用 / DISTINGUISHES 角色区分 / FOLLOWS 路线承接顺序。

## 四、忠实性约定（建图铁律）

1. 图谱内容只来自项目内笔记/路线图文档原文，**不掺入模型训练知识的补全**；笔记没写的字段留空。
2. 每条论文间关系必须有 evidence（笔记原句）+ source（文件路径），confidence 标注证据强度
   （high=原句直引，medium=笔记归纳，route=路线图承接顺序）。
3. 精读论文（status=已读）节点信息密度最高；catalog 里的待读论文只登记路线/状态级元数据，
   待精读后再产出片段升级为富节点。

## 五、常用命令

```powershell
# 全量重建图谱（幂等；--reset 先删库重建）
venv\Scripts\python.exe knowledge_graph\build_graph.py --reset

# 单篇论文全景速览
venv\Scripts\python.exe knowledge_graph\query.py --paper vit

# 内置示例查询（复习链路演示）
venv\Scripts\python.exe knowledge_graph\query.py --demo

# 任意 Cypher
venv\Scripts\python.exe knowledge_graph\query.py "MATCH (a:Paper)-[r:RELATES]->(b:Paper) WHERE r.rel_type='IMPROVES' RETURN a.id, b.id, r.detail"
```

## 六、复习用 Cypher 速查

```cypher
-- 某篇论文的全部出边/入边（它改进了谁、谁改进了它）
MATCH (p:Paper {id:'vit'})-[r:RELATES]->(q) RETURN r.rel_type, q.id, r.detail
MATCH (q)-[r:RELATES]->(p:Paper {id:'vit'}) RETURN r.rel_type, q.id, r.detail

-- 两篇论文之间的关联路径（≤3 跳），复习承接链路
MATCH path=(a:Paper {id:'transformer'})-[:RELATES*1..3]->(b:Paper {id:'mae'})
RETURN [n IN nodes(path) | n.id]

-- 某条主线全部成员（按序）
MATCH (p:Paper)-[b:BELONGS_TO]->(t:Topic {id:'t_vit_line_d'}) RETURN b.seq, p.id ORDER BY b.seq

-- 某个概念被哪些论文使用/提出
MATCH (p:Paper)-[r:PROPOSES|USES]->(c:Concept {id:'patch_embedding'}) RETURN p.id, type(r)

-- 某论文解决了什么、没解决什么
MATCH (p:Paper {id:'detr'}) RETURN p.problem, p.limitations

-- 精读论文旗舰数字
MATCH (p:Paper) WHERE p.status='已读' RETURN p.id, p.key_results

-- 待读池按路线统计
MATCH (p:Paper)-[:BELONGS_TO]->(t:Topic) WHERE p.status<>'已读'
RETURN t.name, count(p) ORDER BY count(p) DESC
```

## 七、新论文追加流程

1. 精读完一篇论文后，按 `data/SCHEMA_SPEC.md` 写一个 `data/papers/<id>.yaml` 片段
   （可让 subagent 照规范产出，铁律：只写笔记里有的、每条关系带 evidence+source）；
2. 若该论文属于新路线/家族，先在 `data/catalog.yaml` 的 topics 里补 Topic；
3. 重跑 `venv\Scripts\python.exe knowledge_graph\build_graph.py --reset` 全量重建（秒级）；
4. 用 `query.py --paper <id>` 验证新节点与关系。
