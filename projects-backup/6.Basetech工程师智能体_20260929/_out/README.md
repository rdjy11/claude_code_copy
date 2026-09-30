# _out —— 智能体产出目录

本目录存放 Basetech 编排者 agent 的产出文件。**只有编排者可写入此目录**；11 个领域专家均为只读（`Read/Grep/Glob`），不会改动任何文件。

## 命名约定

| 工作流 | 文件名 |
|--------|--------|
| 问答 | `qa-<时间戳>.md` |
| 评审 | `review-<时间戳>.md` |
| 生成 | `gen-<时间戳>.md` |

时间戳建议用 `YYYYMMDD-HHMMSS`。

## 产出格式

三条工作流的产出结构由对应配方固定：

- 问答 → `.claude/skills/basetech/jobs/qa.md`
- 评审 → `.claude/skills/basetech/jobs/review.md`
- 生成 → `.claude/skills/basetech/jobs/gen.md`

共同硬约束：每个结论必须挂需求编号；无编号支撑的标「推断」；文档未覆盖则明说「文档未覆盖」，禁止编造编号。
