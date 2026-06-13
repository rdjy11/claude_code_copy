// 课程内容模型：定义 Course → Chapter → Section → KnowledgePoint 的层次结构
// 通过 structure_type 字段区分 hierarchical（三级）和 flat（二级）两种模式

import 'quiz.dart';

/// 知识点：最小的学习单元，包含讲解内容和配套习题
class KnowledgePoint {
  final String id;
  final String title;
  final String contentType;
  final String content;
  final List<String> keyConcepts;
  final List<Quiz> quizzes;

  const KnowledgePoint({
    required this.id,
    required this.title,
    required this.contentType,
    required this.content,
    required this.keyConcepts,
    required this.quizzes,
  });

  factory KnowledgePoint.fromJson(Map<String, dynamic> json) {
    return KnowledgePoint(
      id: json['id'] as String,
      title: json['title'] as String,
      contentType: (json['content_type'] as String?) ?? 'markdown',
      content: json['content'] as String,
      keyConcepts: (json['key_concepts'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ?? [],
      quizzes: (json['quizzes'] as List<dynamic>?)
              ?.map((q) => Quiz.fromJson(q as Map<String, dynamic>))
              .toList() ?? [],
    );
  }
}

/// 节：包含若干知识点，仅在 hierarchical 模式下存在
class Section {
  final String id;
  final String title;
  final List<KnowledgePoint> knowledgePoints;

  const Section({required this.id, required this.title, required this.knowledgePoints});

  factory Section.fromJson(Map<String, dynamic> json) {
    return Section(
      id: json['id'] as String,
      title: json['title'] as String,
      knowledgePoints: (json['knowledge_points'] as List<dynamic>)
          .map((kp) => KnowledgePoint.fromJson(kp as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// 章：在 hierarchical 模式下包含节，在 flat 模式下直接包含知识点
class Chapter {
  final String id;
  final String title;
  final List<Section> sections;
  final List<KnowledgePoint> knowledgePoints;

  const Chapter({
    required this.id,
    required this.title,
    required this.sections,
    required this.knowledgePoints,
  });

  bool get isHierarchical => sections.isNotEmpty;

  factory Chapter.fromJson(Map<String, dynamic> json) {
    return Chapter(
      id: json['id'] as String,
      title: json['title'] as String,
      sections: (json['sections'] as List<dynamic>?)
              ?.map((s) => Section.fromJson(s as Map<String, dynamic>))
              .toList() ?? [],
      knowledgePoints: (json['knowledge_points'] as List<dynamic>?)
              ?.map((kp) => KnowledgePoint.fromJson(kp as Map<String, dynamic>))
              .toList() ?? [],
    );
  }
}

/// 结构类型：hierarchical = 章→节→知识点，flat = 章→知识点
enum StructureType { hierarchical, flat }

/// 课程：一门完整的学科课程，包含其结构和章列表
class Course {
  final String courseId;
  final String courseName;
  final String subjectId;
  final StructureType structureType;
  final List<Chapter> chapters;

  const Course({
    required this.courseId,
    required this.courseName,
    required this.subjectId,
    required this.structureType,
    required this.chapters,
  });

  // 获取课程下所有知识点的扁平列表
  List<KnowledgePoint> get allKnowledgePoints {
    final List<KnowledgePoint> result = [];
    for (final chapter in chapters) {
      if (chapter.isHierarchical) {
        for (final section in chapter.sections) {
          result.addAll(section.knowledgePoints);
        }
      } else {
        result.addAll(chapter.knowledgePoints);
      }
    }
    return result;
  }

  // 获取课程下所有习题的扁平列表
  List<Quiz> get allQuizzes {
    return allKnowledgePoints.expand((kp) => kp.quizzes).toList();
  }

  factory Course.fromJson(Map<String, dynamic> json) {
    final structureStr = json['structure_type'] as String? ?? 'flat';
    return Course(
      courseId: json['course_id'] as String,
      courseName: json['course_name'] as String,
      subjectId: json['subject_id'] as String,
      structureType: structureStr == 'hierarchical'
          ? StructureType.hierarchical
          : StructureType.flat,
      chapters: (json['chapters'] as List<dynamic>)
          .map((c) => Chapter.fromJson(c as Map<String, dynamic>))
          .toList(),
    );
  }
}
