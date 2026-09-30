# Basetech 工程师智能体 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 Base Tech SWRS DHU 的 1999 条需求语料，建成一套 Claude Code 专家 Agent 体系——11 个领域专家 + 1 个编排者 + 3 条工作流，支持问答、评审、生成三类任务。

**Architecture:** 编排者 subagent 持 `Agent(bt-*)` 白名单派发到只读的领域专家；专家按「L0 域索引定位 → L1 需求清单速取 → L2 语料取证」三层取证；产出由编排者独占写入 `_out/`。

**Tech Stack:** Python 3.14.7（**仅标准库**——pytest 未安装）、Claude Code subagent（`.claude/agents/*.md`）、Claude Code Skill（`.claude/skills/basetech/`）。

**Spec:** `docs/superpowers/specs/2026-09-30-basetech-expert-agents-design.md`

## Global Constraints

- **Python**：3.14.7，**只允许标准库**。测试用 `unittest`，运行 `python -m unittest discover -s _tools -p "test_*.py" -v`。
- **无 git**：本项目不是 git 仓库，且用户已决定暂不启用。**计划中没有任何 git 命令**；每个任务的收尾用「检查点」步骤（跑校验 + 追加 `WORK_LOG.md`）代替 commit。
- **中文注释**：所有 `.py` 必须写中文注释说明每段作用（用户全局约定）。
- **路径**：脚本内一律用绝对路径，根为 `C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929`。
- **只读资产**：`Basetech知识库语料/`、`SWRS_DHU_需求清单.md`、`_tools/reqs_raw.json` **不得改写**，只读。
- **专家权限**：专家 agent 的 `tools` 恒为 `Read, Grep, Glob`（不含 `Agent`/`Write`/`Edit`）。
- **可回溯**：任何结论必须挂需求编号；文档未覆盖时答「文档未覆盖」，禁止编造编号。
- **语料标题格式**（两处一致，用于 Grep 定位）：`### <编号> — <标题>`（空格 + 全角破折号 `—` + 空格）。
- **语料卷名格式**：`SWRS_DHU_语料_<NN>_<起>-<止>.md`，如 `SWRS_DHU_语料_01_355-491.md`；索引中的「语料卷」列写短名 `01_355-491`。

## Review Focus

以下 5 类输入/情形，spec 隐含要求但没有任何任务的测试覆盖，最可能在使用中出事——每一条都已在**指定任务的测试步骤**中钉住：

1. **跨域提问**（如「刷写失败后 DTC 怎么置位」同时属 `bt-flash` 与 `bt-dtc`）→ 期望**派发两个专家**并汇总，而非任选其一。钉在 **Task 4 路由验证**。
2. **清单与语料内容不一致**（清单只保留 shall 句，语料有完整正文）→ 专家引用时必须说明来源层级，不得把清单摘要称作「原文」。钉在 **Task 3 冒烟验证**。
3. **输入落在文档未覆盖范围**（云端 OTA 协议、跨车通信）→ 期望明确拒答，**零编造编号**。钉在 **Task 5**。
4. **语料编号跳跃**（418–451 不存在）→ 专家被要求解释这些编号时必须回答「不存在」，而非编造。钉在 **Task 5**。
5. **同一需求落入多个域索引**（多标签）→ 索引间一致性：同一编号的标题必须逐字相同。钉在 **Task 2 测试**。

---

## File Structure

| 文件 | 职责 |
|------|------|
| `_tools/build_domain_index.py` | **新建**。领域归类核心 + 索引生成器。同时产出 11 份域索引与 1 份元规则清单，并输出未命中清单。 |
| `_tools/test_build_domain_index.py` | **新建**。`unittest` 测试。 |
| `_index/by-domain/bt-*.md` | **生成物**（11 份）。「编号 + 标题 + 语料卷」小索引。 |
| `_index/meta-rules.md` | **生成物**。文档元规则清单，仅供编排者。 |
| `.claude/agents/bt-*.md` | **新建**（11 份）。领域专家 subagent。 |
| `.claude/agents/basetech-orchestrator.md` | **新建**。编排者 subagent。 |
| `.claude/skills/basetech/SKILL.md` | **新建**。入口 + 路由表 + 工作流索引。 |
| `.claude/skills/basetech/jobs/{qa,review,gen}.md` | **新建**。三条工作流配方。 |
| `_out/` | **新建目录**。评审报告与生成物落点。 |
| `docs/operations/唤醒调用手册.md` | **新建**。交付物，含角色对应表。 |

---

### Task 1: 领域归类核心（词边界匹配 + 多标签）

**Files:**
- Create: `_tools/build_domain_index.py`
- Test: `_tools/test_build_domain_index.py`

