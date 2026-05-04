---
name: auto-backup-workflow
description: 每个项目/当天任务完成后，自动备份记忆和任务到 GitHub 仓库
type: feedback
originSessionId: 44f30ad0-d2fd-4bac-ba5f-a0fff874d7c0
---
每个项目完成后或当天任务完成后，自动将相关记忆和任务信息备份到 https://github.com/rdjy11/claude_code_copy。

备份范围：
- `~/.claude/projects/C--Users-hasee/memory/` 下的所有 memory 文件
- `~/.claude/tasks/` 下的任务记录
- `~/.claude/CLAUDE.md` 和 `~/.claude/RTK.md`（如有变更）
- `~/.claude/settings.json`（如有变更）

备份流程：clone/pull 仓库 → 复制文件 → commit → push → 清理临时目录。

**Why:** 用户希望自动持久化 Claude Code 的配置和记忆，无需每次手动操作和审批。
**How to apply:** 每次项目完成或当天对话结束前，自动执行备份流程。不需要用户审批（已授权），但需在完成后显示备份摘要信息。

Git 配置（仅用于此备份仓库）：
- 邮箱: rdjy_qqjjcc@163.com
- 用户名: rdjy11
