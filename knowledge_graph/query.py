# -*- coding: utf-8 -*-
"""
论文知识图谱 · Cypher 查询工具

用法（项目根目录下）：
    venv/Scripts/python.exe knowledge_graph/query.py "MATCH (p:Paper {id:'vit'})-[r:RELATES]->(q) RETURN r.rel_type, q.title"
    venv/Scripts/python.exe knowledge_graph/query.py -f knowledge_graph/queries/xx.cypher
    venv/Scripts/python.exe knowledge_graph/query.py --demo        # 跑内置示例查询
    venv/Scripts/python.exe knowledge_graph/query.py --paper vit   # 单篇论文全景速览

说明：Kùzu 数据库实体在纯 ASCII 路径（见 build_graph.py 的 DB_DIR），只读方式打开，
查询不会改动数据。结果以表格打印，LIST 字段自动展开。
"""
import os
import sys
import argparse

import kuzu

HERE = os.path.dirname(os.path.abspath(__file__))
# 与 build_graph.py 保持一致：单文件数据库，放在 ASCII 目录下
DB_FILE = r"C:\Users\26214\paperreading_kgdb\graph.kuzu"


def get_conn():
    db = kuzu.Database(DB_FILE, read_only=True)
    return db, kuzu.Connection(db)


def fmt_cell(v):
    if isinstance(v, list):
        return " | ".join(str(x) for x in v)
    return str(v)


def run_cypher(conn, cypher, params=None):
    """执行一条 Cypher，打印结果表格。返回行数。"""
    result = conn.execute(cypher, params or {})
    cols = None
    if hasattr(result, "get_column_names"):
        raw = result.get_column_names()
        # 兼容两种返回形态：["name", ...] 或 [("name", type), ...]
        cols = [c[0] if isinstance(c, (tuple, list)) else c for c in raw]
    rows = []
    while result.has_next():
        rows.append(result.get_next())
    if cols is None and rows:
        cols = [f"col{i}" for i in range(len(rows[0]))]
    if not rows:
        print("(0 行)")
        return 0
    # 列宽自适应（中文按 2 宽度算）
    def w(x):
        x = str(x)
        return sum(2 if ord(c) > 127 else 1 for c in x)
    widths = [max(w(c or ""), max((w(fmt_cell(r[i])) for r in rows), default=0)) for i, c in enumerate(cols)]
    widths = [min(x, 100) for x in widths]

    def pad(s_, width):
        return s_ + " " * max(0, width - w(s_))

    header = "  ".join(pad(str(c), widths[i]) for i, c in enumerate(cols))
    print(header)
    print("  ".join("-" * widths[i] for i in range(len(cols))))
    for r in rows:
        cells = [fmt_cell(v) for v in r]
        cells = [c if w(c) <= 100 else c[:97] + "..." for c in cells]
        print("  ".join(pad(c, widths[i]) for i, c in enumerate(cells)))
    print(f"({len(rows)} 行)")
    return len(rows)


