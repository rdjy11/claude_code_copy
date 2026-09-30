# -*- coding: utf-8 -*-
"""
SWRS 需求领域索引生成脚本

用途：
    依据关键词规则，把 1999 条需求归类到 11 个专家域（多标签：一条需求可同时
    落入多个域），并生成：
      - _index/by-domain/<专家名>.md   每域一份「编号 + 标题 + 语料卷」小索引
      - _index/meta-rules.md           文档元规则清单（仅供编排者判定优先级）
    同时输出「未命中清单」，用于人工补词直到零无处置盲区。

输入（只读）：_tools/reqs_raw.json
输出：_index/by-domain/*.md（11 份）、_index/meta-rules.md
"""
import os
import re
import sys
import json

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 项目根目录（绝对路径）
BASE = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929"
JSON_PATH = os.path.join(BASE, "_tools", "reqs_raw.json")

# 专家名 -> 中文域标题
EXPERT_TITLES = {
    "bt-dtc": "DTC / 故障管理",
    "bt-uds": "UDS 诊断服务",
    "bt-diag-transport": "诊断传输层 / 网关",
    "bt-flash": "刷写 / 软件下载",
    "bt-ethernet": "车载以太网 / IP",
    "bt-can-lin-flexray": "CAN / LIN / FlexRay",
    "bt-a2b-lvds": "A2B / LVDS 高速链路",
    "bt-nm": "网络管理",
    "bt-carcfg": "车辆配置 CC / CCP",
    "bt-security": "信息安全",
    "bt-platform": "ECU 平台 / AUTOSAR",
}