**Interfaces:**
- Consumes: `_tools/reqs_raw.json`（已有，只读；每项含 `id: int`、`ver: str`、`title: str`、`body: str`）
- Produces:
  - `EXPERT_KEYWORDS: dict[str, list[str]]` —— 11 个专家名 → 关键词表
  - `EXPERT_TITLES: dict[str, str]` —— 专家名 → 中文域标题
  - `META_KEYWORDS: list[str]` —— 元规则判定词
  - `classify(title: str, body: str) -> list[str]`
  - `is_meta(title: str, body: str) -> bool`
  - `volume_of(req_id: int) -> str`
  - `VOLUMES: list[tuple[str, int, int]]` —— `(短名, 起, 止)`

- [ ] **Step 1: Write the failing test**

创建 `_tools/test_build_domain_index.py`：

```python
# -*- coding: utf-8 -*-
"""build_domain_index 归类核心的单元测试（标准库 unittest）"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_domain_index import (
    EXPERT_KEYWORDS, EXPERT_TITLES, META_KEYWORDS,
    classify, is_meta, volume_of,
)


class TestClassify(unittest.TestCase):
    def test_word_boundary_rejects_substring(self):
        """词边界：'can' 不得命中 cannot / candidate（Review Focus #5 的姊妹问题）"""
        self.assertNotIn("bt-can-lin-flexray", classify("Cannot connect", "candidate node"))
        self.assertIn("bt-can-lin-flexray", classify("CAN bus speed", "the can bus shall"))

    def test_multi_label(self):
        """一条需求可同时命中多个域"""
        got = classify("Bootloader DTC handling", "the flash sequence shall set a DTC")
        self.assertIn("bt-flash", got)
        self.assertIn("bt-dtc", got)

    def test_unassigned_returns_empty_list(self):
        """无任何关键词命中时返回空列表，而非 None"""
        self.assertEqual(classify("Document precedence", "priority between documents"), [])

    def test_returns_expert_names_only(self):
        """返回值必须是 EXPERT_KEYWORDS 的键，且按该字典的键顺序"""
        got = classify("CAN bus and UDS session", "diagnostic session shall")
        self.assertTrue(set(got) <= set(EXPERT_KEYWORDS))
        order = [k for k in EXPERT_KEYWORDS if k in got]
        self.assertEqual(got, order)


class TestIsMeta(unittest.TestCase):
    def test_meta_rule_detected(self):
        self.assertTrue(is_meta("Document precedence", "priority between standard documents"))

    def test_technical_req_not_meta(self):
        self.assertFalse(is_meta("DTC setting", "the ECU shall set a DTC"))


class TestVolumeOf(unittest.TestCase):
    def test_boundaries(self):
        """卷边界必须精确落在 filenames 标注的区间上"""
        self.assertEqual(volume_of(355), "01_355-491")
        self.assertEqual(volume_of(491), "01_355-491")
        self.assertEqual(volume_of(492), "02_492-1128")
        self.assertEqual(volume_of(6724), "20_3533-6724")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd "C:/Users/pc/claude_code_copy/projects/6.Basetech工程师智能体_20260929/_tools" && python -m unittest test_build_domain_index -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'build_domain_index'`

- [ ] **Step 3: Implement the classification core in `_tools/build_domain_index.py`**

必须钉死的三个数据结构（其余键名见 Interfaces）：

