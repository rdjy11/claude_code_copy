// JSON 内容加载工具：从 assets 中读取 JSON 文件并解析为 Course 模型

import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import '../models/course.dart';

/// 课程内容加载器，负责从 assets/content/ 读取并解析 JSON 文件
class JsonLoader {
  /// 根据课程 ID 构建文件路径
  static String _filePath(String courseId) {
    const mapping = {
      'calculus': 'assets/content/math_calculus.json',
      'cet6': 'assets/content/english_cet6.json',
      'poetry': 'assets/content/chinese_poetry.json',
      'marxism': 'assets/content/politics_marxism.json',
    };
    final path = mapping[courseId];
    if (path == null) {
      throw ArgumentError('Unknown course ID: $courseId');
    }
    return path;
  }

  /// 从 assets 加载并解析单门课程，返回解析完成的 Course 对象
  static Future<Course> loadCourse(String courseId) async {
    final path = _filePath(courseId);
    final jsonStr = await rootBundle.loadString(path);
    final jsonMap = json.decode(jsonStr) as Map<String, dynamic>;
    return Course.fromJson(jsonMap);
  }
}
