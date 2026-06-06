// 知识内容渲染组件：支持 Markdown 文本和 LaTeX 数学公式的混合渲染

import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter_math_fork/flutter_math.dart';

/// 混合渲染 Markdown 和 LaTeX 的内容视图
class ContentView extends StatelessWidget {
  final String content;

  const ContentView({super.key, required this.content});

  @override
  Widget build(BuildContext context) {
    final parts = _splitContent(content);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: parts.map((part) {
        if (part.isFormula) {
          // 渲染 LaTeX 数学公式，居中显示
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Center(
              child: Math.tex(part.text, mathStyle: MathStyle.display, textScaleFactor: 1.2),
            ),
          );
        } else {
          // 渲染 Markdown 文本
          return MarkdownBody(
            data: part.text,
            selectable: true,
            styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
              h2: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
              p: Theme.of(context).textTheme.bodyLarge?.copyWith(height: 1.8),
            ),
          );
        }
      }).toList(),
    );
  }

  /// 将内容按 $$...$$ 分隔符拆分为文本/公式段落列表
  List<_ContentPart> _splitContent(String text) {
    final parts = <_ContentPart>[];
    final regex = RegExp(r'\$\$([\s\S]*?)\$\$');
    int lastEnd = 0;

    for (final match in regex.allMatches(text)) {
      if (match.start > lastEnd) {
        parts.add(_ContentPart(text: text.substring(lastEnd, match.start).trim(), isFormula: false));
      }
      parts.add(_ContentPart(text: match.group(1)?.trim() ?? '', isFormula: true));
      lastEnd = match.end;
    }

    if (lastEnd < text.length) {
      parts.add(_ContentPart(text: text.substring(lastEnd).trim(), isFormula: false));
    }

    return parts;
  }
}

/// 内容段落的内部表示
class _ContentPart {
  final String text;
  final bool isFormula;
  const _ContentPart({required this.text, required this.isFormula});
}