```python
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

# 关键词一律小写；匹配时对正文做 .lower() 后按词边界匹配
EXPERT_KEYWORDS = {
    "bt-dtc": ["dtc", "fault", "detection", "diagnostic trouble", "freeze frame", "snapshot"],
    "bt-uds": ["uds", "service 0x", "did", "readdata", "writedata", "routinecontrol",
               "session", "securityaccess", "ecu reset", "tester present",
               "communication control", "nrc", "suppress positive response",
               "timeout", "timing", "p2", "s3", "response time", "period", "latency"],
    "bt-diag-transport": ["doip", "docan", "transport layer", "n_pdu", "isolation",
                          "addressing", "functional address", "physical address", "gateway"],
    "bt-flash": ["software download", "bootloader", "flash", "programming", "delta encoding",
                 "compression", "reprogram", "vbf", "swdl", "ota"],
    "bt-ethernet": ["ethernet", "ipv4", "ipv6", "tcp", "udp", "vlan", "rtp", "tsn",
                    "wlan", "socket", "grandmaster", "gptp", "ptp", "domain id",
                    "nomadic", "ip address", "ip address range"],
    "bt-can-lin-flexray": ["can", "canfd", "can-fd", "canh", "canl", "can id",
                           "can frame", "can bus", "lin", "lin bus", "lin slave",
                           "lin master", "flexray", "static segment", "dynamic segment",
                           "bus speed", "resynchronisation", "sample mode", "header", "frame"],
    "bt-a2b-lvds": ["a2b", "lvds", "serializer", "deserializer", "fpd-link", "coax", "i2c"],
    "bt-nm": ["network management", "nm message", "wake up", "sleep", "bus wakeup",
              "partial network", "networkstatus"],
    "bt-carcfg": ["car configuration", "ccp", "vcp", "config parameter", "vehicle configuration"],
    "bt-security": ["security", "hsm", "certificate", "authentication", "encryption",
                    "signature", "random number", "privacy", "cyber", "secure boot", "mac",
                    "asil", "fmea", "iso 26262", "safety related", "safe state",
                    "functional safety"],
    "bt-platform": ["autosar", "bsw", "rte", "ecu platform", "tier1", "tier2", "startup time",
                    "hardware", "voltage", "supply", "ground", "battery", "transceiver",
                    "termination", "wire", "pin", "connector", "power",
                    "asil", "fmea", "iso 26262", "safety related", "safe state",
                    "functional safety"],
}

META_KEYWORDS = ["document precedence", "priority between", "priority of documents"]

# (短名, 起, 止)，须与 Basetech知识库语料/ 下的文件名一致
VOLUMES = [
    ("01_355-491", 355, 491), ("02_492-1128", 492, 1128), ("03_1129-1228", 1129, 1228),
    ("04_1229-1368", 1229, 1368), ("05_1369-1510", 1369, 1510), ("06_1511-1615", 1511, 1615),
    ("07_1625-1821", 1625, 1821), ("08_1822-1921", 1822, 1921), ("09_1922-2021", 1922, 2021),
    ("10_2022-2121", 2022, 2121), ("11_2122-2221", 2122, 2221), ("12_2222-2321", 2222, 2321),
    ("13_2322-2425", 2322, 2425), ("14_2426-2526", 2426, 2526), ("15_2527-2651", 2527, 2651),
    ("16_2653-2765", 2653, 2765), ("17_2766-3070", 2766, 3070), ("18_3071-3356", 3071, 3356),
    ("19_3357-3532", 3357, 3532), ("20_3533-6724", 3533, 6724),
]
```

实现要点（签名与断言已定，以下为需要决定的部分）：

- 匹配用**词边界正则**：单字/数字型关键词（如 `can`、`s3`、`mac`、`pin`、`did`、`wire`）用 `(?<![a-z0-9])kw(?![a-z0-9])`；含空格的关键词直接子串匹配即可。为避免每次重编译，在模块层预编译为 `{kw: Pattern}`。
- `classify` 按 `EXPERT_KEYWORDS` 的**插入顺序**返回命中名单，保证测试 `test_returns_expert_names_only` 的确定性。
- `volume_of` 顺序扫描 `VOLUMES` 返回首个命中的短名；越界时返回 `"??"`。
- 模块顶部加 `sys.stdout.reconfigure(encoding="utf-8")` 以保证 Windows 控制台中文正常（沿用 `_tools/` 既有脚本写法）。

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ".../_tools" && python -m unittest test_build_domain_index -v`
Expected: PASS，7 个测试全绿。

- [ ] **Step 5: 检查点**

```bash
cd "C:/Users/pc/claude_code_copy/projects/6.Basetech工程师智能体_20260929" && python -m unittest discover -s _tools -p "test_*.py" -v
```
Expected: PASS。随后在 `WORK_LOG.md` 追加一行：「新增 `_tools/build_domain_index.py` 归类核心 + 单元测试（7 项通过）」。

---

### Task 2: 生成 11 份域索引 + 元规则清单（零无处置盲区）

**Files:**
- Modify: `_tools/build_domain_index.py`（追加生成逻辑）
- Modify: `_tools/test_build_domain_index.py`（追加测试）
- Create: `_index/by-domain/bt-*.md`（11 份，生成）
- Create: `_index/meta-rules.md`（生成）

**Interfaces:**
- Consumes: Task 1 的 `classify`、`is_meta`、`volume_of`、`EXPERT_TITLES`、`VOLUMES`
- Produces:
  - `load_requirements(json_path: str) -> list[dict]` —— 读 `reqs_raw.json`，按 `id` 升序
  - `build(output_root: str, json_path: str) -> dict` —— 返回
    `{"total": int, "tagged": int, "unassigned": list[tuple[int, str]], "meta": list[int], "per_expert": dict[str, int]}`

- [ ] **Step 1: Write the failing test**

追加到 `_tools/test_build_domain_index.py`：

```python
class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile, build_domain_index as B
        cls.B = B
        cls.tmp = tempfile.mkdtemp()
        cls.stats = B.build(cls.tmp, B.JSON_PATH)

    def test_eleven_indexes_and_meta_written(self):
        """必须产出 11 份域索引 + 1 份 meta-rules.md"""
        d = os.path.join(self.tmp, "by-domain")
        names = sorted(os.listdir(d))
        self.assertEqual(len(names), 11)
        self.assertEqual(names, sorted(f"{k}.md" for k in self.B.EXPERT_KEYWORDS))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "meta-rules.md")))

    def test_zero_blindspot(self):
        """零无处置盲区：未命中且非元规则的条目必须为 0"""
        self.assertEqual(self.stats["unassigned"], [],
                         f"仍有未命中需求：{self.stats['unassigned'][:10]}")

    def test_index_cross_consistency(self):
        """Review Focus #5：同一编号在多份索引中的标题必须逐字相同"""
        import re
        d = os.path.join(self.tmp, "by-domain")
        seen = {}
        for fn in os.listdir(d):
            text = open(os.path.join(d, fn), encoding="utf-8").read()
            for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|", text, re.M):
                rid, title = int(m.group(1)), m.group(2)
                if rid in seen:
                    self.assertEqual(seen[rid], title, f"编号 {rid} 标题不一致")
                seen[rid] = title

    def test_index_volume_column_matches_corpus_files(self):
        """索引中的语料卷短名必须真实存在于 Basetech知识库语料/"""
        import re, glob
        corpus = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(self.B.__file__))), "Basetech知识库语料")
        real = {re.match(r"SWRS_DHU_语料_(\d+_\d+-\d+)\.md", os.path.basename(p)).group(1)
                for p in glob.glob(os.path.join(corpus, "SWRS_DHU_语料_*.md"))}
        d = os.path.join(self.tmp, "by-domain")
        for fn in os.listdir(d):
            text = open(os.path.join(d, fn), encoding="utf-8").read()
            for m in re.finditer(r"^\|\s*\d+\s*\|.+?\|\s*(\d+_\d+-\d+)\s*\|", text, re.M):
                self.assertIn(m.group(1), real)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest test_build_domain_index.TestBuild -v`
Expected: FAIL — `AttributeError: module 'build_domain_index' has no attribute 'build'`

- [ ] **Step 3: Implement `build()` and the CLI in `_tools/build_domain_index.py`**

实现要点：

- 模块级常量：`BASE = r"C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929"`、`JSON_PATH = os.path.join(BASE, "_tools", "reqs_raw.json")`。
- `build()` 先 `os.makedirs(out/by-domain, exist_ok=True)`，并**先清空 `by-domain/` 下的旧 `*.md`**（可复跑，避免残留）。
- 每份索引文件格式（表头两行引注 + 三列表格）：

```md
# bt-dtc 领域索引 — DTC / 故障管理
> 由 _tools/build_domain_index.py 生成｜命中 787 条
> 取正文：在 Basetech知识库语料/ 中 Grep "^### <编号> —"

