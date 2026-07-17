import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/admin_models.dart';

class AdminService {
  Future<AdminHome> enterAdmin(int userId) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.adminEnterEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        )
        .timeout(const Duration(seconds: 15));

    return _parseAdminHome(response);
  }

  Future<AdminHome> fetchAdminHome(int userId) async {
    final response = await http
        .get(Uri.parse('${ApiConfig.adminHomeEndpoint}?user_id=$userId'))
        .timeout(const Duration(seconds: 15));

    return _parseAdminHome(response);
  }

  Future<ExerciseHistory> fetchHistory(int userId) async {
    final response = await http
        .get(Uri.parse('${ApiConfig.adminHistoryEndpoint}?user_id=$userId'))
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load history.');
    }
    return ExerciseHistory.fromJson(body);
  }

  Future<UserStatusData> fetchStatus({
    required int userId,
    int? targetUserId,
  }) async {
    final target = targetUserId ?? userId;
    final response = await http
        .get(Uri.parse(
          '${ApiConfig.adminStatusEndpoint}?user_id=$userId&target_user_id=$target',
        ))
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load status.');
    }
    return UserStatusData.fromJson(body);
  }

  Future<AdminUserList> fetchUsers(int userId) async {
    final response = await http
        .get(Uri.parse('${ApiConfig.adminUsersEndpoint}?user_id=$userId'))
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load users.');
    }
    return AdminUserList.fromJson(body);
  }

  Future<void> deleteUser({
    required int actorUserId,
    required int targetUserId,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.adminDeleteUserEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'actor_user_id': actorUserId,
            'target_user_id': targetUserId,
          }),
        )
        .timeout(const Duration(seconds: 15));

    if (response.statusCode != 200) {
      final body = jsonDecode(response.body) as Map<String, dynamic>;
      throw Exception(body['message'] as String? ?? 'Failed to delete user.');
    }
  }

  Future<PasswordResetForm> fetchPasswordResetForm(int userId) async {
    final response = await http
        .get(Uri.parse('${ApiConfig.adminPasswordResetEndpoint}?user_id=$userId'))
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load password reset form.');
    }
    return PasswordResetForm.fromJson(body);
  }

  Future<PasswordResetResult> submitPasswordReset({
    required int userId,
    required String oldPassword,
    required String newPassword,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.adminPasswordResetEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': userId,
            'old_password': oldPassword,
            'new_password': newPassword,
          }),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to reset password.');
    }
    return PasswordResetResult.fromJson(body);
  }

  Future<String> rankUpUser({
    required int actorUserId,
    required int targetUserId,
  }) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.adminRankUpEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'actor_user_id': actorUserId,
            'target_user_id': targetUserId,
          }),
        )
        .timeout(const Duration(seconds: 15));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to update user.');
    }
    return body['message'] as String? ?? 'Updated.';
  }

  AdminHome _parseAdminHome(http.Response response) {
    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load admin.');
    }
    return AdminHome.fromJson(body);
  }
}
