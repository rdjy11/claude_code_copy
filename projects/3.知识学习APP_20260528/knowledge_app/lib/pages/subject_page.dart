// 学科页：展示某学科下所有课程的章节树

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/subject.dart';
import '../providers/course_provider.dart';
import '../widgets/chapter_tree.dart';
import 'study_page.dart';

/// 学科详情页，展示课程列表及其章节树结构
class SubjectPage extends StatelessWidget {
  final SubjectInfo subject;

  const SubjectPage({super.key, required this.subject});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(subject.name)),
      body: Consumer<CourseProvider>(
        builder: (context, courseProvider, child) {
          final courses = courseProvider.getCoursesBySubject(subject.id);

          if (courses.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }

          return ChapterTree(
            course: courses.first,
            onKpTap: (kp) {
              Navigator.push(context, MaterialPageRoute(
                builder: (_) => StudyPage(course: courses.first, knowledgePoint: kp),
              ));
            },
          );
        },
      ),
    );
  }
}