| 编号 | 标题 | 语料卷 |
|------|------|--------|
| 355 | CC Subscriber ECU configuration states | 01_355-491 |
```

- 标题中的 `|` 需转义为 `\|`，否则破坏表格。
- `unassigned` = `classify()` 为空 **且** `is_meta()` 为假 的条目。
- `meta-rules.md` 格式：标题 + 引注 + 三列表格（编号 / 标题 / 语料卷），并在文首注明「本清单仅供编排者判定文档优先级，不下发专家」。
- CLI：`if __name__ == "__main__":` 调用 `build(BASE, JSON_PATH)`，打印统计与**未命中清单**（编号 + 标题，便于人工补词）。

- [ ] **Step 4: Run test to verify it fails on the blindspot, then iterate keywords**

Run: `python -m unittest test_build_domain_index.TestBuild -v`

首次必然 **FAIL 在 `test_zero_blindspot`**（spec §6.3 实测基线为 135 条未命中）。执行：

```bash
python build_domain_index.py
```

对照打印出的未命中清单（编号 + 标题），**逐条判断归属并补进对应专家的关键词表**，重复「跑脚本 → 看清单 → 补词」直到未命中归零。补词时注意：`bt-can-lin-flexray` 的 `header`/`frame` 等词较宽，补词后需回看 `test_word_boundary_rejects_substring` 是否仍通过。

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m unittest discover -s _tools -p "test_*.py" -v`
Expected: PASS，全部测试绿，`test_zero_blindspot` 通过（`unassigned == []`）。

- [ ] **Step 6: 抽查索引质量**

人工阅读 `_index/by-domain/bt-dtc.md` 与 `bt-can-lin-flexray.md` 的**前 50 条**，确认无过召回（spec §6.3-3 要求）。发现噪声则回到 Step 4 调词。

- [ ] **Step 7: 检查点**

在 `WORK_LOG.md` 追加：11 份域索引 + `meta-rules.md` 已生成；各域条目数；未命中为 0。

---

### Task 3: 首批两个专家 agent（bt-dtc、bt-uds）

**Files:**
- Create: `.claude/agents/bt-dtc.md`
- Create: `.claude/agents/bt-uds.md`

**Interfaces:**
- Consumes: Task 2 产出的 `_index/by-domain/bt-dtc.md`、`_index/by-domain/bt-uds.md`
- Produces: 两个可被点名调用的 subagent，`name` 分别为 `bt-dtc`、`bt-uds`

- [ ] **Step 1: 创建 `bt-dtc.md`（作为 11 个专家的样板）**

