import 'package:flutter/material.dart';

import '../models/exam_analysis.dart';
import '../models/exercise_session.dart';
import '../services/exam_service.dart';
import 'main_menu_screen.dart';

String stripHtml(String value) {
  return value
      .replaceAll(RegExp(r'<br\s*/?>', caseSensitive: false), '\n')
      .replaceAll(RegExp(r'<[^>]*>'), '')
      .replaceAll('&nbsp;', ' ')
      .trim();
}

class ExamFinishScreen extends StatefulWidget {
  const ExamFinishScreen({
    super.key,
    required this.session,
    required this.email,
  });

  final ExerciseSession session;
  final String email;

  @override
  State<ExamFinishScreen> createState() => _ExamFinishScreenState();
}

class _ExamFinishScreenState extends State<ExamFinishScreen> {
  final _examService = ExamService();
  bool _isLoading = false;

  Map<String, dynamic> get _summaryPayload => widget.session.toSummaryPayload();

  Future<void> _openAreaResults() async {
    setState(() => _isLoading = true);
    try {
      final data = await _examService.fetchAreaResults(_summaryPayload);
      if (!mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (_) => AreaResultsScreen(
            data: data,
            email: widget.email,
          ),
        ),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _openCommentsAnalysis() async {
    setState(() => _isLoading = true);
    try {
      final data = await _examService.fetchCommentsAnalysis(_summaryPayload);
      if (!mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (_) => CommentsAnalysisScreen(
            data: data,
            email: widget.email,
          ),
        ),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _returnToMenu() async {
    setState(() => _isLoading = true);
    try {
      await _examService.returnToMainMenu(widget.session.userId);
      if (!mounted) return;
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute<void>(
          builder: (_) => MainMenuScreen(
            userId: widget.session.userId,
            email: widget.email,
          ),
        ),
        (_) => false,
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final session = widget.session;

    return Scaffold(
      appBar: AppBar(title: Text('${session.title}（終了）')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(24),
              children: [
                Text(
                  session.title,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 16),
                const Text('お疲れ様でした。'),
                const SizedBox(height: 12),
                Text('総出題数 ${session.total}問の中で、${session.correct}問が正解です。'),
                Text('正答率は ${session.rate?.toStringAsFixed(1)}% です。'),
                if (session.flag == 1)
                  const Padding(
                    padding: EdgeInsets.only(top: 8),
                    child: Text('修了試験に挑戦できるようになりました。'),
                  ),
                if (session.message != null && session.message!.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  Text(stripHtml(session.message!)),
                ],
                const SizedBox(height: 24),
                FilledButton(
                  onPressed: _openCommentsAnalysis,
                  child: const Text('答案の分析結果'),
                ),
                const SizedBox(height: 12),
                FilledButton(
                  onPressed: _openAreaResults,
                  child: const Text('領域ごとの結果画面'),
                ),
                const SizedBox(height: 12),
                OutlinedButton(
                  onPressed: _returnToMenu,
                  child: const Text('メインメニューへ戻る'),
                ),
              ],
            ),
    );
  }
}

class CommentsAnalysisScreen extends StatelessWidget {
  const CommentsAnalysisScreen({
    super.key,
    required this.data,
    required this.email,
  });

  final CommentsAnalysisData data;
  final String email;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(data.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _SummaryHeader(summary: data.context),
          const SizedBox(height: 16),
          Text(stripHtml(data.commentsHtml)),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: () {
              Navigator.of(context).pushReplacement(
                MaterialPageRoute<void>(
                  builder: (_) => AreaResultsScreenLoader(
                    payload: data.context.toRequestJson(),
                    email: email,
                  ),
                ),
              );
            },
            child: const Text('領域ごとの結果画面'),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            onPressed: () => _returnToMenu(context, data.context.userId, email),
            child: const Text('メインメニューへ戻る'),
          ),
        ],
      ),
    );
  }
}

class AreaResultsScreenLoader extends StatefulWidget {
  const AreaResultsScreenLoader({
    super.key,
    required this.payload,
    required this.email,
  });

  final Map<String, dynamic> payload;
  final String email;

  @override
  State<AreaResultsScreenLoader> createState() => _AreaResultsScreenLoaderState();
}

class _AreaResultsScreenLoaderState extends State<AreaResultsScreenLoader> {
  final _examService = ExamService();
  late Future<AreaResultsData> _future;

  @override
  void initState() {
    super.initState();
    _future = _examService.fetchAreaResults(widget.payload);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<AreaResultsData>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        if (snapshot.hasError) {
          return Scaffold(
            appBar: AppBar(title: const Text('領域ごとの結果')),
            body: Center(child: Text(snapshot.error.toString())),
          );
        }
        return AreaResultsScreen(
          data: snapshot.data!,
          email: widget.email,
        );
      },
    );
  }
}

