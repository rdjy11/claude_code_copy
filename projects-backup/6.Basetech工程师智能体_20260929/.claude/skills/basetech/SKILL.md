---
name: basetech
description: Base Tech SWRS DHU 需求规范的问答 / 评审 / 生成工作流入口。当用户的问题或材料
  涉及 SWRS 需求（DTC、UDS 诊断服务、刷写、车载网络、信息安全、车辆配置、ECU 平台等）时使用。
---

# Basetech 需求助手

面向工程师的全流程助手，处理三类任务：**问答**、**评审**、**生成**。

## 启动前提（重要）

本 Skill 与配套的专业 Agent 都定义在**项目目录**下，因此必须**以项目目录为工作目录**启动 Claude Code，否则它们不会被加载：

```bash
cd "C:/Users/pc/claude_code_copy/projects/6.Basetech工程师智能体_20260929"
claude
```

若从其他目录启动，本 Skill 与 11 个专家 Agent 均不可用。

## 工作流（jobs/）

| 工作流 | 配方 | 用途 |
|--------|------|------|
| 问答 | `jobs/qa.md` | 问「某功能/某服务的具体要求是什么」，答出结论 + 需求编号出处 |
| 评审 | `jobs/review.md` | 给定材料，检查是否满足 SWRS，输出差距清单 |
| 生成 | `jobs/gen.md` | 按既有格式生成新的需求条目 |

## 路由表（需求域 → 派发专家）

按需求所属技术域选择专家；一条需求可属多个域，命中多个时**并行派发全部相关专家**。

| # | 需求域（关键词） | 派发专家 |
|---|---|---|
| 1 | DTC / 故障码 / 检测策略 / 去抖 / 老化自愈 / 快照与扩展数据 / 故障确认 / 状态位与掩码 | `bt-dtc` |
| 2 | UDS 服务 / DID / Routine / Session / SecurityAccess / NRC / P2·S3 时序 / 数据记录 | `bt-uds` |
| 3 | DoIP / DoCAN / UDSonX 承载 / 传输层 N_PDU / 功能与物理寻址 / 诊断网关与路由 | `bt-diag-transport` |
| 4 | 软件下载 SWDL / Bootloader / 刷写流程 / 压缩加密 / Delta Encoding / VBF 格式 | `bt-flash` |
| 5 | 车载以太网 / IPv4·IPv6 / TCP·UDP / VLAN / TSN 与 gPTP / WLAN / IP Command 协议 | `bt-ethernet` |
| 6 | CAN / CAN-FD / LIN 主从与调度表 / FlexRay 静态段与动态段 / 总线速率与失效 | `bt-can-lin-flexray` |
| 7 | A2B / LVDS 1·2·4-wire / SerDes / FPD-Link / 控制通道 UART·I2C | `bt-a2b-lvds` |
| 8 | 网络管理 NM 报文 / 唤醒与睡眠 / 部分网络 PNC / NetworkStatus / 网络管理时间常量 | `bt-nm` |
| 9 | Car Configuration / CCP / VCP / CC Master-Slave 状态机 / Bulk 与 Valid 状态 | `bt-carcfg` |
| 10 | 信息安全 / HSM / 证书 / 签名与软件认证 / SecOC 与 MAC / 隐私 / 功能安全 | `bt-security` |
| 11 | ECU 平台与一致性 / AUTOSAR BSW·RTE / Tier1-Tier2 接口 / Startup Time / 供电与电压 | `bt-platform` |

## 元规则（先于路由表判定）

读 **`_index/meta-rules.md`**（完整路径：`C:\Users\pc\claude_code_copy\projects\6.Basetech工程师智能体_20260929\_index\meta-rules.md`）。

> ⚠️ 注意路径**含 `_index` 子目录**，不是项目根目录。项目根下没有 `meta-rules.md`。

其中是**文档元规则**（如「标准文档与本规范谁优先」），归编排者**直接判定，不下发专家**。

## 三条统一约束

1. **专家只读**——专家只有 `Read/Grep/Glob`，不会修改任何文件；
2. **编排者独占写权限**——所有产出由编排者写入 `_out/`；
3. **结论必须挂需求编号**——无法挂编号的必须显式标注「推断」；文档未覆盖则明说，禁止编造编号。

## 数据资产（只读）

| 层 | 路径 | 用途 |
|---|------|------|
| L0 定位 | `_index/by-domain/<专家>.md` | 该域的「编号 + 标题 + 语料卷」，先在此圈定候选 |
| L0 元规则 | `_index/meta-rules.md` | 文档优先级类需求，由编排者直判 |
| L1 速取 | `SWRS_DHU_需求清单.md` | 编号 → 版本 / 验证方式 / 适用 AUTOSAR / 核心 shall 句 |
| L2 取证 | `Basetech知识库语料/`（20 卷） | 完整正文，仅深度问答与评审时下探 |

## 文件边界提醒

**引用层级必须说清**：L1 清单只保留核心 shall 句，与 L2 语料正文**不等价**。取自清单须写「据需求清单」，只有真正取自语料正文时才可称「语料原文」。
