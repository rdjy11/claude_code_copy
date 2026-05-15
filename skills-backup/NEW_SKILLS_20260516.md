# 新增 Skills 记录 | 2026-05-15 ~ 2026-05-16

## grill-me (需求追问引擎)
- 版本: v1.1.0
- 功能: 逐分支追问用户的计划/设计，直到达成共识
- 文件: grill-me/SKILL.md

## mbse-skill (MBSE 建模助手)
- 版本: v1.3.0 (经 skill-reviewer 评审从 v1.2 优化至 v1.3)
- 功能: MagicGrid + SysML v2 + Cameo 系统建模
- 架构: 主文件 343 行 + references/ + templates/
- 文件: mbse-skill/SKILL.md + references/ + templates/ + CHANGELOG.md

## skill-reviewer (Skill 质量评审器)
- 版本: v1.0.0
- 功能: Darwin 8 维度 Rubric 百分制评分
- 文件: skill-reviewer/SKILL.md + reference/

## mbse-skill 优化链路
安装 v1.2 → 用户要求加 Mermaid 可视化 (v1.2) → skill-reviewer Darwin 评审 70/B → P0拆文件+P0补CP1+P1边界表+P1后驱+P2 Cameo步骤化 (v1.3)
