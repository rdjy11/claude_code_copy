# 知识学习 APP 设计规格书

> 版本: v1.0 | 日期: 2026-05-28 | 状态: 待审批

## 1. 产品概述

一款 Android 平台的知识学习 APP，面向高中生和大学本科生，提供学科关键知识点的讲解与课后练习。v1 覆盖数学、语文、英语、政治四门学科，分别对应微积分、必背诗文、CET6 词汇、马克思主义原理四门课程。APP 采用内容驱动通用引擎架构，后续可低成本扩展更多学科和课程。

## 2. 技术选型

| 决策项 | 选型 | 说明 |
|--------|------|------|
| 开发框架 | Flutter | 跨平台潜力，Material Design 组件丰富 |
| 编程语言 | Dart | Flutter 原生语言 |
| 状态管理 | Provider + ChangeNotifier | 官方推荐，轻量，适合中等复杂度 |
| 内容存储 | 本地 JSON 文件 | 零运维，离线可用，体积最小 |
| 进度持久化 | Hive | 轻量 NoSQL，Flutter 原生支持 |
| 内容格式 | Markdown + LaTeX | 支持公式、表格、富文本 |
| 目标平台 | Android | v1 聚焦 Android |
| minSdkVersion | 21 (Android 5.0) | 覆盖 98%+ 活跃设备 |

## 3. 架构设计：内容驱动通用引擎

### 3.1 架构概览

```
┌──────────────────────────────────┐
│          UI 层 (Pages + Widgets) │
│  HomePage / SubjectPage /        │
│  StudyPage / ProgressPage        │
├──────────────────────────────────┤
│       状态管理层 (Provider)       │
│  CourseProvider / ProgressProvider│
│  QuizSessionProvider             │
├──────────────────────────────────┤
│        数据模型层 (Models)        │
│  Course / Chapter / Section /    │
│  KnowledgePoint / Quiz / Progress│
├──────────────────────────────────┤
│        数据访问层                  │
│  JsonLoader (assets) /           │
│  HiveBox (local storage)         │
└──────────────────────────────────┘
```

核心原则：APP 是通用渲染引擎，学科差异由数据文件定义，新增学科/课程只需新增 JSON 数据文件，无需修改代码。

### 3.2 数据模型

#### 文件组织

```
assets/content/
  math_calculus.json       # 数学-微积分（三级结构）
  english_cet6.json         # 英语-CET6词汇（二级结构）
  chinese_poetry.json       # 语文-必背诗文（二级结构）
  politics_marxism.json     # 政治-马原（三级结构）
```

#### 统一 Schema

```json
{
  "course_id": "string",
  "course_name": "string",
  "subject_id": "string",
  "structure_type": "hierarchical | flat",
  "chapters": [
    {
      "id": "string",
      "title": "string",
      "sections": [
        {
          "id": "string",
          "title": "string",
          "knowledge_points": [
            {
              "id": "string",
              "title": "string",
              "content_type": "markdown",
              "content": "string (Markdown with LaTeX)",
              "key_concepts": ["string"],
              "quizzes": [
                {
                  "id": "string",
                  "type": "single_choice",
                  "question": "string",
                  "options": [
                    {"key": "A", "text": "string"}
                  ],
                  "answer": "A",
                  "explanation": "string"
                }
              ]
            }
          ]
        }
      ],
      "knowledge_points": []
    }
  ]
}
```

**结构规则**：
- `hierarchical`（微积分、马原）：Chapter → Section → KnowledgePoint，`sections` 有值，`chapters[].knowledge_points` 为空
- `flat`（词汇、诗文）：Chapter 作为分类容器，直接包含 KnowledgePoint，`sections` 为空，`chapters[].knowledge_points` 有值

**题型扩展预留**：`Quiz.type` 字段使用枚举值，v1 仅 `single_choice`，后续可扩展 `multi_choice` / `fill_blank` / `short_answer`。

### 3.3 页面架构 & 导航流

