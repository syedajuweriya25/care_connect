# CareConnect

CareConnect is a safety and emergency response platform for gated communities and societies.

## Project structure

- Backend: care_backend/
- Web admin portal: web-admin-portal/
- Mobile app: mobile_app/

## Quick start

### Backend
1. cd care_backend
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py runserver

### Web admin portal
1. cd web-admin-portal
2. npm install
3. npm run dev

### Mobile app
1. cd mobile_app
2. flutter pub get
3. flutter run

## Notes
- The backend exposes a health endpoint at /health/ and Swagger at /swagger/.
- The web portal reads its API base URL from VITE_API_BASE_URL.
