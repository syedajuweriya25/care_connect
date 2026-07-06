from django.contrib import admin
from .models import EmergencyAlert


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
