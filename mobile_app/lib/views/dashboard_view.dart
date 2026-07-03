import 'package:flutter/material.dart';
// This file is used to display the dashboard for the mobile app
class DashboardView extends StatelessWidget {
  // This is the constructor for the DashboardView
  const DashboardView({super.key});
  // This is the build method for the DashboardView
  @override
  Widget build(BuildContext context) {
    return const Scaffold(body: Center(child: Text("CareConnect Mobile Dashboard")));
  }
}