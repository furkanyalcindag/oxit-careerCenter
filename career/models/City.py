from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3, null=True)
