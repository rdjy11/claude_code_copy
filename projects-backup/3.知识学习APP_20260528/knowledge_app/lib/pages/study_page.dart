// 学习页：知识讲解（Markdown + LaTeX）+ 课后习题（选择题）+ 答题反馈

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
  final Course course;
  final KnowledgePoint knowledgePoint;

  const StudyPage({super.key, required this.course, required this.knowledgePoint});

  @override
  State<StudyPage> createState() => _StudyPageState();
}

class _StudyPageState extends State<StudyPage> {
  // 是否显示习题区
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
      create: (_) => QuizSessionProvider()..startSession(widget.knowledgePoint.quizzes),
      child: Scaffold(
        appBar: AppBar(title: Text(widget.knowledgePoint.title)),
        body: Column(
          children: [
            // 上区域：知识讲解 + 关键概念
            Expanded(
              flex: _showQuiz ? 1 : 3,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ContentView(content: widget.knowledgePoint.content),
                    const SizedBox(height: 16),
                    if (widget.knowledgePoint.keyConcepts.isNotEmpty) _buildKeyConcepts(context),
                    const SizedBox(height: 24),
                    if (!_showQuiz) _buildStartQuizButton(context),
                  ],
                ),
              ),
            ),
            // 下区域：习题区
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
        Text('关键概念', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8, runSpacing: 4,
          children: widget.knowledgePoint.keyConcepts.map((concept) {
            return Chip(label: Text(concept), backgroundColor: theme.colorScheme.primaryContainer);
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
        if (quiz == null) return const Center(child: Text('暂无题目'));

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
                    Text('第 ${session.currentIndex + 1} / ${session.quizzes.length} 题', style: Theme.of(context).textTheme.bodySmall),
                    const Spacer(),
                    Text('正确 ${session.correctCount}/${session.submittedCount}', style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Theme.of(context).colorScheme.primary)),
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
                      context.read<ProgressProvider>().recordAnswer(
                        kpId: widget.knowledgePoint.id,
                        quizId: quiz.id,
                        userAnswer: session.currentSelection!,
                        correct: correct,
                      );
                      ResultSheet.show(
                        context: context,
                        isCorrect: correct,
                        quiz: quiz,
                        onNext: () => session.nextQuestion(),
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
                      onPressed: session.currentIndex > 0 ? () => session.previousQuestion() : null,
                      icon: const Icon(Icons.arrow_back), label: const Text('上一题'),
                    ),
                    TextButton.icon(
                      onPressed: session.currentIndex < session.quizzes.length - 1 ? () => session.nextQuestion() : null,
                      icon: const Icon(Icons.arrow_forward), label: const Text('下一题'),
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
