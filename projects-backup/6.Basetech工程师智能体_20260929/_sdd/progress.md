# SDD ledger — plan: docs/superpowers/plans/2026-09-30-basetech-expert-agents.md

## Setup

- Spec 已读：`docs/superpowers/specs/2026-09-30-basetech-expert-agents-design.md`（binding authority）
- 计划已读：9 个任务，Global Constraints 已记录
- 执行方式：Native（用户选定）
- TDD 子技能：已加载

### Ruling: 环境无 git，skill 的 git 依赖全部降级

`task-brief` / `task-start` / `task-done` / `sdd-workspace` / `review-package` 均依赖 git（实测 `task-brief` 报 `fatal: not a git repository`）。本项目非 git 仓库且用户已决定暂不启用。

决定：不用 worktree；不执行任何 git 命令；不做基于 commit 范围的 review-package；账本改为手工维护于本文件；最终复核走「无 subagent 工具则自审」分支（若 Agent 工具能派发具名 subagent，则改用真复核）。

代价（若判断有误）：失去 git 版本控制与 diff 驱动的复核范围，回溯只能靠文件副本与账本。

## Pre-flight 接口扫描

| 生产 → 消费 | 核对结果 |
|---|---|
| Task 1 `classify/is_meta/volume_of/EXPERT_KEYWORDS` → Task 2 `build()` | 一致；Task 2 以 `EXPERT_KEYWORDS` 键为文件名单一事实源 |
| Task 2 `_index/by-domain/*.md` → Task 3 引用的 `bt-dtc.md` / `bt-uds.md` | 一致 |
| Task 3 `bt-dtc`/`bt-uds` → Task 4 编排者 `Agent(...)` 白名单 | 一致（Task 4 仅 2 个，Task 7 补至 11） |
| Task 6 9 个专家 → Task 7 白名单补齐 | 一致 |
| Task 1 `EXPERT_KEYWORDS` → Task 6 name 表、Task 7 路由表 | 一致 |

**Ruling: `VOLUMES` 存在编号间隙（1616–1624、2652）** —— 卷名区间 `06_1511-1615` 与 `07_1625-1821` 之间、`15_2527-2651` 与 `16_2653-2765` 之间不连续。已核实这些编号不存在需求，故 `volume_of()` 对真实数据不会落空；`test_index_volume_column_matches_corpus_files` 只遍历真实索引行，不受影响。保留 `"??"` 作为越界哨兵。
代价（若判断有误）：某条需求的语料卷列显示 `??`，测试会以 `assertIn` 直接失败暴露，不会静默。

**预判风险（非冲突，执行时留意）**：`bt-can-lin-flexray` 的 `header` / `frame`，`bt-platform` 的 `wire` / `pin` / `power` / `supply` / `ground`，`bt-security` 的 `mac` 均为高频英文词，可能造成过召回。Task 2 Step 6 的前 50 条抽查是这道防线。

## Progress

**Ruling（记账粒度）**：`WORK_LOG.md` 改按里程碑批量更新（Task 2 / 5 / 7 / 9 后），逐任务明细留在本账本，避免为每个任务单独改写同一文件。
代价（若判断有误）：`WORK_LOG.md` 粒度较粗，完整过程需查本账本。

Task 1: complete（tests: `python -m unittest discover -s _tools -p "test_*.py"` → 7/7 pass）
- 交付：`_tools/build_domain_index.py`（EXPERT_TITLES / EXPERT_KEYWORDS / META_KEYWORDS / VOLUMES / classify / is_meta / volume_of）、`_tools/test_build_domain_index.py`
- 证据：先观察 RED（`ModuleNotFoundError: No module named 'build_domain_index'`），实现后 GREEN 7/7
- 偏离：无

Task 2: complete（tests: `python -m unittest discover -s _tools -p "test_*.py"` → 12/12 pass）
- 交付：`_index/by-domain/`（11 份）+ `_index/meta-rules.md`；未命中 0；元规则恰为 [460, 468, 1103]
- 各域条数：bt-uds 883 / bt-dtc 583 / bt-flash 546 / bt-can-lin-flexray 461 / bt-ethernet 429 / bt-platform 341 / bt-security 255 / bt-diag-transport 200 / bt-a2b-lvds 180 / bt-carcfg 126 / bt-nm 100；索引条目总数 4104（多标签）
- 迭代过程：未命中 252 → 222 → 33 → 11 → 3 → 0