```
HomePage ─────────────────────────────────────────────┐
  │ 学科入口卡片 × 4 + 全局进度环                       │
  │                                                    │
  ├─ push ─► SubjectPage                               │
  │            │ 课程列表 + 章节树                      │
  │            │                                        │
  │            └─ push ─► StudyPage                    │
  │                         │ 知识讲解 (Markdown)       │
  │                         │ + 课后练习 (选择题)       │
  │                         │ + 结果弹窗 (BottomSheet)  │
  │                                                    │
  └─ BottomTab ─► ProgressPage                         │
                   学习进度总览                          │
```

| 页面 | 职责 | 关键 Widget |
|------|------|------------|
| `HomePage` | 4 学科入口 + 总体进度环 | `SubjectCard`, `ProgressRing` |
| `SubjectPage` | 单学科课程列表 + 章节树 | `CourseHeader`, `ChapterTree` |
| `StudyPage` | 知识讲解 + 答题 | `MarkdownView`, `QuizCard`, `ResultSheet` |
| `ProgressPage` | 全科学习统计 | `ProgressList` |

**StudyPage 交互细节**：
- 知识讲解区可滚动，支持 Markdown 渲染（含 LaTeX 数学公式）
- 关键概念以 Chip 标签形式展示
- 题目一题一屏，点击选项高亮，点击"提交"弹出 BottomSheet 展示结果（对/错 + 正确答案 + 解析）
- 知识点间通过底部"上一知识点/下一知识点"按钮切换

### 3.4 状态管理

```
MultiProvider
  ├── CourseProvider        # 课程内容加载 & 缓存（全 APP 生命周期）
  ├── ProgressProvider      # 学习进度 & 答题记录（全 APP 生命周期，Hive 持久化）
  └── QuizSessionProvider   # 当前答题会话（StudyPage 作用域）
```

| Provider | 暴露方法 | 说明 |
|----------|---------|------|
| `CourseProvider` | `loadCourse(id)`, `getCourse(id)`, `courses` | JSON → Model 解析，内存缓存 |
| `ProgressProvider` | `markKpComplete(kpId)`, `recordAnswer(qId, answer)`, `getSubjectStats(subjId)` | Hive 读写 |
| `QuizSessionProvider` | `selectAnswer(key)`, `submit()`, `nextQuestion()`, `currentIndex` | 临时状态，离开 StudyPage 即销毁 |

### 3.5 进度追踪

**持久化 Model**：

```dart
class KpProgress {
  final String kpId;       // 知识点 ID
  bool completed;           // 讲解已读
  int quizTotal;            // 该知识点总题数
  int quizCorrect;          // 答对数
  DateTime lastStudy;       // 最后学习时间
}

class QuizRecord {
  final String quizId;      // 题目 ID
  final String userAnswer;  // 用户选项 key
  final bool correct;
  final DateTime timestamp;
}
```

**统计公式**（实时计算，不持久化冗余字段）：
- 学科完成度 = 已学知识点数 / 总知识点数
- 学科正确率 = 正确答题数 / 总答题数
- 全局完成度 = 所有学科已学知识点 / 所有学科总知识点

### 3.6 依赖清单

```yaml
dependencies:
  flutter_markdown: ^0.6.0     # Markdown 渲染
  flutter_math_fex: ^0.2.0     # LaTeX 公式渲染
  provider: ^6.1.0             # 状态管理
  hive: ^2.2.3                 # 本地持久化
  hive_flutter: ^1.1.0         # Hive Flutter 适配
  flutter_svg: ^2.0.0          # SVG 图标支持
```

## 4. 非功能需求

| 需求 | 标准 |
|------|------|
| 离线运行 | 全部功能离线可用 |
| 首屏加载 | < 2 秒（冷启动到首页可交互） |
| 内容更新 | 无需应用商店发版，支持 JSON 文件热更新（可选：后续版本） |
| 扩展性 | 新增学科 ≤ 新增 1 个 JSON 文件 + assets 注册，无代码改动 |
| 新增题型 | ≤ 新增答题 Widget + Quiz 枚举值，无需改其他代码 |
| minSdkVersion | Android 5.0 (API 21) |

## 5. 项目路径

```
E:\.Claude Code Project\3.知识学习APP_20260528\
  ├── docs/superpowers/specs/   # 设计文档
  ├── knowledge_app/            # Flutter 项目根目录
  └── assets/content/           # 课程内容 JSON 文件
```