frontmatter **必须逐字**如下（`tools` 与 `model` 是硬约束）：

```markdown
---
name: bt-dtc
description: DTC / 故障管理领域专家。当问题涉及 DTC 定义与编号格式（如 U2300-55）、
  故障检测策略、去抖 debounce、老化自愈 aging/healing、快照与扩展数据 freeze frame/snapshot、
  故障确认与存储、UDS 0x19 读取 DTC 时使用。不负责 UDS 服务本身的语义（见 bt-uds），
  也不负责网络层 DTC 上报路径（见 bt-diag-transport）。
tools: Read, Grep, Glob
model: inherit
---
```

正文五节（顺序固定，见 spec §4.1）：`# 职责范围`、`# 不属于本域`、`# 语料定位方法（必须按序）`、`# 输出要求`、`# 禁止事项`。

`# 语料定位方法` 必须写成三步，且**强制先 L0 后 L1 最后 L2**（防止全量读 2.38 MB 语料）：

```markdown
1. 读 `_index/by-domain/bt-dtc.md`，圈定候选需求编号
2. 在 `SWRS_DHU_需求清单.md` 中 Grep 该编号，取摘要（版本 / 验证方式 / 适用 AUTOSAR / 核心 shall 句）
3. 仅当需要完整正文时，才在 `Basetech知识库语料/` 中 Grep `^### <编号> —` 取原文
```

`# 输出要求` 必须含 spec §7.2 的三行结构（结论 / 依据 / 推断），并声明：

- 每个结论必须挂需求编号 + 标题 + 语料卷；
- **引用摘要时须注明来自「需求清单」，引用完整正文时才称「语料原文」**（Review Focus #2）；
- 文档未覆盖时明确回答「文档未覆盖」，禁止编造编号；
- 无编号支撑的推断必须显式标注「推断」。

`# 禁止事项`：不修改任何文件；不回答非本域问题，改为指出应咨询哪个专家。

- [ ] **Step 2: 创建 `bt-uds.md`**

同 Step 1 的五节结构，差异化内容：

```markdown
---
name: bt-uds
description: UDS 诊断服务领域专家。当问题涉及 DID 读写（0x22/0x2E）、RoutineControl(0x31)、
  诊断会话 Session(0x10)、SecurityAccess(0x27)、CommunicationControl(0x28)、ECUReset(0x11)、
  TesterPresent(0x3E)、时序参数 P2/P2*/S3 与 NRC 时使用。不负责 DTC 检测策略（见 bt-dtc），
  不负责传输层寻址（见 bt-diag-transport）。
tools: Read, Grep, Glob
model: inherit
---
```

`# 语料定位方法` 第 1 步指向 `_index/by-domain/bt-uds.md`。

- [ ] **Step 3: 冒烟验证（点名调用）**

在项目目录下启动 Claude Code（`cd` 到项目根再 `claude`，见 spec §8.1），依次提问：

| # | 提问 | 期望 |
|---|------|------|
| 1 | 「用 bt-dtc 专家：DTC 编号格式 U2300-55 里的 55 是什么意思？」 | 挂出具体需求编号；引用层级写「需求清单」或「语料原文」 |
| 2 | 「用 bt-uds 专家：SecurityAccess 0x27 的 P2 超时要求？」 | 挂需求编号；不越界回答 DTC 检测策略 |
| 3 | 「用 bt-dtc 专家：DID 0xF186 怎么读？」 | 明确说明此问题属 `bt-uds`，不强行作答 |

- [ ] **Step 4: 检查点**

在 `WORK_LOG.md` 追加：`bt-dtc`、`bt-uds` 已创建并通过点名冒烟验证。

---

### Task 4: 编排者 + 最小 SKILL（2 专家 + 问答工作流）

**Files:**
- Create: `.claude/agents/basetech-orchestrator.md`
- Create: `.claude/skills/basetech/SKILL.md`
- Create: `.claude/skills/basetech/jobs/qa.md`

**Interfaces:**
- Consumes: Task 3 的 `bt-dtc`、`bt-uds`；`_index/meta-rules.md`
- Produces: subagent `basetech-orchestrator`；Skill `basetech`

- [ ] **Step 1: 创建编排者 `basetech-orchestrator.md`**

```markdown
---
name: basetech-orchestrator
description: Basetech 需求编排者。用于处理针对 Base Tech SWRS DHU 需求规范的问答、评审、
  生成三类任务：读取路由表判定意图，派发领域专家，汇总结论，并把产出写入 _out/。
tools: Read, Grep, Glob, Write, Agent(bt-dtc, bt-uds)
model: inherit
---
```

> **注意**：本任务的 `Agent(...)` 白名单**只列 bt-dtc 与 bt-uds**（最小闭环）。Task 6 完成后必须补齐至全部 11 个专家。

正文必须含：

