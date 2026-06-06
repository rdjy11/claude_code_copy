// MaterialApp 配置：主题、路由、Provider 注入

import 'package:flutter/material.dart';
import 'pages/main_scaffold.dart';

class KnowledgeApp extends StatelessWidget {
  const KnowledgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '知识学习',
      debugShowCheckedModeBanner: false,
      // 主题配置：蓝色主色调，符合学习类 APP 的安静专业气质
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1565C0),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const MainScaffold(),
    );
  }
}
