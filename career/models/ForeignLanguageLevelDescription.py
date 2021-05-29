from django.db import models

from career.models import ForeignLanguageLevel
from career.models.Language import Language


class ForeignLanguageLevelDescription(models.Model):
    name = models.CharField(max_length=128)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    foreignLanguageLevel = models.ForeignKey(ForeignLanguageLevel, on_delete=models.CASCADE)
