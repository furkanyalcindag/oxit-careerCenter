from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Person import Person


class Instructor(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=128, null=True, blank=True)
