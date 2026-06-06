// 学习进度总览页：展示所有学科的完成度、正确率和知识点统计

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
              Center(child: ProgressRing(progress: globalProgress)),
              const SizedBox(height: 24),
              // 分隔
              Text('学科进度', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              // 各学科进度条
              ...stats.map((s) => ProgressBar(
                label: s.name, value: s.totalKp > 0 ? s.completedKp / s.totalKp : 0, accuracy: s.accuracy,
              )),
              const SizedBox(height: 24),
              // 学习统计卡片
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('学习概况', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
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
          Text(value, style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  /// 计算每个学科的统计数据
  List<_SubjectStat> _calculateStats(CourseProvider courseProvider, ProgressProvider progressProvider) {
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
      return _SubjectStat(name: subject.name, totalKp: totalKp, completedKp: completedKp, accuracy: totalQuiz > 0 ? correctQuiz / totalQuiz : 0.0);
    }).toList();
  }
}

/// 内部辅助类：学科统计数据
class _SubjectStat {
  final String name;
  final int totalKp;
  final int completedKp;
  final double accuracy;
  const _SubjectStat({required this.name, required this.totalKp, required this.completedKp, required this.accuracy});
}
