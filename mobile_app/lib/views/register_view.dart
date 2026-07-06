import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:go_router/go_router.dart';
import '../services/api_config.dart';

class RegisterView extends StatefulWidget {
  const RegisterView({super.key});

  @override
  State<RegisterView> createState() => _RegisterViewState();
}

class _RegisterViewState extends State<RegisterView> {
  final _formKey = GlobalKey<FormState>();
  final _fullNameController = TextEditingController();
  final _emailController = TextEditingController();
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  final _passwordConfirmController = TextEditingController();
  String _role = 'resident';
  bool _isLoading = false;
  String? _errorMessage;
  final _storage = const FlutterSecureStorage();

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    if (_passwordController.text != _passwordConfirmController.text) {
      setState(() => _errorMessage = 'Passwords do not match.');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final client = ApiConfig.getDioClient();
      final response = await client.post('/api/auth/register/', data: {
        'full_name': _fullNameController.text.trim(),
        'email': _emailController.text.trim(),
        'phone': _phoneController.text.trim(),
        'role': _role,
        'password': _passwordController.text,
        'password_confirm': _passwordConfirmController.text,
      });
      await _storage.write(key: 'access_token', value: response.data['access']);
      await _storage.write(key: 'refresh_token', value: response.data['refresh']);
      if (mounted) {
        context.go('/dashboard');
      }
    } catch (error) {
      setState(() => _errorMessage = 'Unable to create your account right now.');
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 420),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: ListView(
                shrinkWrap: true,
                children: [
                  const Text('Create account', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  const Text('Join as a resident, guardian, volunteer, or security member.', textAlign: TextAlign.center),
                  const SizedBox(height: 24),
                  TextFormField(
                    controller: _fullNameController,
                    decoration: const InputDecoration(labelText: 'Full name'),
                    validator: (value) => value == null || value.isEmpty ? 'Enter your name' : null,
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _emailController,
                    decoration: const InputDecoration(labelText: 'Email'),
                    validator: (value) => value == null || value.isEmpty ? 'Enter your email' : null,
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _phoneController,
                    decoration: const InputDecoration(labelText: 'Phone'),
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField<String>(
                    value: _role,
                    decoration: const InputDecoration(labelText: 'Role'),
                    items: const [
                      DropdownMenuItem(value: 'resident', child: Text('Resident')),
                      DropdownMenuItem(value: 'guardian', child: Text('Guardian')),
                      DropdownMenuItem(value: 'volunteer', child: Text('Volunteer')),
                      DropdownMenuItem(value: 'security', child: Text('Security')),
                    ],
                    onChanged: (value) => setState(() => _role = value ?? 'resident'),
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Password'),
                    validator: (value) => value != null && value.length >= 8 ? null : 'Use at least 8 characters',
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _passwordConfirmController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Confirm password'),
                    validator: (value) => value != null && value.isNotEmpty ? null : 'Confirm your password',
                  ),
                  const SizedBox(height: 16),
                  if (_errorMessage != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Text(_errorMessage!, style: const TextStyle(color: Colors.red)),
                    ),
                  FilledButton(
                    onPressed: _isLoading ? null : _submit,
                    child: _isLoading ? const CircularProgressIndicator() : const Text('Register'),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () => context.go('/login'),
                    child: const Text('Back to sign in'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
