# -*- coding: utf-8 -*-
"""§12.2 未决项收尾——证据分析脚本（只读，不修改任何产物）。

设计文档 §12.2 列出三项「跑通验证后再定」的未决事项：
  1. bt-carcfg（87 条）是否并入 bt-platform；
  2. 各专家 model 取值是否锁定；
  3. 「时序/性能」是否从 bt-uds 独立成域。

本脚本给出前三项中「可由数据判定」的两项（1 与 3）的可复现证据。
model 取值属成本偏好，不由本脚本判定（见 §12.2 处置记录）。

跑法：python _tools/analyze_open_items.py
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929")
INDEX_DIR = BASE / "_index" / "by-domain"
CORPUS = BASE / "Basetech知识库语料"

# 索引表格行：| 编号 | 标题 | 语料卷 |
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")

# 时序/性能关键词（用于未决项 3 的独立成域可行性评估）
TIMING_KW = [
    "timeout", "time out", "timing", "timer", "p2", "p2*", "s3",
    "response time", "cycle time", "repetition rate", "period",
    "delay", "latency", "deadline", "time restriction", "minimum time",
    "maximum time", "elapsed time", "watchdog", "backoff",
]

# 评审验证（docs/operations/验证记录-完整.md 测试 3）中三处「时序类」偏差所挂编号。
# 若它们分散在不同域，说明时序是横切维度而非独立语义簇。
REVIEW_TIMING_CASES = {
    "P2 统一取 100ms（UDS 时序）": [2622, 2623],
    "N_WFTmax 取 128（传输层时序）": [1209, 1210],
    "上电 5 秒具备诊断（平台启动时序）": [1673, 2362],
}

_TOK = re.compile(r"^[a-z0-9 ]+$")


def load_index(path):
    """读一份域索引，返回 {需求编号: 标题}。"""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def hits(text, kw):
    """与 build_domain_index.py 同构的双通道匹配：词边界 + camelCase。

    纯小写词用词边界正则（避免 can 命中 cannot）；含非小写词的退化为子串匹配。
    """
    if _TOK.match(kw):
        strict = re.compile(r"(?<![a-z0-9])" + re.escape(kw) + r"(?![a-z0-9])")
        camel = re.compile(r"(?<![A-Za-z0-9])(?i:" + re.escape(kw) + r")(?=[A-Z])")
        return bool(strict.search(text) or camel.search(text))
    return kw.lower() in text.lower()


def main():
    domains = {p.stem: load_index(p) for p in sorted(INDEX_DIR.glob("bt-*.md"))}

    # ---------- 基线：各域体量 ----------
    print("=" * 62)
    print("各域体量（以 _index/by-domain/ 实际条目数为准）")
    print("=" * 62)
    for name, d in sorted(domains.items(), key=lambda kv: -len(kv[1])):
        print(f"  {name:<22} {len(d):>5}")
    total = sum(len(d) for d in domains.values())
    union = set()
    for d in domains.values():
        union |= set(d)
    print(f"  {'合计条目（含多标签）':<20} {total:>5}")
    print(f"  {'并集覆盖需求数':<22} {len(union):>5}")
    print(f"  并集 + 元规则 3 条 = {len(union) + 3}（应等于需求总数 1999）")

    # ---------- 未决项 1：bt-carcfg 是否并入 bt-platform ----------
    print()
    print("=" * 62)
    print("未决项 1｜bt-carcfg 是否并入 bt-platform")
    print("  设计文档设定的触发条件：『与平台问题高频共现』")
    print("=" * 62)
    cc = set(domains["bt-carcfg"])
    others_union = set()
    for n, d in domains.items():
        if n != "bt-carcfg":
            others_union |= set(d)
    solo = cc - others_union
    print(f"  bt-carcfg 总数                  {len(cc)}")
    print(f"  仅 carcfg 单标签（其余域不收）   {len(solo)}"
          f"  （{len(solo)/len(cc)*100:.1f}%）")
    print("\n  bt-carcfg 与各域共现数（由高到低）—— 看谁才是最近邻：")
    for n, d in sorted(domains.items(), key=lambda kv: -len(cc & set(kv[1]))):
        if n == "bt-carcfg":
            continue
        k = len(cc & set(d))
        if k:
            mark = "  ← 设计文档设想的合并目标" if n == "bt-platform" else ""
            print(f"    {n:<22} {k:>4}  （{k/len(cc)*100:>5.1f}%）{mark}")

    # ---------- 未决项 3：时序是否独立成域 ----------
    print()
    print("=" * 62)
    print("未决项 3｜「时序/性能」是否从 bt-uds 独立成域")
    print("  设计文档设定的触发条件：『评审频繁涉及 P2/S3』")
    print("=" * 62)

    timing = set()
    for f in sorted(CORPUS.glob("*.md")):
        if f.name.startswith("00_"):
            continue
        txt = f.read_text(encoding="utf-8", errors="ignore")
        parts = re.split(r"^### (\d+) — ", txt, flags=re.M)
        for i in range(1, len(parts) - 1, 2):
            rid, body = int(parts[i]), parts[i + 1]
            if any(hits(body, k) for k in TIMING_KW):
                timing.add(rid)

    print(f"  以 {len(TIMING_KW)} 个时序关键词扫全文，命中 {len(timing)} 条"
          f"（设计阶段估算 346 条）")
    print("\n  各域当前承担的时序条目数（即独立后会被抽走多少）：")
    for n, d in sorted(domains.items(), key=lambda kv: -len(timing & set(kv[1]))):
        k = len(timing & set(d))
        if k:
            print(f"    {n:<22} {k:>4} / {len(d):>4}  （占该域 {k/len(d)*100:>5.1f}%）")

    covered = [r for r in timing if any(r in d for d in domains.values())]
    multi = [r for r in timing
             if sum(1 for d in domains.values() if r in d) >= 3]
    print(f"\n  时序条目已被现有域覆盖：{len(covered)}/{len(timing)}")
    print(f"  其中被 ≥3 个域共同覆盖：{len(multi)}")

    print("\n  评审验证中三处「时序类」偏差的落域（关键判据）：")
    for label, ids in REVIEW_TIMING_CASES.items():
        print(f"    {label}")
        for rid in ids:
            owners = [n for n, d in domains.items() if rid in d]
            print(f"        {rid} → {', '.join(owners)}")


if __name__ == "__main__":
    main()
