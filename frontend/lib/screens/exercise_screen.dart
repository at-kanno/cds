import 'dart:async';

import 'package:flutter/material.dart';

import '../models/exercise_session.dart';
import '../services/exam_service.dart';
import 'main_menu_screen.dart';

class ExerciseScreen extends StatefulWidget {
  const ExerciseScreen({
    super.key,
    required this.initialSession,
    required this.email,
  });

  final ExerciseSession initialSession;
  final String email;

  @override
  State<ExerciseScreen> createState() => _ExerciseScreenState();
}

class _ExerciseScreenState extends State<ExerciseScreen> {
  final _examService = ExamService();
  late ExerciseSession _session;
  Timer? _timer;
  int _elapsedSeconds = 0;
  bool _isLoading = false;
  int? _selectedAnswer;

  @override
  void initState() {
    super.initState();
    _session = widget.initialSession;
    _selectedAnswer =
        _session.selectedAnswer > 0 ? _session.selectedAnswer : null;
    _elapsedSeconds = _session.timeMin * 60 + _session.timeSec;
    _timer = Timer.periodic(const Duration(seconds: 1), (_) => _tick());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _tick() {
    setState(() {
      _elapsedSeconds += 1;
    });

    if (_elapsedSeconds >= _session.timeLimitSeconds) {
      _timer?.cancel();
      _submitAction('timeout');
    }
  }

  String get _elapsedLabel {
    final minutes = (_elapsedSeconds ~/ 60).toString().padLeft(2, '0');
    final seconds = (_elapsedSeconds % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }

  Future<void> _submitAction(
    String command, {
    int? targetQNo,
  }) async {
    if (_isLoading) {
      return;
    }

    setState(() => _isLoading = true);

    try {
      final minutes = _elapsedSeconds ~/ 60;
      final seconds = _elapsedSeconds % 60;
      final result = await _examService.sendAction(
        _session.toActionPayload(
          command: command,
          targetQNo: targetQNo,
          selectedAnswer: _selectedAnswer,
          timeMin: minutes,
          timeSec: seconds,
        ),
      );

      if (!mounted) {
        return;
      }

      if (result.finished) {
        await Navigator.of(context).pushReplacement(
          MaterialPageRoute<void>(
            builder: (_) => ExamFinishScreen(
              session: result,
              email: widget.email,
            ),
          ),
        );
        return;
      }

      setState(() {
        _session = result;
        _selectedAnswer =
            result.selectedAnswer > 0 ? result.selectedAnswer : null;
      });
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Future<void> _confirmFinish() async {
    if (_session.total != 40) {
      await _submitAction('finish');
      return;
    }

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('終了しますか？'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('キャンセル'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('終了する'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await _submitAction('finish');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_session.title),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text('経過時間 $_elapsedLabel'),
                const SizedBox(height: 12),
                _QuestionNavigator(
                  session: _session,
                  onJump: (qNo) => _submitAction('move', targetQNo: qNo),
                  onToggleMark: (qNo) {
                    if (qNo == _session.qNo) {
                      _submitAction('mark');
                    }
                  },
                ),
                const SizedBox(height: 16),
                Text(
                  '問題 ${_session.qNo}:',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                Text(_stripHtml(_session.question)),
                const SizedBox(height: 16),
                for (final entry in [
                  (1, 'A', _session.selection1),
                  (2, 'B', _session.selection2),
                  (3, 'C', _session.selection3),
                  (4, 'D', _session.selection4),
                ])
                  RadioListTile<int>(
                    value: entry.$1,
                    groupValue: _selectedAnswer,
                    onChanged: (value) => setState(() => _selectedAnswer = value),
                    title: Text('${entry.$2}. ${_stripHtml(entry.$3)}'),
                  ),
                const SizedBox(height: 16),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    OutlinedButton(
                      onPressed: _confirmFinish,
                      child: const Text('終了する'),
                    ),
                    OutlinedButton(
                      onPressed: _session.canGoBack
                          ? () => _submitAction('previous')
                          : null,
                      child: const Text('前に戻る'),
                    ),
                    OutlinedButton(
                      onPressed: () => _submitAction('mark'),
                      child: const Text('マークする'),
                    ),
                    FilledButton(
                      onPressed: _session.canGoForward
                          ? () => _submitAction('next')
                          : null,
                      child: const Text('次へ進む'),
                    ),
                  ],
                ),
              ],
            ),
    );
  }

  String _stripHtml(String value) {
    return value
        .replaceAll(RegExp(r'<[^>]*>'), '')
        .replaceAll('&nbsp;', ' ')
        .trim();
  }
}

class _QuestionNavigator extends StatelessWidget {
  const _QuestionNavigator({
    required this.session,
    required this.onJump,
    required this.onToggleMark,
  });

  final ExerciseSession session;
  final ValueChanged<int> onJump;
  final ValueChanged<int> onToggleMark;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Wrap(
          spacing: 8,
          children: [
            for (var i = 0; i < session.total; i++)
              FilterChip(
                label: Text('Mark ${i + 1}'),
                selected: session.marklist.length > i && session.marklist[i] == '1',
                onSelected: (_) {
                  if (i + 1 == session.qNo) {
                    onToggleMark(i + 1);
                  }
                },
              ),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (var i = 0; i < session.total; i++)
              OutlinedButton(
                onPressed: () => onJump(i + 1),
                style: OutlinedButton.styleFrom(
                  backgroundColor: _buttonColor(session, i + 1),
                ),
                child: Text('Q${i + 1}'),
              ),
          ],
        ),
      ],
    );
  }

  Color? _buttonColor(ExerciseSession session, int qNo) {
    if (qNo == session.qNo) {
      return const Color(0xFFFA8072);
    }
    if (session.answerlist.length >= qNo &&
        session.answerlist[qNo - 1] != '0') {
      return Colors.lightBlue;
    }
    return null;
  }
}

class ExamFinishScreen extends StatelessWidget {
  const ExamFinishScreen({
    super.key,
    required this.session,
    required this.email,
  });

  final ExerciseSession session;
  final String email;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('試験結果'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              session.title,
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Text('Correct: ${session.correct}/${session.total}'),
            Text('Score: ${session.rate?.toStringAsFixed(1)}%'),
            const SizedBox(height: 16),
            Expanded(
              child: SingleChildScrollView(
                child: Text(session.message ?? 'Exam finished.'),
              ),
            ),
            FilledButton(
              onPressed: () {
                Navigator.of(context).pushAndRemoveUntil(
                  MaterialPageRoute<void>(
                    builder: (_) => MainMenuScreen(
                      userId: session.userId,
                      email: email,
                    ),
                  ),
                  (_) => false,
                );
              },
              child: const Text('メインメニューへ戻る'),
            ),
          ],
        ),
      ),
    );
  }
}
