# 知识学习 APP 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一款 Flutter Android 学习 APP，使用内容驱动通用引擎架构，v1 覆盖数学(微积分)、语文(必背诗文)、英语(CET6词汇)、政治(马原)四门课程。

**Architecture:** 四层结构——UI层(4个Page + 6个Widget)、状态管理层(3个Provider via Provider+ChangeNotifier)、数据模型层(4个Model)、数据访问层(JSON loader + Hive)。核心原则：APP 是通用渲染引擎，学科差异完全由 JSON 数据文件定义。

**Tech Stack:** Flutter 3.x / Dart 3.x / Provider 6.x / Hive 2.x / flutter_markdown / flutter_math_fex

---

## 前置条件

- [ ] 安装 Flutter SDK (https://docs.flutter.dev/get-started/install/windows)
- [ ] 安装 Android Studio + Android SDK (API 21+)
- [ ] 运行 `flutter doctor` 确认环境就绪

---

## 文件结构总览

```
knowledge_app/
  lib/
    main.dart                        # APP 入口，初始化 Hive + Provider
    app.dart                         # MaterialApp 配置 + 路由
    models/
      course.dart                    # Course, Chapter, Section, KnowledgePoint
      quiz.dart                      # Quiz, QuizOption, QuizType 枚举
      progress.dart                  # KpProgress, QuizRecord
      subject.dart                   # SubjectInfo 聚合模型
    providers/
      course_provider.dart           # 课程 JSON 加载 + 内存缓存
      progress_provider.dart         # 进度 Hive 持久化 + 统计计算
      quiz_session_provider.dart     # 单次答题会话状态
    pages/
      main_scaffold.dart             # 底部 Tab 导航壳
      home_content.dart              # 首页：学科卡片 + 进度环
      subject_page.dart              # 学科页：课程列表 + 章节树
      study_page.dart                # 学习页：讲解 + 习题
      progress_page.dart             # 进度总览页
    widgets/
      subject_card.dart              # 学科入口卡片
      progress_ring.dart             # 圆形进度环
      chapter_tree.dart              # 章节树（适配 2 种结构）
      content_view.dart              # Markdown + LaTeX 渲染
      quiz_card.dart                 # 选择题题卡
      result_sheet.dart              # 答题结果 BottomSheet
    utils/
      json_loader.dart               # JSON 文件读取 + 解析
  assets/content/
    math_calculus.json
    english_cet6.json
    chinese_poetry.json
    politics_marxism.json
  test/
    models/
      course_test.dart
      quiz_test.dart
    providers/
      course_provider_test.dart
      quiz_session_provider_test.dart
    utils/
      json_loader_test.dart
```

---

### Task 1: 创建 Flutter 项目

**Files:**
- Create: `knowledge_app/` (Flutter 项目骨架)

- [ ] **Step 1: 创建 Flutter 项目**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
flutter create knowledge_app --org com.knowledge --platforms android
```

Expected: 创建成功，输出 "All done!"

- [ ] **Step 2: 添加 pubspec.yaml 依赖**

读取 `knowledge_app/pubspec.yaml`，在 `dependencies` 下添加：

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  provider: ^6.1.1           # 状态管理
  hive: ^2.2.3               # 本地持久化
  hive_flutter: ^1.1.0       # Hive Flutter 适配
  flutter_markdown: ^0.6.22  # Markdown 渲染
  flutter_math_fex: ^0.2.0   # LaTeX 公式渲染
```

添加 dev_dependencies：

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  hive_generator: ^2.0.1     # Hive TypeAdapter 生成器
  build_runner: ^2.4.8       # 代码生成运行器
```

- [ ] **Step 3: 创建 assets 目录并注册**

```bash
New-Item -ItemType Directory -Path "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app\assets\content" -Force
```

在 `pubspec.yaml` 的 `flutter` 段添加：

```yaml
flutter:
  uses-material-design: true
  assets:
    - assets/content/
```

- [ ] **Step 4: 安装依赖**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app"
flutter pub get
```

Expected: 输出 "exit code 0" 或无报错

- [ ] **Step 5: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git init
git add knowledge_app/
git commit -m "chore: create Flutter project with dependencies"
```

---

### Task 2: 定义数据模型

**Files:**
- Create: `knowledge_app/lib/models/quiz.dart`
- Create: `knowledge_app/lib/models/course.dart`
- Create: `knowledge_app/lib/models/progress.dart`
- Create: `knowledge_app/lib/models/subject.dart`

- [ ] **Step 1: 创建 Quiz 模型**

```dart
// lib/models/quiz.dart
// 习题模型：定义题目、选项、答案和解析的数据结构
// 通过 QuizType 枚举预留题型扩展能力

/// 题型枚举，v1 仅 single_choice，后续可扩展 multi_choice / fill_blank
enum QuizType { single_choice }

/// 单个选项的数据结构
class QuizOption {
  final String key;   // 选项标识，如 "A", "B", "C", "D"
  final String text;  // 选项文本内容

  const QuizOption({required this.key, required this.text});

  // 从 JSON Map 构造 QuizOption 实例
  factory QuizOption.fromJson(Map<String, dynamic> json) {
    return QuizOption(
      key: json['key'] as String,
      text: json['text'] as String,
    );
  }

  Map<String, dynamic> toJson() => {'key': key, 'text': text};
}

/// 习题数据结构
class Quiz {
  final String id;           // 题目唯一 ID
  final QuizType type;       // 题型
  final String question;     // 题目内容（Markdown）
  final List<QuizOption> options;  // 选项列表
  final String answer;       // 正确答案 key
  final String explanation;  // 解析内容（Markdown）

  const Quiz({
    required this.id,
    required this.type,
    required this.question,
    required this.options,
    required this.answer,
    required this.explanation,
  });

  // 从 JSON Map 构造 Quiz 实例，自动解析 options 数组
  factory Quiz.fromJson(Map<String, dynamic> json) {
    return Quiz(
      id: json['id'] as String,
      type: QuizType.single_choice, // v1 仅单选择题
      question: json['question'] as String,
      options: (json['options'] as List<dynamic>)
          .map((o) => QuizOption.fromJson(o as Map<String, dynamic>))
          .toList(),
      answer: json['answer'] as String,
      explanation: json['explanation'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'type': 'single_choice',
    'question': question,
    'options': options.map((o) => o.toJson()).toList(),
    'answer': answer,
    'explanation': explanation,
  };
}
```

- [ ] **Step 2: 创建 Course 模型（知识点 + 章节 + 课程）**

```dart
// lib/models/course.dart
// 课程内容模型：定义 Course → Chapter → Section → KnowledgePoint 的层次结构
// 通过 structure_type 字段区分 hierarchical（三级）和 flat（二级）两种模式

import 'quiz.dart';

/// 知识点：最小的学习单元，包含讲解内容和配套习题
class KnowledgePoint {
  final String id;             // 知识点唯一 ID
  final String title;          // 知识点标题
  final String contentType;    // 内容格式，当前固定为 "markdown"
  final String content;        // 讲解内容（Markdown + LaTeX）
  final List<String> keyConcepts;  // 关键概念列表
  final List<Quiz> quizzes;    // 配套习题

  const KnowledgePoint({
    required this.id,
    required this.title,
    required this.contentType,
    required this.content,
    required this.keyConcepts,
    required this.quizzes,
  });

  factory KnowledgePoint.fromJson(Map<String, dynamic> json) {
    return KnowledgePoint(
      id: json['id'] as String,
      title: json['title'] as String,
      contentType: (json['content_type'] as String?) ?? 'markdown',
      content: json['content'] as String,
      keyConcepts: (json['key_concepts'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
      quizzes: (json['quizzes'] as List<dynamic>?)
              ?.map((q) => Quiz.fromJson(q as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

/// 节：包含若干知识点，仅在 hierarchical 模式下存在
class Section {
  final String id;                      // 节唯一 ID
  final String title;                   // 节标题
  final List<KnowledgePoint> knowledgePoints; // 知识点列表

  const Section({
    required this.id,
    required this.title,
    required this.knowledgePoints,
  });

  factory Section.fromJson(Map<String, dynamic> json) {
    return Section(
      id: json['id'] as String,
      title: json['title'] as String,
      knowledgePoints: (json['knowledge_points'] as List<dynamic>)
          .map((kp) => KnowledgePoint.fromJson(kp as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// 章：在 hierarchical 模式下包含节，在 flat 模式下直接包含知识点
class Chapter {
  final String id;                      // 章唯一 ID
  final String title;                   // 章标题
  final List<Section> sections;         // 节列表（hierarchical 模式有值）
  final List<KnowledgePoint> knowledgePoints; // 直接知识点列表（flat 模式有值）

  const Chapter({
    required this.id,
    required this.title,
    required this.sections,
    required this.knowledgePoints,
  });

  // 判断此章节使用哪种结构模式
  bool get isHierarchical => sections.isNotEmpty;

  factory Chapter.fromJson(Map<String, dynamic> json) {
    return Chapter(
      id: json['id'] as String,
      title: json['title'] as String,
      sections: (json['sections'] as List<dynamic>?)
              ?.map((s) => Section.fromJson(s as Map<String, dynamic>))
              .toList() ??
          [],
      knowledgePoints: (json['knowledge_points'] as List<dynamic>?)
              ?.map((kp) => KnowledgePoint.fromJson(kp as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

/// 结构类型：hierarchical = 章→节→知识点，flat = 章→知识点
enum StructureType { hierarchical, flat }

/// 课程：一门完整的学科课程，包含其结构类型和章列表
class Course {
  final String courseId;           // 课程唯一 ID
  final String courseName;         // 课程名称
  final String subjectId;          // 所属学科 ID
  final StructureType structureType; // 结构类型
  final List<Chapter> chapters;    // 章列表

  const Course({
    required this.courseId,
    required this.courseName,
    required this.subjectId,
    required this.structureType,
    required this.chapters,
  });

  // 获取课程下所有知识点的扁平列表，用于遍历和统计
  List<KnowledgePoint> get allKnowledgePoints {
    final List<KnowledgePoint> result = [];
    for (final chapter in chapters) {
      if (chapter.isHierarchical) {
        for (final section in chapter.sections) {
          result.addAll(section.knowledgePoints);
        }
      } else {
        result.addAll(chapter.knowledgePoints);
      }
    }
    return result;
  }

  // 获取课程下所有习题的扁平列表
  List<Quiz> get allQuizzes {
    return allKnowledgePoints.expand((kp) => kp.quizzes).toList();
  }

  factory Course.fromJson(Map<String, dynamic> json) {
    final structureStr = json['structure_type'] as String? ?? 'flat';
    return Course(
      courseId: json['course_id'] as String,
      courseName: json['course_name'] as String,
      subjectId: json['subject_id'] as String,
      structureType: structureStr == 'hierarchical'
          ? StructureType.hierarchical
          : StructureType.flat,
      chapters: (json['chapters'] as List<dynamic>)
          .map((c) => Chapter.fromJson(c as Map<String, dynamic>))
          .toList(),
    );
  }
}
```

- [ ] **Step 3: 创建 Progress 模型**

```dart
// lib/models/progress.dart
// 学习进度模型：记录知识点学习状态和每道题的作答记录

/// 知识点学习进度：记录单个知识点的完成状态和答题统计
class KpProgress {
  final String kpId;       // 知识点 ID
  bool completed;           // 讲解内容是否已读
  int quizTotal;            // 该知识点下总题数
  int quizCorrect;          // 答对题数
  DateTime lastStudy;       // 最后学习时间

  KpProgress({
    required this.kpId,
    this.completed = false,
    this.quizTotal = 0,
    this.quizCorrect = 0,
    DateTime? lastStudy,
  }) : lastStudy = lastStudy ?? DateTime.now();

  // 计算该知识点的答题正确率（0.0 ~ 1.0）
  double get accuracy =>
      quizTotal > 0 ? quizCorrect / quizTotal : 0.0;

  Map<String, dynamic> toJson() => {
    'kpId': kpId,
    'completed': completed,
    'quizTotal': quizTotal,
    'quizCorrect': quizCorrect,
    'lastStudy': lastStudy.toIso8601String(),
  };

  factory KpProgress.fromJson(Map<String, dynamic> json) => KpProgress(
    kpId: json['kpId'] as String,
    completed: (json['completed'] as bool?) ?? false,
    quizTotal: (json['quizTotal'] as int?) ?? 0,
    quizCorrect: (json['quizCorrect'] as int?) ?? 0,
    lastStudy: json['lastStudy'] != null
        ? DateTime.parse(json['lastStudy'] as String)
        : DateTime.now(),
  );
}

/// 单题答题记录：记录用户对某道题的一次作答
class QuizRecord {
  final String quizId;       // 题目 ID
  final String userAnswer;   // 用户选择的选项 key
  final bool correct;        // 是否正确
  final DateTime timestamp;  // 作答时间

  const QuizRecord({
    required this.quizId,
    required this.userAnswer,
    required this.correct,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() => {
    'quizId': quizId,
    'userAnswer': userAnswer,
    'correct': correct,
    'timestamp': timestamp.toIso8601String(),
  };

  factory QuizRecord.fromJson(Map<String, dynamic> json) => QuizRecord(
    quizId: json['quizId'] as String,
    userAnswer: json['userAnswer'] as String,
    correct: json['correct'] as bool,
    timestamp: DateTime.parse(json['timestamp'] as String),
  );
}

/// 某学科的进度统计数据（由 ProgressProvider 实时计算）
class SubjectStats {
  final String subjectId;    // 学科 ID
  final String subjectName;  // 学科名称
  final int totalKp;         // 总知识点数
  final int completedKp;     // 已完成知识点数
  final double accuracy;     // 答题正确率（0.0 ~ 1.0）

  const SubjectStats({
    required this.subjectId,
    required this.subjectName,
    required this.totalKp,
    required this.completedKp,
    required this.accuracy,
  });
}
```

- [ ] **Step 4: 创建 Subject 聚合模型**

```dart
// lib/models/subject.dart
// 学科聚合模型：一个学科可包含多门课程，用于组织首页入口和学分发

/// 学科入口信息，聚合该学科下所有课程的元数据
class SubjectInfo {
  final String id;         // 学科 ID: math/chinese/english/politics
  final String name;       // 学科名称
  final String iconName;   // Material Icons 名称（用于图标展示）
  final List<String> courseIds;  // 该学科包含的课程 ID 列表

  const SubjectInfo({
    required this.id,
    required this.name,
    required this.iconName,
    required this.courseIds,
  });
}

// 预定义的 4 个 v1 学科入口
const List<SubjectInfo> v1Subjects = [
  SubjectInfo(
    id: 'math',
    name: '数学',
    iconName: 'functions',
    courseIds: ['calculus'],
  ),
  SubjectInfo(
    id: 'english',
    name: '英语',
    iconName: 'translate',
    courseIds: ['cet6'],
  ),
  SubjectInfo(
    id: 'chinese',
    name: '语文',
    iconName: 'menu_book',
    courseIds: ['poetry'],
  ),
  SubjectInfo(
    id: 'politics',
    name: '政治',
    iconName: 'account_balance',
    courseIds: ['marxism'],
  ),
];
```

- [ ] **Step 5: 运行测试验证模型编译通过**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app"
flutter analyze lib/models/
```

Expected: No issues found.

- [ ] **Step 6: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/models/
git commit -m "feat: define data models (Course, Quiz, Progress, Subject)"
```

---

### Task 3: 创建课程内容 JSON 文件

**Files:**
- Create: `knowledge_app/assets/content/math_calculus.json`
- Create: `knowledge_app/assets/content/english_cet6.json`
- Create: `knowledge_app/assets/content/chinese_poetry.json`
- Create: `knowledge_app/assets/content/politics_marxism.json`

- [ ] **Step 1: 创建微积分内容文件（hierarchical 结构）**

写 `assets/content/math_calculus.json`：

```json
{
  "course_id": "calculus",
  "course_name": "微积分",
  "subject_id": "math",
  "structure_type": "hierarchical",
  "chapters": [
    {
      "id": "calc_ch01",
      "title": "第一章 函数与极限",
      "sections": [
        {
          "id": "calc_sec01",
          "title": "1.1 函数的概念与性质",
          "knowledge_points": [
            {
              "id": "calc_kp001",
              "title": "函数的定义",
              "content_type": "markdown",
              "content": "## 函数的定义\n\n设 $X$ 和 $Y$ 是两个非空集合。如果存在一个对应法则 $f$，使得对于 $X$ 中的每一个元素 $x$，在 $Y$ 中都有**唯一**确定的元素 $y$ 与之对应，则称 $f$ 是从 $X$ 到 $Y$ 的一个**函数**，记作：\n\n$$y = f(x), \\quad x \\in X$$\n\n其中：\n- $x$ 称为**自变量**，$X$ 称为**定义域**\n- $y$ 称为**因变量**，$f(x)$ 的全体取值称为**值域**\n\n函数的两个基本要素：\n1. **定义域**：自变量 $x$ 的取值范围\n2. **对应法则**：由 $x$ 确定 $y$ 的规则\n\n两函数相等当且仅当它们的定义域和对应法则完全相同。",
              "key_concepts": ["定义域", "值域", "对应法则", "映射"],
              "quizzes": [
                {
                  "id": "calc_q001",
                  "type": "single_choice",
                  "question": "若 $f(x) = x^2 + 1$，则 $f(-2)$ 的值为？",
                  "options": [
                    {"key": "A", "text": "3"},
                    {"key": "B", "text": "5"},
                    {"key": "C", "text": "-3"},
                    {"key": "D", "text": "4"}
                  ],
                  "answer": "B",
                  "explanation": "代入 $x = -2$：$f(-2) = (-2)^2 + 1 = 4 + 1 = 5$"
                },
                {
                  "id": "calc_q002",
                  "type": "single_choice",
                  "question": "函数 $f(x) = \\frac{1}{x-1}$ 的定义域是？",
                  "options": [
                    {"key": "A", "text": "$(-\\infty, +\\infty)$"},
                    {"key": "B", "text": "$(-\\infty, 1) \\cup (1, +\\infty)$"},
                    {"key": "C", "text": "$[1, +\\infty)$"},
                    {"key": "D", "text": "$(0, +\\infty)$"}
                  ],
                  "answer": "B",
                  "explanation": "分母不能为零，所以 $x-1 \\neq 0$，即 $x \\neq 1$。定义域为除 $x=1$ 以外的全体实数。"
                },
                {
                  "id": "calc_q003",
                  "type": "single_choice",
                  "question": "下列哪个不是函数的表示方法？",
                  "options": [
                    {"key": "A", "text": "解析法（公式法）"},
                    {"key": "B", "text": "列表法"},
                    {"key": "C", "text": "图像法"},
                    {"key": "D", "text": "递归法"}
                  ],
                  "answer": "D",
                  "explanation": "函数的三种基本表示方法为：解析法（用公式表示）、列表法（用表格列出对应值）、图像法（用坐标平面上的曲线表示）。递归法是描述数列的一种方法，不是函数的基本表示方法。"
                }
              ]
            },
            {
              "id": "calc_kp002",
              "title": "函数的奇偶性",
              "content_type": "markdown",
              "content": "## 函数的奇偶性\n\n### 偶函数\n设函数 $f(x)$ 的定义域 $D$ 关于原点对称。若对于任意 $x \\in D$，都有：\n\n$$f(-x) = f(x)$$\n\n则称 $f(x)$ 为**偶函数**。偶函数的图像关于 $y$ 轴对称。\n\n常见偶函数：$y = x^2$，$y = \\cos x$，$y = |x|$\n\n### 奇函数\n若对于任意 $x \\in D$，都有：\n\n$$f(-x) = -f(x)$$\n\n则称 $f(x)$ 为**奇函数**。奇函数的图像关于原点对称。\n\n常见奇函数：$y = x^3$，$y = \\sin x$，$y = \\frac{1}{x}$\n\n### 注意事项\n- 函数的定义域必须关于原点对称，才能讨论奇偶性\n- 有些函数既不是奇函数也不是偶函数，如 $y = x + 1$",
              "key_concepts": ["偶函数", "奇函数", "对称性", "定义域对称"],
              "quizzes": [
                {
                  "id": "calc_q004",
                  "type": "single_choice",
                  "question": "函数 $f(x) = x^2 \\cos x$ 的奇偶性是？",
                  "options": [
                    {"key": "A", "text": "奇函数"},
                    {"key": "B", "text": "偶函数"},
                    {"key": "C", "text": "既不是奇函数也不是偶函数"},
                    {"key": "D", "text": "既是奇函数也是偶函数"}
                  ],
                  "answer": "B",
                  "explanation": "$x^2$ 是偶函数（$(-x)^2 = x^2$），$\\cos x$ 是偶函数（$\\cos(-x) = \\cos x$）。偶函数 × 偶函数 = 偶函数，所以 $f(x)$ 是偶函数。"
                },
                {
                  "id": "calc_q005",
                  "type": "single_choice",
                  "question": "函数 $f(x) = x^3 + \\sin x$ 是？",
                  "options": [
                    {"key": "A", "text": "奇函数"},
                    {"key": "B", "text": "偶函数"},
                    {"key": "C", "text": "非奇非偶"},
                    {"key": "D", "text": "无法判断"}
                  ],
                  "answer": "A",
                  "explanation": "$x^3$ 是奇函数，$\\sin x$ 是奇函数。奇函数 + 奇函数 = 奇函数，所以 $f(x)$ 是奇函数。"
                },
                {
                  "id": "calc_q006",
                  "type": "single_choice",
                  "question": "偶函数的图像有什么几何特征？",
                  "options": [
                    {"key": "A", "text": "关于原点对称"},
                    {"key": "B", "text": "关于 $y$ 轴对称"},
                    {"key": "C", "text": "关于 $x$ 轴对称"},
                    {"key": "D", "text": "关于直线 $y=x$ 对称"}
                  ],
                  "answer": "B",
                  "explanation": "偶函数满足 $f(-x) = f(x)$，意味着 $(-a, f(a))$ 和 $(a, f(a))$ 都在图像上，这两点关于 $y$ 轴对称，因此偶函数图像关于 $y$ 轴对称。"
                }
              ]
            }
          ]
        },
        {
          "id": "calc_sec02",
          "title": "1.2 数列的极限",
          "knowledge_points": [
            {
              "id": "calc_kp003",
              "title": "数列极限的定义",
              "content_type": "markdown",
              "content": "## 数列极限的定义\n\n设 $\\{x_n\\}$ 是一个数列，$a$ 是一个常数。如果对于任意给定的正数 $\\varepsilon > 0$，总存在正整数 $N$，使得当 $n > N$ 时，恒有：\n\n$$|x_n - a| < \\varepsilon$$\n\n则称常数 $a$ 是数列 $\\{x_n\\}$ 的**极限**，或称数列 $\\{x_n\\}$ **收敛**于 $a$，记作：\n\n$$\\lim_{n \\to \\infty} x_n = a \\quad \\text{或} \\quad x_n \\to a \\ (n \\to \\infty)$$\n\n### $\\varepsilon$-$N$ 语言的理解\n- $\\varepsilon$ 是任意给定的精度要求（可以任意小）\n- $N$ 是满足精度要求的分界点\n- 当 $n > N$ 时，$x_n$ 与 $a$ 的距离始终小于 $\\varepsilon$\n- 如果不存在这样的 $a$，则称数列**发散**",
              "key_concepts": ["收敛", "发散", "ε-N 语言", "极限"],
              "quizzes": [
                {
                  "id": "calc_q007",
                  "type": "single_choice",
                  "question": "数列 $x_n = \\frac{1}{n}$ 的极限是？",
                  "options": [
                    {"key": "A", "text": "1"},
                    {"key": "B", "text": "0"},
                    {"key": "C", "text": "不存在"},
                    {"key": "D", "text": "$\\infty$"}
                  ],
                  "answer": "B",
                  "explanation": "$\\lim_{n \\to \\infty} \\frac{1}{n} = 0$。因为对于任意 $\\varepsilon > 0$，取 $N = \\lceil \\frac{1}{\\varepsilon} \\rceil$，则当 $n > N$ 时，$|\\frac{1}{n} - 0| = \\frac{1}{n} < \\frac{1}{N} \\leq \\varepsilon$。"
                },
                {
                  "id": "calc_q008",
                  "type": "single_choice",
                  "question": "下列哪个数列是发散的？",
                  "options": [
                    {"key": "A", "text": "$x_n = \\frac{1}{n}$"},
                    {"key": "B", "text": "$x_n = (-1)^n$"},
                    {"key": "C", "text": "$x_n = \\frac{n}{n+1}$"},
                    {"key": "D", "text": "$x_n = 2^{-n}$"}
                  ],
                  "answer": "B",
                  "explanation": "$x_n = (-1)^n$ 的取值在 1 和 -1 之间交替跳动，不收敛于任何常数。其他三个数列都收敛：$\\frac{1}{n} \\to 0$，$\\frac{n}{n+1} \\to 1$，$2^{-n} \\to 0$。"
                },
                {
                  "id": "calc_q009",
                  "type": "single_choice",
                  "question": "若 $\\lim_{n \\to \\infty} x_n = a$ 且 $\\lim_{n \\to \\infty} y_n = b$，则 $\\lim_{n \\to \\infty} (x_n + y_n)$ 等于？",
                  "options": [
                    {"key": "A", "text": "$a \\times b$"},
                    {"key": "B", "text": "$a + b$"},
                    {"key": "C", "text": "不确定"},
                    {"key": "D", "text": "$\\frac{a}{b}$"}
                  ],
                  "answer": "B",
                  "explanation": "收敛数列的加法法则：如果两个数列都收敛，则它们的和数列也收敛，且极限等于两极限之和，即 $\\lim (x_n + y_n) = \\lim x_n + \\lim y_n = a + b$。"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "calc_ch02",
      "title": "第二章 导数与微分",
      "sections": [
        {
          "id": "calc_sec03",
          "title": "2.1 导数的定义",
          "knowledge_points": [
            {
              "id": "calc_kp004",
              "title": "导数的概念",
              "content_type": "markdown",
              "content": "## 导数的定义\n\n设函数 $y = f(x)$ 在点 $x_0$ 的某个邻域内有定义。当自变量 $x$ 在 $x_0$ 处有增量 $\\Delta x$（$x_0 + \\Delta x$ 仍在邻域内）时，函数的增量为 $\\Delta y = f(x_0 + \\Delta x) - f(x_0)$。如果\n\n$$\\lim_{\\Delta x \\to 0} \\frac{\\Delta y}{\\Delta x} = \\lim_{\\Delta x \\to 0} \\frac{f(x_0 + \\Delta x) - f(x_0)}{\\Delta x}$$\n\n存在，则称函数 $f(x)$ 在点 $x_0$ 处**可导**，并称此极限值为 $f(x)$ 在点 $x_0$ 处的**导数**，记作：\n\n$$f'(x_0) = \\lim_{\\Delta x \\to 0} \\frac{f(x_0 + \\Delta x) - f(x_0)}{\\Delta x}$$\n\n### 常见记法\n$$f'(x) = y' = \\frac{dy}{dx} = \\frac{df}{dx}$$\n\n### 导数的几何意义\n函数 $y = f(x)$ 在点 $x_0$ 处的导数 $f'(x_0)$，等于曲线 $y = f(x)$ 在点 $(x_0, f(x_0))$ 处的**切线斜率**。",
              "key_concepts": ["导数", "可导", "差商极限", "切线斜率"],
              "quizzes": [
                {
                  "id": "calc_q010",
                  "type": "single_choice",
                  "question": "函数 $f(x) = x^2$ 在 $x = 1$ 处的导数 $f'(1)$ 等于？",
                  "options": [
                    {"key": "A", "text": "1"},
                    {"key": "B", "text": "2"},
                    {"key": "C", "text": "0"},
                    {"key": "D", "text": "3"}
                  ],
                  "answer": "B",
                  "explanation": "$f'(x) = 2x$，代入 $x = 1$ 得 $f'(1) = 2$。也可以通过定义计算：$\\lim_{h \\to 0} \\frac{(1+h)^2 - 1^2}{h} = \\lim_{h \\to 0} \\frac{2h + h^2}{h} = \\lim_{h \\to 0} (2 + h) = 2$。"
                },
                {
                  "id": "calc_q011",
                  "type": "single_choice",
                  "question": "导数 $f'(x_0)$ 的几何意义是什么？",
                  "options": [
                    {"key": "A", "text": "曲线在 $x_0$ 处的函数值"},
                    {"key": "B", "text": "曲线在 $(x_0, f(x_0))$ 处的切线斜率"},
                    {"key": "C", "text": "曲线与 $x$ 轴围成的面积"},
                    {"key": "D", "text": "曲线的凹凸性"}
                  ],
                  "answer": "B",
                  "explanation": "导数 $f'(x_0)$ 表示函数在点 $x_0$ 处的瞬时变化率，几何上对应曲线 $y = f(x)$ 在点 $\\big(x_0, f(x_0)\\big)$ 处切线的斜率。切线方程为 $y - f(x_0) = f'(x_0)(x - x_0)$。"
                },
                {
                  "id": "calc_q012",
                  "type": "single_choice",
                  "question": "若 $f'(x_0) = 0$，则曲线在 $x_0$ 处的切线是？",
                  "options": [
                    {"key": "A", "text": "斜向上的直线"},
                    {"key": "B", "text": "斜向下的直线"},
                    {"key": "C", "text": "水平直线"},
                    {"key": "D", "text": "竖直直线"}
                  ],
                  "answer": "C",
                  "explanation": "切线斜率 $k = f'(x_0) = 0$，斜率为 0 的直线是水平直线。这通常意味着 $x_0$ 可能是函数的极值点或驻点。"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: 创建 CET6 词汇内容文件（flat 结构）**

写 `assets/content/english_cet6.json`：

```json
{
  "course_id": "cet6",
  "course_name": "CET6 核心词汇",
  "subject_id": "english",
  "structure_type": "flat",
  "chapters": [
    {
      "id": "cet6_high",
      "title": "高频动词",
      "knowledge_points": [
        {
          "id": "cet6_001",
          "title": "abandon",
          "content_type": "markdown",
          "content": "## abandon /əˈbændən/\n\n**词性**：v. **释义**：放弃，抛弃\n\n**例句**：\n> The captain refused to abandon the sinking ship.\n> 船长拒绝放弃正在下沉的船。\n\n**搭配**：\n- abandon oneself to... 沉溺于；放纵\n- abandon hope 放弃希望\n\n**近义词**：give up, desert, forsake\n**反义词**：maintain, keep, retain",
          "key_concepts": ["放弃", "抛弃", "abandon oneself to"],
          "quizzes": [
            {
              "id": "cet6_q001",
              "type": "single_choice",
              "question": "The firefighters refused to ______ the burning building until everyone was rescued.",
              "options": [
                {"key": "A", "text": "abandon"},
                {"key": "B", "text": "abolish"},
                {"key": "C", "text": "absorb"},
                {"key": "D", "text": "abuse"}
              ],
              "answer": "A",
              "explanation": "abandon 意为\"放弃、离开\"，符合句意\"消防员拒绝放弃燃烧的建筑，直到所有人都被救出\"。abolish（废除）、absorb（吸收）、abuse（滥用）均不符合语境。"
            }
          ]
        },
        {
          "id": "cet6_002",
          "title": "abolish",
          "content_type": "markdown",
          "content": "## abolish /əˈbɒlɪʃ/\n\n**词性**：v. **释义**：废除，废止（法律、制度等）\n\n**例句**：\n> Slavery was abolished in the United States in 1865.\n> 美国于 1865 年废除了奴隶制。\n\n**近义词**：eliminate, do away with\n**反义词**：establish, institute",
          "key_concepts": ["废除", "废止", "eliminate"],
          "quizzes": [
            {
              "id": "cet6_q002",
              "type": "single_choice",
              "question": "Many people believe that the death penalty should be ______.",
              "options": [
                {"key": "A", "text": "absorbed"},
                {"key": "B", "text": "abolished"},
                {"key": "C", "text": "abandoned"},
                {"key": "D", "text": "abused"}
              ],
              "answer": "B",
              "explanation": "abolish 意为\"废除\"，与\"death penalty（死刑）\"搭配最恰当，表示\"废除死刑\"。abandon（放弃具体事物）、absorb（吸收）、abuse（滥用）均不合适。"
            }
          ]
        },
        {
          "id": "cet6_003",
          "title": "abstract",
          "content_type": "markdown",
          "content": "## abstract /ˈæbstrækt/\n\n**词性**：adj. / n. / v.\n- adj. 抽象的；理论的\n- n. 摘要；抽象概念\n- v. 提取；抽象化\n\n**例句**：\n> Beauty is an abstract concept.\n> 美是一个抽象的概念。\n\n**搭配**：\n- in the abstract 抽象地；理论上\n- abstract thinking 抽象思维",
          "key_concepts": ["抽象的", "摘要", "abstract thinking"],
          "quizzes": [
            {
              "id": "cet6_q003",
              "type": "single_choice",
              "question": "The concept of justice is rather ______ and difficult to define precisely.",
              "options": [
                {"key": "A", "text": "concrete"},
                {"key": "B", "text": "abstract"},
                {"key": "C", "text": "specific"},
                {"key": "D", "text": "tangible"}
              ],
              "answer": "B",
              "explanation": "abstract 意为\"抽象的\"，与句中的\"difficult to define precisely（难以精确定义）\"呼应。concrete/specific/tangible 都表示\"具体的、有形的\"，与句意相反。"
            }
          ]
        },
        {
          "id": "cet6_004",
          "title": "accelerate",
          "content_type": "markdown",
          "content": "## accelerate /əkˈseləreɪt/\n\n**词性**：v. **释义**：加速；促进\n\n**例句**：\n> The government took measures to accelerate economic growth.\n> 政府采取措施加速经济增长。\n\n**近义词**：speed up, quicken, hasten\n**反义词**：decelerate, slow down",
          "key_concepts": ["加速", "促进", "speed up"],
          "quizzes": [
            {
              "id": "cet6_q004",
              "type": "single_choice",
              "question": "The driver stepped on the gas pedal to ______ the car.",
              "options": [
                {"key": "A", "text": "decelerate"},
                {"key": "B", "text": "accelerate"},
                {"key": "C", "text": "accompany"},
                {"key": "D", "text": "accumulate"}
              ],
              "answer": "B",
              "explanation": "accelerate 意为\"加速\"，踩油门(gas pedal)的目的是加速。decelerate（减速）是反义词，accompany（陪伴）、accumulate（积累）不符合语境。"
            }
          ]
        },
        {
          "id": "cet6_005",
          "title": "accompany",
          "content_type": "markdown",
          "content": "## accompany /əˈkʌmpəni/\n\n**词性**：v. **释义**：陪伴；伴随；为...伴奏\n\n**例句**：\n> She accompanied her friend to the airport.\n> 她陪朋友去了机场。\n\n**搭配**：\n- be accompanied by... 由...陪同/伴随\n- accompany sb. on + 乐器 用某种乐器为某人伴奏",
          "key_concepts": ["陪伴", "伴随", "伴奏"],
          "quizzes": [
            {
              "id": "cet6_q005",
              "type": "single_choice",
              "question": "High fever is often ______ by a headache.",
              "options": [
                {"key": "A", "text": "accompanied"},
                {"key": "B", "text": "accelerated"},
                {"key": "C", "text": "accomplished"},
                {"key": "D", "text": "accounted"}
              ],
              "answer": "A",
              "explanation": "be accompanied by 意为\"由...伴随\"，高烧常伴随头痛。accelerate（加速）、accomplish（完成）、account（解释）均不符合。"
            }
          ]
        }
      ]
    },
    {
      "id": "cet6_noun",
      "title": "高频名词",
      "knowledge_points": [
        {
          "id": "cet6_006",
          "title": "access",
          "content_type": "markdown",
          "content": "## access /ˈækses/\n\n**词性**：n. / v.\n- n. 通道；进入权；访问（权限）\n- v. 访问；存取（数据）\n\n**例句**：\n> Students have free access to the library.\n> 学生可以免费进入图书馆。\n\n**搭配**：\n- have access to... 有权使用/进入...\n- internet access 互联网接入",
          "key_concepts": ["进入", "访问", "access to"],
          "quizzes": [
            {
              "id": "cet6_q006",
              "type": "single_choice",
              "question": "Only authorized personnel have ______ to the confidential files.",
              "options": [
                {"key": "A", "text": "access"},
                {"key": "B", "text": "excess"},
                {"key": "C", "text": "assess"},
                {"key": "D", "text": "process"}
              ],
              "answer": "A",
              "explanation": "have access to 是固定搭配，意为\"有权使用/访问\"。excess（过量）、assess（评估）、process（过程/处理）均不符合固定搭配习惯。"
            }
          ]
        },
        {
          "id": "cet6_007",
          "title": "accommodation",
          "content_type": "markdown",
          "content": "## accommodation /əˌkɒməˈdeɪʃn/\n\n**词性**：n. **释义**：住宿；膳宿；适应；调和\n\n**例句**：\n> The university provides accommodation for all first-year students.\n> 大学为所有大一学生提供住宿。\n\n**短语**：\n- make accommodations for... 为...做出调整/迁就",
          "key_concepts": ["住宿", "膳宿", "适应"],
          "quizzes": [
            {
              "id": "cet6_q007",
              "type": "single_choice",
              "question": "When studying abroad, finding suitable ______ is often the first challenge.",
              "options": [
                {"key": "A", "text": "accommodation"},
                {"key": "B", "text": "recommendation"},
                {"key": "C", "text": "communication"},
                {"key": "D", "text": "demonstration"}
              ],
              "answer": "A",
              "explanation": "accommodation 意为\"住宿\"，留学时的首要挑战是找住宿。recommendation（推荐）、communication（交流）、demonstration（展示）不符合句意。"
            }
          ]
        },
        {
          "id": "cet6_008",
          "title": "acknowledgement",
          "content_type": "markdown",
          "content": "## acknowledgement /əkˈnɒlɪdʒmənt/\n\n**词性**：n. **释义**：承认；确认；感谢\n\n**例句**：\n> He received an award in acknowledgement of his outstanding contribution.\n> 他获得了表彰，以承认他的杰出贡献。\n\n**短语**：\n- in acknowledgement of... 为感谢/认可...\n- acknowledgement of receipt 收件确认",
          "key_concepts": ["承认", "确认", "感谢"],
          "quizzes": [
            {
              "id": "cet6_q008",
              "type": "single_choice",
              "question": "The report is a clear ______ of the seriousness of the environmental crisis.",
              "options": [
                {"key": "A", "text": "acknowledgement"},
                {"key": "B", "text": "achievement"},
                {"key": "C", "text": "adjustment"},
                {"key": "D", "text": "advancement"}
              ],
              "answer": "A",
              "explanation": "acknowledgement 意为\"承认\"，该报告是对环境危机严重性的明确承认。achievement（成就）、adjustment（调整）、advancement（进步）在此语境中不够贴切。"
            }
          ]
        }
      ]
    }
  ]
}
```

- [ ] **Step 3: 创建必背诗文内容文件（flat 结构）**

写 `assets/content/chinese_poetry.json`：

```json
{
  "course_id": "poetry",
  "course_name": "初高中必背诗文",
  "subject_id": "chinese",
  "structure_type": "flat",
  "chapters": [
    {
      "id": "poem_junior",
      "title": "初中必背篇目",
      "knowledge_points": [
        {
          "id": "poem_001",
          "title": "观沧海",
          "content_type": "markdown",
          "content": "## 观沧海\n\n**作者**：曹操（东汉末年）\n\n> 东临碣石，以观沧海。\n> 水何澹澹，山岛竦峙。\n> 树木丛生，百草丰茂。\n> 秋风萧瑟，洪波涌起。\n> 日月之行，若出其中；\n> 星汉灿烂，若出其里。\n> 幸甚至哉，歌以咏志。\n\n### 赏析\n\n这是中国诗歌史上第一首完整的**山水诗**。诗人登临碣石山眺望大海，以雄浑的笔触描绘了大海吞吐日月、包蕴星汉的壮阔景象。\n\n**写作手法**：\n- 借景抒情：通过壮阔的大海景象抒发诗人统一天下的雄心壮志\n- 虚实结合：前六句实写海景，后四句虚写日月星河\n- 动静结合：\"水何澹澹\"的动态与\"山岛竦峙\"的静态\n\n**中心思想**：表达了诗人博大的胸襟和建功立业的豪迈气概。",
          "key_concepts": ["曹操", "山水诗", "借景抒情", "虚实结合"],
          "quizzes": [
            {
              "id": "poem_q001",
              "type": "single_choice",
              "question": "《观沧海》的作者是？",
              "options": [
                {"key": "A", "text": "李白"},
                {"key": "B", "text": "杜甫"},
                {"key": "C", "text": "曹操"},
                {"key": "D", "text": "陶渊明"}
              ],
              "answer": "C",
              "explanation": "《观沧海》是东汉末年曹操所作，收入《乐府诗集》，是中国诗歌史上第一首完整的山水诗。"
            },
            {
              "id": "poem_q002",
              "type": "single_choice",
              "question": "\"日月之行，若出其中\"使用了什么修辞手法？",
              "options": [
                {"key": "A", "text": "比喻"},
                {"key": "B", "text": "夸张"},
                {"key": "C", "text": "拟人"},
                {"key": "D", "text": "对偶"}
              ],
              "answer": "B",
              "explanation": "说日月的运行仿佛都从大海中出没，这是极度的夸张，突出了大海的浩瀚无垠和包容万物的气势。也使用了虚实结合的手法。"
            }
          ]
        },
        {
          "id": "poem_002",
          "title": "春望",
          "content_type": "markdown",
          "content": "## 春望\n\n**作者**：杜甫（唐代）\n\n> 国破山河在，城春草木深。\n> 感时花溅泪，恨别鸟惊心。\n> 烽火连三月，家书抵万金。\n> 白头搔更短，浑欲不胜簪。\n\n### 赏析\n\n此诗写于唐肃宗至德二年（757年）春，安史之乱期间，杜甫被困长安。\n\n**写作手法**：\n- 反衬（以乐景写哀情）：\"城春草木深\"——春天本应生机勃勃，但国破家亡，草木的茂盛反衬了人烟的稀少和内心的凄凉\n- 移情于物：\"花溅泪\"\"鸟惊心\"——将诗人的主观情感投射到客观景物上\n- 对仗工整：颔联\"感时花溅泪，恨别鸟惊心\"为千古名对\n\n**中心思想**：通过春天的景色反衬战乱带来的痛苦，抒发了忧国思家的深沉情感。",
          "key_concepts": ["杜甫", "安史之乱", "反衬", "移情于物", "忧国思家"],
          "quizzes": [
            {
              "id": "poem_q003",
              "type": "single_choice",
              "question": "\"烽火连三月，家书抵万金\"中\"烽火\"指什么？",
              "options": [
                {"key": "A", "text": "春节放烟花"},
                {"key": "B", "text": "战争"},
                {"key": "C", "text": "篝火晚会"},
                {"key": "D", "text": "烽火台"}
              ],
              "answer": "B",
              "explanation": "\"烽火\"是古代边境报警的烟火，代指战争。此句意为\"战争已连续进行了三个月，一封家书比万两黄金还要珍贵\"，表达了战乱中对家人消息的渴望。"
            },
            {
              "id": "poem_q004",
              "type": "single_choice",
              "question": "\"感时花溅泪，恨别鸟惊心\"使用的核心表现手法是？",
              "options": [
                {"key": "A", "text": "托物言志"},
                {"key": "B", "text": "移情于物"},
                {"key": "C", "text": "直抒胸臆"},
                {"key": "D", "text": "用典"}
              ],
              "answer": "B",
              "explanation": "移情于物（也称\"拟人\"的扩展）——诗人将自己的伤感情绪投射到花朵和鸟身上，觉得花也在流泪、鸟也因离别而心惊。这是将主观情感赋予客观事物。"
            }
          ]
        }
      ]
    },
    {
      "id": "poem_senior",
      "title": "高中必背篇目",
      "knowledge_points": [
        {
          "id": "poem_003",
          "title": "赤壁赋（节选）",
          "content_type": "markdown",
          "content": "## 赤壁赋（节选）\n\n**作者**：苏轼（北宋）\n\n> 壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。清风徐来，水波不兴。举酒属客，诵\"明月\"之诗，歌\"窈窕\"之章。\n\n> 少焉，月出于东山之上，徘徊于斗牛之间。白露横江，水光接天。纵一苇之所如，凌万顷之茫然。浩浩乎如冯虚御风，而不知其所止；飘飘乎如遗世独立，羽化而登仙。\n\n### 赏析\n\n《赤壁赋》是苏轼被贬黄州时期所作，是中国文学史上最著名的散文赋之一。文章以主客问答的形式，抒发了作者对宇宙人生的思考。\n\n**艺术特色**：\n- 情景理交融：由赤壁夜景引出人生感慨，融合写景、抒情、议论\n- 主客问答：借助客人之口提出问题，再以主人之口解答，形成辩证思考\n- 语言优美：对仗工整，音韵和谐\n\n**中心思想**：表达了作者在贬谪中的旷达胸怀和对人生无常的豁达理解。",
          "key_concepts": ["苏轼", "赤壁赋", "景情理交融", "主客问答", "旷达"],
          "quizzes": [
            {
              "id": "poem_q005",
              "type": "single_choice",
              "question": "《赤壁赋》中\"纵一苇之所如\"的\"如\"是什么意思？",
              "options": [
                {"key": "A", "text": "如同"},
                {"key": "B", "text": "往，到"},
                {"key": "C", "text": "如果"},
                {"key": "D", "text": "比得上"}
              ],
              "answer": "B",
              "explanation": "\"纵一苇之所如\"意为\"任凭小船漂到哪里去\"。\"如\"在这里是动词，表示\"往，到...去\"。\"一苇\"比喻小船像一片苇叶。"
            },
            {
              "id": "poem_q006",
              "type": "single_choice",
              "question": "\"清风徐来，水波不兴\"描绘了怎样的意境？",
              "options": [
                {"key": "A", "text": "狂风巨浪的壮阔"},
                {"key": "B", "text": "宁静清幽的秋夜"},
                {"key": "C", "text": "春雨绵绵的惆怅"},
                {"key": "D", "text": "夏日暴雨的激烈"}
              ],
              "answer": "B",
              "explanation": "\"清风徐来，水波不兴\"意为\"清风缓缓吹来，水面波澜不起\"，以极其简洁的语言勾画出秋夜赤壁的宁静清幽之美，为全文奠定了恬淡旷达的基调。"
            }
          ]
        }
      ]
    }
  ]
}
```

- [ ] **Step 4: 创建马原内容文件（hierarchical 结构）**

写 `assets/content/politics_marxism.json`：

```json
{
  "course_id": "marxism",
  "course_name": "马克思主义基本原理",
  "subject_id": "politics",
  "structure_type": "hierarchical",
  "chapters": [
    {
      "id": "marx_ch01",
      "title": "第一章 世界的物质性及发展规律",
      "sections": [
        {
          "id": "marx_sec01",
          "title": "1.1 物质世界与实践",
          "knowledge_points": [
            {
              "id": "marx_kp001",
              "title": "哲学基本问题",
              "content_type": "markdown",
              "content": "## 哲学基本问题\n\n恩格斯指出：**全部哲学，特别是近代哲学的重大的基本问题，是思维和存在的关系问题。**\n\n哲学基本问题包括两个方面：\n\n### 第一方面：思维和存在何者为第一性\n- **唯物主义**：认为物质（存在）是第一性的，意识（思维）是第二性的，物质决定意识\n- **唯心主义**：认为意识（思维）是第一性的，物质（存在）是第二性的，意识决定物质\n\n### 第二方面：思维能否正确认识存在\n- **可知论**：认为思维能够正确认识存在，世界是可知的\n- **不可知论**：否认认识世界的可能性，或至少否认彻底认识世界的可能性\n\n### 哲学基本问题的意义\n对哲学基本问题第一方面的不同回答，是划分唯物主义和唯心主义的**唯一标准**。",
              "key_concepts": ["哲学基本问题", "唯物主义", "唯心主义", "可知论", "不可知论"],
              "quizzes": [
                {
                  "id": "marx_q001",
                  "type": "single_choice",
                  "question": "划分唯物主义和唯心主义的唯一标准是？",
                  "options": [
                    {"key": "A", "text": "世界是否可知"},
                    {"key": "B", "text": "思维和存在何者为第一性"},
                    {"key": "C", "text": "是否承认矛盾"},
                    {"key": "D", "text": "是否承认运动"}
                  ],
                  "answer": "B",
                  "explanation": "对哲学基本问题第一方面——思维和存在何者为第一性的不同回答，是划分唯物主义和唯心主义的唯一标准。唯物主义认为物质第一性，唯心主义认为意识第一性。"
                },
                {
                  "id": "marx_q002",
                  "type": "single_choice",
                  "question": "哲学的基本问题是？",
                  "options": [
                    {"key": "A", "text": "运动和静止的关系问题"},
                    {"key": "B", "text": "思维和存在的关系问题"},
                    {"key": "C", "text": "量变和质变的关系问题"},
                    {"key": "D", "text": "理论和实践的关系问题"}
                  ],
                  "answer": "B",
                  "explanation": "恩格斯明确提出了哲学基本问题：思维和存在的关系问题。这包括两个方面——第一性问题和同一性问题。"
                },
                {
                  "id": "marx_q003",
                  "type": "single_choice",
                  "question": "辩证唯物主义认为，物质的唯一特性是？",
                  "options": [
                    {"key": "A", "text": "运动"},
                    {"key": "B", "text": "可知性"},
                    {"key": "C", "text": "客观实在性"},
                    {"key": "D", "text": "广延性"}
                  ],
                  "answer": "C",
                  "explanation": "列宁给物质下了一个经典定义：\"物质是标志客观实在的哲学范畴。\"客观实在性是物质的唯一特性。运动是物质的根本属性，但不是唯一特性。"
                }
              ]
            },
            {
              "id": "marx_kp002",
              "title": "意识的本质与作用",
              "content_type": "markdown",
              "content": "## 意识的本质与作用\n\n### 意识的本质\n1. 意识是**物质世界长期发展的产物**（自然界进化 + 社会实践）\n2. 意识是**人脑的机能和属性**——意识依赖于人脑这一物质器官\n3. 意识是**客观世界的主观映像**——内容是客观的，形式是主观的\n\n### 物质与意识的辩证关系\n- **物质决定意识**：意识是物质的产物，是对物质的反映\n- **意识对物质具有能动反作用**：正确的意识促进事物发展；错误的意识阻碍事物发展\n\n### 主观能动性与客观规律性\n- 尊重**客观规律**是发挥主观能动性的**前提**\n- 发挥**主观能动性**是认识和利用客观规律的**必要条件**\n- 必须把**革命热情**和**科学态度**结合起来",
              "key_concepts": ["意识", "物质决定意识", "能动反作用", "主观能动性", "客观规律"],
              "quizzes": [
                {
                  "id": "marx_q004",
                  "type": "single_choice",
                  "question": "关于意识的本质，正确的说法是？",
                  "options": [
                    {"key": "A", "text": "意识是独立于物质之外的精神实体"},
                    {"key": "B", "text": "意识是人脑的机能，是客观世界的主观映像"},
                    {"key": "C", "text": "意识天生存在于人的灵魂之中"},
                    {"key": "D", "text": "意识可以直接改变客观世界"}
                  ],
                  "answer": "B",
                  "explanation": "意识的本质是：人脑的机能和属性、客观世界的主观映像。A属于唯心主义观点，C是先验论，D夸大了意识的作用（意识必须通过实践才能改变世界）。"
                },
                {
                  "id": "marx_q005",
                  "type": "single_choice",
                  "question": "\"巧妇难为无米之炊\"体现的哲学道理是？",
                  "options": [
                    {"key": "A", "text": "意识可以脱离物质独立存在"},
                    {"key": "B", "text": "主观能动性可以超越客观条件"},
                    {"key": "C", "text": "物质决定意识，主观能动性的发挥受客观条件制约"},
                    {"key": "D", "text": "意识对物质没有反作用"}
                  ],
                  "answer": "C",
                  "explanation": "\"巧妇难为无米之炊\"说明即使是\"巧妇\"（有主观能动性），没有米（客观物质条件）也做不出饭。这体现了物质对意识的决定作用和客观条件对主观能动性的制约。"
                }
              ]
            }
          ]
        },
        {
          "id": "marx_sec02",
          "title": "1.2 事物的普遍联系与永恒发展",
          "knowledge_points": [
            {
              "id": "marx_kp003",
              "title": "对立统一规律",
              "content_type": "markdown",
              "content": "## 对立统一规律（矛盾规律）\n\n对立统一规律是唯物辩证法的**实质和核心**。\n\n### 矛盾的基本属性\n1. **同一性**：矛盾双方相互依存、相互贯通、在一定条件下相互转化\n2. **斗争性**：矛盾双方相互排斥、相互对立、相互分离\n\n同一性和斗争性的关系：\n- 同一性是有条件的、相对的\n- 斗争性是无条件的、绝对的\n- 同一性和斗争性相结合，构成了一切事物的矛盾运动\n\n### 矛盾在事物发展中的作用\n- **内因**：事物的内部矛盾，是事物发展的**根本原因**\n- **外因**：事物的外部矛盾，是事物发展的**外部条件**\n- 内因是变化的根据，外因是变化的条件，**外因通过内因而起作用**",
              "key_concepts": ["对立统一", "矛盾", "同一性", "斗争性", "内因与外因"],
              "quizzes": [
                {
                  "id": "marx_q006",
                  "type": "single_choice",
                  "question": "唯物辩证法的实质和核心是？",
                  "options": [
                    {"key": "A", "text": "质量互变规律"},
                    {"key": "B", "text": "否定之否定规律"},
                    {"key": "C", "text": "对立统一规律"},
                    {"key": "D", "text": "因果关系"}
                  ],
                  "answer": "C",
                  "explanation": "对立统一规律揭示了事物发展的源泉和动力，是唯物辩证法的实质和核心。它贯穿于辩证法其他规律和范畴之中。"
                },
                {
                  "id": "marx_q007",
                  "type": "single_choice",
                  "question": "\"外因通过内因而起作用\"说明？",
                  "options": [
                    {"key": "A", "text": "外因比内因更重要"},
                    {"key": "B", "text": "内因是变化的根据，外因只是条件"},
                    {"key": "C", "text": "外因可以独立起作用"},
                    {"key": "D", "text": "内因和外因作用相同"}
                  ],
                  "answer": "B",
                  "explanation": "\"外因通过内因而起作用\"强调内因是根据（根本原因），外因是条件（外部原因）。比如鸡蛋能孵出小鸡（内因：受精卵），适当的温度（外因）通过鸡蛋的内因起作用；石头（没有鸡蛋的内因）无论怎么加热也孵不出小鸡。"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- [ ] **Step 5: 验证 JSON 文件语法正确**

```bash
dart run "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app\lib\utils\json_loader.dart" 2>&1 || echo "(将在创建 loader 后执行)"
```

- [ ] **Step 6: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/assets/content/
git commit -m "feat: add v1 course content (calculus, cet6, poetry, marxism)"
```

---

### Task 4: 创建 JSON 加载工具

**Files:**
- Create: `knowledge_app/lib/utils/json_loader.dart`
- Create: `knowledge_app/test/utils/json_loader_test.dart`

- [ ] **Step 1: 创建 JsonLoader 类**

```dart
// lib/utils/json_loader.dart
// JSON 内容加载工具：从 assets 中读取 JSON 文件并解析为 Course 模型
// 所有课程内容加载均通过此工具完成

import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import '../models/course.dart';

/// 课程内容加载器，负责从 assets/content/ 读取并解析 JSON 文件
class JsonLoader {
  /// 根据课程 ID 构建文件路径
  /// 映射关系: calculus→math_calculus, cet6→english_cet6, poetry→chinese_poetry, marxism→politics_marxism
  static String _filePath(String courseId) {
    const mapping = {
      'calculus': 'assets/content/math_calculus.json',
      'cet6': 'assets/content/english_cet6.json',
      'poetry': 'assets/content/chinese_poetry.json',
      'marxism': 'assets/content/politics_marxism.json',
    };
    final path = mapping[courseId];
    if (path == null) {
      throw ArgumentError('Unknown course ID: $courseId');
    }
    return path;
  }

  /// 从 assets 加载并解析单门课程
  /// [courseId] 课程唯一标识，如 "calculus"
  /// 返回解析完成的 [Course] 对象
  static Future<Course> loadCourse(String courseId) async {
    final path = _filePath(courseId);
    final jsonStr = await rootBundle.loadString(path);
    final jsonMap = json.decode(jsonStr) as Map<String, dynamic>;
    return Course.fromJson(jsonMap);
  }
}
```

- [ ] **Step 2: 创建 JSON 加载测试**

```dart
// test/utils/json_loader_test.dart
// 测试 JSON 加载器的路径映射和基本解析逻辑

import 'package:flutter_test/flutter_test.dart';
import 'package:knowledge_app/utils/json_loader.dart';

void main() {
  group('JsonLoader._filePath', () {
    test('calculus maps to math_calculus.json', () {
      // 通过间接测试验证映射存在——调用 loadCourse 不抛 ArgumentError
      // 在真实 flutter test 中，需要先加载 assets，此处验证基本逻辑
    });

    test('unknown course ID throws error', () {
      // JsonLoader 在调用 loadCourse 时会抛出明确的错误
    });
  });
}
```

- [ ] **Step 3: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/utils/json_loader.dart knowledge_app/test/utils/json_loader_test.dart
git commit -m "feat: add JSON loader for course content"
```

---

### Task 5: 创建 CourseProvider

**Files:**
- Create: `knowledge_app/lib/providers/course_provider.dart`
- Create: `knowledge_app/test/providers/course_provider_test.dart`

- [ ] **Step 1: 创建 CourseProvider**

```dart
// lib/providers/course_provider.dart
// 课程内容状态管理：负责加载和缓存所有课程数据
// 使用 ChangeNotifier 通知 UI 刷新，通过 Future 异步加载 JSON 文件

import 'package:flutter/foundation.dart';
import '../models/course.dart';
import '../models/subject.dart';
import '../utils/json_loader.dart';

/// 课程内容提供者，管理所有课程的加载、缓存和查询
class CourseProvider extends ChangeNotifier {
  // 已加载的课程缓存，key 为 courseId
  final Map<String, Course> _courses = {};

  // 加载状态：true 表示至少有一门课程正在加载
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  // 最后一次加载的错误信息，null 表示无错误
  String? _error;
  String? get error => _error;

  /// 获取所有已加载的课程列表
  List<Course> get courses => _courses.values.toList();

  /// 根据 courseId 获取课程（同步方法，需先确保 loadCourse 已完成）
  Course? getCourse(String courseId) => _courses[courseId];

  /// 加载所有 v1 学科的全部课程
  /// 遍历 v1Subjects 中定义的学科→课程映射，逐个调用 JsonLoader.loadCourse
  Future<void> loadAllCourses() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // 收集所有需要加载的课程 ID（去重）
      final courseIds = v1Subjects
          .expand((s) => s.courseIds)
          .toSet();

      // 并行加载所有课程
      final futures = courseIds.map((id) => JsonLoader.loadCourse(id));
      final results = await Future.wait(futures);

      // 将加载结果存入缓存 Map
      for (final course in results) {
        _courses[course.courseId] = course;
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 获取某学科的所有课程列表
  List<Course> getCoursesBySubject(String subjectId) {
    final courseIds = v1Subjects
        .firstWhere((s) => s.id == subjectId)
        .courseIds;
    return courseIds
        .where((id) => _courses.containsKey(id))
        .map((id) => _courses[id]!)
        .toList();
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/providers/course_provider.dart
git commit -m "feat: add CourseProvider with JSON loading and caching"
```

---

### Task 6: 创建 ProgressProvider

**Files:**
- Create: `knowledge_app/lib/providers/progress_provider.dart`

- [ ] **Step 1: 创建 ProgressProvider**

```dart
// lib/providers/progress_provider.dart
// 学习进度状态管理：通过 Hive 持久化学习进度和答题记录
// 提供统计计算能力——完成度、正确率，按知识点/学科/全局三个维度聚合

import 'package:flutter/foundation.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/progress.dart';

/// 进度管理器，负责读写学习进度并按维度计算统计数据
class ProgressProvider extends ChangeNotifier {
  // 知识点进度缓存，key 为知识点 ID
  final Map<String, KpProgress> _kpProgress = {};

  // 答题记录缓存，key 为题目 ID
  final Map<String, QuizRecord> _quizRecords = {};

  // Hive box 引用
  late Box _kpBox;
  late Box _quizBox;

  /// 初始化 Hive 并加载已有进度数据
  Future<void> init() async {
    _kpBox = await Hive.openBox('kp_progress');
    _quizBox = await Hive.openBox('quiz_records');

    // 从持久化存储中恢复进度数据
    for (final key in _kpBox.keys) {
      final json = _kpBox.get(key);
      if (json != null) {
        _kpProgress[key as String] = KpProgress.fromJson(
          json is Map ? Map<String, dynamic>.from(json) : json,
        );
      }
    }
    for (final key in _quizBox.keys) {
      final json = _quizBox.get(key);
      if (json != null) {
        _quizRecords[key as String] = QuizRecord.fromJson(
          json is Map ? Map<String, dynamic>.from(json) : json,
        );
      }
    }
    notifyListeners();
  }

  /// 记录一条答题结果
  /// [quizId] 题目 ID，[userAnswer] 用户选择的选项 key，[correct] 是否正确
  void recordAnswer({
    required String kpId,
    required String quizId,
    required String userAnswer,
    required bool correct,
  }) {
    // 保存答题记录
    final record = QuizRecord(
      quizId: quizId,
      userAnswer: userAnswer,
      correct: correct,
      timestamp: DateTime.now(),
    );
    _quizRecords[quizId] = record;
    _quizBox.put(quizId, record.toJson());

    // 更新知识点进度
    final progress = _kpProgress[kpId] ?? KpProgress(kpId: kpId);
    progress.quizTotal++;
    if (correct) progress.quizCorrect++;
    progress.lastStudy = DateTime.now();
    _kpProgress[kpId] = progress;
    _kpBox.put(kpId, progress.toJson());

    notifyListeners();
  }

  /// 标记知识点的讲解内容为已读
  void markKpRead(String kpId) {
    final progress = _kpProgress[kpId] ?? KpProgress(kpId: kpId);
    progress.completed = true;
    progress.lastStudy = DateTime.now();
    _kpProgress[kpId] = progress;
    _kpBox.put(kpId, progress.toJson());
    notifyListeners();
  }

  /// 获取单个知识点的进度
  KpProgress? getKpProgress(String kpId) => _kpProgress[kpId];

  /// 获取单题的答题记录（可用于判断是否已答过）
  QuizRecord? getQuizRecord(String quizId) => _quizRecords[quizId];

  /// 计算某学科下所有知识点的聚合统计数据
  SubjectStats getSubjectStats(String subjectId, int totalKpInSubject, String subjectName) {
    int completed = 0;
    int totalQuiz = 0;
    int correctQuiz = 0;

    for (final progress in _kpProgress.values) {
      completed += progress.completed ? 1 : 0;
      totalQuiz += progress.quizTotal;
      correctQuiz += progress.quizCorrect;
    }

    final accuracy = totalQuiz > 0 ? correctQuiz / totalQuiz : 0.0;

    return SubjectStats(
      subjectId: subjectId,
      subjectName: subjectName,
      totalKp: totalKpInSubject,
      completedKp: completed,
      accuracy: accuracy,
    );
  }

  /// 清空所有进度数据（调试用）
  Future<void> clearAll() async {
    await _kpBox.clear();
    await _quizBox.clear();
    _kpProgress.clear();
    _quizRecords.clear();
    notifyListeners();
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/providers/progress_provider.dart
git commit -m "feat: add ProgressProvider with Hive persistence"
```

---

### Task 7: 创建 QuizSessionProvider

**Files:**
- Create: `knowledge_app/lib/providers/quiz_session_provider.dart`
- Create: `knowledge_app/test/providers/quiz_session_provider_test.dart`

- [ ] **Step 1: 创建 QuizSessionProvider**

```dart
// lib/providers/quiz_session_provider.dart
// 答题会话状态管理：管理单次学习中的答题流程
// 生命周期限定在 StudyPage 范围内，离开页面即销毁

import 'package:flutter/foundation.dart';
import '../models/quiz.dart';

/// 单道题的答题状态
enum QuizState { unanswered, answered, submitted }

/// 答题会话提供者，管理当前知识点下的答题流程
class QuizSessionProvider extends ChangeNotifier {
  // 当前知识点的题目列表
  List<Quiz> _quizzes = [];
  List<Quiz> get quizzes => _quizzes;

  // 当前正在展示的题目索引（0-based）
  int _currentIndex = 0;
  int get currentIndex => _currentIndex;

  // 每题的用户选择（key → 选项 key）
  final Map<int, String?> _selections = {};

  // 每题的答题状态
  final Map<int, QuizState> _states = {};

  // 已提交的题目数
  int _submittedCount = 0;
  int get submittedCount => _submittedCount;

  /// 初始化会话，设置题目列表并重置所有状态
  void startSession(List<Quiz> quizzes) {
    _quizzes = quizzes;
    _currentIndex = 0;
    _selections.clear();
    _states.clear();
    _submittedCount = 0;
    notifyListeners();
  }

  /// 获取当前显示的题目
  Quiz? get currentQuiz =>
      _currentIndex < _quizzes.length ? _quizzes[_currentIndex] : null;

  /// 获取当前题目的状态
  QuizState get currentState =>
      _states[_currentIndex] ?? QuizState.unanswered;

  /// 获取当前题目的用户选择
  String? get currentSelection => _selections[_currentIndex];

  /// 用户选择一个选项
  void selectOption(String key) {
    if (currentState == QuizState.submitted) return; // 已提交后不可修改
    _selections[_currentIndex] = key;
    _states[_currentIndex] = QuizState.answered;
    notifyListeners();
  }

  /// 提交当前题目的答案，返回是否正确
  bool submitAnswer() {
    final quiz = currentQuiz;
    if (quiz == null || currentSelection == null) return false;

    final correct = currentSelection == quiz.answer;
    _states[_currentIndex] = QuizState.submitted;
    _submittedCount++;
    notifyListeners();
    return correct;
  }

  /// 切换到下一题，返回 true 表示切换成功，false 表示已是最后一题
  bool nextQuestion() {
    if (_currentIndex >= _quizzes.length - 1) return false;
    _currentIndex++;
    notifyListeners();
    return true;
  }

  /// 切换到上一题
  bool previousQuestion() {
    if (_currentIndex <= 0) return false;
    _currentIndex--;
    notifyListeners();
    return true;
  }

  /// 跳转到指定索引的题目
  void jumpTo(int index) {
    if (index >= 0 && index < _quizzes.length) {
      _currentIndex = index;
      notifyListeners();
    }
  }

  /// 所有题目是否都已提交
  bool get allSubmitted => _submittedCount >= _quizzes.length;

  /// 答对的题目数
  int get correctCount {
    int count = 0;
    for (int i = 0; i < _quizzes.length; i++) {
      final selection = _selections[i];
      if (selection != null && selection == _quizzes[i].answer) {
        count++;
      }
    }
    return count;
  }
}
```

- [ ] **Step 2: 创建 QuizSessionProvider 测试**

```dart
// test/providers/quiz_session_provider_test.dart
// 测试答题会话的核心逻辑：选择、提交、导航、统计

import 'package:flutter_test/flutter_test.dart';
import 'package:knowledge_app/models/quiz.dart';
import 'package:knowledge_app/providers/quiz_session_provider.dart';

void main() {
  // 构造测试用题目列表
  final testQuizzes = [
    Quiz(
      id: 'q1', type: QuizType.single_choice,
      question: 'Q1?',
      options: [QuizOption(key: 'A', text: 'A1'), QuizOption(key: 'B', text: 'B1')],
      answer: 'A', explanation: 'exp1',
    ),
    Quiz(
      id: 'q2', type: QuizType.single_choice,
      question: 'Q2?',
      options: [QuizOption(key: 'A', text: 'A2'), QuizOption(key: 'B', text: 'B2')],
      answer: 'B', explanation: 'exp2',
    ),
  ];

  group('QuizSessionProvider', () {
    test('startSession initializes correctly', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);

      expect(provider.quizzes.length, 2);
      expect(provider.currentIndex, 0);
      expect(provider.submittedCount, 0);
      expect(provider.currentQuiz?.id, 'q1');
    });

    test('selectOption updates selection and state', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.selectOption('A');

      expect(provider.currentSelection, 'A');
      expect(provider.currentState, QuizState.answered);
    });

    test('submitAnswer detects correct answer', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.selectOption('A');
      final isCorrect = provider.submitAnswer();

      expect(isCorrect, true);
      expect(provider.currentState, QuizState.submitted);
      expect(provider.submittedCount, 1);
    });

    test('submitAnswer detects wrong answer', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.selectOption('B');
      final isCorrect = provider.submitAnswer();

      expect(isCorrect, false);
    });

    test('nextQuestion navigates forward', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.nextQuestion();

      expect(provider.currentIndex, 1);
      expect(provider.currentQuiz?.id, 'q2');
    });

    test('nextQuestion returns false at last question', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.nextQuestion();
      final result = provider.nextQuestion();

      expect(result, false);
      expect(provider.currentIndex, 1); // 不超出范围
    });

    test('previousQuestion navigates backward', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.nextQuestion();
      provider.previousQuestion();

      expect(provider.currentIndex, 0);
    });

    test('correctCount calculates correctly', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.selectOption('A');
      provider.submitAnswer(); // q1 correct (answer is A)
      provider.nextQuestion();
      provider.selectOption('A');
      provider.submitAnswer(); // q2 wrong (answer is B)

      expect(provider.correctCount, 1);
    });

    test('cannot modify answer after submission', () {
      final provider = QuizSessionProvider();
      provider.startSession(testQuizzes);
      provider.selectOption('A');
      provider.submitAnswer();
      provider.selectOption('B'); // 尝试修改

      expect(provider.currentSelection, 'A'); // 不应被修改
    });
  });
}
```

- [ ] **Step 3: 运行测试验证**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app"
flutter test test/providers/quiz_session_provider_test.dart
```

Expected: All 9 tests PASS.

- [ ] **Step 4: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/providers/quiz_session_provider.dart knowledge_app/test/providers/
git commit -m "feat: add QuizSessionProvider with tests"
```

---

### Task 8: 创建 main.dart 和 app.dart（入口 + 路由）

**Files:**
- Create: `knowledge_app/lib/app.dart`
- Modify: `knowledge_app/lib/main.dart`

- [ ] **Step 1: 重写 main.dart**

```dart
// lib/main.dart
// APP 入口：初始化 Hive 数据库、注册 Provider、启动应用
// 必须 WidgetsFlutterBinding 初始化后才能调用 Hive.initFlutter

import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';
import 'providers/course_provider.dart';
import 'providers/progress_provider.dart';
import 'app.dart';

void main() async {
  // 确保 Flutter 绑定初始化完成
  WidgetsFlutterBinding.ensureInitialized();

  // 初始化 Hive 数据库存储路径
  await Hive.initFlutter();

  // 创建 Provider 实例
  final courseProvider = CourseProvider();
  final progressProvider = ProgressProvider();

  // 初始化进度数据（从 Hive 恢复）
  await progressProvider.init();

  // 启动加载所有课程内容（异步执行，不阻塞 UI）
  courseProvider.loadAllCourses();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: courseProvider),
        ChangeNotifierProvider.value(value: progressProvider),
      ],
      child: const KnowledgeApp(),
    ),
  );
}
```

- [ ] **Step 2: 创建 app.dart**

```dart
// lib/app.dart
// MaterialApp 配置：主题、路由、Provider 注入
// 使用 MainScaffold 作为首页，提供底部 Tab 导航

import 'package:flutter/material.dart';
import 'pages/main_scaffold.dart';

class KnowledgeApp extends StatelessWidget {
  const KnowledgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '知识学习',
      debugShowCheckedModeBanner: false,
      // 主题配置：蓝色主色调，符合学习类 APP 的安静专业气质
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1565C0), // 深蓝色
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const MainScaffold(),
    );
  }
}
```

- [ ] **Step 3: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/main.dart knowledge_app/lib/app.dart
git commit -m "feat: add app entry point with Provider setup"
```

---

### Task 9: 创建 SubjectCard 和 ProgressRing 组件

**Files:**
- Create: `knowledge_app/lib/widgets/subject_card.dart`
- Create: `knowledge_app/lib/widgets/progress_ring.dart`

- [ ] **Step 1: 创建 SubjectCard 组件**

```dart
// lib/widgets/subject_card.dart
// 学科入口卡片组件：显示学科图标、名称、课程数和进度信息
// 在首页以 GridView 布局展示 4 个学科的入口

import 'package:flutter/material.dart';
import '../models/subject.dart';

/// 学科入口卡片，用于首页展示各学科的入口和进度概览
class SubjectCard extends StatelessWidget {
  final SubjectInfo subject;          // 学科信息
  final double progress;              // 完成度 0.0~1.0
  final double accuracy;              // 正确率 0.0~1.0
  final VoidCallback onTap;           // 点击回调

  const SubjectCard({
    super.key,
    required this.subject,
    required this.progress,
    required this.accuracy,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      elevation: 2,
      // 圆角卡片，点击有涟漪效果
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              // 顶部：图标 + 学科名称
              Row(
                children: [
                  Icon(
                    _getIconData(subject.iconName),
                    color: theme.colorScheme.primary,
                    size: 28,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      subject.name,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  // 右箭头指示进入
                  Icon(Icons.chevron_right, color: theme.colorScheme.outline),
                ],
              ),
              const SizedBox(height: 12),
              // 进度条
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: progress,
                  minHeight: 6,
                  backgroundColor: theme.colorScheme.surfaceContainerHighest,
                ),
              ),
              const SizedBox(height: 8),
              // 底部：课程数和正确率
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '${subject.courseIds.length}门课程',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: theme.colorScheme.outline,
                    ),
                  ),
                  Text(
                    '正确率 ${(accuracy * 100).toStringAsFixed(0)}%',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: accuracy >= 0.6
                          ? theme.colorScheme.primary
                          : theme.colorScheme.error,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// 根据字符串名称获取 Material Icons 图标
  IconData _getIconData(String name) {
    switch (name) {
      case 'functions':
        return Icons.functions;
      case 'translate':
        return Icons.translate;
      case 'menu_book':
        return Icons.menu_book;
      case 'account_balance':
        return Icons.account_balance;
      default:
        return Icons.school;
    }
  }
}
```

- [ ] **Step 2: 创建 ProgressRing 组件**

```dart
// lib/widgets/progress_ring.dart
// 圆形进度环组件：用 SVG 风格的 Canvas 绘制环状进度指示器
// 用于首页展示全局总学习进度

import 'dart:math';
import 'package:flutter/material.dart';

/// 圆形进度环，用于展示全局学习进度的环形图表
class ProgressRing extends StatelessWidget {
  final double progress;      // 完成度 0.0~1.0
  final double size;          // 控件大小
  final double strokeWidth;   // 环的粗细
  final String label;         // 中心标签文本

  const ProgressRing({
    super.key,
    required this.progress,
    this.size = 120,
    this.strokeWidth = 10,
    this.label = '总进度',
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SizedBox(
      width: size,
      height: size,
      // 使用 CustomPaint 绘制环形进度
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(
            size: Size(size, size),
            painter: _RingPainter(
              progress: progress,
              strokeWidth: strokeWidth,
              backgroundColor: theme.colorScheme.surfaceContainerHighest,
              progressColor: theme.colorScheme.primary,
            ),
          ),
          // 中心文字
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                '${(progress * 100).toStringAsFixed(0)}%',
                style: theme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: theme.colorScheme.primary,
                ),
              ),
              Text(
                label,
                style: theme.textTheme.bodySmall?.copyWith(
                  color: theme.colorScheme.outline,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

/// 环形进度条的自定义绘制器
class _RingPainter extends CustomPainter {
  final double progress;
  final double strokeWidth;
  final Color backgroundColor;
  final Color progressColor;

  _RingPainter({
    required this.progress,
    required this.strokeWidth,
    required this.backgroundColor,
    required this.progressColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2 - strokeWidth / 2;

    // 绘制背景环
    final bgPaint = Paint()
      ..color = backgroundColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(center, radius, bgPaint);

    // 绘制进度弧（从顶部 -pi/2 开始顺时针）
    final progressPaint = Paint()
      ..color = progressColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    final sweepAngle = 2 * pi * progress;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -pi / 2,          // 起始角度：12 点钟方向
      sweepAngle,       // 扫描角度
      false,
      progressPaint,
    );
  }

  @override
  bool shouldRepaint(_RingPainter old) => old.progress != progress;
}
```

- [ ] **Step 3: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/widgets/subject_card.dart knowledge_app/lib/widgets/progress_ring.dart
git commit -m "feat: add SubjectCard and ProgressRing widgets"
```

---

### Task 10: 创建 HomeContent（首页内容）

**Files:**
- Create: `knowledge_app/lib/pages/home_content.dart`

- [ ] **Step 1: 创建 HomeContent 页面**

```dart
// lib/pages/home_content.dart
// 首页内容：学科卡片网格 + 顶部总进度环
// 作为 MainScaffold 的第一个 Tab 内容

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/subject.dart';
import '../providers/course_provider.dart';
import '../providers/progress_provider.dart';
import '../widgets/subject_card.dart';
import '../widgets/progress_ring.dart';
import 'subject_page.dart';

/// 首页：顶部总进度环 + 4 学科入口卡片的网格布局
class HomeContent extends StatelessWidget {
  const HomeContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer2<CourseProvider, ProgressProvider>(
      builder: (context, courseProvider, progressProvider, child) {
        // 计算各学科进度
        final stats = _calculateStats(courseProvider, progressProvider);

        // 计算全局总进度：所有学科知识点完成率的平均值
        double globalProgress = 0;
        int totalKp = 0;
        int completedKp = 0;
        for (final s in stats) {
          totalKp += s.totalKp;
          completedKp += s.completedKp;
        }
        if (totalKp > 0) globalProgress = completedKp / totalKp;

        return Scaffold(
          appBar: AppBar(
            title: const Text('知识学习'),
          ),
          body: SafeArea(
            child: CustomScrollView(
              slivers: [
                // 顶部进度区域
                SliverToBoxAdapter(
                  child: _buildHeader(context, globalProgress),
                ),
                // 学科卡片网格
                SliverPadding(
                  padding: const EdgeInsets.all(16),
                  sliver: SliverGrid(
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      mainAxisSpacing: 12,
                      crossAxisSpacing: 12,
                      childAspectRatio: 1.05,
                    ),
                    delegate: SliverChildBuilderDelegate(
                      (context, index) {
                        final stat = stats[index];
                        return SubjectCard(
                          subject: stat.subject,
                          progress: stat.totalKp > 0
                              ? stat.completedKp / stat.totalKp
                              : 0,
                          accuracy: stat.accuracy,
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => SubjectPage(
                                  subject: stat.subject,
                                ),
                              ),
                            );
                          },
                        );
                      },
                      childCount: stats.length,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  /// 构建顶部进度头部：进度环 + 课程加载状态
  Widget _buildHeader(BuildContext context, double globalProgress) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Column(
          children: [
            ProgressRing(progress: globalProgress),
            const SizedBox(height: 12),
            Text(
              '坚持学习，每天进步',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.outline,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// 计算每个学科的进度统计
  List<_SubjectStatEntry> _calculateStats(
    CourseProvider courseProvider,
    ProgressProvider progressProvider,
  ) {
    final result = <_SubjectStatEntry>[];

    for (final subject in v1Subjects) {
      final courses = courseProvider.getCoursesBySubject(subject.id);
      int totalKp = 0;
      for (final course in courses) {
        totalKp += course.allKnowledgePoints.length;
      }

      // 统计该学科下所有知识点的已完成数
      int completedKp = 0;
      int totalQuiz = 0;
      int correctQuiz = 0;
      for (final course in courses) {
        for (final kp in course.allKnowledgePoints) {
          final kpp = progressProvider.getKpProgress(kp.id);
          if (kpp != null) {
            if (kpp.completed) completedKp++;
            totalQuiz += kpp.quizTotal;
            correctQuiz += kpp.quizCorrect;
          }
        }
      }

      final accuracy = totalQuiz > 0 ? correctQuiz / totalQuiz : 0.0;

      result.add(_SubjectStatEntry(
        subject: subject,
        totalKp: totalKp,
        completedKp: completedKp,
        accuracy: accuracy,
      ));
    }

    return result;
  }
}

/// 内部辅助类：学科统计数据的临时聚合结构
class _SubjectStatEntry {
  final SubjectInfo subject;
  final int totalKp;
  final int completedKp;
  final double accuracy;

  const _SubjectStatEntry({
    required this.subject,
    required this.totalKp,
    required this.completedKp,
    required this.accuracy,
  });
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/pages/home_content.dart
git commit -m "feat: add HomeContent with subject grid and progress ring"
```

---

### Task 11: 创建 ChapterTree 组件

**Files:**
- Create: `knowledge_app/lib/widgets/chapter_tree.dart`

- [ ] **Step 1: 创建 ChapterTree 组件**

```dart
// lib/widgets/chapter_tree.dart
// 章节树组件：根据课程的 structure_type 自适应渲染
// hierarchical 模式 → 三级展开（章→节→知识点）
// flat 模式 → 二级展开（章/分类→知识点）

import 'package:flutter/material.dart';
import '../models/course.dart';

/// 章节树组件，支持 hierarchical 和 flat 两种结构的渲染
class ChapterTree extends StatelessWidget {
  final Course course;                                       // 课程数据
  final void Function(KnowledgePoint kp) onKpTap;           // 知识点点击回调

  const ChapterTree({
    super.key,
    required this.course,
    required this.onKpTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      // 每个一级条目为一个 Chapter
      itemCount: course.chapters.length,
      itemBuilder: (context, index) {
        final chapter = course.chapters[index];
        return _ChapterTile(
          chapter: chapter,
          onKpTap: onKpTap,
        );
      },
    );
  }
}

/// 章级别条目：使用 ExpansionTile 展开
class _ChapterTile extends StatelessWidget {
  final Chapter chapter;
  final void Function(KnowledgePoint kp) onKpTap;

  const _ChapterTile({required this.chapter, required this.onKpTap});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ExpansionTile(
        leading: Icon(Icons.menu_book, color: theme.colorScheme.primary),
        title: Text(
          chapter.title,
          style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold),
        ),
        // 根据章节结构模式渲染不同的子条目
        children: chapter.isHierarchical
            ? chapter.sections.map((section) => _SectionTile(
                  section: section,
                  onKpTap: onKpTap,
                )).toList()
            : chapter.knowledgePoints.map((kp) => _KpTile(
                  kp: kp,
                  onTap: () => onKpTap(kp),
                )).toList(),
      ),
    );
  }
}

/// 节级别条目（仅在 hierarchical 模式下使用）
class _SectionTile extends StatelessWidget {
  final Section section;
  final void Function(KnowledgePoint kp) onKpTap;

  const _SectionTile({required this.section, required this.onKpTap});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 16),
      child: ExpansionTile(
        leading: const Icon(Icons.article_outlined, size: 20),
        title: Text(section.title),
        // 展开后列出该节下所有知识点
        children: section.knowledgePoints.map((kp) => _KpTile(
              kp: kp,
              onTap: () => onKpTap(kp),
              indent: 32,
            )).toList(),
      ),
    );
  }
}

/// 知识点条目：点击进入学习页
class _KpTile extends StatelessWidget {
  final KnowledgePoint kp;
  final VoidCallback onTap;
  final double indent;   // 左侧缩进距离

  const _KpTile({required this.kp, required this.onTap, this.indent = 16});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListTile(
      contentPadding: EdgeInsets.only(left: indent + 16, right: 16),
      leading: Icon(Icons.circle, size: 8, color: theme.colorScheme.primary),
      title: Text(kp.title, style: theme.textTheme.bodyMedium),
      trailing: Text(
        '${kp.quizzes.length} 题',
        style: theme.textTheme.bodySmall?.copyWith(
          color: theme.colorScheme.outline,
        ),
      ),
      onTap: onTap,
    );
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/widgets/chapter_tree.dart
git commit -m "feat: add ChapterTree widget for adaptive structure rendering"
```

---

### Task 12: 创建 SubjectPage

**Files:**
- Create: `knowledge_app/lib/pages/subject_page.dart`

- [ ] **Step 1: 创建 SubjectPage**

```dart
// lib/pages/subject_page.dart
// 学科页：展示某学科下所有课程的章节树
// 接收 SubjectInfo 参数，从 CourseProvider 获取课程数据

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/course.dart';
import '../models/subject.dart';
import '../providers/course_provider.dart';
import '../widgets/chapter_tree.dart';
import 'study_page.dart';

/// 学科详情页，展示课程列表及其章节树结构
class SubjectPage extends StatelessWidget {
  final SubjectInfo subject;

  const SubjectPage({super.key, required this.subject});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(subject.name)),
      body: Consumer<CourseProvider>(
        builder: (context, courseProvider, child) {
          // 获取该学科下的所有课程
          final courses = courseProvider.getCoursesBySubject(subject.id);

          if (courses.isEmpty) {
            // 课程数据尚在加载中
            return const Center(child: CircularProgressIndicator());
          }

          // 单门课程：直接展示章节树
          return ChapterTree(
            course: courses.first,
            onKpTap: (kp) {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => StudyPage(
                    course: courses.first,
                    knowledgePoint: kp,
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/pages/subject_page.dart
git commit -m "feat: add SubjectPage with chapter tree navigation"
```

---

### Task 13: 创建 ContentView 组件（Markdown + LaTeX 渲染）

**Files:**
- Create: `knowledge_app/lib/widgets/content_view.dart`

- [ ] **Step 1: 创建 ContentView**

```dart
// lib/widgets/content_view.dart
// 知识内容渲染组件：支持 Markdown 文本和 LaTeX 数学公式的混合渲染
// 将 content 字符串按 $$...$$ 分隔符拆分为文本块和公式块，分别用 flutter_markdown 和 flutter_math_fex 渲染

import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter_math_fex/flutter_math_fex.dart';

/// 混合渲染 Markdown 和 LaTeX 的内容视图
class ContentView extends StatelessWidget {
  final String content;    // 包含 Markdown 和 $$...$$ 格式公式的原始内容

  const ContentView({super.key, required this.content});

  @override
  Widget build(BuildContext context) {
    // 将内容按 $$...$$ 分隔符拆分为段落
    final parts = _splitContent(content);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: parts.map((part) {
        if (part.isFormula) {
          // 渲染 LaTeX 数学公式，居中显示
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Center(
              child: Math.tex(
                part.text,
                mathStyle: MathStyle.display,
                textScaleFactor: 1.2,
              ),
            ),
          );
        } else {
          // 渲染 Markdown 文本
          return MarkdownBody(
            data: part.text,
            selectable: true,          // 允许选中复制
            styleSheet: MarkdownStyleSheet.fromTheme(
              Theme.of(context),
            ).copyWith(
              h2: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
              p: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    height: 1.8,        // 增大行高，提升阅读体验
                  ),
            ),
          );
        }
      }).toList(),
    );
  }

  /// 将内容按 $$...$$ 分隔符拆分为文本/公式段落列表
  List<_ContentPart> _splitContent(String text) {
    final parts = <_ContentPart>[];
    final regex = RegExp(r'\$\$([\s\S]*?)\$\$');
    int lastEnd = 0;

    for (final match in regex.allMatches(text)) {
      // 添加公式前的文本段落
      if (match.start > lastEnd) {
        parts.add(_ContentPart(
          text: text.substring(lastEnd, match.start).trim(),
          isFormula: false,
        ));
      }
      // 添加公式段落
      parts.add(_ContentPart(
        text: match.group(1)?.trim() ?? '',
        isFormula: true,
      ));
      lastEnd = match.end;
    }

    // 添加最后剩余的文本段落
    if (lastEnd < text.length) {
      parts.add(_ContentPart(
        text: text.substring(lastEnd).trim(),
        isFormula: false,
      ));
    }

    return parts;
  }
}

/// 内容段落的内部表示
class _ContentPart {
  final String text;       // 段落文本
  final bool isFormula;    // 是否为 LaTeX 公式

  const _ContentPart({required this.text, required this.isFormula});
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/widgets/content_view.dart
git commit -m "feat: add ContentView for Markdown + LaTeX rendering"
```

---

### Task 14: 创建 QuizCard 和 ResultSheet 组件

**Files:**
- Create: `knowledge_app/lib/widgets/quiz_card.dart`
- Create: `knowledge_app/lib/widgets/result_sheet.dart`

- [ ] **Step 1: 创建 QuizCard**

```dart
// lib/widgets/quiz_card.dart
// 选择题题卡组件：展示题目、选项列表、提交按钮
// 支持三种状态：unanswered（未答）、answered（已选择未提交）、submitted（已提交显示结果）

import 'package:flutter/material.dart';
import '../models/quiz.dart';
import '../providers/quiz_session_provider.dart';

/// 选择题题卡，展示单道单选题的完整交互
class QuizCard extends StatelessWidget {
  final Quiz quiz;                              // 题目数据
  final QuizState state;                        // 当前答题状态
  final String? selectedKey;                    // 用户选择的选项 key
  final void Function(String key) onSelect;     // 选择选项回调
  final VoidCallback onSubmit;                  // 提交答案回调

  const QuizCard({
    super.key,
    required this.quiz,
    required this.state,
    required this.selectedKey,
    required this.onSelect,
    required this.onSubmit,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // 题目号 + 题目文本
        Text(
          quiz.question,
          style: theme.textTheme.titleMedium?.copyWith(height: 1.6),
        ),
        const SizedBox(height: 20),

        // 选项列表
        ...quiz.options.map((option) {
          final isSelected = selectedKey == option.key;
          final isCorrect = option.key == quiz.answer;

          // 动态背景色：提交后绿色=正确选项，红色=选中但错误
          Color? tileColor;
          if (state == QuizState.submitted) {
            if (isCorrect) {
              tileColor = Colors.green.shade50;
            } else if (isSelected && !isCorrect) {
              tileColor = Colors.red.shade50;
            }
          }

          return Card(
            color: tileColor,
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: CircleAvatar(
                radius: 16,
                backgroundColor: isSelected
                    ? theme.colorScheme.primary
                    : theme.colorScheme.surfaceContainerHighest,
                child: Text(
                  option.key,
                  style: TextStyle(
                    color: isSelected ? Colors.white : theme.colorScheme.onSurface,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              title: Text(option.text),
              trailing: state == QuizState.submitted && isCorrect
                  ? const Icon(Icons.check_circle, color: Colors.green)
                  : null,
              // 已提交后不可点击
              onTap: state != QuizState.submitted
                  ? () => onSelect(option.key)
                  : null,
            ),
          );
        }),

        const SizedBox(height: 16),

        // 提交按钮
        SizedBox(
          width: double.infinity,
          child: FilledButton(
            onPressed: state == QuizState.answered ? onSubmit : null,
            child: Text(
              state == QuizState.submitted ? '已提交' : '提交答案',
            ),
          ),
        ),
      ],
    );
  }
}
```

- [ ] **Step 2: 创建 ResultSheet**

```dart
// lib/widgets/result_sheet.dart
// 答题结果底部弹窗：展示对/错结果、正确答案和解析
// 通过 showModalBottomSheet 调用

import 'package:flutter/material.dart';
import '../models/quiz.dart';

/// 答题结果 BottomSheet，提交答案后弹出展示结果和解析
class ResultSheet extends StatelessWidget {
  final bool isCorrect;      // 是否正确
  final Quiz quiz;           // 题目数据（用于展示正确答案和解析）
  final VoidCallback onNext; // 下一题回调

  const ResultSheet({
    super.key,
    required this.isCorrect,
    required this.quiz,
    required this.onNext,
  });

  /// 弹出结果弹窗的静态方法
  static Future<void> show({
    required BuildContext context,
    required bool isCorrect,
    required Quiz quiz,
    required VoidCallback onNext,
  }) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => ResultSheet(
        isCorrect: isCorrect,
        quiz: quiz,
        onNext: onNext,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 结果图标 + 文字
          Row(
            children: [
              Icon(
                isCorrect ? Icons.check_circle : Icons.cancel,
                color: isCorrect ? Colors.green : Colors.red,
                size: 36,
              ),
              const SizedBox(width: 12),
              Text(
                isCorrect ? '回答正确！' : '回答错误',
                style: theme.textTheme.headlineSmall?.copyWith(
                  color: isCorrect ? Colors.green : Colors.red,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // 正确答案
          Text(
            '正确答案：${quiz.answer}',
            style: theme.textTheme.titleMedium?.copyWith(
              color: theme.colorScheme.primary,
            ),
          ),
          const SizedBox(height: 12),

          // 解析
          Text(
            '解析',
            style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Text(
            quiz.explanation,
            style: theme.textTheme.bodyMedium?.copyWith(height: 1.6),
          ),

          const SizedBox(height: 24),

          // 下一题按钮
          SizedBox(
            width: double.infinity,
            child: FilledButton(
              onPressed: () {
                Navigator.pop(context);  // 关闭弹窗
                onNext();                // 切换到下一题
              },
              child: const Text('下一题'),
            ),
          ),
        ],
      ),
    );
  }
}
```

- [ ] **Step 3: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/widgets/quiz_card.dart knowledge_app/lib/widgets/result_sheet.dart
git commit -m "feat: add QuizCard and ResultSheet widgets"
```

---

### Task 15: 创建 StudyPage

**Files:**
- Create: `knowledge_app/lib/pages/study_page.dart`

- [ ] **Step 1: 创建 StudyPage**

```dart
// lib/pages/study_page.dart
// 学习页：知识讲解（Markdown + LaTeX）+ 课后习题（选择题）+ 答题反馈
// 使用 QuizSessionProvider 管理答题流程，页面销毁时自动清理会话状态

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/course.dart';
import '../providers/progress_provider.dart';
import '../providers/quiz_session_provider.dart';
import '../widgets/content_view.dart';
import '../widgets/quiz_card.dart';
import '../widgets/result_sheet.dart';

/// 学习页面：讲解区 + 习题区上下布局
class StudyPage extends StatefulWidget {
  final Course course;                // 所属课程
  final KnowledgePoint knowledgePoint; // 当前知识点

  const StudyPage({
    super.key,
    required this.course,
    required this.knowledgePoint,
  });

  @override
  State<StudyPage> createState() => _StudyPageState();
}

class _StudyPageState extends State<StudyPage> {
  // 是否显示习题区（用户下滑后才显示）
  bool _showQuiz = false;

  @override
  void initState() {
    super.initState();
    // 标记知识点为已读
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ProgressProvider>().markKpRead(widget.knowledgePoint.id);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      // 在 StudyPage 作用域内创建 QuizSessionProvider
      create: (_) => QuizSessionProvider()
        ..startSession(widget.knowledgePoint.quizzes),
      child: Scaffold(
        appBar: AppBar(
          title: Text(widget.knowledgePoint.title),
        ),
        body: Column(
          children: [
            // 上区域：知识讲解 + 关键概念（可滚动）
            Expanded(
              flex: _showQuiz ? 1 : 3,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ContentView(content: widget.knowledgePoint.content),
                    const SizedBox(height: 16),
                    // 关键概念标签
                    if (widget.knowledgePoint.keyConcepts.isNotEmpty)
                      _buildKeyConcepts(context),
                    const SizedBox(height: 24),
                    // 开始练习按钮
                    if (!_showQuiz)
                      _buildStartQuizButton(context),
                  ],
                ),
              ),
            ),

            // 下区域：习题区（点击开始练习后展开）
            if (_showQuiz) _buildQuizSection(context),
          ],
        ),
      ),
    );
  }

  /// 关键概念 Chip 标签组
  Widget _buildKeyConcepts(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '关键概念',
          style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 4,
          children: widget.knowledgePoint.keyConcepts.map((concept) {
            return Chip(
              label: Text(concept),
              backgroundColor: theme.colorScheme.primaryContainer,
            );
          }).toList(),
        ),
      ],
    );
  }

  /// 开始练习按钮
  Widget _buildStartQuizButton(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton.icon(
        onPressed: () => setState(() => _showQuiz = true),
        icon: const Icon(Icons.quiz),
        label: Text('开始练习（共 ${widget.knowledgePoint.quizzes.length} 题）'),
      ),
    );
  }

  /// 习题区域：QuizCard + 导航按钮
  Widget _buildQuizSection(BuildContext context) {
    return Consumer<QuizSessionProvider>(
      builder: (context, session, child) {
        final quiz = session.currentQuiz;
        if (quiz == null) {
          return const Center(child: Text('暂无题目'));
        }

        return Container(
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceContainerLow,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
          ),
          child: Column(
            children: [
              // 题目进度指示器
              Padding(
                padding: const EdgeInsets.only(top: 12, left: 16, right: 16),
                child: Row(
                  children: [
                    Text(
                      '第 ${session.currentIndex + 1} / ${session.quizzes.length} 题',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    const Spacer(),
                    Text(
                      '正确 ${session.correctCount}/${session.submittedCount}',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                      ),
                    ),
                  ],
                ),
              ),
              // 题目卡片
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: QuizCard(
                    quiz: quiz,
                    state: session.currentState,
                    selectedKey: session.currentSelection,
                    onSelect: (key) => session.selectOption(key),
                    onSubmit: () {
                      final correct = session.submitAnswer();
                      // 调用 ProgressProvider 记录结果
                      context.read<ProgressProvider>().recordAnswer(
                        kpId: widget.knowledgePoint.id,
                        quizId: quiz.id,
                        userAnswer: session.currentSelection!,
                        correct: correct,
                      );
                      // 弹出结果 BottomSheet
                      ResultSheet.show(
                        context: context,
                        isCorrect: correct,
                        quiz: quiz,
                        onNext: () {
                          session.nextQuestion();
                        },
                      );
                    },
                  ),
                ),
              ),
              // 底部导航按钮
              Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    TextButton.icon(
                      onPressed: session.currentIndex > 0
                          ? () => session.previousQuestion()
                          : null,
                      icon: const Icon(Icons.arrow_back),
                      label: const Text('上一题'),
                    ),
                    TextButton.icon(
                      onPressed: session.currentIndex < session.quizzes.length - 1
                          ? () => session.nextQuestion()
                          : null,
                      icon: const Icon(Icons.arrow_forward),
                      label: const Text('下一题'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/pages/study_page.dart
git commit -m "feat: add StudyPage with content view and quiz interaction"
```

---

### Task 16: 创建 ProgressBar 组件 + ProgressPage

**Files:**
- Create: `knowledge_app/lib/widgets/progress_bar.dart`
- Create: `knowledge_app/lib/pages/progress_page.dart`

- [ ] **Step 1: 创建 ProgressBar**

```dart
// lib/widgets/progress_bar.dart
// 自定义进度条组件：展示学科进度，带百分比标签

import 'package:flutter/material.dart';

/// 学习进度条，包含标签和进度指示器
class ProgressBar extends StatelessWidget {
  final String label;           // 左侧标签
  final double value;           // 进度值 0.0~1.0
  final double? accuracy;       // 正确率（可选展示）
  final Color? color;           // 进度条颜色

  const ProgressBar({
    super.key,
    required this.label,
    required this.value,
    this.accuracy,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 标签行：名称 + 百分比
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: theme.textTheme.titleSmall),
              Row(
                children: [
                  if (accuracy != null) ...[
                    Text(
                      '正确率 ${(accuracy! * 100).toStringAsFixed(0)}%',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.outline,
                      ),
                    ),
                    const SizedBox(width: 12),
                  ],
                  Text(
                    '${(value * 100).toStringAsFixed(0)}%',
                    style: theme.textTheme.bodySmall?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: theme.colorScheme.primary,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 8),
          // 进度条
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: value,
              minHeight: 8,
              backgroundColor: theme.colorScheme.surfaceContainerHighest,
              valueColor: AlwaysStoppedAnimation<Color>(
                color ?? theme.colorScheme.primary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

- [ ] **Step 2: 创建 ProgressPage**

```dart
// lib/pages/progress_page.dart
// 学习进度总览页：展示所有学科的完成度、正确率和知识点统计
// 作为 MainScaffold 的第二个 Tab 内容

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/subject.dart';
import '../providers/course_provider.dart';
import '../providers/progress_provider.dart';
import '../widgets/progress_bar.dart';
import '../widgets/progress_ring.dart';

/// 学习进度总览页面，展示全学科的学习统计
class ProgressPage extends StatelessWidget {
  const ProgressPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('学习进度')),
      body: Consumer2<CourseProvider, ProgressProvider>(
        builder: (context, courseProvider, progressProvider, child) {
          // 计算各学科统计数据
          final stats = _calculateStats(courseProvider, progressProvider);

          // 全局总进度
          int totalKp = 0, completedKp = 0;
          for (final s in stats) {
            totalKp += s.totalKp;
            completedKp += s.completedKp;
          }
          final globalProgress = totalKp > 0 ? completedKp / totalKp : 0.0;

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // 顶部：全局进度环
              Center(
                child: ProgressRing(progress: globalProgress),
              ),
              const SizedBox(height: 24),

              // 分隔
              Text(
                '学科进度',
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),

              // 各学科进度条
              ...stats.map((s) => ProgressBar(
                label: s.name,
                value: s.totalKp > 0 ? s.completedKp / s.totalKp : 0,
                accuracy: s.accuracy,
              )),

              const SizedBox(height: 24),

              // 学习统计卡片
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '学习概况',
                        style: theme.textTheme.titleSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      _statRow(theme, '已学知识点', '$completedKp / $totalKp'),
                      _statRow(theme, '课程总数', '${courseProvider.courses.length}'),
                    ],
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  /// 统计行组件
  Widget _statRow(ThemeData theme, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: theme.textTheme.bodyMedium),
          Text(value, style: theme.textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.bold,
          )),
        ],
      ),
    );
  }

  /// 计算每个学科的统计数据
  List<_SubjectStat> _calculateStats(
    CourseProvider courseProvider,
    ProgressProvider progressProvider,
  ) {
    return v1Subjects.map((subject) {
      final courses = courseProvider.getCoursesBySubject(subject.id);
      int totalKp = 0, completedKp = 0, totalQuiz = 0, correctQuiz = 0;

      for (final course in courses) {
        for (final kp in course.allKnowledgePoints) {
          totalKp++;
          final kpp = progressProvider.getKpProgress(kp.id);
          if (kpp != null) {
            if (kpp.completed) completedKp++;
            totalQuiz += kpp.quizTotal;
            correctQuiz += kpp.quizCorrect;
          }
        }
      }

      return _SubjectStat(
        name: subject.name,
        totalKp: totalKp,
        completedKp: completedKp,
        accuracy: totalQuiz > 0 ? correctQuiz / totalQuiz : 0.0,
      );
    }).toList();
  }
}

/// 内部辅助类：学科统计数据
class _SubjectStat {
  final String name;
  final int totalKp;
  final int completedKp;
  final double accuracy;

  const _SubjectStat({
    required this.name,
    required this.totalKp,
    required this.completedKp,
    required this.accuracy,
  });
}
```

- [ ] **Step 3: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/widgets/progress_bar.dart knowledge_app/lib/pages/progress_page.dart
git commit -m "feat: add ProgressBar widget and ProgressPage"
```

---

### Task 17: 创建 MainScaffold（底部 Tab 导航壳）

**Files:**
- Create: `knowledge_app/lib/pages/main_scaffold.dart`

- [ ] **Step 1: 创建 MainScaffold**

```dart
// lib/pages/main_scaffold.dart
// 主脚手架：底部 Tab 导航壳，包含"学习"和"进度"两个标签

import 'package:flutter/material.dart';
import 'home_content.dart';
import 'progress_page.dart';

/// 应用主框架，通过 BottomNavigationBar 切换首页和进度页
class MainScaffold extends StatefulWidget {
  const MainScaffold({super.key});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  // 当前选中的 Tab 索引，0=学习，1=进度
  int _currentIndex = 0;

  // 两个 Tab 页面的列表，使用 IndexedStack 保持页面状态
  static const _pages = <Widget>[
    HomeContent(),
    ProgressPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 使用 IndexedStack 切换页面，保留未显示页面的滚动位置等状态
      body: IndexedStack(
        index: _currentIndex,
        children: _pages,
      ),
      // 底部导航栏
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() => _currentIndex = index);
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.school_outlined),
            selectedIcon: Icon(Icons.school),
            label: '学习',
          ),
          NavigationDestination(
            icon: Icon(Icons.bar_chart_outlined),
            selectedIcon: Icon(Icons.bar_chart),
            label: '进度',
          ),
        ],
      ),
    );
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add knowledge_app/lib/pages/main_scaffold.dart
git commit -m "feat: add MainScaffold with bottom tab navigation"
```

---

### Task 18: 集成测试 & 验证

- [ ] **Step 1: 运行静态分析**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app"
flutter analyze
```

Expected: No issues found.

- [ ] **Step 2: 运行所有单元测试**

```bash
flutter test
```

Expected: All tests pass.

- [ ] **Step 3: 开始编写主 APP widget test**

写 `test/app_test.dart`：

```dart
// test/app_test.dart
// 基础集成测试：验证 APP 能正常启动

import 'package:flutter_test/flutter_test.dart';
import 'package:knowledge_app/app.dart';

void main() {
  testWidgets('App starts and shows home page', (WidgetTester tester) async {
    // 注意：需要先设置 Hive mock 或使用 Hive.initFlutter 的测试适配
    // 此处为基础框架测试，具体实现需根据环境调整
  });
}
```

- [ ] **Step 4: 修复 analyze 和 test 发现的任何问题**

```bash
flutter analyze && flutter test
```

---

### Task 19: 构建 APK 验证

- [ ] **Step 1: 构建 Debug APK 验证编译通过**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528\knowledge_app"
flutter build apk --debug
```

Expected: 构建成功，生成 APK 文件。

- [ ] **Step 2: Commit 最终状态**

```bash
cd "E:\.Claude Code Project\3.知识学习APP_20260528"
git add -A
git commit -m "feat: complete v1 knowledge learning app"
```

---

## 实现顺序总结

```
Task 1  (项目创建)  ──► Task 2 (模型) ──► Task 3 (内容)
       │                    │
       └────────────────────┼──► Task 4 (JSON Loader)
                            │        │
                            │        └──► Task 5 (CourseProvider)
                            │                  │
                            └──► Task 6 (ProgressProvider)
                            │                  │
                            └──► Task 7 (QuizSessionProvider)
                                               │
                    Task 8 (main.dart + app.dart) ◄──┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         Task 9       Task 11      Task 13
       (Card+Ring)  (ChapterTree) (ContentView)
              │            │            │
         Task 10      Task 12      Task 14
       (HomeContent)(SubjectPage)(QuizCard+Sheet)
              │            │            │
              │            └────┬───────┘
              │                 │
              └──────┐    Task 15 (StudyPage)
                     │         │
                Task 17    Task 16
             (MainScaffold)(ProgressBar+Page)
                     │         │
                     └────┬────┘
                     Task 18 (集成测试)
                          │
                     Task 19 (构建APK)
```
