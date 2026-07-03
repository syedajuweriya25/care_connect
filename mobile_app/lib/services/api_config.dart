// This file is used to configure the API client for the mobile app
import 'package:dio/dio';

// This class is used to configure the API client for the mobile app
class ApiConfig {
  // Your backend base destination
  static const String baseUrl = "http://10.0.2.2:8000/api/v1/"; 
  
  // NOTE: In Flutter development, 10.0.2.2 is a special loopback address 
  // that allows the Android Emulator to connect directly to your local computer's localhost:8000.

// This method is used to get the API client for the mobile app
  static Dio getDioClient() {
    // This is the base options for the API client
    BaseOptions options = BaseOptions(
      // This is the base URL for the API client
      baseUrl: baseUrl,
      // This is the connect timeout for the API client
      connectTimeout: const Duration(seconds: 5),
      // This is the receive timeout for the API client
      receiveTimeout: const Duration(seconds: 3),
      // This is the headers for the API client
      headers: {
        'Content-Type': 'application/json',
      },
    );
    // This is the API client for the mobile app
    return Dio(options);
  }
}