1. **执行顺序**：① 读 `_index/meta-rules.md` 判定文档优先级 → ② 读 `SKILL.md` 取路由表 → ③ 判定意图选工作流 → ④ 切域并并行派发 → ⑤ 汇总 → ⑥ 写 `_out/`。
2. **元规则处置**：文档优先级类需求由编排者**直接判定，不下发专家**。
3. **禁止**：不得向用户提问（subagent 无此能力）——信息不足时**必须返回主 Agent 请求澄清**，不得自行假设。
4. **跨域必须全派**：若提问同时命中多个域，**必须派发全部相关专家**并汇总，不得只选其一（Review Focus #1）。

- [ ] **Step 2: 创建 `SKILL.md`（含路由表骨架）**

必须含：① 启动前提提示（须从项目目录启动，否则 agent 不加载）；② **路由表**（需求域 → 专家）；③ 工作流索引（本任务只登记 `qa`）。

路由表格式：

| 需求域（关键词） | 派发专家 |
|---|---|
| DTC / 故障码 / 检测策略 / 老化自愈 | `bt-dtc` |
| UDS 服务 / DID / Routine / Session / SecurityAccess / P2 / NRC | `bt-uds` |

（Task 7 补齐其余 9 行。）

- [ ] **Step 3: 创建 `jobs/qa.md`**

问答工作流配方，硬约束照抄 spec §7：派 1–2 个专家；输出结构为 `**结论** / **依据** / **推断**` 三段；每个结论挂需求编号；无编号支撑标「推断」；文档未覆盖则答「未覆盖」，禁止编造编号。产出写入 `_out/qa-<时间戳>.md`。

- [ ] **Step 4: 路由验证（含跨域）**

在项目目录下启动 Claude Code，提问：

| # | 提问 | 期望 |
|---|------|------|
| 1 | 「Basetech 问答：DTC 需要满足什么检测条件？」 | 派 `bt-dtc`，结论挂编号 |
| 2 | 「Basetech 问答：SecurityAccess 的时序要求？」 | 派 `bt-uds` |
| 3 | **跨域**「Basetech 问答：刷写失败后 DTC 怎么置位？」 | **同时派 `bt-dtc` 与 `bt-uds`**（当前白名单只有这两个，须两者都派并汇总），不得只答其一 |

> 记录 #3 的实际派发情况。若编排者只派一个，回到 Step 1 强化第 4 条措辞后重试。

- [ ] **Step 5: 检查点**

`WORK_LOG.md` 追加：编排者 + 最小 SKILL（qa）已建；路由验证 #1–#3 结果，含 #3 是否双派。

---

### Task 5: 最小闭环验证（防幻觉 + 编号跳跃）

**Files:**
- Create: `docs/operations/验证记录-最小闭环.md`

**Interfaces:**
- Consumes: Task 3、Task 4 的全部产出
- Produces: 一份含原始问答与判定的验证记录

- [ ] **Step 1: 防幻觉测试**

连续提问以下 5 题，逐题复制问答原文进验证记录：

| # | 提问 | 期望 |
|---|------|------|
| 1 | 「SWRS 里 DTC 老化条件是什么？」 | 挂真实编号 |
| 2 | 「云端 OTA 差分包的协议怎么定义？」 | **答「文档未覆盖」**（spec 只管车端） |
| 3 | 「跨车 V2X 的 DTC 传播规则？」 | **答「文档未覆盖」** |
| 4 | 「需求编号 418 的内容是什么？」 | **答「该编号在文档中不存在」**（418–451 为文档自身跳跃，Review Focus #4） |
| 5 | 「需求编号 430 的内容是什么？」 | 同上，不存在 |

- [ ] **Step 2: 判定并记录**

通过条件：**5 题零编造编号**；#2/#3/#4/#5 必须明确拒答或说明不存在。任何一题编造编号即为不通过，记录实际输出。

- [ ] **Step 3: 修正循环**

若不通过：优先检查专家正文的 `# 输出要求` 是否写明了拒答规则；其次检查 L0 索引是否把不存在编号误收录。修正后重跑 Step 1。

- [ ] **Step 4: 检查点**

写入 `docs/operations/验证记录-最小闭环.md`，并在 `WORK_LOG.md` 追加结论（通过 / 不通过 + 修正内容）。

---

### Task 6: 其余 9 个领域专家 agent

**Files:**
- Create: `.claude/agents/{bt-diag-transport,bt-flash,bt-ethernet,bt-can-lin-flexray,bt-a2b-lvds,bt-nm,bt-carcfg,bt-security,bt-platform}.md`

**Interfaces:**
- Consumes: Task 2 的 `_index/by-domain/<name>.md`（9 份）；Task 3 的 `bt-dtc.md` 作为样板
- Produces: 9 个 subagent，`name` 与文件名一致

- [ ] **Step 1: 逐个创建（样板 = Task 3 的 bt-dtc.md）**

