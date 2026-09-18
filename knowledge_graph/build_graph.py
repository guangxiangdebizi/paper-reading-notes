# -*- coding: utf-8 -*-
"""
论文知识图谱构建器（Kùzu 嵌入式图数据库）。

数据来源：knowledge_graph/data/*.yaml（papers.yaml 精读论文富信息 + catalog.yaml 待读/登记目录）。
设计原则：忠实笔记原文、高信息密度、每个节点/关系可溯源（source 精确到笔记文件）。

用法：
    venv/Scripts/python.exe knowledge_graph/build_graph.py            # 全量重建
    venv/Scripts/python.exe knowledge_graph/build_graph.py --reset    # 先删库再重建

注意：Kùzu 0.11 无法在含非 ASCII 字符的路径上打开数据库（实测报 "Cannot open file"）。
因此数据库实体存放在纯 ASCII 路径 DB_FILE；项目内 knowledge_graph/db 是指向它所在目录的
junction（目录联接），方便在项目里直接看到。脚本一律打开 DB_FILE。
"""
import os
import sys
import shutil
import argparse

import yaml
import kuzu

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
# 纯 ASCII 实体路径（Kùzu 要求）；项目内 knowledge_graph/db 为指向它的 junction
# 注意：Kùzu 0.11 数据库是单文件格式，DB_FILE 不能是已存在的目录
DB_PARENT = r"C:\Users\26214\paperreading_kgdb"
DB_FILE = os.path.join(DB_PARENT, "graph.kuzu")

# ---- 关系类型词表（RELATES.rel_type 取值，语义见 README）----
REL_TYPES = {
    "INHERITS",         # 继承/采用架构（如 DETR 采用 Transformer）
    "IMPROVES",         # 改进（如 Swin 改进 ViT）
    "CONTINUES",        # 续作/解释根因（如 LAST-ViT 续 Registers）
    "SUPERSEDES",       # 对比超越/终结其时代（如 RAFT 终结 PWC-Net）
    "CONTRAST",         # 对比（不分胜负的对照，如 ConvNeXt 对照 Swin）
    "REFUTES",          # 反驳/回应其论点（如 ConvNeXt 反驳 ViT 大数据论点）
    "INSPIRES",         # 启发/思想源头（如 ViT §4.6 启发 MAE）
    "BORROWS",          # 借鉴技巧（如 RAFT 借鉴 FlowNet2 梯度截断）
    "PROVIDES_RECIPE",  # 提供配方/基座（如 DeiT 提供配方给 ConvNeXt）
    "CORROBORATES",     # 立场呼应（弱关系，如 Swin↔ConvNeXt）
    "FOLLOWS",          # 阅读路线承接顺序（来自 catalog）
    "USES_AS_TOOL",     # 作为工具/验证手段引用（如 Registers 用 LOST）
    "DISTINGUISHES",    # 角色区分/对比表（如 Registers vs DETR object query）
}


