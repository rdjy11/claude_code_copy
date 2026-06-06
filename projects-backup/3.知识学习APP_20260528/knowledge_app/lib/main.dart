// APP 入口：初始化 Hive 数据库、注册 Provider、启动应用

import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';
import 'providers/course_provider.dart';
import 'providers/progress_provider.dart';
import 'app.dart';

void main() async {
  // 确保 Flutter 绑定初始化完成
  WidgetsFlutterBinding.ensureInitialized();

  // 初始化 Hive 数据库存储路径
  await Hive.initFlutter();

  // 创建 Provider 实例
  final courseProvider = CourseProvider();
  final progressProvider = ProgressProvider();

  // 初始化进度数据（从 Hive 恢复）
  await progressProvider.init();

  // 启动加载所有课程内容（异步执行，不阻塞 UI）
  courseProvider.loadAllCourses();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: courseProvider),
        ChangeNotifierProvider.value(value: progressProvider),
      ],
      child: const KnowledgeApp(),
    ),
  );
}
