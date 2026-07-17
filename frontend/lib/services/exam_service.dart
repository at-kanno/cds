import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/exercise_session.dart';
import '../models/single_question_session.dart';

class ExamService {
  Future<ExerciseSession> startExam({
    required int userId,
    required int category,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.examStartEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': userId,
            'category': category,
          }),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to start exam.');
    }

    return ExerciseSession.fromJson(body);
  }

  Future<ExerciseSession> sendAction(Map<String, dynamic> payload) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.examActionEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to update exam.');
    }

    return ExerciseSession.fromJson(body);
  }

  Future<SingleQuestionSession> startSingleExam({
    required int userId,
    required int category,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.singleExamStartEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': userId,
            'category': category,
          }),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(
        body['message'] as String? ?? 'Failed to start single-question exam.',
      );
    }

    return SingleQuestionSession.fromJson(body);
  }

  Future<SingleQuestionResult> checkSingleAnswer({
    required SingleQuestionSession session,
    required int answer,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.singleExamCheckEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': session.userId,
            'category': session.category,
            'area': session.area,
            'crct': session.crct,
            'num': session.num,
            'permutation': session.permutation,
            'cid': session.cid,
            'answer': answer,
          }),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to check answer.');
    }

    return SingleQuestionResult.fromJson(body);
  }
}