# 关键词一律小写；匹配时对「标题 + 正文」做 .lower() 后按词边界匹配
EXPERT_KEYWORDS = {
    "bt-dtc": ["dtc", "dtcs", "fault", "detection", "diagnostic trouble", "freeze frame",
               "snapshot", "readdtcinformation", "cleardiagnosticinformation", "dtcstatus",
               "reportdtc", "dtc setting", "controldtcsetting", "suppressed dtc",
               "snapshot record", "extended data", "permanent status", "status mask",
               "failure type"],
    "bt-uds": ["uds", "service", "services", "diagnostic", "diagnostics",
               "did", "readdata", "writedata", "routinecontrol", "routine", "routines",
               "sub-function", "session", "securityaccess", "tester present", "testerpresent",
               "communication control", "nrc", "suppress positive response",
               "negative response", "positive response", "response message",
               "entry condition", "entry conditions", "affecting ecu functionality",
               "data record", "data records", "data identifier", "data identifiers",
               "register read", "timeout", "timing", "p2", "s3", "response time",
               "period", "latency", "ecureset",
               "cleardiagnosticinformation", "dynamicallydefinedataidentifier",
               "readdatabyidentifier", "readdatabyperiodicidentifier",
               "readmemorybyaddress", "writedatabyidentifier", "writememorybyaddress",
               "readgenericinformation", "diagnosticsessioncontrol",
               "requestdownload", "requestupload", "requestfiletransfer",
               "requesttransferexit", "transferdata", "inputoutputcontrolbyidentifier"],
    "bt-diag-transport": ["doip", "docan", "transport layer", "n_pdu", "isolation",
                          "addressing", "functional address", "physical address", "gateway",
                          "functional request", "in-vehicle gw", "n_wftmax", "wftmax"],
    "bt-flash": ["software download", "bootloader", "flash", "programming", "delta encoding",
                 "delta file", "compression", "decompression", "reprogram", "vbf", "swdl", "ota",
                 "requestdownload", "requestupload", "requestfiletransfer",
                 "requesttransferexit", "transferdata", "block sequence",
                 "installation", "software part", "erase", "memory size",
                 "compatible validation", "data section", "description identifier"],
    "bt-ethernet": ["ethernet", "ipv4", "ipv6", "tcp", "udp", "vlan", "rtp", "tsn",
                    "wlan", "socket", "grandmaster", "gptp", "ptp", "domain id",
                    "nomadic", "ip address", "ip address range",
                    "multicast", "arp", "icmp", "fragmentation", "fragmented", "time-to-live",
                    "congestion", "port number", "port scan", "routing", "throughput",
                    "broadcast", "ip traffic", "ip implementation", "tcp connection",
                    "tcpconnection", "ip bus", "ip command", "ip application",
                    "link monitoring", "mib", "resource group", "lsc", "lm module",
                    "notification", "operationid", "datagram", "reassembl", "retransmission",
                    "domain master", "progsignature", "edge node", "wifi", "wi-fi", "p2p",
                    "ssid", "wireless", "tuned scanning", "fixed bytes", "scan setting",
                    "payload", "concurrent", "parallel communication", "message sequence",
                    "datatype"],
    "bt-can-lin-flexray": ["can", "canfd", "can-fd", "canh", "canl", "can id",
                           "can frame", "can bus", "lin", "lin bus", "lin slave",
                           "lin master", "flexray", "static segment", "dynamic segment",
                           "bus speed", "resynchronisation", "sample mode", "controller area network",
                           "header", "headers", "frame", "frames",
                           "cold start", "warm start", "checksum", "check-sum", "endianness",
                           "heartbeat", "bus signal", "message length", "buffersize"],
    "bt-a2b-lvds": ["a2b", "lvds", "serializer", "deserializer", "fpd-link", "coax", "i2c",
                    "verifylinkcommunication", "equalization", "preemphasis", "prbs",
                    "pll", "1wire", "2wire", "4wire",
                    "header frame", "response frame"],
    "bt-nm": ["network management", "nm message", "wake up", "wakeup", "sleep", "bus wakeup",
              "partial network", "networkstatus", "network request", "resume com",
              "resumecom", "pnc", "powerwakeup", "wakeuptoapp", "tcan", "tfr"],
    "bt-carcfg": ["car configuration", "ccp", "vcp", "config parameter", "vehicle configuration",
                  "local configuration"],
    "bt-security": ["security", "hsm", "certificate", "authentication", "encryption",
                    "signature", "signing", "random number", "privacy", "cyber",
                    "secure boot", "mac", "hash function", "private key", "public key",
                    "integrity check", "hardening", "sha256", "rsa2048", "verification block",
                    "privilege",
                    "asil", "fmea", "iso 26262", "safety related", "safe state",
                    "functional safety"],
    # 注：刻意不收 wire / pin / connector / power —— 这四词在本规范里大量指向
    # LVDS 链路（one-wire / two-wire / four-wire）与总线事件（Power on - master
    # sends the first header），会把 A2B/LVDS 与总线域的需求错收进平台域。
    "bt-platform": ["autosar", "bsw", "rte", "ecu platform", "tier1", "tier2",
                    "startup time", "start up", "start-up", "startup",
                    "hardware", "voltage", "supply", "ground", "battery", "transceiver",
                    "termination", "conformance",
                    "interrupted communication", "secondary processor", "persistency",
                    "asil", "fmea", "iso 26262", "safety related", "safe state",
                    "functional safety"],
}

# 文档元规则判定词（不属任何技术域，归编排者）
META_KEYWORDS = ["document precedence", "priority between", "priority of documents"]

# 泛化词：**只在标题中**参与匹配。
# 需求正文平均 1357 字符，frame / power / wire / service 这类英文常用词在正文里
# 几乎必然出现，若一并计入会把大量无关需求卷进域索引（实测 bt-can-lin-flexray
# 曾有 48% 的条目仅靠正文泛词命中，甚至把「one-wire LVDS」错收进 bt-platform）。
# 标题短且作者有意为之，泛词出现在标题里才是可靠信号。
WEAK_KEYWORDS = {
    "frame", "frames", "header", "headers", "period", "supply", "ground",
    "payload", "broadcast", "routing", "throughput", "concurrent",
    "notification", "service", "services", "diagnostic", "diagnostics", "session",
    "timing", "timeout", "latency", "detection", "fault", "can", "lin",
    "hardware", "message length", "scan setting",
}

