// 选择题题卡组件：展示题目、选项列表、提交按钮

import 'package:flutter/material.dart';
import '../models/quiz.dart';
import '../providers/quiz_session_provider.dart';

/// 选择题题卡，展示单道单选题的完整交互
class QuizCard extends StatelessWidget {
  final Quiz quiz;
  final QuizState state;
  final String? selectedKey;
  final void Function(String key) onSelect;
  final VoidCallback onSubmit;

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
        // 题目文本
        Text(quiz.question, style: theme.textTheme.titleMedium?.copyWith(height: 1.6)),
        const SizedBox(height: 20),
        // 选项列表
        ...quiz.options.map((option) {
          final isSelected = selectedKey == option.key;
          final isCorrect = option.key == quiz.answer;
          // 提交后：绿色=正确选项，红色=选中但错误
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
                backgroundColor: isSelected ? theme.colorScheme.primary : theme.colorScheme.surfaceContainerHighest,
                child: Text(option.key, style: TextStyle(color: isSelected ? Colors.white : theme.colorScheme.onSurface, fontWeight: FontWeight.bold)),
              ),
              title: Text(option.text),
              trailing: state == QuizState.submitted && isCorrect ? const Icon(Icons.check_circle, color: Colors.green) : null,
              onTap: state != QuizState.submitted ? () => onSelect(option.key) : null,
            ),
          );
        }),
        const SizedBox(height: 16),
        // 提交按钮
        SizedBox(
          width: double.infinity,
          child: FilledButton(
            onPressed: state == QuizState.answered ? onSubmit : null,
            child: Text(state == QuizState.submitted ? '已提交' : '提交答案'),
          ),
        ),
      ],
    );
  }
}
