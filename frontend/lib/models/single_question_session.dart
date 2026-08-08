import 'exam_media.dart';

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
    required this.choiceCount,
    required this.crct,
    required this.cid,
    required this.num,
    required this.permutation,
    required this.timeLimitSeconds,
    this.audio,
    this.choiceAudio,
    this.image,
    this.audioSetNote,
  });

  factory SingleQuestionSession.fromJson(Map<String, dynamic> json) {
    final selection1 = json['selection1'] as String? ?? '';
    final selection2 = json['selection2'] as String? ?? '';
    final selection3 = json['selection3'] as String? ?? '';
    final selection4 = json['selection4'] as String? ?? '';
    final choiceAudio = parseChoiceAudio(json['choice_audio']);
    int asInt(dynamic value, [int fallback = 0]) {
      if (value is int) return value;
      if (value is double) return value.toInt();
      return int.tryParse('$value') ?? fallback;
    }

    return SingleQuestionSession(
      userId: asInt(json['user_id']),
      category: asInt(json['category']),
      area: json['area'] as String? ?? '',
      title: json['title'] as String? ?? '',
      question: json['question'] as String? ?? '',
      selection1: selection1,
      selection2: selection2,
      selection3: selection3,
      selection4: selection4,
      choiceCount: effectiveChoiceCount(
        choiceCount: asInt(json['choice_count'], 4),
        choiceAudio: choiceAudio,
        selection1: selection1,
        selection2: selection2,
        selection3: selection3,
        selection4: selection4,
      ),
      crct: asInt(json['crct']),
      cid: asInt(json['cid']),
      num: json['num'] as String? ?? '',
      permutation: json['permutation'] as String? ?? '',
      // Match exercise2.html default when API omits the field (YAML is source of truth).
      timeLimitSeconds: asInt(json['time_limit_seconds'], 90),
      audio: parseExamAudio(json['audio']),
      choiceAudio: choiceAudio,
      image: parseExamImage(json['image']),
      audioSetNote: json['audio_set_note'] as String?,
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
  final int choiceCount;
  final int crct;
  final int cid;
  final String num;
  final String permutation;
  final int timeLimitSeconds;
  final ExamAudio? audio;
  final ChoiceAudioBundle? choiceAudio;
  final ExamImage? image;
  final String? audioSetNote;
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
    required this.choiceCount,
    required this.comment,
    this.promptText,
    this.audio,
    this.choiceAudio,
    this.image,
  });

  factory SingleQuestionResult.fromJson(Map<String, dynamic> json) {
    final selection1 = json['selection1'] as String? ?? '';
    final selection2 = json['selection2'] as String? ?? '';
    final selection3 = json['selection3'] as String? ?? '';
    final selection4 = json['selection4'] as String? ?? '';
    final choiceAudio = parseChoiceAudio(json['choice_audio']);
    int asInt(dynamic value, [int fallback = 0]) {
      if (value is int) return value;
      if (value is double) return value.toInt();
      return int.tryParse('$value') ?? fallback;
    }

    return SingleQuestionResult(
      userId: asInt(json['user_id']),
      category: asInt(json['category']),
      area: json['area'] as String? ?? '',
      title: json['title'] as String? ?? '',
      resultMessage: json['result_message'] as String? ?? '',
      correctAnswer: json['correct_answer'] as String? ?? '',
      question: json['question'] as String? ?? '',
      selection1: selection1,
      selection2: selection2,
      selection3: selection3,
      selection4: selection4,
      choiceCount: effectiveChoiceCount(
        choiceCount: asInt(json['choice_count'], 4),
        choiceAudio: choiceAudio,
        selection1: selection1,
        selection2: selection2,
        selection3: selection3,
        selection4: selection4,
      ),
      comment: json['comment'] as String? ?? '',
      promptText: json['prompt_text'] as String?,
      audio: parseExamAudio(json['audio']),
      choiceAudio: choiceAudio,
      image: parseExamImage(json['image']),
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
  final int choiceCount;
  final String comment;
  final String? promptText;
  final ExamAudio? audio;
  final ChoiceAudioBundle? choiceAudio;
  final ExamImage? image;
}
