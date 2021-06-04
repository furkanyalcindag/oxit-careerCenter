from django.db import models

from career.models import BaseModel
from career.models.Person import Person
from career.models.Unit import Unit


class UnitStaff(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

