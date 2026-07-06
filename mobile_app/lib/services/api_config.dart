// This file is used to configure the API client for the mobile app
import 'package:dio/dio.dart';

class ApiConfig {
  static const String baseUrl = 'http://10.0.2.2:8000';

  static Dio getDioClient() {
    final options = BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 3),
      headers: {'Content-Type': 'application/json'},
    );

    return Dio(options);
  }
}