// 课程内容状态管理：负责加载和缓存所有课程数据

import 'package:flutter/foundation.dart';
import '../models/course.dart';
import '../models/subject.dart';
import '../utils/json_loader.dart';

/// 课程内容提供者，管理所有课程的加载、缓存和查询
class CourseProvider extends ChangeNotifier {
  // 已加载的课程缓存，key 为 courseId
  final Map<String, Course> _courses = {};

  // 加载状态标志
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  // 最后一次加载的错误信息
  String? _error;
  String? get error => _error;

  /// 获取所有已加载的课程列表
  List<Course> get courses => _courses.values.toList();

  /// 根据 courseId 获取课程（先确保 loadCourse 已完成）
  Course? getCourse(String courseId) => _courses[courseId];

  /// 加载所有 v1 学科的全部课程，并行加载提升性能
  Future<void> loadAllCourses() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final courseIds = v1Subjects.expand((s) => s.courseIds).toSet();
      final futures = courseIds.map((id) => JsonLoader.loadCourse(id));
      final results = await Future.wait(futures);

      for (final course in results) {
        _courses[course.courseId] = course;
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 获取某学科的所有课程列表
  List<Course> getCoursesBySubject(String subjectId) {
    final courseIds = v1Subjects
        .firstWhere((s) => s.id == subjectId)
        .courseIds;
    return courseIds
        .where((id) => _courses.containsKey(id))
        .map((id) => _courses[id]!)
        .toList();
  }
}
