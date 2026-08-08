import 'dart:async';

import 'package:flutter/material.dart';

import '../models/single_question_session.dart';
import '../services/exam_service.dart';
import '../widgets/exam_question_body.dart';
import 'main_menu_screen.dart';

class SingleExerciseScreen extends StatefulWidget {
  const SingleExerciseScreen({
    super.key,
    required this.session,
    required this.email,
  });

  final SingleQuestionSession session;
  final String email;

  @override
  State<SingleExerciseScreen> createState() => _SingleExerciseScreenState();
}

class _SingleExerciseScreenState extends State<SingleExerciseScreen> {
  final _examService = ExamService();
  final Map<String, int> _audioPlayCounts = {};
  Timer? _timer;
  int _elapsedSeconds = 0;
  int? _selectedAnswer;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) => _tick());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _tick() {
    setState(() => _elapsedSeconds += 1);
    if (_elapsedSeconds >= widget.session.timeLimitSeconds) {
      _timer?.cancel();
      _submitAnswer(timeout: true);
    }
  }

  String get _elapsedLabel {
    final minutes = (_elapsedSeconds ~/ 60).toString().padLeft(2, '0');
    final seconds = (_elapsedSeconds % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }

  String get _limitLabel {
    final total = widget.session.timeLimitSeconds;
    final minutes = total ~/ 60;
    final seconds = total % 60;
    if (minutes > 0 && seconds > 0) {
      return '解答時間は$minutes分$seconds秒/1問です。';
    }
    if (minutes > 0) {
      return '解答時間は$minutes分/1問です。';
    }
    return '解答時間は$seconds秒/1問です。';
  }

  Future<void> _submitAnswer({bool timeout = false}) async {
    if (_isLoading) {
      return;
    }

    setState(() => _isLoading = true);

    try {
      final answer = timeout ? 9 : (_selectedAnswer ?? 9);
      final result = await _examService.checkSingleAnswer(
        session: widget.session,
        answer: answer,
      );

      if (!mounted) {
        return;
      }

      await Navigator.of(context).pushReplacement(
        MaterialPageRoute<void>(
          builder: (_) => SingleAnalysisScreen(
            result: result,
            email: widget.email,
          ),
        ),
      );
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

  @override
  Widget build(BuildContext context) {
    final session = widget.session;

    return Scaffold(
      appBar: AppBar(
        title: Text(session.title),
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : ListView(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                children: [
                  Text('経過時間 $_elapsedLabel'),
                  Text(_limitLabel),
                  const SizedBox(height: 16),
                  Text(
                    '問題:',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  ExamQuestionBody(
                    question: session.question,
                    choiceCount: session.choiceCount,
                    selection1: session.selection1,
                    selection2: session.selection2,
                    selection3: session.selection3,
                    selection4: session.selection4,
                    image: session.image,
                    audio: session.audio,
                    choiceAudio: session.choiceAudio,
                    audioSetNote: session.audioSetNote,
                    selectedAnswer: _selectedAnswer,
                    onSelect: (value) => setState(() => _selectedAnswer = value),
                    playCounts: _audioPlayCounts,
                    audioScopeKey: 'single_${session.cid}',
                    enforceAudioLimit: true,
                    showChoiceTextWhenAudio: false,
                  ),
                ],
              ),
      ),
      bottomNavigationBar: _isLoading
          ? null
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: FilledButton(
                  onPressed: _submitAnswer,
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFFD13415),
                    minimumSize: const Size.fromHeight(48),
                  ),
                  child: const Text('解答を見る'),
                ),
              ),
            ),
    );
  }
}

class SingleAnalysisScreen extends StatelessWidget {
  SingleAnalysisScreen({
    super.key,
    required this.result,
    required this.email,
  });

  final SingleQuestionResult result;
  final String email;
  final Map<String, int> _playCounts = {};

  Future<void> _continue(BuildContext context) async {
    final examService = ExamService();
    final session = await examService.startSingleExam(
      userId: result.userId,
      category: result.category,
    );

    if (!context.mounted) {
      return;
    }

    await Navigator.of(context).pushReplacement(
      MaterialPageRoute<void>(
        builder: (_) => SingleExerciseScreen(
          session: session,
          email: email,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(result.title),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            result.resultMessage,
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 16),
          ExamQuestionBody(
            question: result.question,
            choiceCount: result.choiceCount,
            selection1: result.selection1,
            selection2: result.selection2,
            selection3: result.selection3,
            selection4: result.selection4,
            image: result.image,
            audio: result.audio,
            choiceAudio: result.choiceAudio,
            promptText: result.promptText,
            playCounts: _playCounts,
            audioScopeKey: 'single_result_${result.userId}_${result.category}',
            enforceAudioLimit: false,
            showChoiceTextWhenAudio: true,
          ),
          const SizedBox(height: 16),
          Text('正解は 「${result.correctAnswer}」です。'),
          const SizedBox(height: 16),
          Text(
            stripExamHtml(result.comment),
            style: const TextStyle(color: Colors.red),
          ),
          const SizedBox(height: 24),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: [
              OutlinedButton(
                onPressed: () {
                  Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute<void>(
                      builder: (_) => MainMenuScreen(
                        userId: result.userId,
                        email: email,
                      ),
                    ),
                    (_) => false,
                  );
                },
                child: const Text('終了する'),
              ),
              FilledButton(
                onPressed: () => _continue(context),
                child: const Text('続ける'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
