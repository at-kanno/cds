import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';

class AuthResult {
  const AuthResult({
    required this.success,
    this.token,
    this.message,
    this.userId,
    this.status,
  });

  final bool success;
  final String? token;
  final String? message;
  final int? userId;
  final int? status;
}

class AuthService {
  Future<AuthResult> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse(ApiConfig.loginEndpoint),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'email': email,
              'password': password,
            }),
          )
          .timeout(const Duration(seconds: 10));

      final decoded = jsonDecode(response.body);
      if (decoded is! Map<String, dynamic>) {
        return const AuthResult(
          success: false,
          message: 'Unexpected server response.',
        );
      }
      final body = decoded;

      if (response.statusCode == 200) {
        final rawUserId = body['user_id'];
        final userId = rawUserId is int
            ? rawUserId
            : int.tryParse('$rawUserId');
        final rawStatus = body['status'];
        final status = rawStatus is int
            ? rawStatus
            : int.tryParse('$rawStatus');
        if (userId == null) {
          return const AuthResult(
            success: false,
            message: 'Login succeeded but user_id was missing.',
          );
        }
        return AuthResult(
          success: true,
          token: body['token'] as String?,
          message: body['message'] as String?,
          userId: userId,
          status: status,
        );
      }

      return AuthResult(
        success: false,
        message: body['message'] as String? ?? 'Login failed.',
      );
    } on FormatException {
      return const AuthResult(
        success: false,
        message: 'Server returned an invalid response.',
      );
    } catch (_) {
      return const AuthResult(
        success: false,
        message: 'Could not reach the server. Check the network connection.',
      );
    }
  }
}
