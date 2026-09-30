# -*- coding: utf-8 -*-
"""
SWRS 源文档结构核查脚本

用途：
    扫描「Basetech技术文档」目录下的全部分页 md 文件，统计每份文件实际
    覆盖的页码范围、需求条目编号（形如 "2121 v3"）、章节号（形如 "4.5.2.1"），
    用于判断原始分页导出是否存在重复或缺失。

输出：
    在标准输出打印核查报告（各文件覆盖范围 + 全库汇总）。
"""
import os
import re
import sys
import glob

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 源文档目录
SRC_DIR = r"D:\知识库资料源\汽车知识库\Basetech技术文档"

# 页码标记，如 "Page No101(1572)" 或纯文本 "101(1572)"
PAGE_RE = re.compile(r"(\d+)\s*\(\s*1572\s*\)")
# 需求条目编号 + 版本号，如 "2121 v3 Sampling..."、"2315 v1Access to..."
REQ_RE = re.compile(r"(?<![\d.])(\d{3,4})\s+v(\d+)(?=\s|[A-Z])")
# 章节号，如 "4.5.2.1"、"4.1"
SEC_RE = re.compile(r"(?<![\d.])4(?:\.\d+){1,7}(?![\d])")
# HTML 标签
TAG_RE = re.compile(r"<[^>]+>")


def page_sort_key(path):
    """按文件名中的起始页码做数字排序，确保 1-100 排在 101-200 之前。"""
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
    all_reqs = set()
    all_pages = set()
    print("=" * 72)
    print("SWRS 源文档结构核查报告")
    print("=" * 72)
    for path in files:
        text = load_plain(path)
        pages = sorted({int(p) for p in PAGE_RE.findall(text)})
        reqs = sorted({int(m.group(1)) for m in REQ_RE.finditer(text)})
        vh = len(re.findall(r"Version history", text))
        all_reqs.update(reqs)
        all_pages.update(pages)
        name = os.path.basename(path)
        pr = f"{pages[0]}~{pages[-1]}" if pages else "无"
        print(f"\n[{name}]")
        print(f"  页码标记 {len(pages)} 个，范围 {pr}")
        print(f"  Version history 出现 {vh} 次")
        print(f"  需求条目 {len(reqs)} 条: {','.join(map(str, reqs))}")
    print("\n" + "=" * 72)
    print(f"全库去重: 页码标记 {len(all_pages)} 个, 需求条目编号 {len(all_reqs)} 条")
    if all_pages:
        print(f"页码标记总范围: {min(all_pages)} ~ {max(all_pages)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
