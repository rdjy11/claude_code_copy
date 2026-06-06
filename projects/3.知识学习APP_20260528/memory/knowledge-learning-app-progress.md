---
name: knowledge-learning-app-progress
description: 知识学习APP v1.3.0——微积分完整8章35知识点65题+2983词CET6+诗文+马原，共125题
metadata: 
  node_type: memory
  type: project
  originSessionId: 2c28e8f7-1fd9-4dc2-95b1-3b304e719762
---

# 知识学习 APP 开发进度

**项目路径**: `E:\.Claude Code Project\3.知识学习APP_20260528\`
**ASCII 联结**: `E:\.Claude Code Project\3.knowledge-app\` → 原目录

## 当前版本: v1.3.0 ✅ (2026-06-07)

### 版本历史

| 版本 | 主要内容 | 微积分 | CET6 | 总题数 |
|------|---------|--------|------|--------|
| v1.0.0 | 4学科基础版 | 12题 | 8题 | 33 |
| v1.1.0 | CET6完整词表(2983词+47题) | 12题 | 47题 | 72 |
| v1.2.0 | 微积分Ch1-3扩展 | 30题 | 47题 | 90 |
| v1.3.0 | 微积分Ch4-8扩展(不定积分→微分方程) | 65题 | 47题 | **125** |

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

### 全APP统计
| 学科 | 内容量 | 习题 |
|------|--------|------|
| 数学 | 35知识点 | 65题 |
| 英语 | 2983词 | 47题 |
| 语文 | 3篇诗文 | 6题 |
| 政治 | 3知识点 | 7题 |
| **合计** | **3024** | **125题** |

### 关键产出文件
- APK: `knowledge_app\build\app\outputs\flutter-apk\app-debug.apk` (v1.3.0)
- 微积分JSON: `math_calculus.json` (66KB)
- CET6 JSON: `english_cet6.json` (1159KB)
- 预览: `preview.html`
- 文档: `docs/CET6_vocabulary_quizzes_part1_AM.md`, `docs/CET6_vocabulary_quizzes_part2_NZ.md`
- 构建脚本: `build_cet6_json.js`, `build_calculus_json.py`

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