**Ruling (Task 2a): 词边界规则误伤 camelCase，补 camel 匹配通道**
发现：`readDataByIdentifier` 小写化后为 `readdatabyidentifier`，关键词 `readdata` 后邻 `b` 被判为非边界而拒配，导致整个 UDS 服务族（DTC/DID/Routine）集体漏配——初始 252 条未命中里过半源于此。
决定：`_compile` 对单字关键词编译两条正则——`strict`（小写全文、前后皆非字母数字）与 `camel`（原文、前邻非字母数字且后邻为大写字母），任一命中即可。既保住 `can` 不误命中 `cannot`，又让 camelCase 标识符可被捕获。
代价（若判断有误）：`CanBus` 之类也会命中 `can`（视为正确）；若某驼峰词恰好以大写开头且语义无关，会误召回。

**Ruling (Task 2b): 引入 WEAK_KEYWORDS，泛化词只在标题中匹配**
发现：正文平均 1357 字符，`frame`/`header`/`can`/`period`/`service` 等英文常用词在正文中几乎必然出现。实测 `bt-can-lin-flexray` 665 条中有 317 条（48%）仅靠正文泛词命中，`bt-platform` 甚至把「one-wire LVDS」用 `wire` 错收进来。违反 spec §6.3-3 的精度要求。
决定：新增 `WEAK_KEYWORDS` 集合，其中的泛化词仅对**标题**匹配；强关键词（具体术语）仍对标题+正文匹配。先写测试 `test_weak_keyword_counts_in_title_only` 观察 RED，再实现。
效果：索引条目总数 4701 → 4104，`bt-can-lin-flexray` 665 → 461（-31%）。
代价（若判断有误）：正文里出现的泛词不再计入，可能使少量需求少一个域标签；由「零盲区」门槛与人工抽查兜底。

**Ruling (Task 2c): `build()` 内部拼 `_index`，而非由调用方传入**
发现：实现时 `build(output_root)` 内部拼 `output_root/"by-domain"`，CLI 传 `BASE` 便把产物写到了**项目根**下的 `by-domain/`，与 spec §8 要求的 `_index/by-domain/` 不符（测试因传 tmp 而恰好掩盖）。
决定：改为契约「`build(project_root)`，产物固定落在 `<project_root>/_index/`」。先改测试断言为 `tmp/_index/by-domain` 观察 RED，再改实现；并删除误建的 `<项目根>/by-domain/`。
代价（若判断有误）：无——该改动消除了一处易犯的调用错误。

**Ruling (Task 2d): `bt-platform` 移除 wire / pin / connector / power**
发现：抽查仅靠标题泛词入选的条目时，`bt-platform` 52 条中大量为「one-wire LVDS」「four-wire LVDS」「Power on - master sends the first header」——实属 A2B/LVDS 与总线域。这四词在本规范里主要指向 LVDS 链路与总线事件。
决定：从 `bt-platform` 关键词表移除这四词，保留 hardware / voltage / supply / ground / battery / transceiver / termination。
代价（若判断有误）：真正属线束/供电平台的需求会少一个标签；`bt-platform` 由 356 降至 341，抽查未见真需求流失。

**已知残留（不修，记入验证记录）**：时序类泛词（timeout / timing / latency / period）仍使 `bt-uds` 收入 138 条纯时序条目（如「By-Pass Latency」「Slave discovery timeout」）。但 spec §4.4 已明确「时序/性能（346 条）并入 `bt-uds` 与 `bt-diag-transport`」，故这属**设计意图**而非缺陷。

**环境修复**：测试中的 `open(...).read()` 未关闭文件产生 ResourceWarning，改用 `_read()` 上下文管理器，恢复 TDD 要求的「输出无警告」。测试数 7 → 12。

Task 3: complete（内容验证通过，见下方 Ruling 3a 对验证方式的说明）
- 交付：`.claude/agents/bt-dtc.md`、`.claude/agents/bt-uds.md`（五节结构 + `tools: Read, Grep, Glob` + `model: inherit`）
- 证据：两次独立内容验证均通过——`bt-dtc` 就 U2300-55 挂出真实编号 1817/2100 并把 DID 问题**转介**给 `bt-uds`；`bt-uds` 就 SecurityAccess/P2 答出语料原文（2622/2623/2620：50 ms 非编程会话、25 ms 编程会话、P2\* 5000 ms）并把 DTC 老化问题**转介**给 `bt-dtc`。两者均零编造编号，且都显式区分了「据需求清单」与「语料原文」。

