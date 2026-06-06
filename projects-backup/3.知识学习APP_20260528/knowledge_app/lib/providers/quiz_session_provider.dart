// 答题会话状态管理：管理单次学习中的答题流程，生命周期限定在 StudyPage 范围内

import 'package:flutter/foundation.dart';
import '../models/quiz.dart';

/// 单道题的答题状态枚举
enum QuizState { unanswered, answered, submitted }

/// 答题会话提供者，管理当前知识点下的答题流程
class QuizSessionProvider extends ChangeNotifier {
  List<Quiz> _quizzes = [];
  List<Quiz> get quizzes => _quizzes;

  int _currentIndex = 0;
  int get currentIndex => _currentIndex;

  final Map<int, String?> _selections = {};
  final Map<int, QuizState> _states = {};

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
    if (currentState == QuizState.submitted) return;
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

  /// 切换到下一题，返回 true 表示切换成功
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
