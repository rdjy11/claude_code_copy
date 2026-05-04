# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### Skill Boundary Rules

Superpowers (`superpowers:*`) 是**软件开发方法论框架**，知识工作类技能 (nuwa/cangjie/xray/academic-paper/patent/boss-perspective) 是**领域工具**。两者不冲突，但需要区分场景：

| 场景 | 该用什么 |
|------|---------|
| 写代码、修bug、加功能 | **Superpowers** 全流程 (brainstorm → plan → tdd → execute → review → finish) |
| 论文分析/专利/拆书/人物蒸馏 | **原有领域技能** (xray/patent/cangjie/nuwa/composer/strategist) |
| 汇报评审 | **boss-perspective** |
| 调试 | **Superpowers** systematic-debugging |
| 模糊需求 | 软件相关→brainstorming；思维框架相关→nuwa |
| **不确定** | **直接问我** |

### Other Installed Skills

| Skill | Purpose |
|-------|---------|
| `/boss-perspective` | 领导视角汇报评审框架 (GSA结构+指标闭环+体感驱动+对标牵引+翻译意识) |
| `/huashu-nuwa` | 女娲造人：输入人名自动蒸馏思维框架，生成人物 Skill |
| `/cangjie-skill` | book2skill：把一本书蒸馏成一组可执行的 Agent Skills (RIA-TV++ 方法论) |
| `/cn-patent-disclosure` | 中文专利交底书撰写：将技术材料整理为结构化交底书草稿，支持 Markdown/DOCX |
| `/ljg-xray-paper` | 论文X光机：解构学术论文，输出认知碰撞卡片 + ASCII art 餐巾纸图 |
| `/academic-paper-strategist` | 学术论文战略规划：平台分析→文献缺口→大纲（含审稿人评分） |
| `/academic-paper-composer` | 学术论文撰写执行：从大纲到完稿，逐章质量检测 |

### Code Project Storage Convention

All code/development projects must be stored in `E:\.Claude Code Project\`. When creating a new project:

1. List existing project folders under `E:\.Claude Code Project\` to determine the next sequence number
2. Create a new folder named `{序号}.{项目名称}_{YYYYMMDD}` (e.g., `3.某项目_20260501`)
3. Save all project files and artifacts inside that folder

**Existing projects**:
- `E:\.Claude Code Project\1.新闻网站爬虫_20260501\`
- `E:\.Claude Code Project\2.版本管理系统_20250501\`

@RTK.md
