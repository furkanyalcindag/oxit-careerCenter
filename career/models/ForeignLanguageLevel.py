from django.db import models


class ForeignLanguageLevel(models.Model):
    keyword = models.CharField(max_length=128)
