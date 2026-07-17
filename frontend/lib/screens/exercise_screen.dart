import 'dart:async';

import 'package:flutter/material.dart';

import '../models/exercise_session.dart';
import '../services/exam_service.dart';
import 'exam_analysis_screen.dart';

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

  void _toggleMark(int qNo) {
    final index = qNo - 1;
    if (index < 0 || index >= _session.total) {
      return;
    }

    final marks = _session.marklist.padRight(_session.total, '0').split('');
    marks[index] = marks[index] == '1' ? '0' : '1';

    setState(() {
      _session = _session.copyWith(marklist: marks.join());
    });
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
        _timer?.cancel();
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
        _session = result.copyWith(marklist: _session.marklist);
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
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : ListView(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                children: [
                  Text('経過時間 $_elapsedLabel'),
                  const SizedBox(height: 12),
                  _QuestionNavigator(
                    session: _session,
                    onJump: (qNo) => _submitAction('move', targetQNo: qNo),
                    onToggleMark: _toggleMark,
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
                      contentPadding: EdgeInsets.zero,
                    ),
                ],
              ),
      ),
      bottomNavigationBar: _isLoading
          ? null
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(12, 8, 12, 12),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  alignment: WrapAlignment.center,
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
                    FilledButton(
                      onPressed: _session.canGoForward
                          ? () => _submitAction('next')
                          : null,
                      child: const Text('次へ'),
                    ),
                  ],
                ),
              ),
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
    final marklist = session.marklist.padRight(session.total, '0');

    return Wrap(
      spacing: 6,
      runSpacing: 6,
      children: [
        for (var i = 0; i < session.total; i++)
          SizedBox(
            width: 52,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  height: 28,
                  child: Checkbox(
                    value: marklist[i] == '1',
                    onChanged: (_) => onToggleMark(i + 1),
                    materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    visualDensity: VisualDensity.compact,
                  ),
                ),
                OutlinedButton(
                  onPressed: () => onJump(i + 1),
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size(48, 36),
                    padding: EdgeInsets.zero,
                    backgroundColor: _buttonColor(session, i + 1),
                  ),
                  child: Text('Q${i + 1}'),
                ),
              ],
            ),
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
