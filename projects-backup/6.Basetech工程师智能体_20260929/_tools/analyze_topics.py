# -*- coding: utf-8 -*-
"""
Basetech SWRS 文档主题分析脚本

用途：
    统计需求条目标题的高频关键词、Verification Method 分布，
    并按编号区间抽样输出标题，用于归纳文档的技术主题与方法论。
"""
import os
import re
import sys
import json
import collections

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 中间结果 JSON 的绝对路径
JSON_PATH = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929\_tools\reqs_raw.json"
with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)
data.sort(key=lambda x: int(x["id"]))

titles = [x["title"] for x in data]

# 常见虚词，统计关键词时排除
STOP = {
    "shall", "with", "from", "that", "this", "when", "have", "been", "which",
    "using", "used", "they", "their", "other", "also", "into", "than", "then",
    "there", "these", "those", "will", "must", "where", "each", "more", "less",
    "only", "same", "such", "after", "before", "during", "under", "over",
    "between", "within", "without", "supported", "requirement", "requirements",
    "based", "definition", "defined", "support", "value", "values",
}

print("=== 标题高频词 Top 80 ===")
counter = collections.Counter(
    w.lower() for t in titles for w in re.findall(r"[A-Za-z]{4,}", t)
    if w.lower() not in STOP
)
print(", ".join(f"{w}({n})" for w, n in counter.most_common(80)))

print()
print("=== Verification Method 分布 ===")
vm = collections.Counter()
for x in data:
    m = re.search(r"Verification Method:\s*(Test|Analysis|Inspection)", x["body"])
    vm[m.group(1) if m else "未标注"] += 1
print(vm.most_common())

print()
print("=== 按编号区间抽样标题（每 200 条取 8 条）===")
for i in range(0, len(data), 200):
    seg = data[i:i + 200]
    print(f"\n-- 编号 {seg[0]['id']} ~ {seg[-1]['id']} --")
    for x in seg[::25]:
        print(f"  {x['id']} | {x['title'][:95]}")
