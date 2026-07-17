class ExerciseSession {
  const ExerciseSession({
    required this.finished,
    required this.userId,
    required this.examId,
    required this.title,
    required this.total,
    required this.qNo,
    required this.examlist,
    required this.arealist,
    required this.question,
    required this.selection1,
    required this.selection2,
    required this.selection3,
    required this.selection4,
    required this.marklist,
    required this.answerlist,
    required this.selectedAnswer,
    required this.timeMin,
    required this.timeSec,
    required this.canGoBack,
    required this.canGoForward,
    required this.timeLimitSeconds,
    this.correct,
    this.rate,
    this.resultlist,
    this.message,
    this.flag,
  });

  factory ExerciseSession.fromJson(Map<String, dynamic> json) {
    return ExerciseSession(
      finished: json['finished'] as bool? ?? false,
      userId: json['user_id'] as int,
      examId: json['exam_id'] as int,
      title: json['title'] as String? ?? '',
      total: json['total'] as int,
      qNo: json['q_no'] as int? ?? 1,
      examlist: json['examlist'] as String? ?? '',
      arealist: json['arealist'] as String? ?? '',
      question: json['question'] as String? ?? '',
      selection1: json['selection1'] as String? ?? '',
      selection2: json['selection2'] as String? ?? '',
      selection3: json['selection3'] as String? ?? '',
      selection4: json['selection4'] as String? ?? '',
      marklist: json['marklist'] as String? ?? '',
      answerlist: json['answerlist'] as String? ?? '',
      selectedAnswer: json['selected_answer'] as int? ?? 0,
      timeMin: json['time_min'] as int? ?? 0,
      timeSec: json['time_sec'] as int? ?? 0,
      canGoBack: json['can_go_back'] as bool? ?? false,
      canGoForward: json['can_go_forward'] as bool? ?? false,
      timeLimitSeconds: json['time_limit_seconds'] as int? ?? 0,
      correct: json['correct'] as int?,
      rate: (json['rate'] as num?)?.toDouble(),
      resultlist: json['resultlist'] as String?,
      message: json['message'] as String?,
      flag: json['flag'] as int?,
    );
  }

  final bool finished;
  final int userId;
  final int examId;
  final String title;
  final int total;
  final int qNo;
  final String examlist;
  final String arealist;
  final String question;
  final String selection1;
  final String selection2;
  final String selection3;
  final String selection4;
  final String marklist;
  final String answerlist;
  final int selectedAnswer;
  final int timeMin;
  final int timeSec;
  final bool canGoBack;
  final bool canGoForward;
  final int timeLimitSeconds;
  final int? correct;
  final double? rate;
  final String? resultlist;
  final String? message;
  final int? flag;

  Map<String, dynamic> toActionPayload({
    required String command,
    int? targetQNo,
    int? selectedAnswer,
    int? timeMin,
    int? timeSec,
  }) {
    return {
      'command': command,
      'user_id': userId,
      'exam_id': examId,
      'title': title,
      'total': total,
      'q_no': qNo,
      'examlist': examlist,
      'arealist': arealist,
      'marklist': marklist,
      'answerlist': answerlist,
      'time_min': timeMin ?? this.timeMin,
      'time_sec': timeSec ?? this.timeSec,
      if (targetQNo != null) 'target_q_no': targetQNo,
      if (selectedAnswer != null) 'selected_answer': selectedAnswer,
    };
  }

  ExerciseSession copyWith({
    int? selectedAnswer,
    String? marklist,
    String? answerlist,
    int? qNo,
    int? timeMin,
    int? timeSec,
  }) {
    return ExerciseSession(
      finished: finished,
      userId: userId,
      examId: examId,
      title: title,
      total: total,
      qNo: qNo ?? this.qNo,
      examlist: examlist,
      arealist: arealist,
      question: question,
      selection1: selection1,
      selection2: selection2,
      selection3: selection3,
      selection4: selection4,
      marklist: marklist ?? this.marklist,
      answerlist: answerlist ?? this.answerlist,
      selectedAnswer: selectedAnswer ?? this.selectedAnswer,
      timeMin: timeMin ?? this.timeMin,
      timeSec: timeSec ?? this.timeSec,
      canGoBack: canGoBack,
      canGoForward: canGoForward,
      timeLimitSeconds: timeLimitSeconds,
      correct: correct,
      rate: rate,
      resultlist: resultlist,
      message: message,
      flag: flag,
    );
  }
}
