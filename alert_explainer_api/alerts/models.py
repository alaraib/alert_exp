from django.db import models
from django.utils import timezone


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ("critical", "Critical"),
        ("warning", "Warning"),
        ("info", "Info"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    source = models.CharField(max_length=255)
    metric_name = models.CharField(max_length=255)
    metric_value = models.FloatField()
    threshold = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "alerts"

    def __str__(self):
        return f"{self.severity}: {self.title}"