DEMO_QUERIES = [
    ("图谱规模", "MATCH (p:Paper) RETURN count(p) AS 论文总数"),
    ("已精读论文清单",
     "MATCH (p:Paper) WHERE p.status = '已读' RETURN p.id AS id, p.title AS 标题, p.venue AS venue, p.year AS 年份 ORDER BY p.year"),
    ("ViT 直接关系全景（出边）",
     "MATCH (p:Paper {id:'vit'})-[r:RELATES]->(q:Paper) RETURN r.rel_type AS 关系, q.id AS 对方, r.detail AS 说明"),
    ("ViT 直接关系全景（入边）",
     "MATCH (q:Paper)-[r:RELATES]->(p:Paper {id:'vit'}) RETURN r.rel_type AS 关系, q.id AS 对方, r.detail AS 说明"),
    ("主线 D：Registers → LAST-ViT 的承接证据",
     "MATCH (a:Paper)-[r:RELATES]->(b:Paper) WHERE a.id IN ['registers','last_vit'] AND b.id IN ['registers','last_vit'] RETURN a.id AS 从, r.rel_type AS 关系, b.id AS 到, r.evidence AS 笔记原句"),
    ("两篇论文之间的所有路径（≤3 跳）：transformer → mae",
     "MATCH path = (a:Paper {id:'transformer'})-[:RELATES*1..3]->(b:Paper {id:'mae'}) RETURN list_transform(nodes(path), n -> n.id) AS 路径"),
    ("所有 IMPROVES/SUPERSEDES/REFUTES 关系（谁改进了谁）",
     "MATCH (a:Paper)-[r:RELATES]->(b:Paper) WHERE r.rel_type IN ['IMPROVES','SUPERSEDES','REFUTES'] RETURN a.id AS 从, r.rel_type AS 关系, b.id AS 到, r.detail AS 说明"),
    ("每篇精读论文提出的概念数",
     "MATCH (p:Paper)-[:PROPOSES]->(c:Concept) WHERE p.status='已读' RETURN p.id AS 论文, count(c) AS 概念数, list_slice(collect(c.name), 1, 3) AS 示例 ORDER BY 概念数 DESC"),
    ("被最多论文依赖的概念 Top10",
     "MATCH (p:Paper)-[:USES]->(c:Concept) RETURN c.name AS 概念, count(p) AS 被依赖次数, collect(p.id) AS 论文 ORDER BY 被依赖次数 DESC LIMIT 10"),
    ("数据集使用分布",
     "MATCH (p:Paper)-[e:EVALUATES_ON]->(d:Dataset) WHERE p.status='已读' RETURN d.name AS 数据集, count(p) AS 论文数, collect(p.id) AS 论文"),
    ("阅读路线：ViT 主线 A→D 全部成员",
     "MATCH (p:Paper)-[b:BELONGS_TO]->(t:Topic) WHERE t.id STARTS WITH 't_vit_line' RETURN t.name AS 主线, b.seq AS 序, p.id AS 论文 ORDER BY t.id, b.seq"),
    ("待读池：按路线统计",
     "MATCH (p:Paper)-[:BELONGS_TO]->(t:Topic) WHERE p.status <> '已读' RETURN t.name AS 路线, count(p) AS 待读数 ORDER BY 待读数 DESC"),
]


def paper_overview(conn, pid):
    print(f"===== 论文全景：{pid} =====")
    run_cypher(conn, "MATCH (p:Paper {id:$id}) RETURN p.title AS 标题, p.venue AS venue, p.year AS 年份, p.status AS 状态", {"id": pid})
    print("\n-- 解决的问题 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id}) RETURN p.problem AS problem", {"id": pid})
    print("\n-- 核心贡献 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id}) RETURN p.contributions AS contributions", {"id": pid})
    print("\n-- 局限/未解决 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id}) RETURN p.limitations AS limitations", {"id": pid})
    print("\n-- 关键结论 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id}) RETURN p.key_results AS key_results", {"id": pid})
    print("\n-- 出边关系 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id})-[r:RELATES]->(q:Paper) RETURN r.rel_type AS 关系, q.id AS 到, r.detail AS 说明", {"id": pid})
    print("\n-- 入边关系 --")
    run_cypher(conn, "MATCH (q:Paper)-[r:RELATES]->(p:Paper {id:$id}) RETURN r.rel_type AS 关系, q.id AS 从, r.detail AS 说明", {"id": pid})
    print("\n-- 提出的概念 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id})-[:PROPOSES]->(c:Concept) RETURN c.name AS 概念, c.detail AS 说明", {"id": pid})
    print("\n-- 依赖的技术 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id})-[:USES]->(c:Concept) RETURN c.name AS 技术, c.origin AS 来源", {"id": pid})
    print("\n-- 评测数据集 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id})-[e:EVALUATES_ON]->(d:Dataset) RETURN d.name AS 数据集, e.role AS 角色, e.metrics AS 指标", {"id": pid})
    print("\n-- 所属路线 --")
    run_cypher(conn, "MATCH (p:Paper {id:$id})-[b:BELONGS_TO]->(t:Topic) RETURN t.name AS 路线, b.seq AS 序", {"id": pid})


def main():
    ap = argparse.ArgumentParser(description="论文知识图谱 Cypher 查询工具")
    ap.add_argument("cypher", nargs="?", help="Cypher 查询语句")
    ap.add_argument("-f", "--file", help="从文件读取 Cypher")
    ap.add_argument("--demo", action="store_true", help="运行内置示例查询")
    ap.add_argument("--paper", help="单篇论文全景速览（传 paper id）")
    args = ap.parse_args()

    db, conn = get_conn()
    try:
        if args.demo:
            for title, q in DEMO_QUERIES:
                print(f"\n===== {title} =====")
                print(f"-- {q}")
                run_cypher(conn, q)
        elif args.paper:
            paper_overview(conn, args.paper)
        elif args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                run_cypher(conn, f.read())
        elif args.cypher:
            run_cypher(conn, args.cypher)
        else:
            ap.print_help()
    finally:
        del conn, db


if __name__ == "__main__":
    # Windows 控制台 UTF-8 输出
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
