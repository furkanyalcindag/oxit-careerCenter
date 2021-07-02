from django.db import models

from career.models.BaseModel import BaseModel


class Category(BaseModel):
    keyword = models.CharField(max_length=256)
    type = models.CharField(max_length=128, null=True)
    isButton = models.BooleanField(default=False)
