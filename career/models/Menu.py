from django.db import models

from accounts.models import UrlName
from career.models import BaseModel


class Menu(BaseModel):
    header = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    icon = models.CharField(max_length=256, null=True)
    route = models.CharField(max_length=256, null=True)
    parent = models.CharField(max_length=256, null=True)
    order = models.IntegerField(default=0, null=True)
    relationField = models.ForeignKey(UrlName, on_delete=models.CASCADE, null=True)
