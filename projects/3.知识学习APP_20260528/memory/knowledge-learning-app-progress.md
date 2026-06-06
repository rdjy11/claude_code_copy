---
name: knowledge-learning-app-progress
description: 知识学习APP——v1.1.0完成，2983词CET6词汇+47习题，APK构建成功(145MB)
metadata: 
  node_type: memory
  type: project
  originSessionId: 2c28e8f7-1fd9-4dc2-95b1-3b304e719762
---

# 知识学习 APP 开发进度

**项目路径**: `E:\.Claude Code Project\3.知识学习APP_20260528\`
**ASCII 联结**: `E:\.Claude Code Project\3.knowledge-app\` → 原目录（构建必须用此路径）

## 当前阶段：v1.1.0 完成 ✅ (2026-06-07)

### 版本历史

| 版本 | 日期 | 主要内容 |
|------|------|---------|
| v1.0.0 | 2026-05-30 | 4学科基础版（微积分/词汇/诗文/马原），33题 |
| v1.1.0 | 2026-06-07 | CET6完整词汇表导入，2983词+47题，A-Z分章 |

### v1.1.0 关键产出

- `english_cet6.json` — 从《大学英语六级词汇表(全)含音标.docx》导入 2983 词
- A-Z 共 25 章，每词含音标+释义
- 47 道选择题（标注词典出处：Cambridge/Oxford/Collins/Merriam-Webster/Longman/Macmillan）
- `CHANGELOG.md` — 完整版本历史
- `docs/CET6_vocabulary_quizzes_part1_AM.md` — A-M 词汇例句+习题文档（30词）
- `docs/CET6_vocabulary_quizzes_part2_NZ.md` — N-Z 词汇例句+习题文档（45词）
- APK: `build\app\outputs\flutter-apk\app-debug.apk` (145.3 MB)

### v1.0.0 已知文件

- 20 个 Dart 源文件（模型/Provider/Widget/Page/Util）
- 4 门课程 JSON（微积分12题/词汇→v1.1升级/诗文6题/马原7题）
- `preview.html` — APP 界面模拟器

## 环境信息

| 组件 | 路径 | 版本 |
|------|------|------|
| Flutter | `E:\flutter\` | 3.44.0 |
| Dart | (随 Flutter) | 3.12.0 |
| Java JDK | `E:\Program Files\Java\jdk-17.0.19+10\` | 17.0.19 |
| Android SDK | `E:\Android\` | 34/35/36 |
| VS Build Tools | `E:\VisualStudio\BuildTools\` | 2022 (MSVC 19.44) |
| NDK | `E:\Android\ndk\28.2.13676358\` | 28.2 |

## 构建命令

```powershell
$env:JAVA_HOME = "E:\Program Files\Java\jdk-17.0.19+10"
$env:ANDROID_HOME = "E:\Android"
$env:Path = "$env:JAVA_HOME\bin;E:\flutter\bin;" + $env:Path
cd "E:\.Claude Code Project\3.knowledge-app\knowledge_app"
flutter build apk --debug
```

## 数据源

- CET6词汇表: `C:\Users\hasee\Downloads\大学英语六级词汇表(全)含音标.docx`
- 解析脚本: `build_cet6_json.js` (Node.js，含全部75道习题数据)
- 原始提取: `cet6_words_raw.json` (PowerShell ConvertTo-Json)

## 重要注意事项

1. Flutter 必须在 `E:\flutter\` (无空格)
2. Android SDK 在 `E:\Android\` (无空格)
3. 构建必须用 ASCII 联结路径: `E:\.Claude Code Project\3.knowledge-app\knowledge_app`
4. Gradle 镜像：腾讯云 + 阿里云
5. `flutter_math_fex` → `flutter_math_fork`
6. `android.overridePathCheck=true`
7. 所有代码加中文注释
8. 所有软件装 E 盘
