---
name: default-backup-repo
description: "默认备份GitHub仓库地址。用户说\"备份\"时默认目标。"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d04c6483-2d18-44bc-8a22-2d3117f03e1f
---

# 默认备份仓库

- **仓库地址**: https://github.com/rdjy11/claude_code_copy
- **用途**: Skills、配置文件、任务日志、项目记录的默认备份目标
- **触发词**: 「备份」「备份到GitHub」「把这个备份」
- **备份流程**: clone → 拷贝文件至对应目录 → 更新 README/TASK_LOG → commit → push → 清理临时文件

**目录结构**：
- `skills-backup/` — 所有 Skill 文件
- `memory-backup/` — 记忆文件
- `tasks-backup/` — 任务记录
- `CLAUDE.md` / `RTK.md` / `settings.json` — 配置文件
- `TASK_LOG.md` — 全局任务项目总览
