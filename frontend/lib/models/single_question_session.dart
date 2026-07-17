class SingleQuestionSession {
  const SingleQuestionSession({
    required this.userId,
    required this.category,
    required this.area,
    required this.title,
    required this.question,
    required this.selection1,
    required this.selection2,
    required this.selection3,
    required this.selection4,
    required this.crct,
    required this.cid,
    required this.num,
    required this.permutation,
    required this.timeLimitSeconds,
  });

  factory SingleQuestionSession.fromJson(Map<String, dynamic> json) {
    return SingleQuestionSession(
      userId: json['user_id'] as int,
      category: json['category'] as int,
      area: json['area'] as String? ?? '',
      title: json['title'] as String? ?? '',
      question: json['question'] as String? ?? '',
      selection1: json['selection1'] as String? ?? '',
      selection2: json['selection2'] as String? ?? '',
      selection3: json['selection3'] as String? ?? '',
      selection4: json['selection4'] as String? ?? '',
      crct: json['crct'] as int? ?? 0,
      cid: json['cid'] as int? ?? 0,
      num: json['num'] as String? ?? '',
      permutation: json['permutation'] as String? ?? '',
      timeLimitSeconds: json['time_limit_seconds'] as int? ?? 135,
    );
  }

  final int userId;
  final int category;
  final String area;
  final String title;
  final String question;
  final String selection1;
  final String selection2;
  final String selection3;
  final String selection4;
  final int crct;
  final int cid;
  final String num;
  final String permutation;
  final int timeLimitSeconds;
}

class SingleQuestionResult {
  const SingleQuestionResult({
    required this.userId,
    required this.category,
    required this.area,
    required this.title,
    required this.resultMessage,
    required this.correctAnswer,
    required this.question,
    required this.selection1,
    required this.selection2,
    required this.selection3,
    required this.selection4,
    required this.comment,
  });

  factory SingleQuestionResult.fromJson(Map<String, dynamic> json) {
    return SingleQuestionResult(
      userId: json['user_id'] as int,
      category: json['category'] as int,
      area: json['area'] as String? ?? '',
      title: json['title'] as String? ?? '',
      resultMessage: json['result_message'] as String? ?? '',
      correctAnswer: json['correct_answer'] as String? ?? '',
      question: json['question'] as String? ?? '',
      selection1: json['selection1'] as String? ?? '',
      selection2: json['selection2'] as String? ?? '',
      selection3: json['selection3'] as String? ?? '',
      selection4: json['selection4'] as String? ?? '',
      comment: json['comment'] as String? ?? '',
    );
  }

  final int userId;
  final int category;
  final String area;
  final String title;
  final String resultMessage;
  final String correctAnswer;
  final String question;
  final String selection1;
  final String selection2;
  final String selection3;
  final String selection4;
  final String comment;
}
