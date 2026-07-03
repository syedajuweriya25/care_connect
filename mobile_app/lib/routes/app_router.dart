// This file is used to configure the routes for the mobile app
// It uses the GoRouter package to configure the routes
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../views/login_view.dart';
import '../views/dashboard_view.dart';

// This class is used to configure the routes for the mobile app
class AppRouter {
  // This is the router for the mobile app
  static final GoRouter router = GoRouter(
    // This is the initial location for the mobile app
    initialLocation: '/login',
    // This is the routes for the mobile app
    routes: [
      // This is the login route for the mobile app
      GoRoute(
        path: '/login',
        builder: (BuildContext context, GoRouterState state) => const LoginView(),
      ),
      // This is the dashboard route for the mobile app
      GoRoute(
        path: '/dashboard',
        builder: (BuildContext context, GoRouterState state) => const DashboardView(),
      ),
    ],
  );
}