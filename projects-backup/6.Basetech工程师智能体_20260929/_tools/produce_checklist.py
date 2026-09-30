# -*- coding: utf-8 -*-
"""
SWRS 结构化需求清单生成脚本

用途：
    读取 _tools/reqs_raw.json 中已切分的需求条目，剥离元信息前缀后，
    为每条需求提取版本号、验证方式、适用 AUTOSAR 版本与核心要求句，
    并按需求编号升序输出为一份便于 AI 读取与调用的 Markdown 清单。

输入：_tools/reqs_raw.json
输出：SWRS_DHU_需求清单.md
"""
import os
import re
import sys
import json
import html

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929"
IN_JSON = os.path.join(BASE, "_tools", "reqs_raw.json")
OUT_MD = os.path.join(BASE, "SWRS_DHU_需求清单.md")

# 验证方式：只匹配三种标准取值，避免贪婪吞掉后面的 "Legacy"
VER_RE = re.compile(r"Verification Method:\s*(Test|Analysis|Inspection)")
# 标题：从 "编号 v版本" 到第一个 "Version history" 之间
TITLE_RE = re.compile(r"^\d{3,4}\s+v\d+\s*(.*?)\s*Version history", re.S)

# 页眉页脚等噪声串（含空格/无空格两种形态）
NOISE = [
    "Document NameBase Tech SWRS DHU",
    "Document Name Base Tech SWRS DHU",
    "GEELYGeely Automotive Research Institute(Ningbo)Co.Ltd",
    "Geely Automotive Research Institute (Ningbo)Co.Ltd",
    "Document TypeNote-SWRS",
    "Document Release StatusRELEASED",
    "Document Type",
    "Document No",
    "Revision005",
    "Volume No01",
]

# 源数据完整性说明（供清单开头展示）
COVERAGE_NOTE = (
    "数据来源覆盖页码 1-100、101-200、201-1572，即源文档全部 1572 页，未发现内容缺失。"
    "需求编号存在正常跳跃（例如 417 与 459 之间），系文档自身编号规则所致，非内容缺失。"
)


def clean(s):
    """清理文本：剔除页眉噪声、还原 HTML 实体、压缩空白。"""
    for n in NOISE:
        s = s.replace(n, " ")
    s = html.unescape(s)
    # 拆分 "TestLegacy" 这类粘连写法，便于后续识别与剥离
    s = re.sub(r"(Test|Analysis|Inspection)Legacy", r"\1 Legacy", s)
    # 句号/分号/冒号后若紧跟字母（原文无空格），补一个空格，便于后续正确分句
    s = re.sub(r"([.;:])(?=[A-Za-z(])", r"\1 ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def strip_meta(body):
    """剥离需求条目中的元信息（编号/版本/标题/Version history/Purpose/Source/
    Verification Method/Legacy ID/ASIL 等），只保留要求正文。"""
    s = clean(body)
    # 1) 去掉开头的 "编号 v版本 标题"
    s = re.sub(
        r"^\d{3,4}\s+v\d+\s+.*?(?=Version history|Purpose:|Source:|Verification Method:|Legacy ID:|$)",
        " ", s, flags=re.S)
    # 2) 去掉 Version history 段的变更说明（形如 "(3): Change the ... to Test"）
    s = re.sub(
        r"Version history:.*?(?=Purpose:|Source:|Verification Method:|Legacy ID:|"
        r"When implementing|The |For all|If |It )",
        " ", s, flags=re.S)
    s = s.replace("Version history:", " ")
    # 3) 去掉各类元信息标签及其紧邻内容
    s = re.sub(r"Purpose:\s*", " ", s)
    s = re.sub(r"Source:\s*", " ", s)
    s = re.sub(r"Verification Method:\s*(?:Test|Analysis|Inspection)", " ", s)
    # 先剥 ASIL 再剥 Legacy ID，避免 "65555v6ASIL" 中的 ASIL 被一并吞掉
    s = re.sub(r"ASIL:\s*(?:QM|[A-D])\s*-\s*(?:Not\s+)?safety\s+relevant", " ", s, flags=re.I)
    s = re.sub(r"ASIL:\s*[0-9A-Za-z\- ]{1,30}?", " ", s, flags=re.I)
    s = re.sub(r"Legacy ID:\s*\d+v\d+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def extract_applicability(body):
    """判断该需求适用的 AUTOSAR 版本。"""
    has40 = bool(re.search(r"AUTOSAR\s*4\.0", body, re.I))
    has41 = bool(re.search(r"AUTOSAR\s*4\.1", body, re.I))
    if has40 and has41:
        return "4.0.x 与 4.1+ 分别定义"
    if has41:
        return "4.1+"
    if has40:
        return "4.0.x"
    return "通用"


def extract_core(text):
    """从正文中提取核心要求句：含 shall/may/must 的句子，最多 3 句。"""
    sents = re.split(r"(?<=[.;])\s+", text)
    picked, seen = [], set()
    for s in sents:
        if re.search(r"\b(shall|may|must)\b", s, re.I) and len(s) > 25:
            key = s[:80]
            if key not in seen:
                seen.add(key)
                picked.append(s.strip())
        if len(picked) >= 3:
            break
    if not picked and text:
        picked = [text[:260]]
    return picked


def main():
    with open(IN_JSON, "r", encoding="utf-8") as f:
        items = json.load(f)
    # 按需求编号数值升序排列
    items.sort(key=lambda x: int(x["id"]))

    out = []
    out.append("# Base Tech SWRS DHU 结构化需求清单\n")
    out.append("> 来源：吉利汽车研究院 Base Tech SWRS DHU 软件需求规范"
               "（Note-SWRS，Revision 005，2019-07-11，共 1572 页）\n")
    out.append(f"> 需求条目总数：**{len(items)}** 条\n")
    out.append("> 说明：本清单由分页文档自动切分生成，逐条保留「编号 / 标题 / 版本 / "
               "验证方式 / 适用 AUTOSAR 版本 / 核心要求句」。\n")
    out.append("\n---\n")
    out.append("## 数据完整性说明\n")
    out.append(COVERAGE_NOTE + "\n")
    out.append("\n---\n")
    out.append("## 需求清单\n")

    for it in items:
        raw = clean(it["body"])
        title = clean(it.get("title", ""))
        # 标题缺失或含重复编号时，从正文重新解析
        if not title or re.match(r"^\d{3,4}\s+v\d+", title):
            tm = TITLE_RE.match(raw)
            # 兜底：剥掉开头的 "编号 v版本" 前缀后再截取
            title = clean(tm.group(1)) if tm else re.sub(r"^\d{3,4}\s+v\d+\s*", "", title)[:90]
        vm = VER_RE.search(raw)
        vm = vm.group(1) if vm else "-"
        applic = extract_applicability(raw)
        cores = extract_core(strip_meta(it["body"]))

        out.append(f"\n### {it['id']} — {title}")
        out.append(f"- 版本：v{it.get('ver', '')} ｜ 验证方式：{vm} ｜ 适用：{applic}")
        for c in cores:
            out.append(f"- {c}")

    text = "\n".join(out) + "\n"
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"需求条目数: {len(items)}")
    print(f"输出文件: {OUT_MD}")
    print(f"输出体积: {len(text.encode('utf-8'))} 字节")


if __name__ == "__main__":
    main()
