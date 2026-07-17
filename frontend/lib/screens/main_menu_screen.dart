import 'package:flutter/material.dart';

import '../models/main_menu.dart';
import '../services/admin_service.dart';
import '../services/exam_service.dart';
import '../services/menu_service.dart';
import 'admin_screen.dart';
import 'exercise_screen.dart';
import 'login_screen.dart';
import 'single_exercise_screen.dart';

class MainMenuScreen extends StatefulWidget {
  const MainMenuScreen({
    super.key,
    required this.userId,
    required this.email,
  });

  final int userId;
  final String email;

  @override
  State<MainMenuScreen> createState() => _MainMenuScreenState();
}

class _MainMenuScreenState extends State<MainMenuScreen> {
  final _menuService = MenuService();
  final _examService = ExamService();
  final _adminService = AdminService();
  late Future<MainMenu> _menuFuture;

  @override
  void initState() {
    super.initState();
    _menuFuture = _menuService.fetchMainMenu(widget.userId);
  }

  Future<void> _reloadMenu() async {
    setState(() {
      _menuFuture = _menuService.fetchMainMenu(widget.userId);
    });
    await _menuFuture;
  }

  Color _parseColor(String hex) {
    final value = hex.replaceFirst('#', '');
    return Color(int.parse('FF$value', radix: 16));
  }

  Future<void> _onMenuItemTap(MenuItem item, String? sectionMessage) async {
    if (!item.enabled) {
      final message = sectionMessage ?? 'This option is not available yet.';
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(message)),
      );
      return;
    }

    if (item.action == 'makeExam3') {
      try {
        final session = await _examService.startSingleExam(
          userId: widget.userId,
          category: item.category,
        );
        if (!mounted) {
          return;
        }
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => SingleExerciseScreen(
              session: session,
              email: widget.email,
            ),
          ),
        );
        await _reloadMenu();
      } catch (error) {
        if (!mounted) {
          return;
        }
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error.toString())),
        );
      }
      return;
    }

    if (item.action != 'makeExam') {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('This exam type will be added in a future update.'),
        ),
      );
      return;
    }

    try {
      final session = await _examService.startExam(
        userId: widget.userId,
        category: item.category,
      );
      if (!mounted) {
        return;
      }
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (_) => ExerciseScreen(
            initialSession: session,
            email: widget.email,
          ),
        ),
      );
      await _reloadMenu();
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    }
  }

  Future<void> _onActionTap(MenuAction action) async {
    if (action.id == 'logout') {
      await _menuService.logout(widget.userId);
      if (!mounted) {
        return;
      }
      await Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute<void>(builder: (_) => const LoginScreen()),
        (_) => false,
      );
      return;
    }

    if (action.id == 'admin') {
      try {
        final home = await _adminService.enterAdmin(widget.userId);
        if (!mounted) {
          return;
        }
        await Navigator.of(context).push(
          MaterialPageRoute<void>(
            builder: (_) => AdminScreen(
              userId: widget.userId,
              email: widget.email,
              initialHome: home,
            ),
          ),
        );
        await _reloadMenu();
      } catch (error) {
        if (!mounted) {
          return;
        }
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error.toString())),
        );
      }
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('${action.label} will open in a future update.')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('メインメニュー'),
        actions: [
          IconButton(
            onPressed: _reloadMenu,
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: FutureBuilder<MainMenu>(
        future: _menuFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(snapshot.error.toString()),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _reloadMenu,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            );
          }

          final menu = snapshot.data!;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Text(
                menu.email.isNotEmpty ? menu.email : widget.email,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              Text('Status: ${menu.status}'),
              const SizedBox(height: 16),
              for (final section in menu.sections) ...[
                Text(
                  section.title,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                if (section.message != null) ...[
                  const SizedBox(height: 8),
                  Text(section.message!),
                ],
                const SizedBox(height: 12),
                for (final item in section.items)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: _MenuButton(
                      item: item,
                      color: _parseColor(item.color),
                      onTap: () => _onMenuItemTap(item, section.message),
                    ),
                  ),
                const SizedBox(height: 16),
              ],
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  for (final action in menu.actions)
                    OutlinedButton(
                      onPressed: action.enabled ? () => _onActionTap(action) : null,
                      child: Text(action.label),
                    ),
                ],
              ),
            ],
          );
        },
      ),
    );
  }
}

class _MenuButton extends StatelessWidget {
  const _MenuButton({
    required this.item,
    required this.color,
    required this.onTap,
  });

  final MenuItem item;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final background = item.enabled ? color : Colors.grey.shade400;

    return Material(
      color: background,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                item.label,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                item.subtitle,
                style: const TextStyle(color: Colors.white),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
