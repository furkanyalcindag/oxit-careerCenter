from django.db import models

from career.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=128, null=True, default=True)
    address = models.CharField(max_length=256)
    phoneNumber = models.CharField(max_length=128)
