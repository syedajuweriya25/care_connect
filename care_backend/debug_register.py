import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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
print('api type:', type(response))
print('api content type:', response['Content-Type'])
print('api content len:', len(response.content))
print('api headers:', dict(response.items()))
print('api container:', getattr(response, '_container', None))
print('api charset:', response.charset)
print('api reason_phrase:', response.reason_phrase)
try:
    print('api data:', response.data)
except Exception as e:
    print('api data error:', e)
