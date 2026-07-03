// this file is used to configure the theme for the mobile app
import 'package:flutter/material.dart';

abstract final class AppTheme {
  // 1. Premium Classy Color Palette Tokens (This is the premium classy color palette tokens)
  static const Color primaryObsidian = Color(0xFF11141A); // Deep, cool charcoal black
  static const Color luxuryGold     = Color(0xFFC5A880); // Understated champagne gold accent
  static const Color mutedSlate      = Color(0xFF64748B); // This is the cool, readable slate gray
  static const Color premiumPlatinum = Color(0xFFF8FAFC); // This is the clean, ultra-light canvas gray
  static const Color surfacePure     = Color(0xFFFFFFFF); // This is the sharp container background
  
  // High-visibility semantic colors (kept simple for safety actions) (This is the high-visibility semantic colors (kept simple for safety actions))     (This is the vibrant crimson for critical SOS alerts)
  static const Color safetyRed       = Color(0xFFE11D48); // This is the vibrant crimson for critical SOS alerts
  static const Color warningAmber    = Color(0xFFD97706); // This is the warm amber for pending alerts

  // 2. Classy & Aesthetic Flutter Theme Constructor (This is the classy & aesthetic Flutter Theme Constructor) (This is the light theme)
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: premiumPlatinum,
      
      // Map brand colors into Flutter's functional token engine (This is the color scheme for the light theme)
      colorScheme: const ColorScheme.light(
        primary: primaryObsidian,
        secondary: luxuryGold,
        error: safetyRed,
        surface: surfacePure,
        onPrimary: surfacePure,
        onSecondary: primaryObsidian,
      ),

      // 3. Clean, Sophisticated Typography Layout (This is the text theme for the light theme)
      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          fontSize: 26.0,
          fontWeight: FontWeight.w700, // This is the clean, geometric bold weight
          letterSpacing: -0.5,         // Modern aesthetic tracking
          color: primaryObsidian,
        ),
        titleMedium: TextStyle(
          fontSize: 16.0,
          fontWeight: FontWeight.w600, // This is the semi-bold for navigational labels
          letterSpacing: 0.1,
          color: primaryObsidian,
        ),
        bodyMedium: TextStyle(
          fontSize: 14.0,
          fontWeight: FontWeight.w400, // This is the light and spacious line balance
          height: 1.5,                 // This is the clean line-height for seamless scanning
          color: mutedSlate,
        ),
      ),

      // 4. Component-Specific Aesthetic Overrides (This is the app bar theme for the light theme)
      appBarTheme: const AppBarTheme(
        backgroundColor: premiumPlatinum,
        elevation: 0,                  // This is the perfectly flat, clean header
        centerTitle: false,             // This is the modern left-aligned look
        iconTheme: IconThemeData(color: primaryObsidian),
        titleTextStyle: TextStyle(
          fontSize: 20.0,
          fontWeight: FontWeight.w700,
          color: primaryObsidian,
          letterSpacing: -0.5,
        ),
      ),

      // Premium styling for rounded interaction cards (This is the card theme for the light theme)
      cardTheme: CardThemeData(
        color: surfacePure,
        elevation: 0,
        shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16.0), // This is the generous, smooth aesthetic radius
        side: const BorderSide(color: Color(0xFFE2E8F0), width: 1.0), // This is the elegant hairline border
        ),
      ),
    );
  }
}