import os
import django
import json

django_env = os.path.join(os.path.dirname(__file__), 'care_backend', 'care_backend', 'settings.py')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
django.setup()

from rest_framework.test import APIClient
from users.serializers import RegisterSerializer

payload = {
    'full_name': 'Test User',
    'email': 'testuserx@example.com',
    'phone': '1234567890',
    'role': 'resident',
    'password': 'StrongPass123',
    'password_confirm': 'StrongPass123',
    'role_details': {'apartment_number': 'A-101'},
    'blood_group': 'O+',
    'emergency_contact_name': 'Jane Doe',
    'emergency_contact_phone': '0987654321',
    'medical_conditions': 'None',
    'allergies': 'Peanuts',
    'address': '123 Main Street',
}

serializer = RegisterSerializer(data=payload)
print('serializer valid:', serializer.is_valid())
print('serializer errors:', serializer.errors)

client = APIClient()
response = client.post('/api/auth/register/', payload, format='json')
print('api status:', response.status_code)
print('api data type:', type(response.data) if hasattr(response, 'data') else 'no data')
print('api response repr:', repr(response.content[:1000]))
