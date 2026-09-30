# -*- coding: utf-8 -*-
"""
SWRS 需求 RAG 语料切分脚本

用途：
    以「单条需求」为最小语义单元，将 Base Tech SWRS DHU 的需求条目切分为
    若干语料分卷，供 RAG / 大模型检索使用。切分严格以需求条目为边界，
    保证任一条需求（含其完整正文）不会被拆分到两个语料文件中。

输入：_tools/reqs_raw.json
输出：Basetech知识库语料/ 目录下的分卷语料 + 00_INDEX.md
"""
import os
import re
import sys
import json

BASE = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929"
TOOLS = os.path.join(BASE, "_tools")
sys.path.insert(0, TOOLS)

# 复用清单脚本中的文本清理与字段提取逻辑
from produce_checklist import clean, strip_meta, extract_applicability, VER_RE, TITLE_RE

IN_JSON = os.path.join(BASE, "_tools", "reqs_raw.json")
OUT_DIR = os.path.join(BASE, "Basetech知识库语料")
PER_FILE = 100  # 每卷包含的需求条数
LEGACY_RE = re.compile(r"Legacy ID:\s*(\d+v\d+)")


def render_req(it):
    """将单条需求渲染为一段完整的 RAG 语料文本（含编号、元信息与完整正文）。"""
    raw = clean(it["body"])
    title = clean(it.get("title", ""))
    # 标题缺失或含重复编号时，从正文重新解析
    if not title or re.match(r"^\d{3,4}\s+v\d+", title):
        tm = TITLE_RE.match(raw)
        title = clean(tm.group(1)) if tm else re.sub(r"^\d{3,4}\s+v\d+\s*", "", title)[:120]

    vm = VER_RE.search(raw)
    vm = vm.group(1) if vm else "-"
    applic = extract_applicability(raw)
    legacy = LEGACY_RE.search(raw)
    legacy = legacy.group(1) if legacy else "-"

    # 正文保留完整内容，仅剥离页眉与元信息标签噪声
    body = strip_meta(it["body"])

    return "\n".join([
        f"### {it['id']} — {title}",
        f"- 版本：v{it.get('ver', '')} ｜ 验证方式：{vm} ｜ 适用：{applic} ｜ Legacy ID：{legacy}",
        "",
        body,
        "",
    ])


def main():
    with open(IN_JSON, "r", encoding="utf-8") as f:
        items = json.load(f)
    # 按需求编号数值升序排列
    items.sort(key=lambda x: int(x["id"]))

    os.makedirs(OUT_DIR, exist_ok=True)
    # 只清理本脚本生成的文件，避免误删目录内其他内容
    for name in os.listdir(OUT_DIR):
        if name.startswith("SWRS_DHU_语料_") or name == "00_INDEX.md":
            os.remove(os.path.join(OUT_DIR, name))

    volumes = []
    for start in range(0, len(items), PER_FILE):
        chunk = items[start:start + PER_FILE]
        idx = start // PER_FILE + 1
        lo, hi = chunk[0]["id"], chunk[-1]["id"]
        fname = f"SWRS_DHU_语料_{idx:02d}_{lo}-{hi}.md"

        parts = [
            f"# Base Tech SWRS DHU 需求语料 · 第 {idx:02d} 卷",
            "",
            "> 来源：吉利汽车研究院 Base Tech SWRS DHU 软件需求规范"
            "（Note-SWRS，Revision 005，2019-07-11，共 1572 页）",
            f"> 本卷范围：需求编号 {lo} – {hi}（共 {len(chunk)} 条）",
            "> 切分说明：以单条需求为最小语义单元，条目完整、不跨卷拆分。",
            "",
            "---",
            "",
        ]
        for it in chunk:
            parts.append(render_req(it))

        text = "\n".join(parts)
        with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(text)
        volumes.append((fname, lo, hi, len(chunk), len(text.encode("utf-8"))))

    # 生成总索引
    idx_lines = [
        "# Base Tech SWRS DHU 需求语料 · 总索引",
        "",
        "> 来源：吉利汽车研究院 Base Tech SWRS DHU 软件需求规范"
        "（Note-SWRS，Revision 005，2019-07-11，共 1572 页）",
        f"> 语料总量：{len(items)} 条需求，{len(volumes)} 个分卷",
        "> 切分原则：以单条需求为最小语义单元，任何一条需求（含正文）均不跨卷拆分。",
        "",
        "| 分卷文件 | 需求编号范围 | 条数 | 体积 |",
        "|---------|-------------|------|------|",
    ]
    for fname, lo, hi, cnt, size in volumes:
        idx_lines.append(f"| {fname} | {lo} – {hi} | {cnt} | {size // 1024} KB |")
    idx_lines.append("")
    with open(os.path.join(OUT_DIR, "00_INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines))

    total = sum(v[4] for v in volumes)
    print(f"需求条数: {len(items)}")
    print(f"分卷数: {len(volumes)}")
    print(f"语料总体积: {total} 字节")
    print(f"输出目录: {OUT_DIR}")


if __name__ == "__main__":
    main()
