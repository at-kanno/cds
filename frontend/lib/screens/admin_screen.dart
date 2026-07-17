import 'package:flutter/material.dart';

import '../models/admin_models.dart';
import '../services/admin_service.dart';
import 'main_menu_screen.dart';
import 'password_reset_screen.dart';

class AdminScreen extends StatefulWidget {
  const AdminScreen({
    super.key,
    required this.userId,
    required this.email,
    required this.initialHome,
  });

  final int userId;
  final String email;
  final AdminHome initialHome;

  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  final _adminService = AdminService();
  late AdminHome _home;

  @override
  void initState() {
    super.initState();
    _home = widget.initialHome;
  }

  Color get _backgroundColor =>
      _home.isStaff ? const Color(0xFFF8CBAD) : const Color(0xFFCCFFCC);

  Future<void> _openAction(AdminAction action) async {
    if (!action.enabled) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(action.message ?? 'Not available yet.')),
      );
      return;
    }

    switch (action.id) {
      case 'history':
        final history = await _adminService.fetchHistory(widget.userId);
        if (!mounted) return;
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => HistoryScreen(
              history: history,
              userId: widget.userId,
            ),
          ),
        );
        return;
      case 'status':
        final status = await _adminService.fetchStatus(userId: widget.userId);
        if (!mounted) return;
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => StatusScreen(
              status: status,
              userId: widget.userId,
            ),
          ),
        );
        return;
      case 'user_list':
        final users = await _adminService.fetchUsers(widget.userId);
        if (!mounted) return;
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => UserListScreen(
              userList: users,
              actorUserId: widget.userId,
            ),
          ),
        );
        return;
      case 'reset_password':
        final form = await _adminService.fetchPasswordResetForm(widget.userId);
        if (!mounted) return;
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => PasswordResetScreen(form: form),
          ),
        );
        return;
      default:
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(action.message ?? 'Not available yet.')),
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _backgroundColor,
      appBar: AppBar(
        title: Text(_home.title),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (final action in _home.actions)
            Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: FilledButton(
                onPressed: () => _openAction(action),
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(56),
                  backgroundColor: action.enabled ? null : Colors.grey,
                ),
                child: Text(action.label),
              ),
            ),
          const SizedBox(height: 16),
          OutlinedButton(
            onPressed: () {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute<void>(
                  builder: (_) => MainMenuScreen(
                    userId: widget.userId,
                    email: widget.email,
                  ),
                ),
                (_) => false,
              );
            },
            child: const Text('メインメニューへ戻る'),
          ),
        ],
      ),
    );
  }
}

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({
    super.key,
    required this.history,
    required this.userId,
  });

  final ExerciseHistory history;
  final int userId;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(history.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (history.count == 0)
            const Text('演習履歴はありません。')
          else
            for (final item in history.items)
              Card(
                child: ListTile(
                  title: Text(item.label),
                  trailing: Text(item.passed ? '合格' : '不合格'),
                ),
              ),
        ],
      ),
    );
  }
}

class StatusScreen extends StatelessWidget {
  const StatusScreen({
    super.key,
    required this.status,
    required this.userId,
  });

  final UserStatusData status;
  final int userId;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(status.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('【ステータス】${status.grade}'),
          const SizedBox(height: 24),
          Text('模擬試験の履歴', style: Theme.of(context).textTheme.titleLarge),
          if (status.mockCount == 0)
            const Text('模擬試験の履歴はありません。')
          else
            for (final item in status.mockItems)
              ListTile(
                title: Text(item.label),
                trailing: Text(item.passed ? '合格' : '不合格'),
              ),
          const SizedBox(height: 24),
          Text('修了試験の履歴', style: Theme.of(context).textTheme.titleLarge),
          if (status.finalCount == 0)
            const Text('修了試験の履歴はありません。')
          else
            for (final item in status.finalItems)
              ListTile(
                title: Text(item.label),
                trailing: Text(item.passed ? '合格' : '不合格'),
              ),
        ],
      ),
    );
  }
}

class UserListScreen extends StatefulWidget {
  const UserListScreen({
    super.key,
    required this.userList,
    required this.actorUserId,
  });

  final AdminUserList userList;
  final int actorUserId;

  @override
  State<UserListScreen> createState() => _UserListScreenState();
}

class _UserListScreenState extends State<UserListScreen> {
  final _adminService = AdminService();
  late List<AdminUser> _users;

  @override
  void initState() {
    super.initState();
    _users = widget.userList.users;
  }

  Future<void> _reload() async {
    final users = await _adminService.fetchUsers(widget.actorUserId);
    setState(() => _users = users.users);
  }

  Future<void> _deleteUser(AdminUser user) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('削除確認'),
        content: Text('${user.label} を削除しても構いませんか？'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('キャンセル')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('削除')),
        ],
      ),
    );
    if (confirmed != true) return;

    await _adminService.deleteUser(
      actorUserId: widget.actorUserId,
      targetUserId: user.id,
    );
    await _reload();
  }

  Future<void> _rankUp(AdminUser user) async {
    final message = await _adminService.rankUpUser(
      actorUserId: widget.actorUserId,
      targetUserId: user.id,
    );
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _showStatus(AdminUser user) async {
    final status = await _adminService.fetchStatus(
      userId: widget.actorUserId,
      targetUserId: user.id,
    );
    if (!mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => StatusScreen(status: status, userId: widget.actorUserId),
      ),
    );
  }

  Future<void> _showHistory(AdminUser user) async {
    final history = await _adminService.fetchHistory(user.id);
    if (!mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => HistoryScreen(history: history, userId: user.id),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.userList.title)),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _users.length,
        itemBuilder: (context, index) {
          final user = _users[index];
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(user.label),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      OutlinedButton(onPressed: () => _showHistory(user), child: const Text('履歴')),
                      OutlinedButton(onPressed: () => _showStatus(user), child: const Text('状態')),
                      OutlinedButton(onPressed: () => _rankUp(user), child: const Text('模試')),
                      OutlinedButton(onPressed: () => _deleteUser(user), child: const Text('削除')),
                    ],
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
