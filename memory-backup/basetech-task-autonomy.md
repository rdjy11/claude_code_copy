---
name: basetech-task-autonomy
description: 项目 6（Basetech 工程师智能体）后续开发中，用户已预授权自主编写脚本与执行 shell，无需逐次请求权限
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-09-30
  originSessionId: c4b75c45-a383-4100-ae7a-760125b5ec82
---

**规则**：在项目 6（Basetech 工程师智能体）的后续开发中，任务所需的脚本文件编写、shell 指令执行可**自行执行，不必再逐次请求权限或让用户点击确认**；任务完成后反馈结果即可。

**Why:** 用户在 2026-09-30 主动授予，认为逐次权限确认拖慢节奏。用户原话：「我允许你有本地计算机管理员的权限……任务完成后反馈给我结果即可」。

**How to apply:**

- 适用范围**仅限项目 6 的开发工作**（语料处理、索引生成、agent/skill 文件创建、验证跑测）。
- **不外延到**：删除用户文件、`git push` 等影响远端或不可逆的操作、向外部系统发送内容、改动 `~/.claude/settings.json` 等全局配置——这些仍先确认。
- 授权锚定在"本任务"。若用户日后开启新任务，应重新确认是否沿用。
- 报告方式：任务完成后给结果，不必中途逐步请示；但遇到**与预期不符的发现**（如数据异常、路径失效）仍应即时说明。

关联：[[basetech-engineer-agent]] [[code-comments-required]]
