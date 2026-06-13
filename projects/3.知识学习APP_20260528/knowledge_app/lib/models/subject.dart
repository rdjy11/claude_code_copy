// 学科聚合模型：一个学科可包含多门课程，用于组织首页入口和课程分发

/// 学科入口信息，聚合该学科下所有课程的元数据
class SubjectInfo {
  final String id;
  final String name;
  final String iconName;
  final List<String> courseIds;

  const SubjectInfo({
    required this.id,
    required this.name,
    required this.iconName,
    required this.courseIds,
  });
}

// 预定义的 4 个 v1 学科入口
const List<SubjectInfo> v1Subjects = [
  SubjectInfo(
    id: 'math', name: '数学', iconName: 'functions', courseIds: ['calculus'],
  ),
  SubjectInfo(
    id: 'english', name: '英语', iconName: 'translate', courseIds: ['cet6'],
  ),
  SubjectInfo(
    id: 'chinese', name: '语文', iconName: 'menu_book', courseIds: ['poetry'],
  ),
  SubjectInfo(
    id: 'politics', name: '政治', iconName: 'account_balance', courseIds: ['marxism'],
  ),
];