五节结构与 `tools: Read, Grep, Glob` / `model: inherit` 完全沿用。每个 agent 的 `description` 路由信号与职责边界**照 spec §4.2 该行原文**；`# 语料定位方法` 第 1 步指向自己的 `_index/by-domain/<name>.md`。

九个专家的 name 与中文标题（取自 Task 1 的 `EXPERT_TITLES`）：

| name | 中文标题 |
|------|---------|
| `bt-diag-transport` | 诊断传输层 / 网关 |
| `bt-flash` | 刷写 / 软件下载 |
| `bt-ethernet` | 车载以太网 / IP |
| `bt-can-lin-flexray` | CAN / LIN / FlexRay |
| `bt-a2b-lvds` | A2B / LVDS 高速链路 |
| `bt-nm` | 网络管理 |
| `bt-carcfg` | 车辆配置 CC / CCP |
| `bt-security` | 信息安全 |
| `bt-platform` | ECU 平台 / AUTOSAR |

`# 不属于本域` 必须写清 spec §4.3 的四处刻意重叠中与本专家相关的边界（如 `bt-flash` ↔ `bt-uds`、`bt-security` ↔ `bt-flash`）。

- [ ] **Step 2: 逐个冒烟验证**

对 9 个专家各提 1 个**本域**问题 + 1 个**邻域**问题，确认：本域问题挂编号作答、邻域问题明确转介。结果记入 `docs/operations/验证记录-最小闭环.md` 的续节。

- [ ] **Step 3: 检查点**

`WORK_LOG.md` 追加：9 个专家已建；冒烟结果。

---

### Task 7: 完整路由表 + 评审/生成工作流 + 补齐白名单

**Files:**
- Modify: `.claude/agents/basetech-orchestrator.md`（`tools` 白名单补齐至 11 个）
- Modify: `.claude/skills/basetech/SKILL.md`（路由表补齐至 11 行）
- Create: `.claude/skills/basetech/jobs/review.md`
- Create: `.claude/skills/basetech/jobs/gen.md`
- Create: `_out/.gitkeep`

**Interfaces:**
- Consumes: Task 6 的 11 个专家
- Produces: 完整可用的三条工作流

- [ ] **Step 1: 补齐编排者白名单**

把 frontmatter 改为（11 个一并列出，顺序与 `EXPERT_KEYWORDS` 一致）：

```yaml
tools: Read, Grep, Glob, Write, Agent(bt-dtc, bt-uds, bt-diag-transport, bt-flash, bt-ethernet, bt-can-lin-flexray, bt-a2b-lvds, bt-nm, bt-carcfg, bt-security, bt-platform)
```

- [ ] **Step 2: 补齐 `SKILL.md` 路由表**

按 Task 1 的 `EXPERT_KEYWORDS` 把 11 行全部写全，每行「需求域（关键词）| 派发专家」。同时把工作流索引补齐为 qa / review / gen 三条。

- [ ] **Step 3: 创建 `jobs/review.md`**

评审配方，硬约束照抄 spec §7 与 §7.1：

- 输入：待评审材料（文本或文件路径）；
- 编排者**先切域**，再**并行派发全部相关专家**；
- 每个专家返回差距清单行：`编号｜要求摘要｜材料现状｜判定(符合/不符合/无法判定)｜依据原文`；
- 编排者汇总：去重、**按严重度降序**、单列**跨域冲突**、单列**无法判定项及原因**；
- 报告结构照抄 spec §7.1 模板；产出写入 `_out/review-<时间戳>.md`。

- [ ] **Step 4: 创建 `jobs/gen.md`**

生成配方：

- 输入：生成意图（如「为某 ECU 生成 UDS 诊断需求条目」）；
- 派 1–2 个专家；
- 输出必须**复用文档既有格式**：编号占位 / 标题 / Version / Verification Method / 适用 AUTOSAR / shall 句；
- 必须是 **shall 句式**；
- 每条标注「新增，编号待人工确认」；
- 产出写入 `_out/gen-<时间戳>.md`。

- [ ] **Step 5: 验证三条工作流可用**

各跑 1 次：问答（`_out/qa-*.md` 生成）、评审（给一段自拟的 ECU 说明，`_out/review-*.md` 生成且含统计行与跨域冲突节）、生成（`_out/gen-*.md` 生成且条目为 shall 句式）。

- [ ] **Step 6: 检查点**

`WORK_LOG.md` 追加：白名单补齐至 11；三条工作流均已实跑产出。

---

### Task 8: 完整验证（§10 四项）

**Files:**
- Create: `docs/operations/验证记录-完整.md`

**Interfaces:**
- Consumes: Task 7 的完整体系
- Produces: 四项测试的通过/不通过结论

- [ ] **Step 1: 测试 1｜路由测试（约 20 题）**

11 个域各出 1–2 个真实问题。逐题记录：提问 / 实际派发专家 / 是否正确。通过条件：**路由准确率 ≥ 85%**。

