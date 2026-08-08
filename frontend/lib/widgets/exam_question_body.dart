import 'package:flutter/material.dart';

import '../models/exam_media.dart';
import 'limited_audio_player.dart';

String stripExamHtml(String value) {
  return value
      .replaceAll(RegExp(r'<br\s*/?>', caseSensitive: false), '\n')
      .replaceAll(RegExp(r'<[^>]*>'), '')
      .replaceAll('&nbsp;', ' ')
      .trim();
}

/// Shared question body: stem, image, listening audio, and A–D choices.
class ExamQuestionBody extends StatelessWidget {
  const ExamQuestionBody({
    super.key,
    required this.question,
    required this.choiceCount,
    required this.selection1,
    required this.selection2,
    required this.selection3,
    required this.selection4,
    required this.playCounts,
    required this.audioScopeKey,
    this.stemAudioScopeKey,
    this.image,
    this.audio,
    this.choiceAudio,
    this.promptText,
    this.audioSetNote,
    this.setHeadQNo,
    this.onJumpToSetHead,
    this.selectedAnswer,
    this.onSelect,
    this.enforceAudioLimit = true,
    this.showChoiceTextWhenAudio = false,
  });

  final String question;
  final int choiceCount;
  final String selection1;
  final String selection2;
  final String selection3;
  final String selection4;
  final Map<String, int> playCounts;
  /// Scope for choice audio play limits (`{examId}_{qNo}`).
  final String audioScopeKey;
  /// Scope for main stem audio + set-listening “再生済み” check.
  /// Defaults to [audioScopeKey] when null.
  final String? stemAudioScopeKey;
  final ExamImage? image;
  final ExamAudio? audio;
  final ChoiceAudioBundle? choiceAudio;
  final String? promptText;
  final String? audioSetNote;
  final int? setHeadQNo;
  final VoidCallback? onJumpToSetHead;
  final int? selectedAnswer;
  final ValueChanged<int>? onSelect;
  final bool enforceAudioLimit;
  final bool showChoiceTextWhenAudio;

  String get _stemScope => stemAudioScopeKey ?? audioScopeKey;

  List<(int, String, String)> get _choices {
    final all = [
      (1, 'A', selection1),
      (2, 'B', selection2),
      (3, 'C', selection3),
      (4, 'D', selection4),
    ];
    return all.take(choiceCount.clamp(2, 4)).toList();
  }

  String? get _resolvedSetNote {
    final note = audioSetNote?.trim();
    if (note == null || note.isEmpty) {
      return null;
    }
    final headQ = setHeadQNo;
    if (headQ != null && headQ > 0) {
      final plays = playCounts['${_stemScope}_main'] ?? 0;
      if (plays > 0 && !note.contains('再生済み')) {
        return '$note（再生済みです）';
      }
    }
    return note;
  }

  @override
  Widget build(BuildContext context) {
    final hideChoiceText =
        choiceAudio != null && !showChoiceTextWhenAudio;
    // HTML analysis.html: prompt_text is shown only with stem audio AND
    // choice audio (Part2). Part1 also has A4 in DB, but must not show it here.
    final showPrompt = audio != null &&
        choiceAudio != null &&
        promptText != null &&
        promptText!.trim().isNotEmpty;
    final setNote = _resolvedSetNote;
    final headQ = setHeadQNo;
    final showJump = headQ != null && headQ > 0 && onJumpToSetHead != null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(stripExamHtml(question)),
        if (image != null) ...[
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 360),
              child: Image.network(
                image!.absoluteUrl,
                fit: BoxFit.contain,
                errorBuilder: (_, _, _) => const Text('画像を表示できませんでした。'),
              ),
            ),
          ),
        ],
        if (setNote != null) ...[
          const SizedBox(height: 8),
          Text(
            setNote,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Colors.grey.shade700,
                ),
          ),
          if (showJump)
            TextButton(
              onPressed: onJumpToSetHead,
              style: TextButton.styleFrom(
                padding: EdgeInsets.zero,
                minimumSize: Size.zero,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
              child: Text('問題$headQへ'),
            ),
        ],
        if (audio != null) ...[
          const SizedBox(height: 12),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: LimitedAudioPlayer(
                  url: audio!.absoluteUrl,
                  storageKey: '${_stemScope}_main',
                  playCounts: playCounts,
                  maxPlays: audio!.maxAudioPlays,
                  enforceLimit: enforceAudioLimit,
                  label: '設問音声',
                ),
              ),
              if (showPrompt) ...[
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    stripExamHtml(promptText!),
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
              ],
            ],
          ),
        ],
        if (choiceAudio != null && enforceAudioLimit) ...[
          const SizedBox(height: 8),
          Text(
            '各選択肢の音声: 各 ${choiceAudio!.maxAudioPlays} 回まで',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
        const SizedBox(height: 12),
        for (final entry in _choices)
          _ChoiceTile(
            value: entry.$1,
            letter: entry.$2,
            text: entry.$3,
            groupValue: selectedAnswer,
            onChanged: onSelect,
            audio: choiceAudio?[entry.$2],
            hideText: hideChoiceText,
            playCounts: playCounts,
            storageKey: '${audioScopeKey}_${entry.$2}',
            maxPlays: choiceAudio?.maxAudioPlays ?? 0,
            enforceLimit: enforceAudioLimit,
          ),
      ],
    );
  }
}

class _ChoiceTile extends StatelessWidget {
  const _ChoiceTile({
    required this.value,
    required this.letter,
    required this.text,
    required this.groupValue,
    required this.onChanged,
    required this.playCounts,
    required this.storageKey,
    required this.maxPlays,
    required this.enforceLimit,
    this.audio,
    this.hideText = false,
  });

  final int value;
  final String letter;
  final String text;
  final int? groupValue;
  final ValueChanged<int>? onChanged;
  final MediaFileRef? audio;
  final bool hideText;
  final Map<String, int> playCounts;
  final String storageKey;
  final int maxPlays;
  final bool enforceLimit;

  @override
  Widget build(BuildContext context) {
    return RadioListTile<int>(
      value: value,
      groupValue: groupValue,
      onChanged: onChanged == null ? null : (v) => onChanged!(v!),
      contentPadding: EdgeInsets.zero,
      title: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('$letter.'),
          if (audio != null)
            LimitedAudioPlayer(
              url: audio!.absoluteUrl,
              storageKey: storageKey,
              playCounts: playCounts,
              maxPlays: maxPlays,
              enforceLimit: enforceLimit,
            ),
          if (!hideText && text.trim().isNotEmpty)
            Text(stripExamHtml(text)),
          if (audio == null && text.trim().isEmpty)
            Text(
              '（音声選択肢 $letter）',
              style: Theme.of(context).textTheme.bodySmall,
            ),
        ],
      ),
    );
  }
}
