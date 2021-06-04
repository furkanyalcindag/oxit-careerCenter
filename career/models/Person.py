from django.db import models

from career.models import BaseModel


class Person(BaseModel):
    firstName = models.CharField(max_length=64, null=True, blank=True)
    lastName = models.CharField(max_length=64, null=True, blank=True)
    title = models.CharField(max_length=64, null=True, blank=True)
    cvLink = models.CharField(max_length=256,null=True,blank=True)
