// This file is used to run the mobile app
import 'package:flutter/material.dart';
import 'routes/app_router.dart';
import 'theme/app_theme.dart';

// This is the main function for the mobile app
void main() {
  // This ensures that all underlying native platform channel communication is ready 
  // before the application engine launches
  WidgetsFlutterBinding.ensureInitialized();
  // This runs the mobile app
  runApp(const CareConnectMobileApp());
}
// This is the main class for the mobile app
class CareConnectMobileApp extends StatelessWidget {
  // This is the constructor for the CareConnectMobileApp
  const CareConnectMobileApp({super.key});
  // This is the build method for the CareConnectMobileApp
  @override
  Widget build(BuildContext context) {
    // We change this from a basic 'MaterialApp' to a 'MaterialApp.router'
    return MaterialApp.router(
      title: 'CareConnect Mobile App',
      
      // This links Flutter directly to our custom go_router configuration engine
      routerConfig: AppRouter.router, 
      // This hooks into our centralized design system colors and fonts
      theme: AppTheme.lightTheme,     
      // This removes the red 'DEBUG' banner overlay from the top corner
      debugShowCheckedModeBanner: false,
    );
  }
}
