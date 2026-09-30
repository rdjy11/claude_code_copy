# -*- coding: utf-8 -*-
"""
SWRS 需求条目提取与规模评估脚本

用途：
    按页码顺序读取全部分页 md 文件，去除 HTML 标签后，依据
    "编号 v版本 标题" 模式切分需求条目，统计条目总数、去重后数量、
    正文体积、标题样例等，为最终「结构化需求清单」的体量评估提供依据。

输出：
    标准输出打印统计信息，并将去重后的条目明细写入 _tools/reqs_raw.json。
"""
import os
import re
import sys
import glob
import json

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SRC_DIR = r"D:\知识库资料源\汽车知识库\Basetech技术文档"
OUT_DIR = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929"

# HTML 标签
TAG_RE = re.compile(r"<[^>]+>")
# 需求条目起点：编号 + v版本（后面可能直接跟标题字母）
REQ_SPLIT_RE = re.compile(r"(?<![\d.])(\d{3,4})\s+v(\d+)(?=\s|[A-Z])")
# 从条目正文中解析标题（到第一个 Version history 之前）
TITLE_RE = re.compile(r"^\d{3,4}\s+v\d+\s*(.*?)\s*Version history", re.S)


def page_sort_key(path):
    """按文件名中的起始页码做数字排序，保证读取顺序与文档页码一致。"""
    m = re.search(r"(\d+)-(\d+)\.md$", path)
    return int(m.group(1)) if m else 0


def load_plain(path):
    """读取文件，去除 HTML 标签并归一化空白，返回纯文本。"""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    text = TAG_RE.sub(" ", raw)
    text = re.sub(r"\s+", " ", text)
    return text


def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.md")), key=page_sort_key)
    parts = [load_plain(p) for p in files]
    text = re.sub(r"\s+", " ", " ".join(parts))

    # 定位所有需求条目起点
    marks = list(REQ_SPLIT_RE.finditer(text))
    print(f"需求起点标记总数: {len(marks)}")

    items = []
    for i, m in enumerate(marks):
        start = m.start()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[start:end].strip()
        tm = TITLE_RE.match(body)
        title = tm.group(1).strip() if tm else body[:80]
        items.append({"id": m.group(1), "ver": m.group(2), "title": title, "body": body})

    # 去重：同一需求编号保留正文最长的那条（通常信息最完整）
    best = {}
    for it in items:
        k = it["id"]
        if k not in best or len(it["body"]) > len(best[k]["body"]):
            best[k] = it

    total = sum(len(v["body"]) for v in best.values())
    print(f"切分条目数: {len(items)}")
    print(f"去重后条目数: {len(best)}")
    print(f"去重后正文总字符: {total}")
    if best:
        print(f"平均每条字符: {total // len(best)}")

    print("\n--- 前 5 条标题样例 ---")
    for k in list(best)[:5]:
        print(f"  [{k}] v{best[k]['ver']} {best[k]['title'][:90]}")

    # 保存中间结果，供后续整合使用
    out = os.path.join(OUT_DIR, "_tools", "reqs_raw.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(list(best.values()), f, ensure_ascii=False, indent=1)
    print(f"\n已保存中间结果: {out}")


if __name__ == "__main__":
    main()
