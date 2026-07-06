// lib/components/custom_button.dart
import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool helpNeeded;

  const CustomButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.helpNeeded = false,
  });

  @override
  Widget build(BuildContext context) {
    // Looks up primary blue or emergency red dynamically from our design token mapping
    final Color buttonColor = helpNeeded
        ? Theme.of(context).colorScheme.error
        : Theme.of(context).colorScheme.primary;

    return FilledButton(
      style: FilledButton.styleFrom(
        backgroundColor: buttonColor,
        padding: const EdgeInsets.symmetric(vertical: 12.0, horizontal: 24.0),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(6.0), // System design radius token
        ),
      ),
      onPressed: onPressed,
      child: Text(
        label,
        style: const TextStyle(fontSize: 14.0, fontWeight: FontWeight.w600),
      ),
    );
  }
}