# 语料分卷：(短名, 起, 止)，须与 Basetech知识库语料/ 下的文件名一致
VOLUMES = [
    ("01_355-491", 355, 491), ("02_492-1128", 492, 1128), ("03_1129-1228", 1129, 1228),
    ("04_1229-1368", 1229, 1368), ("05_1369-1510", 1369, 1510), ("06_1511-1615", 1511, 1615),
    ("07_1625-1821", 1625, 1821), ("08_1822-1921", 1822, 1921), ("09_1922-2021", 1922, 2021),
    ("10_2022-2121", 2022, 2121), ("11_2122-2221", 2122, 2221), ("12_2222-2321", 2222, 2321),
    ("13_2322-2425", 2322, 2425), ("14_2426-2526", 2426, 2526), ("15_2527-2651", 2527, 2651),
    ("16_2653-2765", 2653, 2765), ("17_2766-3070", 2766, 3070), ("18_3071-3356", 3071, 3356),
    ("19_3357-3532", 3357, 3532), ("20_3533-6724", 3533, 6724),
]

# 纯字母数字的单字关键词（can / s3 / mac 等）需按词边界匹配，
# 否则 "cannot" 会误命中 "can"、"candidate" 亦然。含空格或连字符的关键词按子串匹配。
_TOKEN_RE = re.compile(r"^[a-z0-9]+$")


def _compile(keyword):
    """
    把单字关键词编译成两条正则；非单字关键词返回 None（走子串匹配）。

    为什么是两条：本规范大量使用驼峰技术标识符（readDataByIdentifier、
    ReadDTCInformation、DTCNumber）。只按「后邻非字母数字」判定词边界，会使
    'readdata' 在 'readdatabyidentifier' 中拒绝匹配，导致整个 UDS 服务族漏配；
    反之若放宽成纯子串，'can' 又会命中 'cannot'。

    故分两路任一命中即可：
      - strict：小写全文上「前后皆非字母数字」——覆盖独立词（CAN、DTC）
      - camel ：原文上「前邻非字母数字 且 后邻为大写字母」——覆盖驼峰起始
                （DTCNumber、readDataByIdentifier）
    """
    if _TOKEN_RE.match(keyword):
        esc = re.escape(keyword)
        strict = re.compile(r"(?<![a-z0-9])" + esc + r"(?![a-z0-9])")
        camel = re.compile(r"(?<![A-Za-z0-9])(?i:" + esc + r")(?=[A-Z])")
        return (strict, camel)
    return None


# 预编译全部关键词，避免每次匹配重复编译
_COMPILED = {kw: _compile(kw) for kws in EXPERT_KEYWORDS.values() for kw in kws}
_META_COMPILED = {kw: _compile(kw) for kw in META_KEYWORDS}


def _matches(blob_lower, blob_orig, keywords, compiled):
    """判断是否命中任一关键词；blob_lower 供词边界匹配，blob_orig 供驼峰匹配"""
    for kw in keywords:
        entry = compiled.get(kw)
        if entry is None:
            # 多词或含连字符的关键词：直接子串匹配
            if kw in blob_lower:
                return True
        else:
            strict, camel = entry
            if strict.search(blob_lower) or camel.search(blob_orig):
                return True
    return False


def classify(title, body):
    """
    返回命中的专家名列表（多标签），顺序与 EXPERT_KEYWORDS 的键顺序一致。

    匹配分两级：强关键词（具体术语）对标题与正文都算数；泛化词（WEAK_KEYWORDS）
    仅对标题算数，以免长正文里的常用英文词造成大面积误召回。
    """
    t_orig, t_low = title, title.lower()
    b_orig, b_low = body, body.lower()
    out = []
    for name, kws in EXPERT_KEYWORDS.items():
        strong = [k for k in kws if k not in WEAK_KEYWORDS]
        weak = [k for k in kws if k in WEAK_KEYWORDS]
        if _matches(t_low, t_orig, strong, _COMPILED) or \
           _matches(b_low, b_orig, strong, _COMPILED) or \
           _matches(t_low, t_orig, weak, _COMPILED):
            out.append(name)
    return out


