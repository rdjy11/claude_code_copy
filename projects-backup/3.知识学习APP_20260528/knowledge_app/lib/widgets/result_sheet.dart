// 答题结果底部弹窗：展示对/错结果、正确答案和解析

import 'package:flutter/material.dart';
import '../models/quiz.dart';

/// 答题结果 BottomSheet，提交答案后弹出展示结果和解析
class ResultSheet extends StatelessWidget {
  final bool isCorrect;
  final Quiz quiz;
  final VoidCallback onNext;

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
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (_) => ResultSheet(isCorrect: isCorrect, quiz: quiz, onNext: onNext),
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
              Icon(isCorrect ? Icons.check_circle : Icons.cancel, color: isCorrect ? Colors.green : Colors.red, size: 36),
              const SizedBox(width: 12),
              Text(isCorrect ? '回答正确！' : '回答错误', style: theme.textTheme.headlineSmall?.copyWith(color: isCorrect ? Colors.green : Colors.red, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 16),
          // 正确答案
          Text('正确答案：${quiz.answer}', style: theme.textTheme.titleMedium?.copyWith(color: theme.colorScheme.primary)),
          const SizedBox(height: 12),
          // 解析
          Text('解析', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          Text(quiz.explanation, style: theme.textTheme.bodyMedium?.copyWith(height: 1.6)),
          const SizedBox(height: 24),
          // 下一题按钮
          SizedBox(width: double.infinity, child: FilledButton(onPressed: () { Navigator.pop(context); onNext(); }, child: const Text('下一题'))),
        ],
      ),
    );
  }
}
