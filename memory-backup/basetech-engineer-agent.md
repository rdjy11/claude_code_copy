---
name: basetech-engineer-agent
description: Basetech 工程师智能体（项目 6）——基于 Base Tech SWRS DHU 需求规范拆分 11 个领域专家 Agent，唤醒词「Basetech智能体」「汽车诊断智能体」「Basetech工程师智能体」
metadata: 
  node_type: memory
  type: project
  modified: 2026-10-15T14:31:07.181Z
  originSessionId: c4b75c45-a383-4100-ae7a-760125b5ec82
---

# Basetech 工程师智能体（项目 6）

项目目录：`C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929\`
（目录名 2026-09-29 由「汽车诊断智能体」改为「Basetech工程师智能体」）

## 语料基础（已完成）

源文档为吉利汽车研究院 **Base Tech SWRS DHU** 软件需求规范（Note-SWRS，Rev 005，2019-07-11，1572 页），源文件在 `D:\知识库资料源\汽车知识库\Basetech技术文档`（16 个分页 md）。

已产出两份可复用资产：

- `SWRS_DHU_需求清单.md`——1999 条需求，逐条含 编号/标题/版本/验证方式/适用 AUTOSAR/核心 shall 句（约 871 KB）
- `Basetech知识库语料/`——20 卷 RAG 语料 + `00_INDEX.md`，以「单条需求」为最小语义单元，任一条目不跨卷（约 2.38 MB）

## 智能体体系（2026-09-30 已建成并验证）

**用途**：全流程助手（问答 + 评审 + 生成）。**载体**：Claude Code 原生 subagent。

**⚠️ 启动前提**：agent 与 skill 定义在**项目目录**下，必须 `cd` 到项目目录再启动 `claude`，否则全部不加载。

**架构**：15 个角色 = 12 个 subagent + 3 个 Skill

- 领域层 **11 个专家**（只读 `Read/Grep/Glob`）：`bt-dtc`、`bt-uds`、`bt-diag-transport`、`bt-flash`、`bt-ethernet`、`bt-can-lin-flexray`、`bt-a2b-lvds`、`bt-nm`、`bt-carcfg`、`bt-security`、`bt-platform`
- 职能层：1 个编排 subagent（`basetech-orchestrator`，持 `Agent(bt-*)` 白名单）+ 3 条工作流 Skill（`qa`/`review`/`gen`）

**三条铁律**：专家只读；编排者独占写权限（产出落 `_out/`）；结论必须挂需求编号。

**关键实测发现**（推翻了先前的目测判断）：

1. 语料卷号**不能**用于领域定位——每个领域都横跨几乎全部 20 卷，各领域按需求编号交织；
2. 初版关键词表有 **135 条需求（6.8%）无任何域命中**，索引生成必须做到「零无处置盲区」；
3. 需用词边界匹配（`\bcan\b`），否则 `can` 会误命中 `cannot`。

**Claude Code 平台事实**（已核实）：subagent 支持嵌套至深度 3；并发上限 20；官方建议工作流 Agent 数 < 15。

## 交付物（均已建成）

| 类别 | 路径 |
|------|------|
| 索引生成器 + 14 项单测 | `_tools/build_domain_index.py`、`_tools/test_build_domain_index.py` |
| 域索引（生成物） | `_index/by-domain/*.md`（11 份）、`_index/meta-rules.md` |
| 领域专家 | `.claude/agents/bt-*.md`（11 个） |
| 编排者 | `.claude/agents/basetech-orchestrator.md` |
| 工作流 | `.claude/skills/basetech/SKILL.md`、`jobs/{qa,review,gen}.md` |
| 产出目录 | `_out/` |
| 验证记录 | `docs/operations/验证记录-最小闭环.md`、`验证记录-完整.md` |
| 操作手册 | `docs/operations/唤醒调用手册.md` + 飞书 https://my.feishu.cn/docx/BfiOdaYO2ogr9ExTo1HcgbIknZb |
| 执行账本（全部裁决） | `_sdd/progress.md` |
| §12.2 判定证据脚本 | `_tools/analyze_open_items.py`（只读可复现） |

**验证结果**：路由 12/12（100%）、零编造编号、评审召回 5/5、生成格式 7/7、零盲区（1999 条全覆盖）。

**⚠️ 会话限制**：执行会话无法派发项目级具名 subagent，故内容验证替代了机制验证；**机制侧已由用户于 2026-09-30 在交互式会话中补验通过**（证据 `_out/qa-20260930-234601.md`，用户确认格式合规）。

**实测输出质量**：问答产出会主动区分「引用层级」（L1 清单 vs L2 语料）、单列「文档未覆盖」边界、并处理 AUTOSAR 4.0.x / 4.1+ 的跨版本行为分支。

## §12.2 未决项已全部关闭（2026-10-15）——结构锁定

原三项「跑通验证后再定」用实测数据关闭，**结构最终锁定 11 专家 + 1 编排 + 3 工作流**，无悬置增减项。证据脚本 `_tools/analyze_open_items.py`。

| 事项 | 决定 | 关键依据 |
|------|------|---------|
| `model` 取值 | 专家 `sonnet` / 编排者 `opus` | 见 [[claude-model-alias-mapping]]——本环境下 `sonnet` 与 `inherit` 等价，仅 `opus` 映射更强模型；已验证质量出自便宜档 |
| `bt-carcfg` 是否并入 `bt-platform` | **不并入** | 设计设定的触发条件「与平台高频共现」**不成立**：仅 22.2%，而 `bt-dtc` 49.2%、`bt-ethernet` 36.5% 更高——platform 只是第 4 近邻 |
| 时序是否独立成域 | **不独立** | 触发条件字面成立（评审 5 处偏差中 3 处属时序），**但结论反转**：三处分落三个不同域（`bt-uds`/`bt-diag-transport`/`bt-platform`），时序是横切维度而非语义簇；329 条时序需求 329/329 已被现有域覆盖 |

**副产澄清（非缺陷）**：曾疑心 1873–1956 那批 `agedDTCLimit`/`ConfirmedDTCLimit` 是 `bt-dtc` 召回缺口，实查 **90/90 全在 `bt-dtc`**。

**方法论留痕**：未决项 3 是「触发条件成立但蕴含动作错误」的典型——触发词写的是"考虑"，考虑了，答案是"不"。判定时不能只看条件是否满足，要看条件背后的动作是否成立。

## 设计文档

- 本地：`docs/superpowers/specs/2026-09-30-basetech-expert-agents-design.md`
- 飞书云文档：https://my.feishu.cn/docx/LEU1d4sk8oZJ63x61gQcWDOcnng
  （2026-09-30 以**用户身份**导入，用户可直接打开。另有一份应用身份的冗余副本 `GSDLdaEayoTZNBxgXUkcmIBQnOd`，用户看不到，可弃）
- 该目录**未启用 git**（用户决定暂不纳入版本管理）

## 唤醒词

「Basetech智能体」「Basetech工程师智能体」「汽车诊断智能体」「专家Agent拆分」

关联：[[project-storage-convention]] [[user-profile]]
