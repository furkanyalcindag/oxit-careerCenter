from django.db import models

from career.models import BaseModel


class MenuStudent(BaseModel):
    header = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    icon = models.CharField(max_length=256, null=True)
    route = models.CharField(max_length=256, null=True)
    parent = models.CharField(max_length=256, null=True)
    order = models.IntegerField(default=0, null=True)