- [ ] **Step 2: 测试 2｜防幻觉测试（10 题，含 3 题未覆盖）**

复用 Task 5 的 5 题并扩充至 10 题（覆盖更多域），其中 3 题为文档未覆盖。通过条件：**零编造编号**。

- [ ] **Step 3: 测试 3｜评审召回**

自拟一份含 **5 处已知偏差**的 ECU 设计说明（例如：把 P2 超时写成 50 ms 而文档要求另有其值、漏写 DTC 老化条件、SecurityAccess 缺少错误计数器、刷写缺少 Delta Encoding 要求、以太网未配 VLAN）。通过条件：差距清单**抓全 5 处**。漏抓的记入验证记录并修正对应专家。

- [ ] **Step 4: 测试 4｜生成一致性**

生成 5 条需求，人工核对：格式字段齐全、shall 句式、标注「编号待人工确认」。通过条件：**无格式漂移**。

- [ ] **Step 5: 检查点**

写入 `docs/operations/验证记录-完整.md`，四项各记「通过 / 不通过 + 证据」；`WORK_LOG.md` 追加总结。

---

### Task 9: Agent 唤醒调用操作手册（交付物）+ 飞书导入

**Files:**
- Create: `docs/operations/唤醒调用手册.md`

**Interfaces:**
- Consumes: Task 1–8 的全部产出（尤其 11 个专家名与路由表）
- Produces: 面向业务使用者的手册 + 一份飞书云文档

- [ ] **Step 1: 撰写手册（六章，见 spec §9.1）**

| # | 章节 | 要点 |
|---|------|------|
| 1 | **角色对应表** | 12 个 subagent + 3 个 Skill 的「名称 → 中文名 → 职责 → 典型问法」一览 |
| 2 | 启动前提 | 必须 `cd` 到项目目录再 `claude`，否则 agent 不加载 |
| 3 | 唤醒方式 | 编排者与各专家的显式调用写法；哪些会自动路由、哪些需点名 |
| 4 | 三条工作流用法 | 问答 / 评审 / 生成 的输入写法与产出位置（`_out/`） |
| 5 | 样例 | 每类任务 1 个可直接复制的示例请求 |
| 6 | 故障排查 | agent 未加载 / 路由到错误专家 / 回答未覆盖 / 产出文件找不到 |

措辞面向工程师，**不假设其了解 subagent 机制**。

- [ ] **Step 2: 导入飞书云文档**

用 `mcp__lark-mcp__docx_builtin_import`，**必须 `useUAT: true`**（tenant 身份建出的文档用户打不开）。`file_name` ≤ 27 字符，取值 `Basetech智能体唤醒手册`。

- [ ] **Step 3: 回报链接并检查点**

把飞书链接写回手册文件首行，并在 `WORK_LOG.md` 追加：手册已成文并导入飞书。

---

## Self-Review

**1. Spec coverage**：spec §1 目标→Task 3/6/7；§3 架构与三条铁律→Task 3/4/7 的 frontmatter 与正文约束；§4.1–4.2 专家清单→Task 3/6；§4.3 边界重叠→Task 6 Step 1；§4.4 合并决策→Task 1 的 `EXPERT_KEYWORDS`；§5.1 编排者→Task 4/7；§5.2 三工作流→Task 4/7；§6.1 三层接入→Task 3 的定位方法；§6.2 索引生成→Task 1/2；§6.3 零盲区与词边界→Task 2；§7 输出契约→Task 4/7；§8 文件结构→File Structure 表；§9 构建顺序→Task 顺序；§9.1 手册→Task 9；§10 验证→Task 5/8；§11 风险→已转为 Task 2/4 的验证步骤；§12 决策→Task 7 白名单、Global Constraints 的「无 git」；§13 模板→Task 3。

**2. Step scan**：已剔除所有「TBD / 处理边界情况 / 写相应测试」类空转步骤。Task 2 Step 4 保留了「迭代补词」这一无法预先穷举的循环，但它给出了明确的终止条件（未命中归零）与可见反馈（脚本打印清单），不属空转。

**3. Type consistency**：`classify` / `is_meta` / `volume_of` / `build` / `load_requirements` 在 Task 1 定义、Task 2 使用，签名一致；`EXPERT_KEYWORDS` 既作关键词表又作专家名的权威来源，Task 2 的文件名断言、Task 6 的 name 表、Task 7 的路由表与白名单均以它为单一事实源。

**4. Review Focus**：5 条已分别钉在 Task 2（#5 索引一致性）、Task 3（#2 引用层级）、Task 4（#1 跨域双派）、Task 5（#3 未覆盖拒答、#4 编号跳跃）。

**5. Proportion**：计划约 470 行，与 470 行的 spec 基本等长；除 Task 1 的关键词表（数据，无法由实现者推断）外，无大段代码正文。