**Ruling (Task 3a): 以「读取定义文件正文并当作指令执行」替代「点名调用 subagent」**
发现：实测 `Agent(subagent_type="bt-dtc")` 返回 `Agent type 'bt-dtc' not found. Available agents: claude, claude-code-guide, Explore, general-purpose, Plan, statusline-setup`。项目级 `.claude/agents/*.md` **只在以项目目录为 cwd 的交互式 Claude Code 会话中注册**，本执行会话的工具集不含它们。计划中所有「点名调用」步骤（Task 3.3 / 4.4 / 5 / 6.2 / 7.5 / 8）因此都无法按原样执行。
决定：改用通用 subagent 读取该 md 文件、把 frontmatter 之外的正文当作自身操作指令并严格执行，再由我核对回答质量。
覆盖范围：**能**验证定义内容的质量——语料三层导航是否可行、边界转介是否正确、引用层级是否区分、是否拒答与是否编造编号。**不能**验证 Claude Code 的注册与语义路由机制本身。
代价（若判断有误）：若 harness 的注册/description 匹配存在问题，本替代方案不会暴露；交回用户交互式会话后需补一次真实验证。

Task 4: complete（路由验证通过）
- 交付：`.claude/agents/basetech-orchestrator.md`、`.claude/skills/basetech/SKILL.md`、`.claude/skills/basetech/jobs/qa.md`、`_out/README.md`
- 证据：三次提问的路由决策全部正确——Q1「DTC 检测条件」→ 1 个专家 `bt-dtc`；Q2「SecurityAccess 时序」→ 1 个专家 `bt-uds`；**Q3 跨域「0x19 响应超时 + DTC 状态字节」→ 并行派 2 个专家（`bt-uds` + `bt-dtc`）**，符合 Review Focus #1 要求。元规则（460/468/1103）正确判定为不触发。
- 附带发现：编排者主动识别出结构性缺口——9 个域「`_index/by-domain/` 有索引、`.claude/agents/` 无专家体」，并声明命中未建成域时应升级请求澄清而非编造，符合「禁止编造」约束。

**Ruling (Task 4a): 跨域验证题改用真正横跨两个已建专家的题目**
发现：计划 Task 4 Step 4 的跨域测试题为「刷写失败后 DTC 怎么置位？」，期望派 `bt-dtc` + `bt-uds`。但刷写属 `bt-flash`（尚未建成），`bt-uds` 并非该问题的第二个正确域——计划的期望与自身的路由表不自洽。
决定：改用「ReadDTCInformation（0x19）的响应超时是多少？读回的 DTC 状态字节怎么解读？」——该题真实横跨 `bt-uds`（服务时序，需求 2422/2622/2623）与 `bt-dtc`（状态位语义，需求 2125–2132），是当前两个已建专家间唯一干净的跨域用例。
代价（若判断有误）：跨域双派能力只在「UDS 服务时序 × DTC 状态语义」这一种组合上得到验证；其余跨域组合（如刷写×DTC）待 `bt-flash` 建成后需补验。

**Ruling (Task 4b): 提前创建 `_out/` 目录**
发现：编排者需向 `_out/` 写产出，但该目录此前不存在（计划把它排在 Task 7 Step 4）。验证时已实际暴露此空档。
决定：提前至 Task 4 创建，并附 `_out/README.md` 说明命名约定与产出格式。
代价（若判断有误）：无——仅为目录前置，不改变任何契约。

Task 5: complete（防幻觉与编号跳跃验证通过）
- 交付：`docs/operations/验证记录-最小闭环.md`
- 证据：5 题 **零编造编号**——题 1 作答并挂真实编号 1812/1804/1813/2134；题 2（云端 OTA 差分协议）、题 3（跨车 V2X）正确答「文档未覆盖」；题 4（编号 418）、题 5（编号 430）正确说明不存在，且核对扎实（11 份索引词边界 Grep、清单序列 417→452 断档、语料 Grep 三重确认）。
- 结论：**最小闭环成立**——架构（专家只读 / 编排者派发 / 三层语料导航 / 引用纪律 / 拒答机制）在 2 个域上验证有效，可以铺满 11 个域。

