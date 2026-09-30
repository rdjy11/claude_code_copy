# -*- coding: utf-8 -*-
"""
SWRS DHU 需求领域归类脚本

用途：
    基于关键词对 1999 条需求做粗分类，统计各技术领域的需求条数，
    为组建 Basetech 开发团队时的专业角色划分提供量化依据。
    一条需求可命中多个领域（按关键词命中累加）。

输入：_tools/reqs_raw.json（绝对路径）
输出：标准输出打印各领域命中条数与占比。
"""
import json
import re
import sys

# 保证中文输出在 Windows 控制台正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 需求切分中间结果（绝对路径）
JSON_PATH = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929\_tools\reqs_raw.json"

# 领域 → 关键词列表（不区分大小写）
DOMAINS = {
    "DTC/故障管理": ["dtc", "fault", "detection", "diagnostic trouble", "freeze frame", "snapshot"],
    "UDS 服务": ["uds", "service 0x", "did", "readdata", "writedata", "routinecontrol", "session",
                 "securityaccess", "ecu reset", "tester present", "communication control"],
    "诊断传输层/寻址": ["doip", "docan", "transport layer", "n_pdu", "isolation", "addressing",
                        "functional address", "physical address", "gateway"],
    "刷写/软件下载": ["software download", "bootloader", "flash", "programming", "delta encoding",
                      "compression", "reprogram", "vbf", "swdl", "ota"],
    "Ethernet/IP": ["ethernet", "ipv4", "ipv6", "tcp", "udp", "vlan", "rtp", "tsn", "wlan", "socket"],
    "CAN": ["can ", "canfd", "can-fd", "canh", "canl", "can id", "can frame", "can bus"],
    "LIN": ["lin ", "lin bus", "lin slave", "lin master"],
    "FlexRay": ["flexray", "fr_", "static segment", "dynamic segment"],
    "A2B/LVDS/音视频链路": ["a2b", "lvds", "serializer", "deserializer", "fpd-link", "coax"],
    "网络管理": ["network management", "nm message", "wake up", "sleep", "bus wakeup", "partial network"],
    "车辆配置": ["car configuration", "ccp", "vcp", "config parameter", "vehicle configuration"],
    "信息安全": ["security", "hsm", "certificate", "authentication", "encryption", "signature",
                 "random number", "privacy", "cyber", "secure boot", "mac"],
    "AUTOSAR/平台": ["autosar", "bsw", "rte", "ecu platform", "tier1", "tier2", "startup time"],
    "硬件/物理层/供电": ["hardware", "voltage", "supply", "ground", "battery", "transceiver",
                         "termination", "wire", "pin", "connector", "power"],
    "时序/性能": ["timeout", "timing", "p2", "s3", "response time", "period", "latency"],
    "功能安全": ["asil", "fmea", "iso 26262", "safety related", "safe state", "functional safety"],
}

data = json.load(open(JSON_PATH, encoding="utf-8"))
total = len(data)
hits = {k: 0 for k in DOMAINS}

for item in data:
    blob = (item["title"] + " " + item["body"]).lower()
    for name, kws in DOMAINS.items():
        if any(kw in blob for kw in kws):
            hits[name] += 1

print(f"需求总条数：{total}\n")
print(f"{'领域':<22}{'命中条数':>8}{'占比':>9}")
print("-" * 42)
for name, n in sorted(hits.items(), key=lambda t: -t[1]):
    print(f"{name:<22}{n:>8}{n / total * 100:>8.1f}%")
