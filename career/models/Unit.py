from django.db import models

from career.models import BaseModel


class Unit(BaseModel):
    name = models.CharField(max_length=256)
    website = models.CharField(max_length=256, null=True)
    order = models.IntegerField(null=False)