**任务清单勘误**：Task 4 的待办在 TodoWrite 中一度被漏列（呈现为 10 项而非 11 项），已补齐；实际执行未受影响。

Task 6: complete（9 个新专家冒烟验证 9/9 通过）
- 交付：`.claude/agents/` 下 `bt-diag-transport` / `bt-flash` / `bt-ethernet` / `bt-can-lin-flexray` / `bt-a2b-lvds` / `bt-nm` / `bt-carcfg` / `bt-security` / `bt-platform`
- 证据：9 题分别在各自域内挂出真实编号（N_WFTmax=255 挂 1209/1210；VBF 数据段挂 3483/3484；LIN 调度表挂 6270/6271；1-wire vs 2-wire 挂 1026/1027；PNC 转发挂 3548/3550；Bulk→Valid 挂 359；签名方法挂 1598/1594/1595/1596；Startup Time 挂 1673），**无编造、无越界**。
- 一致性核对：`.claude/agents/*.md` 12 个（1 编排 + 11 专家），与 `_index/by-domain/` 11 份一一对应。
- 附带发现（已修）：验证者指出需求 **2362《ECU start up time》只进了 `bt-nm` 索引、未进 `bt-platform`**——因关键词只收连写 `startup time`，漏了 `start up` / `start-up` 分隔变体。

**Ruling (Task 6a): 补复合词分隔变体关键词**
发现：需求 2362《ECU start up time》标题用空格分隔，而 `bt-platform` 关键词只有连写 `startup time`，导致该需求被错归到他域、平台域漏收。
决定：先写测试 `test_compound_term_separator_variants`（对 `Startup Time` / `ECU start up time` / `ECU start-up time` 三种写法断言命中 `bt-platform`）观察 RED，再补 `start up` / `start-up` / `startup` 三个关键词。测试数 12 → 13，`bt-platform` 341 → 379，未命中仍为 0。
代价（若判断有误）：`startup` 一词较泛，可能让平台域多收少量条目；抽查未见明显噪声。2362 目前同时出现在 `bt-nm` 与 `bt-platform` 索引中，属多标签重叠（设计允许），但 `bt-nm` 那条归属存疑，列为遗留观察项。

Task 7: complete（评审与生成工作流验证通过）
- 交付：编排者 `tools` 白名单补齐至 11 个专家；`SKILL.md` 路由表补齐至 11 行；新增 `jobs/review.md`、`jobs/gen.md`
- 证据（评审）：对一份含 **3 处埋设偏差**的自拟材料评审，**3/3 全部抓到**且判定为「不符合」并挂真实编号——① SecurityAccess 在默认会话的支持被写反（挂 **2502**）；② P2 写为 100 ms（挂 **2622**/2623，实为 50 ms / 25 ms）；③ 遗漏 DTC 老化（挂 **1812**/1804）。同时对材料中 2 个**干净项未误报**（判「符合」）。报告四要素齐全：统计行、按严重度降序的差距清单、跨域冲突节、无法判定项及原因节。
- 证据（生成）：为「周期读取 DID」生成 1 条新增条目，**格式 7/7 齐备**（`<新增>` 占位 / 版本 / 验证方式 / 适用 / shall 句式含 shall not / 「编号待人工确认」标注 / 参照依据编号 2474–2480 等），**零编造编号**。
- 已知限制：验证以编排者直接执行替代真实子进程派发（见 Ruling 3a）；引用层级为 L1 清单而非 L2 语料正文。

Task 8: complete（§10 四项验证全部通过）
- 交付：`docs/operations/验证记录-完整.md`
- 证据：
  - **测试 1 路由**：覆盖全部 11 个域 + 1 个跨域题，**12/12 正确 = 100%**（≥ 85% 门槛）。跨域题并行派 2 个专家。
  - **测试 2 防幻觉**：**编造编号 0 个**；云端 OTA 差分协议、跨车 V2X 正确答「未覆盖」；编号 418 / 430 三重核对后答「不存在」。
  - **测试 3 评审召回**：含 5 处埋设偏差的材料，**5/5 全抓到**（2622/2623、2502、2097/1811/1812、1209/1210、1673/2362），**零误报**，报告四要素齐全。
  - **测试 4 生成一致性**：**7/7 字段齐备**，无格式漂移。
