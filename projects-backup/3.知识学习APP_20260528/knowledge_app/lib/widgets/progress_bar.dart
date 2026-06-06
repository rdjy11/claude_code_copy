// 学科进度条组件：展示学科名称、线性进度条和正确率

import 'package:flutter/material.dart';

/// 学科进度条，用于进度总览页展示单个学科的完成度和正确率
class ProgressBar extends StatelessWidget {
  final String label;
  final double value;
  final double accuracy;

  const ProgressBar({
    super.key,
    required this.label,
    required this.value,
    required this.accuracy,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 标签行：学科名称 + 进度百分比 + 正确率
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w500)),
              Row(
                children: [
                  Text(
                    '${(value * 100).toStringAsFixed(0)}%',
                    style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.primary),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    '正确率 ${(accuracy * 100).toStringAsFixed(0)}%',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: accuracy >= 0.6 ? theme.colorScheme.primary : theme.colorScheme.error,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 6),
          // 线性进度条
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: value,
              minHeight: 8,
              backgroundColor: theme.colorScheme.surfaceContainerHighest,
            ),
          ),
        ],
      ),
    );
  }
}
