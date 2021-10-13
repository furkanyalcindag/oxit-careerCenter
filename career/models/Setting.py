from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=128)
    value = models.TextField()
