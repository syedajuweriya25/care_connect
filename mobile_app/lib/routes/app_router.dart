import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:go_router/go_router.dart';
import '../views/login_view.dart';
import '../views/dashboard_view.dart';
import '../views/register_view.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/login',
    redirect: (context, state) async {
      final storage = const FlutterSecureStorage();
      final token = await storage.read(key: 'access_token');
      final isAuthenticatedRoute = state.matchedLocation == '/dashboard';
      final isAuthRoute = state.matchedLocation == '/login' || state.matchedLocation == '/register';

      if (isAuthenticatedRoute && token == null) {
        return '/login';
      }
      if (isAuthRoute && token != null) {
        return '/dashboard';
      }
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (context, state) => const LoginView()),
      GoRoute(path: '/register', builder: (context, state) => const RegisterView()),
      GoRoute(path: '/dashboard', builder: (context, state) => const DashboardView()),
    ],
  );
}