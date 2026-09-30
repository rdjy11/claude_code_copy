# -*- coding: utf-8 -*-
"""
SWRS DHU 文档目录（TOC）提取脚本

用途：
    从源文档第 1 个分页文件（含封面与目录）中提取一/二级章节号与标题，
    用于梳理文档覆盖的全部技术领域，作为团队角色划分的依据。

输出：
    标准输出打印 1~2 级章节清单。
"""
import os
import re
import sys

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 源文档目录（绝对路径）
SRC_DIR = r"D:\知识库资料源\汽车知识库\Basetech技术文档"
SRC_FILE = os.path.join(SRC_DIR, "full_1-100.md")

# 章节行：以 "数字[.数字[.数字]]" 开头，后接英文标题
CHAPTER_RE = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,2})\s+([A-Za-z][^.]{0,90})")
# 行尾的页码与省略号（如 " .... 84" 或 " 84"）
TAIL_RE = re.compile(r"[\s.…]+\d{0,4}\s*$")


def main():
    text = open(SRC_FILE, encoding="utf-8", errors="replace").read()
    # 剥离 HTML 标签
    text = re.sub(r"<[^>]+>", " ", text)

    seen = set()
    for raw in text.splitlines():
        line = raw.strip()
        m = CHAPTER_RE.match(line)
        if not m:
            continue
        num = m.group(1)
        if num in seen:
            continue
        seen.add(num)
        title = TAIL_RE.sub("", m.group(2)).strip()
        indent = "    " * num.count(".")
        print(f"{indent}{num}  {title}")


if __name__ == "__main__":
    main()
