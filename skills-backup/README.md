# Skills Backup

> 最后更新：2026-05-28

## 评分总览

| Skill | 版本 | Darwin评分 | 等级 | 状态 |
|-------|------|-----------|------|------|
| **prd-reviewer** | v1.0.0 | **91** | **S** | 标杆，无需优化 |
| skill-reviewer | v1.0.0 | ~90+ | S | 方法论Skill参考实现 |
| **prd-generator** | v2.0.0 | **84** | **A** | 边界设计标杆 |
| **grill-me** | v1.1.0 | — | — | 需求追问引擎 |
| **mbse-skill** | v1.4.0 | 70 | B | 经v1.3优化，v1.4用户精简 |
| **pro-doc-generator** | v2.1.0 | 73→B | B | 经v2.1优化重构 |

## 优化案例

### mbse-skill: v1.2 → v1.3 (skill-reviewer驱动)
- 评审得分: 70/B
- 核心问题: D6单文件1055行超载, D4缺HARD-GATE, D3缺边界
- 改造: 拆文件(↓67%), 补CP1+边界表, Cameo步骤化
- 用户后续简化至v1.4.0 (499行纯SysML核心)

### pro-doc-generator: v2.0 → v2.1 (skill-reviewer驱动)  
- 评审得分: 73/B
- 核心问题: D5满分但D6单文件849行, D4无检查点, D3无边界
- 改造: 拆scripts/templates/references, 补CP1+CP2 HARD-GATE, 7边界条件
- 主文件849→307行(↓64%)

## 文件结构

```
skills-backup/
├── README.md                    ← 本文件
├── NEW_SKILLS_20260516.md      ← 05-16 新增Skill汇总
├── grill-me/SKILL.md
├── mbse-skill/
│   ├── SKILL.md                (v1.4.0)
│   ├── references/engine-architecture.md
│   └── templates/automotive.md
├── skill-reviewer/
│   ├── SKILL.md
│   └── reference/
├── prd-generator/SKILL.md
├── prd-reviewer/
│   ├── SKILL.md
│   └── reference/
├── pro-doc-generator/
│   ├── SKILL.md                (v2.1.0)
│   ├── scripts/canvas-functions.js
│   ├── templates/swimlane.html
│   └── references/lark-output-spec.md
└── (原有22个Skills...)
```
