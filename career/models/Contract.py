from django.db import models


class Contract(models.Model):
    name = models.CharField(max_length=128)
    text = models.TextField()
    isActive = models.BooleanField()
