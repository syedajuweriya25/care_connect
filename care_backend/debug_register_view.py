import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from users.views import RegisterView
from django.conf import settings
settings.DEBUG = True

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

factory = APIRequestFactory()
request = factory.post('/api/auth/register/', payload, format='json')
view = RegisterView.as_view()
try:
    response = view(request)
    print('response status', response.status_code)
    print('response type', type(response))
    if hasattr(response, 'data'):
        print('response data', response.data)
    else:
        print('response content', response.content[:1000])
except Exception as exc:
    import traceback
    traceback.print_exc()
