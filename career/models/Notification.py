from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    keyword = models.CharField(max_length=128, null=True)
