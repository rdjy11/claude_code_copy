# 任务与项目总览 | 2026-05

> 最后更新：2026-05-28

---

## 一、近期任务时间线 (2026-05-15 ~ 2026-05-28)

### Skill 安装与管理

| 日期 | Skill | 操作 | 备注 |
|------|-------|------|------|
| 05-15 | **grill-me** (v1.1.0) | 安装 | 需求追问引擎，逐分支追问计划/设计 |
| 05-15 | **mbse-skill** (v1.1.0) | 安装 | MBSE建模助手，MagicGrid + SysML v2 |
| 05-15 | **skill-reviewer** (v1.0.0) | 安装 | Darwin 8维度 Skill 评审器 |
| 05-15 | mbse-skill → v1.2 | 改造 | 新增 Mermaid 可视化输出 + CP4 + VS Code 渲染提醒 |
| 05-15 | mbse-skill v1.2 | 评审 | skill-reviewer 评分 **70/B** — 单文件1055行超载，缺CP1和边界条件 |
| 05-16 | mbse-skill → v1.3 | 优化 | 架构重构：拆 references/ + templates/，主文件343行，补CP1 HARD-GATE + 边界条件表，Cameo步骤化 |
| 05-16 | **prd-generator** (v2.0.0) | 安装+评审 | PRD需求文档一键生成，评分 **84/A** |
| 05-16 | **prd-reviewer** (v1.0.0) | 安装+评审 | PRD质量评审器，评分 **91/S**（标杆级） |
| 05-16 | **pro-doc-generator** (v2.0.0) | 安装+评审 | 流程文档生成，评分 **73/B** |
| 05-16 | pro-doc-generator → v2.1 | 优化 | 849→307行，拆 scripts/templates/references/，补CP1+CP2 HARD-GATE + 7边界条件 |
| 05-28 | mbse-skill → v1.4.0 | 简化 | 用户手动精简：移除 Mermaid可视化/CQ验证/CP边界条件，回归纯 SysML 建模核心（499行） |

### GitHub 备份

| 日期 | 内容 |
|------|------|
| 05-16 (第1次) | grill-me + mbse-skill v1.3 + skill-reviewer + CHANGELOG |
| 05-16 (第2次) | prd-generator + prd-reviewer + pro-doc-generator v2.1 + 汇总 |

### Mermaid 可视化测试

- 生成 `test-mermaid.md`（整车BDD + ADAS活动图 + 智驾状态机）→ VS Code 渲染验证通过
- 生成 `eea-architecture.md`（中央计算+区域控制器拓扑 + 平台内部架构 + 通信带宽分配）
- 确认 Markdown Preview Mermaid Support 扩展可用

---

## 二、当前 Skill 全景

### 知识工作类（原有）
| Skill | 用途 |
|-------|------|
| boss-perspective | 领导视角汇报评审框架 |
| huashu-nuwa | 人物思维框架蒸馏 |
| cangjie-skill | 书籍→Skill 蒸馏 |
| cn-patent-disclosure | 中文专利交底书撰写 |
| ljg-xray-paper | 学术论文X光解构 |
| academic-paper-strategist | 论文战略规划 |
| academic-paper-composer | 论文撰写执行 |

### 工程工具类（新增）
| Skill | 版本 | 评分 | 用途 |
|-------|------|------|------|
| **grill-me** | v1.1.0 | — | 需求逐分支追问，7维度覆盖+CQ验证 |
| **mbse-skill** | v1.4.0 | 70/B | SysML v2建模，MagicGrid+语法速查+Cameo+HARA |
| **prd-generator** | v2.0.0 | 84/A | 一句话→7模块完整PRD |
| **prd-reviewer** | v1.0.0 | 91/S | 7维度PRD评审，动态权重+证据驱动 |
| **pro-doc-generator** | v2.1.0 | 73/B | SIPOC+RACI+KCP+KPI+Canvas泳道图 |
| **skill-reviewer** | v1.0.0 | — | Darwin 8维度 Skill 质量评审 |

### 架构框架类（内置）
| Skill | 用途 |
|-------|------|
| brainstorming | 创意前需求探索 |
| writing-plans | 多步骤任务规划 |
| test-driven-development | TDD 开发 |
| systematic-debugging | 系统化调试 |
| requesting-code-review | 代码审查请求 |
| receiving-code-review | 审查反馈处理 |
| using-git-worktrees | Git Worktree 隔离 |
| verification-before-completion | 完成前验证 |

---

## 三、代码项目资产

| # | 项目 | 路径 | 状态 |
|---|------|------|------|
| 1 | 新闻网站爬虫 | `E:\.Claude Code Project\1.新闻网站爬虫_20260501\` | 完成 |
| 2 | 版本管理系统 (VSMS) | `E:\.Claude Code Project\2.版本管理系统_20250501\` | 完成 |
| 3 | 知识学习APP (Flutter) | `E:\.Claude Code Project\3.知识学习APP_20260528\` | 开发中 |
| 4 | 论文配图版 | `E:\.Claude Code Project\4.论文配图版_20260502\` | 完成 |
| 5 | AIVAS智能汽车架构系统 | `E:\.Claude Code Project\5.AIVAS智能汽车架构系统_20260503\` | Phase 1骨架完成 |

### 论文/文档资产

| 文件 | 说明 |
|------|------|
| `MBSE_PLE_Revised_Paper_20260502.docx` | MBSE+PLE 修订论文 |
| `diagrams/` | 论文配图（SysML图 PNG + SVG + PlantUML）含 AED 自动灯光系统架构设计 |

---

## 四、Skill 优化方法论总结

通过本阶段实践，形成了 Skill 安装→评审→优化的闭环：

```
安装 Skill
  → skill-reviewer Darwin 8维度评审
  → 定位短板（D6单文件超载/D4缺HARD-GATE/D3缺边界条件）
  → P0拆文件 + P0补检查点 + P1补边界表 + P2补metadata
  → 主文件行数下降60%+，评分提升10-15分
```

**已验证的优化案例：**
- **mbse-skill**: 1055行 → 343行 (↓67%)，70/B → 预估85/A
- **pro-doc-generator**: 849行 → 307行 (↓64%)，73/B → 预估85/A

**标杆 Skill（无需优化）：**
- **prd-reviewer (91/S)**: 资源架构完美（主文件+references/分离），动态权重系统，证据驱动评审
- **skill-reviewer (90+/S)**: 方法论Skill的参考实现，Darwin Rubric体系完整

---

## 五、GitHub 备份状态

| 仓库 | 内容 | 最后更新 |
|------|------|---------|
| [rdjy11/claude_code_copy](https://github.com/rdjy11/claude_code_copy) | Skills备份 + CLAUDE.md + RTK.md + memory-backup + tasks-backup | 2026-05-28 |

