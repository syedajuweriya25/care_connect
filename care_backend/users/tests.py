import json

from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get(reverse('health-check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')


class AuthenticationTests(TestCase):
    def test_registration_creates_user_and_returns_tokens(self):
        response = self.client.post(
            reverse('register'),
            data=json.dumps({
                'full_name': 'Ava Patel',
                'email': 'ava@example.com',
                'phone': '1555123456',
                'password': 'StrongPass123!',
                'password_confirm': 'StrongPass123!',
                'role': 'resident',
                'role_details': {'apartment_number': 'A-101'},
                'blood_group': 'O+',
                'emergency_contact_name': 'Maya Patel',
                'emergency_contact_phone': '0987654321',
                'medical_conditions': 'None',
                'allergies': 'None',
                'address': '101 Main Street',
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_login_returns_tokens_for_existing_user(self):
        self.client.post(
            reverse('register'),
            data=json.dumps({
                'full_name': 'Noah Chen',
                'email': 'noah@example.com',
                'phone': '1555123456',
                'password': 'StrongPass123!',
                'password_confirm': 'StrongPass123!',
                'role': 'volunteer',
                'role_details': {'volunteer_skills': 'Community assistance'},
                'blood_group': 'A+',
                'emergency_contact_name': 'Sam Chen',
                'emergency_contact_phone': '0987654321',
                'medical_conditions': 'None',
                'allergies': 'None',
                'address': '202 Elm Street',
            }),
            content_type='application/json',
        )

        response = self.client.post(
            reverse('login'),
            {'email': 'noah@example.com', 'password': 'StrongPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
