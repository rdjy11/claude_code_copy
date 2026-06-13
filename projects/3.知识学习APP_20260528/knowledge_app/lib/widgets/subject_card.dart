// 学科入口卡片组件：显示学科图标、名称、课程数和进度信息

import 'package:flutter/material.dart';
import '../models/subject.dart';

/// 学科入口卡片，用于首页展示各学科的入口和进度概览
class SubjectCard extends StatelessWidget {
  final SubjectInfo subject;
  final double progress;
  final double accuracy;
  final VoidCallback onTap;

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
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              // 顶部：图标 + 学科名称 + 箭头
              Row(
                children: [
                  Icon(_getIconData(subject.iconName), color: theme.colorScheme.primary, size: 28),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(subject.name, style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                  ),
                  Icon(Icons.chevron_right, color: theme.colorScheme.outline),
                ],
              ),
              const SizedBox(height: 12),
              // 进度条
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: progress, minHeight: 6,
                  backgroundColor: theme.colorScheme.surfaceContainerHighest,
                ),
              ),
              const SizedBox(height: 8),
              // 底部：课程数和正确率
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('${subject.courseIds.length}门课程', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.outline)),
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
        ),
      ),
    );
  }

  /// 根据字符串名称获取 Material Icons 图标
  IconData _getIconData(String name) {
    switch (name) {
      case 'functions': return Icons.functions;
      case 'translate': return Icons.translate;
      case 'menu_book': return Icons.menu_book;
      case 'account_balance': return Icons.account_balance;
      default: return Icons.school;
    }
  }
}
