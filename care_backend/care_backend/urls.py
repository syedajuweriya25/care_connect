"""
URL configuration for care_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as static_serve
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({'status': 'ok', 'service': 'care_backend'})


schema_view = get_schema_view(
    openapi.Info(
        title="CareConnect - Community Emergency Response API",
        default_version='v1',
        description="Backend REST APIs for the CareConnect emergency response system.",
    ),
    public=True,
    # change permismission to IsAuthenticated before deploying
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('api/auth/', include('users.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif settings.SERVE_STATIC_FILES:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
