import 'package:flutter/foundation.dart';

class ApiConfig {
  static String? _overrideBaseUrl;

  static void setBaseUrl(String? url) {
    final trimmed = url?.trim();
    if (trimmed == null || trimmed.isEmpty) {
      _overrideBaseUrl = null;
      return;
    }
    _overrideBaseUrl = trimmed.endsWith('/')
        ? trimmed.substring(0, trimmed.length - 1)
        : trimmed;
  }

  static String get baseUrl {
    const envUrl = String.fromEnvironment('API_BASE_URL');
    if (envUrl.isNotEmpty) {
      return envUrl;
    }
    if (_overrideBaseUrl != null && _overrideBaseUrl!.isNotEmpty) {
      return _overrideBaseUrl!;
    }

    if (kIsWeb) {
      return 'http://localhost:8080';
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return 'http://10.0.2.2:8080';
      default:
        return 'http://localhost:8080';
    }
  }

  static String get loginEndpoint => '$baseUrl/api/login';
  static String get mainMenuEndpoint => '$baseUrl/api/main-menu';
  static String get logoutEndpoint => '$baseUrl/api/logout';
  static String get examStartEndpoint => '$baseUrl/api/exam/start';
  static String get examActionEndpoint => '$baseUrl/api/exam/action';
  static String get examSummaryAreaEndpoint => '$baseUrl/api/exam/summary/area';
  static String get examSummaryCommentsEndpoint =>
      '$baseUrl/api/exam/summary/comments';
  static String get examAnalyzeEndpoint => '$baseUrl/api/exam/analyze';
  static String get examReturnMenuEndpoint => '$baseUrl/api/exam/return-menu';
  static String get singleExamStartEndpoint => '$baseUrl/api/single-exam/start';
  static String get singleExamCheckEndpoint => '$baseUrl/api/single-exam/check';
  static String get adminEnterEndpoint => '$baseUrl/api/admin/enter';
  static String get adminHomeEndpoint => '$baseUrl/api/admin/home';
  static String get adminHistoryEndpoint => '$baseUrl/api/admin/history';
  static String get adminStatusEndpoint => '$baseUrl/api/admin/status';
  static String get adminUsersEndpoint => '$baseUrl/api/admin/users';
  static String get adminDeleteUserEndpoint => '$baseUrl/api/admin/users/delete';
  static String get adminRankUpEndpoint => '$baseUrl/api/admin/users/rankup';
  static String get adminPasswordResetEndpoint => '$baseUrl/api/admin/password-reset';
}
