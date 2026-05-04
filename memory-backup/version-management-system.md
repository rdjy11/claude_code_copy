---
name: 版本管理系统 (VSMS)
description: 汽车软件版本管理系统，Flask + 原生 JS SPA，管理基线/版本/配置项/变更/发布/文件
type: project
originSessionId: current
---

项目位于 `E:\.Claude Code Project\2.版本管理系统_20250501\`。

**功能**：汽车电子软件版本管理平台，覆盖基线管理、ECU 版本追踪、配置项管理、变更请求(ECR/ECN)看板、发布包编排、全链路追溯、合规标准参考，内置 AI 助手面板。

**架构**：
- 后端：Flask REST API（`backend/app.py`），SQLite(默认)/MySQL 双模式，7 组端点（baselines / versions / config-items / changes / releases / files / stats）
- 前端：单文件 SPA（`version-management-system.html`），原生 JS 无框架，8 个页面 + AI 面板
- 架构图：`version-management-system-architecture.html`

**启动**：
```bash
cd "E:\.Claude Code Project\2.版本管理系统_20250501\backend"
pip install flask
python app.py
# 访问 http://localhost:5000
```

**数据库**：SQLite 默认（`vsms.db`），含种子数据（5 基线、10 版本、7 CI、7 变更、3 发布）。环境变量 `VSMS_DB_MODE=mysql` 切换 MySQL。

**领域模型**：Baseline 1:N → Version / ConfigItem / Change / File；Release N:M → Baseline（通过 release_baselines 关联表）。

**前端映射**：API 返回 snake_case（如 `ecu_count`），前端 JS 通过 map 函数转为 camelCase（如 `ecuCount`）。

**合规对齐**：ASPICE SUP.8 / ISO 26262-8 / UNECE R156 (SUMS) / UNECE R155 (CSMS) / EU GPSR-PLD。

**唤醒词**：「版本管理系统」「VSMS」「基线管理」「软件版本管理」「版本追溯」「ECR 变更」「SUMS 合规」