class AreaResultsScreen extends StatelessWidget {
  const AreaResultsScreen({
    super.key,
    required this.data,
    required this.email,
  });

  final AreaResultsData data;
  final String email;

  Future<void> _openQuestion(
    BuildContext context,
    int qNo,
  ) async {
    final examService = ExamService();
    final payload = {
      ...data.context.toRequestJson(),
      'q_no': qNo,
    };

    try {
      final analysis = await examService.fetchQuestionAnalysis(payload);
      if (!context.mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (_) => QuestionAnalysisScreen(
            data: analysis,
            email: email,
          ),
        ),
      );
    } catch (error) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(data.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _SummaryHeader(summary: data.context),
          const SizedBox(height: 16),
          for (final area in data.areas) ...[
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      area.label,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    Text('採点結果: ${area.scoreLabel}  正答率: ${area.percentLabel}'),
                    const SizedBox(height: 8),
                    for (final chapter in area.chapters) ...[
                      Text(chapter.label),
                      Text('${chapter.scoreLabel} / ${chapter.percentLabel}'),
                      if (chapter.questions.isNotEmpty)
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            for (final question in chapter.questions)
                              OutlinedButton(
                                onPressed: () => _openQuestion(context, question.qNo),
                                style: OutlinedButton.styleFrom(
                                  foregroundColor:
                                      question.correct ? Colors.black : Colors.red,
                                ),
                                child: Text('${question.qNo}'),
                              ),
                          ],
                        ),
                      const SizedBox(height: 8),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 8),
          ],
          FilledButton(
            onPressed: () {
              Navigator.of(context).pushReplacement(
                MaterialPageRoute<void>(
                  builder: (_) => CommentsAnalysisScreenLoader(
                    payload: data.context.toRequestJson(),
                    email: email,
                  ),
                ),
              );
            },
            child: const Text('答案の分析結果'),
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            onPressed: () => _returnToMenu(context, data.context.userId, email),
            child: const Text('メインメニューへ戻る'),
          ),
        ],
      ),
    );
  }
}

class CommentsAnalysisScreenLoader extends StatefulWidget {
  const CommentsAnalysisScreenLoader({
    super.key,
    required this.payload,
    required this.email,
  });

  final Map<String, dynamic> payload;
  final String email;

  @override
  State<CommentsAnalysisScreenLoader> createState() =>
      _CommentsAnalysisScreenLoaderState();
}

class _CommentsAnalysisScreenLoaderState extends State<CommentsAnalysisScreenLoader> {
  final _examService = ExamService();
  late Future<CommentsAnalysisData> _future;

  @override
  void initState() {
    super.initState();
    _future = _examService.fetchCommentsAnalysis(widget.payload);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CommentsAnalysisData>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        if (snapshot.hasError) {
          return Scaffold(
            appBar: AppBar(title: const Text('分析結果')),
            body: Center(child: Text(snapshot.error.toString())),
          );
        }
        return CommentsAnalysisScreen(
          data: snapshot.data!,
          email: widget.email,
        );
      },
    );
  }
}

class QuestionAnalysisScreen extends StatelessWidget {
  const QuestionAnalysisScreen({
    super.key,
    required this.data,
    required this.email,
  });

  final QuestionAnalysisData data;
  final String email;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(data.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _SummaryHeader(summary: data.context),
          const SizedBox(height: 16),
          Text('問題 ${data.qNo}', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Text(stripHtml(data.question)),
          const SizedBox(height: 12),
          Text('A. ${stripHtml(data.selection1)}'),
          Text('B. ${stripHtml(data.selection2)}'),
          Text('C. ${stripHtml(data.selection3)}'),
          Text('D. ${stripHtml(data.selection4)}'),
          const SizedBox(height: 16),
          Text('正解は 「${data.correctAnswer}」 です。'),
          const SizedBox(height: 16),
          Text(
            stripHtml(data.commentHtml),
            style: const TextStyle(color: Colors.red),
          ),
          const SizedBox(height: 24),
          OutlinedButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('戻る'),
          ),
        ],
      ),
    );
  }
}

class _SummaryHeader extends StatelessWidget {
  const _SummaryHeader({required this.summary});

  final ExamSummaryContext summary;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('実施日時：${summary.stime}'),
        Text(
          '採点結果：${summary.rate.toStringAsFixed(1)}  '
          '正答率：${summary.correct} / ${summary.total}  '
          '合否：${summary.result}',
        ),
      ],
    );
  }
}

Future<void> _returnToMenu(
  BuildContext context,
  int userId,
  String email,
) async {
  final examService = ExamService();
  try {
    await examService.returnToMainMenu(userId);
    if (!context.mounted) return;
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute<void>(
        builder: (_) => MainMenuScreen(userId: userId, email: email),
      ),
      (_) => false,
    );
  } catch (error) {
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(error.toString())),
    );
  }
}