- 结论：四项全部达到通过条件，**完整体系验证通过**。

**执行汇总**：9 个任务全部完成。13 项单元测试 + 12 项路由 + 5 题防幻觉 + 8 项评审（3+5）+ 生成格式核对，均通过。

Task 9: complete
- 交付：`docs/operations/唤醒调用手册.md`（六章：角色对应表 / 启动前提 / 唤醒方式 / 三条工作流用法 / 可复制样例 / 故障排查 + 数据位置附录）
- 飞书云文档（用户身份导入）：https://my.feishu.cn/docx/BfiOdaYO2ogr9ExTo1HcgbIknZb
- 措辞面向工程师，不假设其了解 subagent 机制；角色对应表含 12 个 agent + 3 条工作流的「名称 → 中文名 → 职责 → 典型问法」

---

## 全部 9 个任务完成

**交付物清单**

| 类别 | 文件 |
|------|------|
| 索引生成器 | `_tools/build_domain_index.py`、`_tools/test_build_domain_index.py`（13 项测试） |
| 域索引（生成物） | `_index/by-domain/*.md`（11 份）、`_index/meta-rules.md` |
| 领域专家 | `.claude/agents/bt-*.md`（11 个） |
| 编排者 | `.claude/agents/basetech-orchestrator.md` |
| 工作流 | `.claude/skills/basetech/SKILL.md`、`jobs/{qa,review,gen}.md` |
| 产出目录 | `_out/README.md` |
| 验证记录 | `docs/operations/验证记录-最小闭环.md`、`验证记录-完整.md` |
| 操作手册 | `docs/operations/唤醒调用手册.md` + 飞书文档 |

**Ruling 汇总（共 8 条）**：R1 无 git 时 skill 的 git 依赖降级；2a camelCase 匹配通道；2b 泛化词仅匹配标题；2c `build()` 内部拼 `_index`；2d `bt-platform` 移除 wire/pin/connector/power；3a 以「读取定义文件充当指令」替代具名 subagent 派发；4a 跨域验证题更换；4b 提前创建 `_out/`；6a 补复合词分隔变体关键词。

---

## 最终整体复核（独立复核者，最强模型，全新上下文）

**结论：无 Critical、无 Important。** 独立核实通过项：

- 生成物可复现：重跑 `build()` 到临时目录，与仓库内 11 份索引 + `meta-rules.md` **逐字节一致**；
- **零盲区独立重算成立**：11 份索引 + meta 的并集**恰好覆盖 1999 条**，`missing=NONE`、`extra=NONE`；
- 编排者白名单恰为 11 个、与 `.claude/agents/` 一一对应；`SKILL.md` 路由表 11 行与之一致；
- 11 个专家全部含五节结构、`tools` 均写死为只读；
- 全部 `bt-*` 交叉引用无悬空；
- **验证记录未夸大**——「harness 层注册与语义路由未验证」被明确标为未覆盖，未把替代验证写成真实验证；记录引用的编号经核全部真实存在；
- 手册的启动前提与角色表与实际目录结构一致。

**复核发现的处理**：

**Final: fixed 泛化词单复数自相矛盾** —— `frame`/`header` 已入 `WEAK_KEYWORDS`，但其复数 `frames`/`headers` 未入，仍按强词在正文匹配，与 Ruling 2b「泛化词只在标题算数」的决策自相矛盾。
处理：先写测试 `test_weak_keyword_plurals_also_title_only` 观察 RED，把 `frames`/`headers` 补入 `WEAK_KEYWORDS`。
**连带影响（重要）**：该修复触发 1 条新盲区——需求 **1091《Time restrictions of message》** 原先仅靠正文里的复数 `header frame`/`response frame` 命中。经查其正文（13.75 µsec 字节间隔、Message type1/2、CheckSum/ACK），属 **LVDS 控制通道报文协议**，与 1104/1108 同族，应归 `bt-a2b-lvds`。故补该协议专属强关键词 `header frame` / `response frame`。
结果：测试 13 → **14 项全绿**；未命中回到 **0**；`bt-can-lin-flexray` 461 → 429（正是要消除的噪声）、`bt-a2b-lvds` 180 → 192。

**判定说明**：复核将此项评为 Minor，但它是**执行者自身决策（Ruling 2b）的实现遗漏**，属未完成的自身改动而非新增范围，故按 `verification-before-completion` 的要求修复，而非延后。

