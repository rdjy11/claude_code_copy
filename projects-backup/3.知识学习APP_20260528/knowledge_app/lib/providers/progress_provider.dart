// 学习进度状态管理：通过 Hive 持久化学习进度和答题记录，提供统计计算能力

import 'package:flutter/foundation.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/progress.dart';

/// 进度管理器，负责读写学习进度并按维度计算统计数据
class ProgressProvider extends ChangeNotifier {
  final Map<String, KpProgress> _kpProgress = {};
  final Map<String, QuizRecord> _quizRecords = {};

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

  /// 记录一条答题结果，同时更新知识点进度
  void recordAnswer({
    required String kpId,
    required String quizId,
    required String userAnswer,
    required bool correct,
  }) {
    final record = QuizRecord(
      quizId: quizId,
      userAnswer: userAnswer,
      correct: correct,
      timestamp: DateTime.now(),
    );
    _quizRecords[quizId] = record;
    _quizBox.put(quizId, record.toJson());

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

  /// 获取单题的答题记录
  QuizRecord? getQuizRecord(String quizId) => _quizRecords[quizId];

  /// 计算某学科的聚合统计数据
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
