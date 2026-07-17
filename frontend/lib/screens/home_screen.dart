import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({
    super.key,
    required this.email,
    this.userId,
    this.status,
  });

  final String email;
  final int? userId;
  final int? status;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('ITIL4'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome, $email',
              style: theme.textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            if (userId != null) Text('User ID: $userId'),
            if (status != null) Text('Status: $status'),
            const SizedBox(height: 24),
            Text(
              'Login is connected to the ITIL4 server. '
              'Exam screens will be added here for web, iPhone, and Android.',
              style: theme.textTheme.bodyLarge,
            ),
          ],
        ),
      ),
    );
  }
}
