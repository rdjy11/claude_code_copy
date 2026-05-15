# 新增 Skills 记录 | 2026-05-15 ~ 2026-05-16

## grill-me (需求追问引擎) — v1.1.0
- 功能: 逐分支追问用户计划/设计，直到达成共识
- 文件: grill-me/SKILL.md

## mbse-skill (MBSE 建模助手) — v1.3.0
- 功能: MagicGrid + SysML v2 + Cameo 系统建模 + Mermaid 可视化
- 优化: skill-reviewer Darwin 评审 70/B → v1.3 架构重构 (P0拆文件+P0补CP1+P1边界表+P1后驱+P2 Cameo步骤化)
- 文件: mbse-skill/SKILL.md + references/ + templates/ + CHANGELOG.md

## skill-reviewer (Skill 质量评审器) — v1.0.0
- 功能: Darwin 8 维度 Rubric 百分制评分
- 文件: skill-reviewer/SKILL.md + reference/

## prd-generator (PRD需求文档一键生成) — v2.0.0 ⭐新增
- 功能: 一句话需求 → 7模块完整PRD (用户故事/GWT/数据模型/灰度策略)
- 评审成绩: 84分/A级 — 边界条件设计标杆
- 文件: prd-generator/SKILL.md

## prd-reviewer (PRD质量评审器) — v1.0.0 ⭐新增
- 功能: 7维度100分制 PRD 评审 (按类型动态调整权重)
- 评审成绩: 91分/S级 — 可直接推广，证据驱动+动态权重是核心优势
- 文件: prd-reviewer/SKILL.md + reference/

## pro-doc-generator (专业流程文件生成) — v2.1.0 ⭐新增
- 功能: SIPOC+RACI+KCP+KPI+Canvas泳道图+飞书输出
- 评审: 73/B → 经优化至 v2.1 (849→307行, +CP1/CP2 HARD-GATE, +7边界条件, +scripts/templates/references)
- 文件: pro-doc-generator/SKILL.md + scripts/ + templates/ + references/

## 优化链路总结
```
mbse-skill v1.2 → skill-reviewer评审(70/B) → v1.3重构 (343行)
prd-generator → skill-reviewer评审(84/A) → 保留原版
prd-reviewer → skill-reviewer评审(91/S) → 保留原版  
pro-doc-generator → skill-reviewer评审(73/B) → v2.1重构 (307行)
```
