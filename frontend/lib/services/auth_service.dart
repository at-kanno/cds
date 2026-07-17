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

      final body = jsonDecode(response.body) as Map<String, dynamic>;

      if (response.statusCode == 200) {
        return AuthResult(
          success: true,
          token: body['token'] as String?,
          message: body['message'] as String?,
          userId: body['user_id'] as int?,
          status: body['status'] as int?,
        );
      }

      return AuthResult(
        success: false,
        message: body['message'] as String? ?? 'Login failed.',
      );
    } catch (_) {
      return const AuthResult(
        success: false,
        message: 'Could not reach the server. Check that Flask is running.',
      );
    }
  }
}
