---
name: knowledge-learning-app-progress
description: 知识学习APP v1.3.0修复版——PS ConvertTo-Json数据损坏已修复，Node.js合并，APK正常工作
metadata: 
  node_type: memory
  type: project
  originSessionId: 2c28e8f7-1fd9-4dc2-95b1-3b304e719762
---

# 知识学习 APP 开发进度

**项目路径**: `E:\.Claude Code Project\3.知识学习APP_20260528\`
**ASCII 联结**: `E:\.Claude Code Project\3.knowledge-app\` → 原目录（构建必须用此路径）

## 当前版本: v1.3.0 修复版 ✅ (2026-06-07)

### ⚠️ v1.3.0 关键 BUG 修复记录

| 项目 | 详情 |
|------|------|
| **症状** | APK 安装后题库加载不出来 |
| **根因** | PowerShell `ConvertTo-Json -Depth 6` 在合并 Ch1-3 + Ch4-5 + Ch6-8 时将习题对象损坏为 `""` 空字符串 |
| **崩溃点** | `Quiz.fromJson()` → `json['id'] as String` → quiz 数据是 String 而非 Map → `_CastError` → 整个课程加载失败 |
| **影响** | 微积分全部 65 题损坏；CET6 47 题因未经过 PS 合并故完好 |
| **修复** | 改用 Node.js `JSON.parse/stringify` 合并三个 JSON 文件，完全避免 PS 的序列化 bug |
| **修复后** | math_calculus.json 从 66KB → 99KB（数据恢复），35知识点/65题全部正常 |
| **构建时间** | 增量编译 99.4s |

### 版本历史

| 版本 | 主要内容 | 微积分题 | CET6题 | 总题 |
|------|---------|---------|--------|------|
| v1.0.0 | 4学科基础版 | 12 | 8 | 33 |
| v1.1.0 | CET6完整词表(2983词+47题) | 12 | 47 | 72 |
| v1.2.0 | 微积分Ch1-3扩展 | 30 | 47 | 90 |
| v1.3.0 | 微积分Ch4-8+修复 | 65 | 47 | **125** |

### 微积分完整体系 (v1.3.0)

| 章 | 内容 | 知识点 | 习题 |
|----|------|--------|------|
| 1 | 函数与极限 | 7 | 15 |
| 2 | 导数与微分 | 4 | 7 |
| 3 | 中值定理与导数应用 | 4 | 8 |
| 4 | 不定积分 | 5 | 8 |
| 5 | 定积分与反常积分 | 5 | 7 |
| 6 | 多元函数微积分 | 5 | 7 |
| 7 | 无穷级数 | 5 | 7 |
| 8 | 微分方程基础 | 4 | 6 |
| **合计** | **8章23节** | **35** | **65** |

### 关键产出文件
- **APK v1.3.0 修复版**: `knowledge_app\build\app\outputs\flutter-apk\app-debug.apk` (145.33 MB, 2026-06-07 01:27)
- **微积分 JSON** (修复后): `math_calculus.json` (99 KB)
- **CET6 JSON**: `english_cet6.json` (1159 KB)
- **预览 HTML v1.3.0**: `preview.html` (全部8章35知识点34题可交互演示)
- **修复脚本**: `merge_calculus.js` (Node.js 合并，替代 PS ConvertTo-Json)
- **构建脚本**: `build_cet6_json.js`, `build_calculus_json.py`
- **文档**: `CHANGELOG.md`, `docs/CET6_vocabulary_quizzes_part1_AM.md`, `docs/CET6_vocabulary_quizzes_part2_NZ.md`

### 重要教训
- **禁止**用 PowerShell `ConvertTo-Json` 处理嵌套 JSON（会损坏深层数据）
- **必须**用 Node.js `JSON.parse/stringify` 或 Python `json.dump/load` 处理 JSON 合并

## 环境信息

| 组件 | 路径 | 版本 |
|------|------|------|
| Flutter | `E:\flutter\` | 3.44.0 |
| Java | `E:\Program Files\Java\jdk-17.0.19+10\` | 17 |
| Android SDK | `E:\Android\` | 34/35/36 |
| VS Build Tools | `E:\VisualStudio\BuildTools\` | 2022 |

## 构建命令
```powershell
$env:JAVA_HOME = "E:\Program Files\Java\jdk-17.0.19+10"
$env:ANDROID_HOME = "E:\Android"
$env:Path = "$env:JAVA_HOME\bin;E:\flutter\bin;" + $env:Path
cd "E:\.Claude Code Project\3.knowledge-app\knowledge_app"
flutter build apk --debug
```
