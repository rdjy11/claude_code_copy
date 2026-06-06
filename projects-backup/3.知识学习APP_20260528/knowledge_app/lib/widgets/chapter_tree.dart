// 章节树组件：根据课程的 structure_type 自适应渲染章节结构

import 'package:flutter/material.dart';
import '../models/course.dart';

/// 章节树组件，支持 hierarchical 和 flat 两种结构的渲染
class ChapterTree extends StatelessWidget {
  final Course course;
  final void Function(KnowledgePoint kp) onKpTap;

  const ChapterTree({super.key, required this.course, required this.onKpTap});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: course.chapters.length,
      itemBuilder: (context, index) {
        final chapter = course.chapters[index];
        return _ChapterTile(chapter: chapter, onKpTap: onKpTap);
      },
    );
  }
}

/// 章级别条目：使用 ExpansionTile 展开
class _ChapterTile extends StatelessWidget {
  final Chapter chapter;
  final void Function(KnowledgePoint kp) onKpTap;

  const _ChapterTile({required this.chapter, required this.onKpTap});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: ExpansionTile(
        leading: Icon(Icons.menu_book, color: theme.colorScheme.primary),
        title: Text(chapter.title, style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
        // 根据章节结构模式渲染不同的子条目
        children: chapter.isHierarchical
            ? chapter.sections.map((section) => _SectionTile(section: section, onKpTap: onKpTap)).toList()
            : chapter.knowledgePoints.map((kp) => _KpTile(kp: kp, onTap: () => onKpTap(kp))).toList(),
      ),
    );
  }
}

/// 节级别条目（仅在 hierarchical 模式下使用）
class _SectionTile extends StatelessWidget {
  final Section section;
  final void Function(KnowledgePoint kp) onKpTap;

  const _SectionTile({required this.section, required this.onKpTap});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 16),
      child: ExpansionTile(
        leading: const Icon(Icons.article_outlined, size: 20),
        title: Text(section.title),
        children: section.knowledgePoints.map((kp) => _KpTile(kp: kp, onTap: () => onKpTap(kp), indent: 32)).toList(),
      ),
    );
  }
}

/// 知识点条目：点击进入学习页
class _KpTile extends StatelessWidget {
  final KnowledgePoint kp;
  final VoidCallback onTap;
  final double indent;

  const _KpTile({required this.kp, required this.onTap, this.indent = 16});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListTile(
      contentPadding: EdgeInsets.only(left: indent + 16, right: 16),
      leading: Icon(Icons.circle, size: 8, color: theme.colorScheme.primary),
      title: Text(kp.title, style: theme.textTheme.bodyMedium),
      trailing: Text('${kp.quizzes.length} 题', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.outline)),
      onTap: onTap,
    );
  }
}
