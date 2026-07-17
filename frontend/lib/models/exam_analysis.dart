class ExamSummaryContext {
  const ExamSummaryContext({
    required this.userId,
    required this.examId,
    required this.title,
    required this.total,
    required this.correct,
    required this.rate,
    required this.passed,
    required this.result,
    required this.stime,
    required this.arealist,
    required this.resultlist,
  });

  factory ExamSummaryContext.fromFinishJson(Map<String, dynamic> json) {
    return ExamSummaryContext(
      userId: json['user_id'] as int,
      examId: json['exam_id'] as int,
      title: json['title'] as String? ?? '',
      total: json['total'] as int,
      correct: json['correct'] as int? ?? 0,
      rate: (json['rate'] as num?)?.toDouble() ?? 0,
      passed: json['passed'] as bool? ?? false,
      result: json['result'] as String? ?? '',
      stime: json['stime'] as String? ?? '',
      arealist: json['arealist'] as String? ?? '',
      resultlist: json['resultlist'] as String? ?? '',
    );
  }

  factory ExamSummaryContext.fromJson(Map<String, dynamic> json) {
    return ExamSummaryContext(
      userId: json['user_id'] as int,
      examId: json['exam_id'] as int,
      title: json['title'] as String? ?? '',
      total: json['total'] as int,
      correct: json['correct'] as int? ?? 0,
      rate: (json['rate'] as num?)?.toDouble() ?? 0,
      passed: json['passed'] as bool? ?? false,
      result: json['result'] as String? ?? '',
      stime: json['stime'] as String? ?? '',
      arealist: json['arealist'] as String? ?? '',
      resultlist: json['resultlist'] as String? ?? '',
    );
  }

  final int userId;
  final int examId;
  final String title;
  final int total;
  final int correct;
  final double rate;
  final bool passed;
  final String result;
  final String stime;
  final String arealist;
  final String resultlist;

  Map<String, dynamic> toRequestJson() {
    return {
      'user_id': userId,
      'exam_id': examId,
      'title': title,
      'total': total,
      'correct': correct,
      'resultlist': resultlist,
      'arealist': arealist,
      'stime': stime,
    };
  }
}

class QuestionRef {
  const QuestionRef({
    required this.qNo,
    required this.correct,
  });

  factory QuestionRef.fromJson(Map<String, dynamic> json) {
    return QuestionRef(
      qNo: json['q_no'] as int,
      correct: json['correct'] as bool? ?? true,
    );
  }

  final int qNo;
  final bool correct;
}

class AreaChapterResult {
  const AreaChapterResult({
    required this.label,
    required this.scoreLabel,
    required this.percentLabel,
    required this.questions,
  });

  factory AreaChapterResult.fromJson(Map<String, dynamic> json) {
    return AreaChapterResult(
      label: json['label'] as String? ?? '',
      scoreLabel: json['score_label'] as String? ?? '',
      percentLabel: json['percent_label'] as String? ?? '',
      questions: (json['questions'] as List<dynamic>? ?? [])
          .map((item) => QuestionRef.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final String label;
  final String scoreLabel;
  final String percentLabel;
  final List<QuestionRef> questions;
}

class AreaResult {
  const AreaResult({
    required this.label,
    required this.scoreLabel,
    required this.percentLabel,
    required this.chapters,
  });

  factory AreaResult.fromJson(Map<String, dynamic> json) {
    return AreaResult(
      label: json['label'] as String? ?? '',
      scoreLabel: json['score_label'] as String? ?? '',
      percentLabel: json['percent_label'] as String? ?? '',
      chapters: (json['chapters'] as List<dynamic>? ?? [])
          .map((item) => AreaChapterResult.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final String label;
  final String scoreLabel;
  final String percentLabel;
  final List<AreaChapterResult> chapters;
}

class AreaResultsData {
  const AreaResultsData({
    required this.context,
    required this.title,
    required this.areas,
  });

  factory AreaResultsData.fromJson(Map<String, dynamic> json) {
    return AreaResultsData(
      context: ExamSummaryContext.fromJson(json),
      title: json['title'] as String? ?? '',
      areas: (json['areas'] as List<dynamic>? ?? [])
          .map((item) => AreaResult.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final ExamSummaryContext context;
  final String title;
  final List<AreaResult> areas;
}

class CommentsAnalysisData {
  const CommentsAnalysisData({
    required this.context,
    required this.title,
    required this.commentsHtml,
  });

  factory CommentsAnalysisData.fromJson(Map<String, dynamic> json) {
    return CommentsAnalysisData(
      context: ExamSummaryContext.fromJson(json),
      title: json['title'] as String? ?? '',
      commentsHtml: json['comments_html'] as String? ?? '',
    );
  }

  final ExamSummaryContext context;
  final String title;
  final String commentsHtml;
}

class QuestionAnalysisData {
  const QuestionAnalysisData({
    required this.context,
    required this.title,
    required this.qNo,
    required this.question,
    required this.selection1,
    required this.selection2,
    required this.selection3,
    required this.selection4,
    required this.correctAnswer,
    required this.commentHtml,
  });

  factory QuestionAnalysisData.fromJson(Map<String, dynamic> json) {
    return QuestionAnalysisData(
      context: ExamSummaryContext.fromJson(json),
      title: json['title'] as String? ?? '',
      qNo: json['q_no'] as int,
      question: json['question'] as String? ?? '',
      selection1: json['selection1'] as String? ?? '',
      selection2: json['selection2'] as String? ?? '',
      selection3: json['selection3'] as String? ?? '',
      selection4: json['selection4'] as String? ?? '',
      correctAnswer: json['correct_answer'] as String? ?? '',
      commentHtml: json['comment_html'] as String? ?? '',
    );
  }

  final ExamSummaryContext context;
  final String title;
  final int qNo;
  final String question;
  final String selection1;
  final String selection2;
  final String selection3;
  final String selection4;
  final String correctAnswer;
  final String commentHtml;
}
