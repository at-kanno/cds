class AdminAction {
  const AdminAction({
    required this.id,
    required this.label,
    required this.enabled,
    this.message,
  });

  factory AdminAction.fromJson(Map<String, dynamic> json) {
    return AdminAction(
      id: json['id'] as String,
      label: json['label'] as String,
      enabled: json['enabled'] as bool? ?? true,
      message: json['message'] as String?,
    );
  }

  final String id;
  final String label;
  final bool enabled;
  final String? message;
}

class AdminHome {
  const AdminHome({
    required this.userId,
    required this.title,
    required this.isAdmin,
    required this.isStaff,
    required this.actions,
  });

  factory AdminHome.fromJson(Map<String, dynamic> json) {
    return AdminHome(
      userId: json['user_id'] as int,
      title: json['title'] as String? ?? '管理画面',
      isAdmin: json['is_admin'] as bool? ?? false,
      isStaff: json['is_staff'] as bool? ?? false,
      actions: (json['actions'] as List<dynamic>)
          .map((item) => AdminAction.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final int userId;
  final String title;
  final bool isAdmin;
  final bool isStaff;
  final List<AdminAction> actions;
}

class HistoryItem {
  const HistoryItem({
    required this.label,
    required this.passed,
  });

  factory HistoryItem.fromJson(Map<String, dynamic> json) {
    return HistoryItem(
      label: json['label'] as String? ?? '',
      passed: json['passed'] as bool? ?? false,
    );
  }

  final String label;
  final bool passed;
}

class ExerciseHistory {
  const ExerciseHistory({
    required this.userId,
    required this.title,
    required this.count,
    required this.items,
  });

  factory ExerciseHistory.fromJson(Map<String, dynamic> json) {
    return ExerciseHistory(
      userId: json['user_id'] as int,
      title: json['title'] as String? ?? '演習履歴',
      count: json['count'] as int? ?? 0,
      items: (json['items'] as List<dynamic>? ?? [])
          .map((item) => HistoryItem.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final int userId;
  final String title;
  final int count;
  final List<HistoryItem> items;
}

class UserStatusData {
  const UserStatusData({
    required this.userId,
    required this.targetUserId,
    required this.title,
    required this.grade,
    required this.mockItems,
    required this.finalItems,
    required this.mockCount,
    required this.finalCount,
  });

  factory UserStatusData.fromJson(Map<String, dynamic> json) {
    final mock = json['mock_exam_history'] as Map<String, dynamic>? ?? {};
    final finalHistory = json['final_exam_history'] as Map<String, dynamic>? ?? {};
    return UserStatusData(
      userId: json['user_id'] as int,
      targetUserId: json['target_user_id'] as int,
      title: json['title'] as String? ?? '現在のステータス',
      grade: json['grade'] as String? ?? '',
      mockCount: mock['count'] as int? ?? 0,
      finalCount: finalHistory['count'] as int? ?? 0,
      mockItems: (mock['items'] as List<dynamic>? ?? [])
          .map((item) => HistoryItem.fromJson(item as Map<String, dynamic>))
          .toList(),
      finalItems: (finalHistory['items'] as List<dynamic>? ?? [])
          .map((item) => HistoryItem.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final int userId;
  final int targetUserId;
  final String title;
  final String grade;
  final int mockCount;
  final int finalCount;
  final List<HistoryItem> mockItems;
  final List<HistoryItem> finalItems;
}

class AdminUser {
  const AdminUser({
    required this.id,
    required this.label,
    required this.lastname,
    required this.email,
  });

  factory AdminUser.fromJson(Map<String, dynamic> json) {
    return AdminUser(
      id: json['id'] as int,
      label: json['label'] as String? ?? '',
      lastname: json['lastname'] as String? ?? '',
      email: json['email'] as String? ?? '',
    );
  }

  final int id;
  final String label;
  final String lastname;
  final String email;
}

class PasswordResetForm {
  const PasswordResetForm({
    required this.userId,
    required this.title,
    required this.name,
    required this.isStaff,
  });

  factory PasswordResetForm.fromJson(Map<String, dynamic> json) {
    return PasswordResetForm(
      userId: json['user_id'] as int,
      title: json['title'] as String? ?? 'パスワード設定画面',
      name: json['name'] as String? ?? '',
      isStaff: json['is_staff'] as bool? ?? false,
    );
  }

  final int userId;
  final String title;
  final String name;
  final bool isStaff;
}

class PasswordResetResult {
  const PasswordResetResult({
    required this.success,
    required this.message,
  });

  factory PasswordResetResult.fromJson(Map<String, dynamic> json) {
    return PasswordResetResult(
      success: json['success'] as bool? ?? false,
      message: json['message'] as String? ?? '',
    );
  }

  final bool success;
  final String message;
}

class AdminUserList {
  const AdminUserList({
    required this.userId,
    required this.title,
    required this.users,
  });

  factory AdminUserList.fromJson(Map<String, dynamic> json) {
    return AdminUserList(
      userId: json['user_id'] as int,
      title: json['title'] as String? ?? 'ユーザ・リスト',
      users: (json['users'] as List<dynamic>? ?? [])
          .map((item) => AdminUser.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final int userId;
  final String title;
  final List<AdminUser> users;
}