**Final: Ruling 账本不删除** —— skill 要求复核通过后删除本计划的工作区，理由是「git 历史即记录」。但本项目**无 git**，账本是唯一过程记录，删除即丢失全部裁决与证据链。决定保留 `_sdd/progress.md`。
代价（若判断有误）：项目内多一个 `_sdd/` 目录；若日后启用 git，可将其移入忽略清单。

---

## 收尾：最后一项未验证项关闭（用户补验）

执行会话无法派发项目级具名 subagent，故「Claude Code 的 agent 注册与语义路由机制」此前列为未覆盖。**用户已于 2026-09-30 在交互式会话中补验通过**：

- 证据：产出文件 `_out/qa-20260930-234601.md`（问答「DTC 老化（aging）条件是什么？」）
- 该文件自行声明 `路由：DTC / 老化 → 专家 bt-dtc（单域，未触发元规则 460/468/1103）`，证明**加载 → 路由 → 派发 → 写 `_out/` 全链路生效**
- 用户确认：**输出结果已确认，格式规则符合要求**
- 输出契约逐项核对通过：三段结构 / 引用层级声明 / 结论挂编号+标题+卷 / 推断显式标注 / 文档未覆盖主动划界 / 编号双向核对
- 额外印证：产出正确处理了 AUTOSAR 4.0.x 与 4.1+ 的**跨版本行为分支**（4.0.x 保留 DTC 记录并置 SI30 bit3；4.1+ 清除 snapshot/extended data 且 bit3 恒 0），并归纳出各故障类型 `agedDTCLimit` 的取值规律

**至此 9 个任务、4 项正式验证、以及机制侧补验全部通过，无遗留未验证项。**

---

## 后续请求：归档协作范例（2026-10-01，用户下发）

用户要求把该次问答归档为范例，并记录「对应问题 / 由哪个 Agent 产出 / 哪些 Agent 参与 / 如何交互与分配」。
执行者**未凭设计推测**，而是从运行时记录中提取真实轨迹：

- 主会话：`~/.claude/projects/C--Users-pc-claude-code-copy-projects-6-Basetech-------20260929/8006b8e9-....jsonl`
- 子 Agent：同目录 `.../subagents/agent-a12411177a7a74873.jsonl`

**交付**：`docs/operations/范例-专家智能体协作全记录.md` + 飞书 https://my.feishu.cn/docx/CckXdwhqOoIfUOxbNijcD0Bdnre
产出归档至 `_out/samples/范例1-问答-DTC老化-20260930.md`（从 `_out/` 根目录移入 `samples/`）。

**提取到的真实事实**：仅 2 个角色参与——**主 Agent（承担编排）+ 领域专家 `bt-dtc`**；子 Agent 侧 41 步（15 次 Read、19 次 Grep、1 次 Glob，触及 8 个语料卷）。

**由此暴露的两个问题（均已修）**：

**Final: fixed 项目根残留 `meta-rules.md`** —— 真实会话读取元规则时用的是 `<项目根>/meta-rules.md`，丢了 `_index` 一层。之所以未报错，是因为项目根下**恰好残留着一份同类文件**（Task 2 的 `_index` 路径 bug 造成，当时只清理了误建的 `by-domain/`，漏了这份；两者内容因 meta-rules 不受后续关键词调整影响而恰好一致）。
处理：① 删除根目录残留；② 在 `SKILL.md` 与 `basetech-orchestrator.md` 中把该路径写为完整绝对路径，并显式提示「路径含 `_index` 子目录，项目根下没有 `meta-rules.md`」。
代价（若判断有误）：无。但**若不删残留，同样的路径猜测会一直被掩盖**，属典型「错路径被同名文件兜住」的隐性缺陷。

**观察：`basetech-orchestrator` 在真实会话中未被调用** —— 编排实际由主 Agent 直接完成。功能无损失且更省（少一层中转），且更优（主 Agent 能与用户交互，而编排者作为 subagent 不能）。已作为「待议事项」写入范例第六节，建议后续考虑把设计改为「主 Agent 编排 + 编排者仅在无人值守场景使用」。

**自查纠正**：撰写范例时曾在文首写下一行**凭空编造的飞书 URL 占位**，导入前已发现并删除，未流入交付物。

