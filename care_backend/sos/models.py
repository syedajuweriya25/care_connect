from django.db import models


class EmergencyAlert(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Emergency Alert'
        verbose_name_plural = 'Emergency Alerts'

    def __str__(self) -> str:
        return self.title