def load_yaml(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_paper_fragments():
    """优先加载 data/papers/*.yaml 单篇片段（每篇一个文件，subagent 逐篇产出）；
    若目录为空，回退到 data/papers.yaml 单体模式。返回 paper dict 列表。"""
    frag_dir = os.path.join(DATA_DIR, "papers")
    papers = []
    if os.path.isdir(frag_dir):
        for fn in sorted(os.listdir(frag_dir)):
            if not fn.endswith((".yaml", ".yml")):
                continue
            doc = load_yaml(os.path.join(frag_dir, fn))
            if isinstance(doc, dict) and "paper" in doc:
                papers.append(doc["paper"])
            elif isinstance(doc, dict) and "papers" in doc:
                papers.extend(doc["papers"] or [])
    if not papers:
        mono = load_yaml(os.path.join(DATA_DIR, "papers.yaml")) or {}
        papers = mono.get("papers", []) or []
    return papers


def s(v, default=""):
    """字符串化，None -> default。"""
    if v is None:
        return default
    return str(v)


def lst(v):
    """列表化，None/标量 -> []。"""
    if v is None:
        return []
    if isinstance(v, list):
        return [s(x) for x in v]
    return [s(v)]


def i64(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
DDL = [
    # 节点表
    """CREATE NODE TABLE Paper(
        id STRING, title STRING, aliases STRING[], authors STRING,
        affiliation STRING, year INT64, venue STRING, arxiv STRING,
        status STRING, notes_path STRING, problem STRING,
        contributions STRING[], limitations STRING[], key_results STRING[],
        source STRING, PRIMARY KEY(id))""",
    """CREATE NODE TABLE Topic(
        id STRING, name STRING, kind STRING, parent STRING,
        description STRING, source STRING, PRIMARY KEY(id))""",
    """CREATE NODE TABLE Concept(
        id STRING, name STRING, detail STRING, origin STRING,
        source STRING, PRIMARY KEY(id))""",
    """CREATE NODE TABLE Dataset(
        name STRING, scale STRING, source STRING, PRIMARY KEY(name))""",
    """CREATE NODE TABLE Problem(
        id STRING, description STRING, source STRING, PRIMARY KEY(id))""",
    # 关系表
    """CREATE REL TABLE RELATES(FROM Paper TO Paper,
        rel_type STRING, detail STRING, evidence STRING,
        source STRING, confidence STRING)""",
    """CREATE REL TABLE PROPOSES(FROM Paper TO Concept, detail STRING, source STRING)""",
    """CREATE REL TABLE USES(FROM Paper TO Concept, detail STRING, source STRING)""",
    """CREATE REL TABLE EVALUATES_ON(FROM Paper TO Dataset,
        role STRING, metrics STRING, source STRING)""",
    """CREATE REL TABLE ADDRESSES(FROM Paper TO Problem, source STRING)""",
    """CREATE REL TABLE BELONGS_TO(FROM Paper TO Topic, seq INT64, source STRING)""",
]


def create_schema(conn):
    for stmt in DDL:
        conn.execute(stmt)


# ---------------------------------------------------------------------------
# 插入辅助
# ---------------------------------------------------------------------------
def create_node(conn, table, props):
    """用命名参数 CREATE 一个节点（Kùzu 不支持 map 参数，须逐字段 $name）。"""
    keys = list(props.keys())
    clause = ", ".join(f"{k}:${k}" for k in keys)
    conn.execute(f"CREATE (n:{table} {{{clause}}})", props)


def create_rel(conn, from_table, from_key, from_val,
               rel_table, to_table, to_key, to_val, props):
    keys = list(props.keys())
    clause = (", ".join(f"{k}:${k}" for k in keys)) if keys else ""
    if clause:
        clause = " {" + clause + "}"
    q = (f"MATCH (a:{from_table}) WHERE a.{from_key} = $fv "
         f"MATCH (b:{to_table}) WHERE b.{to_key} = $tv "
         f"CREATE (a)-[:{rel_table}{clause}]->(b)")
    params = {"fv": from_val, "tv": to_val}
    params.update(props)
    conn.execute(q, params)


# ---------------------------------------------------------------------------
# 主构建流程
# ---------------------------------------------------------------------------
def build(reset=False):
    # 始终全量重建（删旧库文件），保证幂等：YAML 是唯一事实源
    for f in (DB_FILE, DB_FILE + ".wal"):
        if os.path.exists(f):
            os.remove(f)
    os.makedirs(DB_PARENT, exist_ok=True)

    db = kuzu.Database(DB_FILE)
    conn = kuzu.Connection(db)
    create_schema(conn)

    read_papers = load_paper_fragments()
    catalog_yaml = load_yaml(os.path.join(DATA_DIR, "catalog.yaml")) or {}
    cat_papers = catalog_yaml.get("papers", []) or []
    topics = catalog_yaml.get("topics", []) or []
    follows = catalog_yaml.get("follows", []) or []

    # ---- 1. 收集全部 Paper（精读 + 目录），去重 ----
    paper_index = {}   # id -> dict
    for p in read_papers + cat_papers:
        pid = s(p.get("id"))
        if not pid:
            continue
        if pid in paper_index:
            # 精读条目优先覆盖目录条目（信息更富）
            if p in read_papers:
                paper_index[pid] = p
            continue
        paper_index[pid] = p

    # 关系目标里引用到、但两个文件都没建的论文 -> 建 stub，避免丢边
    def ensure_paper(pid):
        if pid not in paper_index:
            paper_index[pid] = {
                "id": pid, "title": pid, "status": "被引用·未建条目",
                "source": "(由关系推断，待补全)",
            }

    for p in read_papers:
        for r in p.get("relates", []) or []:
            ensure_paper(s(r.get("to")))
    for f in follows:
        ensure_paper(s(f.get("from")))
        ensure_paper(s(f.get("to")))

    # ---- 2. 插入 Paper 节点 ----
    for pid, p in paper_index.items():
        create_node(conn, "Paper", {
            "id": pid,
            "title": s(p.get("title", pid)),
            "aliases": lst(p.get("aliases")),
            "authors": s(p.get("authors")),
            "affiliation": s(p.get("affiliation")),
            "year": i64(p.get("year"), 0),
            "venue": s(p.get("venue")),
            "arxiv": s(p.get("arxiv")),
            "status": s(p.get("status")),
            "notes_path": s(p.get("notes_path")),
            "problem": s(p.get("problem")),
            "contributions": lst(p.get("contributions")),
            "limitations": lst(p.get("limitations")),
            "key_results": lst(p.get("key_results")),
            "source": s(p.get("source")),
        })

    # ---- 3. 插入 Topic 节点 ----
    for t in topics:
        tid = s(t.get("id"))
        if not tid:
            continue
        create_node(conn, "Topic", {
            "id": tid, "name": s(t.get("name", tid)), "kind": s(t.get("kind")),
            "parent": s(t.get("parent")), "description": s(t.get("description")),
            "source": s(t.get("source")),
        })

    # ---- 4. Concept / Dataset / Problem 去重收集 ----
    concepts = {}   # id -> dict
    datasets = {}   # name -> dict
    problems = {}   # id -> dict

    def add_concept(c):
        cid = s(c.get("id"))
        if cid and cid not in concepts:
            concepts[cid] = {
                "id": cid, "name": s(c.get("name", cid)),
                "detail": s(c.get("detail")), "origin": s(c.get("origin")),
                "source": s(c.get("source")),
            }
        return cid

    def add_dataset(d):
        nm = s(d.get("name"))
        if not nm:
            return ""
        # 名称大小写归一化去重（ImageNet-1K / ImageNet-1k 视为同一数据集）
        key = nm.lower().replace(" ", "")
        if key not in datasets:
            datasets[key] = {"name": nm, "scale": s(d.get("scale")),
                             "source": s(d.get("source"))}
        else:
            # 合并信息：已有条目缺 scale 而新条目有，则补上
            if not datasets[key]["scale"] and d.get("scale"):
                datasets[key]["scale"] = s(d.get("scale"))
        return datasets[key]["name"]

    def add_problem(pr):
        pid = s(pr.get("id"))
        if pid and pid not in problems:
            problems[pid] = {"id": pid, "description": s(pr.get("description")),
                             "source": s(pr.get("source"))}
        return pid

    for p in read_papers:
        for c in p.get("concepts", []) or []:
            add_concept(c)
        for c in p.get("depends", []) or []:
            add_concept(c)
        for d in p.get("datasets", []) or []:
            add_dataset(d)
        for pr in p.get("problems", []) or []:
            add_problem(pr)

    for cid, c in concepts.items():
        create_node(conn, "Concept", c)
    for nm, d in datasets.items():
        create_node(conn, "Dataset", d)
    for pid, pr in problems.items():
        create_node(conn, "Problem", pr)

    # ---- 5. 插入关系 ----
    stats = {"RELATES": 0, "PROPOSES": 0, "USES": 0, "EVALUATES_ON": 0,
             "ADDRESSES": 0, "BELONGS_TO": 0}

    for p in read_papers:
        pid = s(p.get("id"))
        src_default = s(p.get("source"))
        # 5a. RELATES（论文间关系）
        for r in p.get("relates", []) or []:
            to = s(r.get("to"))
            rt = s(r.get("rel_type"), "CONTRAST").upper()
            if rt not in REL_TYPES:
                print(f"  [warn] 未知 rel_type '{rt}'（{pid}->{to}），按 CONTRAST 处理")
                rt = "CONTRAST"
            create_rel(conn, "Paper", "id", pid, "RELATES", "Paper", "id", to, {
                "rel_type": rt, "detail": s(r.get("detail")),
                "evidence": s(r.get("evidence")),
                "source": s(r.get("source"), src_default),
                "confidence": s(r.get("confidence"), "medium"),
            })
            stats["RELATES"] += 1
        # 5b. PROPOSES（提出的方法/概念）
        for c in p.get("concepts", []) or []:
            cid = add_concept(c)
            if cid:
                create_rel(conn, "Paper", "id", pid, "PROPOSES", "Concept", "id", cid,
                           {"detail": s(c.get("detail")), "source": s(c.get("source"), src_default)})
                stats["PROPOSES"] += 1
        # 5c. USES（依赖/借鉴的外部技术）
        for c in p.get("depends", []) or []:
            cid = add_concept(c)
            if cid:
                create_rel(conn, "Paper", "id", pid, "USES", "Concept", "id", cid,
                           {"detail": s(c.get("detail")), "source": s(c.get("source"), src_default)})
                stats["USES"] += 1
        # 5d. EVALUATES_ON
        for d in p.get("datasets", []) or []:
            nm = add_dataset(d)
            if nm:
                create_rel(conn, "Paper", "id", pid, "EVALUATES_ON", "Dataset", "name", nm,
                           {"role": s(d.get("role")), "metrics": s(d.get("metrics")),
                            "source": s(d.get("source"), src_default)})
                stats["EVALUATES_ON"] += 1
        # 5e. ADDRESSES
        for pr in p.get("problems", []) or []:
            prid = add_problem(pr)
            if prid:
                create_rel(conn, "Paper", "id", pid, "ADDRESSES", "Problem", "id", prid,
                           {"source": s(pr.get("source"), src_default)})
                stats["ADDRESSES"] += 1
        # 5f. BELONGS_TO（精读论文也可挂 topic；片段字段名为 order，兼容 seq）
        for b in p.get("belongs_to", []) or []:
            tid = s(b.get("topic") if isinstance(b, dict) else b)
            seq = i64(b.get("order", b.get("seq")) if isinstance(b, dict) else None, 0)
            if tid:
                create_rel(conn, "Paper", "id", pid, "BELONGS_TO", "Topic", "id", tid,
                           {"seq": seq, "source": s(b.get("source") if isinstance(b, dict) else "", src_default)})
                stats["BELONGS_TO"] += 1

    # 5g. catalog 论文的 BELONGS_TO
    for p in cat_papers:
        pid = s(p.get("id"))
        for b in p.get("belongs_to", []) or []:
            tid = s(b.get("topic") if isinstance(b, dict) else b)
            seq = i64(b.get("order"), 0) if isinstance(b, dict) else 0
            if tid:
                create_rel(conn, "Paper", "id", pid, "BELONGS_TO", "Topic", "id", tid,
                           {"seq": seq, "source": s(b.get("source") if isinstance(b, dict) else "", s(p.get("source")))})
                stats["BELONGS_TO"] += 1

    # 5h. FOLLOWS（路线承接，作为 RELATES 的一种 rel_type）
    for f in follows:
        frm, to = s(f.get("from")), s(f.get("to"))
        if not frm or not to:
            continue
        create_rel(conn, "Paper", "id", frm, "RELATES", "Paper", "id", to, {
            "rel_type": "FOLLOWS", "detail": s(f.get("detail")),
            "evidence": "", "source": s(f.get("source")), "confidence": "route",
        })
        stats["RELATES"] += 1

    # ---- 6. 统计 ----
    def count(table):
        r = conn.execute(f"MATCH (n:{table}) RETURN count(n)")
        return r.get_next()[0]

    print("=" * 56)
    print("知识图谱构建完成")
    print("=" * 56)
    print(f"数据库文件（实体）: {DB_FILE}")
    print(f"项目内视图（junction）: {os.path.join(HERE, 'db')}")
    print("-" * 56)
    for t in ["Paper", "Topic", "Concept", "Dataset", "Problem"]:
        print(f"  节点 {t:<10}: {count(t)}")
    print("-" * 56)
    for k, v in stats.items():
        print(f"  关系 {k:<14}: {v}")
    # 精读 vs 待读
    r = conn.execute("MATCH (p:Paper) WHERE p.status = '已读' RETURN count(p)")
    print(f"  其中已精读论文 : {r.get_next()[0]}")
    print("=" * 56)

    del conn, db


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="先删除旧库再全量重建")
    args = ap.parse_args()
    build(reset=args.reset)
