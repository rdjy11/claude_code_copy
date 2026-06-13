// 习题模型：定义题目、选项、答案和解析的数据结构
// 通过 QuizType 枚举预留题型扩展能力

// ignore_for_file: constant_identifier_names

/// 题型枚举，v1 仅 single_choice，后续可扩展 multi_choice / fill_blank
enum QuizType { single_choice }

/// 单个选项的数据结构
class QuizOption {
  final String key;   // 选项标识，如 "A", "B", "C", "D"
  final String text;  // 选项文本内容

  const QuizOption({required this.key, required this.text});

  // 从 JSON Map 构造 QuizOption 实例
  factory QuizOption.fromJson(Map<String, dynamic> json) {
    return QuizOption(
      key: json['key'] as String,
      text: json['text'] as String,
    );
  }

  Map<String, dynamic> toJson() => {'key': key, 'text': text};
}

/// 习题数据结构
class Quiz {
  final String id;           // 题目唯一 ID
  final QuizType type;       // 题型
  final String question;     // 题目内容（Markdown）
  final List<QuizOption> options;  // 选项列表
  final String answer;       // 正确答案 key
  final String explanation;  // 解析内容（Markdown）

  const Quiz({
    required this.id,
    required this.type,
    required this.question,
    required this.options,
    required this.answer,
    required this.explanation,
  });

  // 从 JSON Map 构造 Quiz 实例，自动解析 options 数组
  factory Quiz.fromJson(Map<String, dynamic> json) {
    return Quiz(
      id: json['id'] as String,
      type: QuizType.single_choice,
      question: json['question'] as String,
      options: (json['options'] as List<dynamic>)
          .map((o) => QuizOption.fromJson(o as Map<String, dynamic>))
          .toList(),
      answer: json['answer'] as String,
      explanation: json['explanation'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'type': 'single_choice',
    'question': question,
    'options': options.map((o) => o.toJson()).toList(),
    'answer': answer,
    'explanation': explanation,
  };
}
