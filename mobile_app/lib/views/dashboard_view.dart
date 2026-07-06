import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:go_router/go_router.dart';

class DashboardView extends StatelessWidget {
  const DashboardView({super.key});

  Future<void> _logout(BuildContext context) async {
    const storage = FlutterSecureStorage();
    await storage.delete(key: 'access_token');
    await storage.delete(key: 'refresh_token');
    if (context.mounted) context.go('/login');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('CareConnect Dashboard')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Secure dashboard ready', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            const Text('Your authenticated session is active.'),
            const SizedBox(height: 16),
            FilledButton(onPressed: () => _logout(context), child: const Text('Logout')),
          ],
        ),
      ),
    );
  }
}