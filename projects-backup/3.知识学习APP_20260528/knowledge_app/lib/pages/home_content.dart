// 首页内容：学科卡片网格 + 顶部总进度环，作为 MainScaffold 的第一个 Tab 内容

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

        // 计算全局总进度
        int totalKp = 0, completedKp = 0;
        for (final s in stats) {
          totalKp += s.totalKp;
          completedKp += s.completedKp;
        }
        final globalProgress = totalKp > 0 ? completedKp / totalKp : 0.0;

        return Scaffold(
          appBar: AppBar(title: const Text('知识学习')),
          body: SafeArea(
            child: CustomScrollView(
              slivers: [
                // 顶部进度区域
                SliverToBoxAdapter(child: _buildHeader(context, globalProgress)),
                // 学科卡片网格
                SliverPadding(
                  padding: const EdgeInsets.all(16),
                  sliver: SliverGrid(
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2, mainAxisSpacing: 12, crossAxisSpacing: 12, childAspectRatio: 1.05,
                    ),
                    delegate: SliverChildBuilderDelegate(
                      (context, index) {
                        final stat = stats[index];
                        return SubjectCard(
                          subject: stat.subject,
                          progress: stat.totalKp > 0 ? stat.completedKp / stat.totalKp : 0,
                          accuracy: stat.accuracy,
                          onTap: () {
                            Navigator.push(context, MaterialPageRoute(builder: (_) => SubjectPage(subject: stat.subject)));
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

  /// 构建顶部进度头部：进度环 + 鼓励语
  Widget _buildHeader(BuildContext context, double globalProgress) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Column(
          children: [
            ProgressRing(progress: globalProgress),
            const SizedBox(height: 12),
            Text('坚持学习，每天进步', style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.outline)),
          ],
        ),
      ),
    );
  }

  /// 计算每个学科的进度统计
  List<_SubjectStatEntry> _calculateStats(CourseProvider courseProvider, ProgressProvider progressProvider) {
    final result = <_SubjectStatEntry>[];
    for (final subject in v1Subjects) {
      final courses = courseProvider.getCoursesBySubject(subject.id);
      int totalKp = 0;
      for (final course in courses) {
        totalKp += course.allKnowledgePoints.length;
      }
      int completedKp = 0, totalQuiz = 0, correctQuiz = 0;
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
      result.add(_SubjectStatEntry(subject: subject, totalKp: totalKp, completedKp: completedKp, accuracy: accuracy));
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
  const _SubjectStatEntry({required this.subject, required this.totalKp, required this.completedKp, required this.accuracy});
}
