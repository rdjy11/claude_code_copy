// 学习进度模型：记录知识点学习状态和每道题的作答记录

/// 知识点学习进度：记录单个知识点的完成状态和答题统计
class KpProgress {
  final String kpId;
  bool completed;
  int quizTotal;
  int quizCorrect;
  DateTime lastStudy;

  KpProgress({
    required this.kpId,
    this.completed = false,
    this.quizTotal = 0,
    this.quizCorrect = 0,
    DateTime? lastStudy,
  }) : lastStudy = lastStudy ?? DateTime.now();

  double get accuracy => quizTotal > 0 ? quizCorrect / quizTotal : 0.0;

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
  final String quizId;
  final String userAnswer;
  final bool correct;
  final DateTime timestamp;

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
  final String subjectId;
  final String subjectName;
  final int totalKp;
  final int completedKp;
  final double accuracy;

  const SubjectStats({
    required this.subjectId,
    required this.subjectName,
    required this.totalKp,
    required this.completedKp,
    required this.accuracy,
  });
}
