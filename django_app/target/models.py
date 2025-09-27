from django.db import models

from mission.models import Mission


class Target(models.Model):
    name = models.CharField(max_length=74)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    country = models.CharField(max_length=25)
    notes = models.TextField()
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
