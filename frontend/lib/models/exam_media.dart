import '../config/api_config.dart';

class MediaFileRef {
  const MediaFileRef({
    required this.filename,
    required this.url,
  });

  factory MediaFileRef.fromJson(Map<String, dynamic> json) {
    return MediaFileRef(
      filename: json['filename'] as String? ?? '',
      url: json['url'] as String? ?? '',
    );
  }

  final String filename;
  final String url;

  String get absoluteUrl => ApiConfig.resolveMediaUrl(url);
}

class ExamAudio {
  const ExamAudio({
    required this.filename,
    required this.url,
    required this.maxAudioPlays,
    this.setRole,
  });

  factory ExamAudio.fromJson(Map<String, dynamic> json) {
    return ExamAudio(
      filename: json['filename'] as String? ?? '',
      url: json['url'] as String? ?? '',
      maxAudioPlays: (json['max_audio_plays'] as num?)?.toInt() ?? 0,
      setRole: json['set_role'] as String?,
    );
  }

  final String filename;
  final String url;
  final int maxAudioPlays;

  /// Part3/4 set listening (FLAG 301-399 / 401-499): `head` or `follow_up`.
  final String? setRole;

  String get absoluteUrl => ApiConfig.resolveMediaUrl(url);
}

class ChoiceAudioBundle {
  const ChoiceAudioBundle({
    required this.choices,
    required this.maxAudioPlays,
  });

  factory ChoiceAudioBundle.fromJson(Map<String, dynamic> json) {
    final raw = json['choices'] as Map<String, dynamic>? ?? const {};
    final choices = <String, MediaFileRef>{};
    for (final entry in raw.entries) {
      choices[entry.key] = MediaFileRef.fromJson(
        entry.value as Map<String, dynamic>,
      );
    }
    return ChoiceAudioBundle(
      choices: choices,
      maxAudioPlays: (json['max_audio_plays'] as num?)?.toInt() ?? 0,
    );
  }

  final Map<String, MediaFileRef> choices;
  final int maxAudioPlays;

  MediaFileRef? operator [](String letter) => choices[letter];
}

class ExamImage {
  const ExamImage({
    required this.filename,
    required this.url,
  });

  factory ExamImage.fromJson(Map<String, dynamic> json) {
    return ExamImage(
      filename: json['filename'] as String? ?? '',
      url: json['url'] as String? ?? '',
    );
  }

  final String filename;
  final String url;

  String get absoluteUrl => ApiConfig.resolveMediaUrl(url);
}

ExamAudio? parseExamAudio(dynamic value) {
  if (value is Map<String, dynamic>) {
    return ExamAudio.fromJson(value);
  }
  return null;
}

ChoiceAudioBundle? parseChoiceAudio(dynamic value) {
  if (value is Map<String, dynamic>) {
    return ChoiceAudioBundle.fromJson(value);
  }
  return null;
}

ExamImage? parseExamImage(dynamic value) {
  if (value is Map<String, dynamic>) {
    return ExamImage.fromJson(value);
  }
  return null;
}

int effectiveChoiceCount({
  required int choiceCount,
  ChoiceAudioBundle? choiceAudio,
  required String selection1,
  required String selection2,
  required String selection3,
  required String selection4,
}) {
  if (choiceAudio != null && choiceAudio.choices.isNotEmpty) {
    var max = 0;
    const letters = ['A', 'B', 'C', 'D'];
    for (var i = 0; i < letters.length; i++) {
      if (choiceAudio.choices.containsKey(letters[i])) {
        max = i + 1;
      }
    }
    if (max > 0) {
      return max;
    }
  }
  if (choiceCount >= 2 && choiceCount <= 4) {
    return choiceCount;
  }
  final texts = [selection1, selection2, selection3, selection4];
  var count = 0;
  for (final text in texts) {
    if (text.trim().isNotEmpty) {
      count += 1;
    }
  }
  return count.clamp(2, 4);
}