def is_meta(title, body):
    """判断是否为文档元规则类需求（如文档优先级）"""
    orig = title + " " + body
    return _matches(orig.lower(), orig, META_KEYWORDS, _META_COMPILED)


def volume_of(req_id):
    """按需求编号返回语料卷短名；落在卷间空隙时返回 '??' 作为哨兵"""
    for name, lo, hi in VOLUMES:
        if lo <= req_id <= hi:
            return name
    return "??"


def load_requirements(json_path):
    """读取需求切分结果，按编号升序返回"""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    data.sort(key=lambda x: int(x["id"]))
    return data


def _cell(text):
    """转义 Markdown 表格单元格：竖线会破坏表格结构，换行需压平"""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _write_table(path, header_lines, rows):
    """写出一份「编号 | 标题 | 语料卷」三列表格文件"""
    lines = list(header_lines) + ["", "| 编号 | 标题 | 语料卷 |", "|------|------|--------|"]
    for rid, title in rows:
        lines.append(f"| {rid} | {_cell(title)} | {volume_of(rid)} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build(project_root, json_path):
    """
    生成 11 份域索引与 1 份元规则清单，并返回统计信息：
        total / tagged / unassigned / meta / per_expert

    参数 project_root 是**项目根目录**，产物固定落在 <项目根>/_index/ 下
    （spec §8）：_index/by-domain/<专家>.md 与 _index/meta-rules.md。
    内部拼 _index 而非由调用方传入，避免调用方漏拼而写错位置。
    可复跑：每次都清空 by-domain/ 下的旧索引。
    """
    data = load_requirements(json_path)
    index_root = os.path.join(project_root, "_index")
    by_domain = os.path.join(index_root, "by-domain")
    os.makedirs(by_domain, exist_ok=True)

    # 清空旧索引，避免上次运行的文件残留
    for fn in os.listdir(by_domain):
        if fn.endswith(".md"):
            os.remove(os.path.join(by_domain, fn))

    buckets = {name: [] for name in EXPERT_KEYWORDS}
    meta_rows = []
    unassigned = []

    for item in data:
        rid = int(item["id"])
        title = item["title"]
        body = item.get("body", "")
        hits = classify(title, body)
        for name in hits:
            buckets[name].append((rid, title))
        if not hits:
            # 无技术域命中：若属文档元规则则归编排者，否则计入盲区
            if is_meta(title, body):
                meta_rows.append((rid, title))
            else:
                unassigned.append((rid, title))

    for name, rows in buckets.items():
        _write_table(
            os.path.join(by_domain, f"{name}.md"),
            [
                f"# {name} 领域索引 — {EXPERT_TITLES[name]}",
                f"> 由 _tools/build_domain_index.py 生成｜命中 {len(rows)} 条",
                '> 取正文：在 Basetech知识库语料/ 中 Grep "^### <编号> —"',
            ],
            rows,
        )

    _write_table(
        os.path.join(index_root, "meta-rules.md"),
        [
            "# 文档元规则清单",
            "> 由 _tools/build_domain_index.py 生成｜仅供编排者判定文档优先级，不下发专家",
            f"> 共 {len(meta_rows)} 条",
        ],
        meta_rows,
    )

    return {
        "total": len(data),
        "tagged": sum(len(v) for v in buckets.values()),
        "unassigned": unassigned,
        "meta": [rid for rid, _ in meta_rows],
        "per_expert": {k: len(v) for k, v in buckets.items()},
    }


if __name__ == "__main__":
    stats = build(BASE, JSON_PATH)
    print(f"需求总数：{stats['total']}")
    print(f"索引条目总数（多标签）：{stats['tagged']}")
    print("\n各域命中条数：")
    for name, cnt in stats["per_expert"].items():
        print(f"  {name:<20} {cnt:>5}")
    print(f"\n元规则条目：{len(stats['meta'])}  {stats['meta']}")
    print(f"\n未命中需求：{len(stats['unassigned'])}")
    for rid, title in stats["unassigned"]:
        print(f"  {rid:<6} {title}")
