from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Instructor import Instructor
from career.models.Location import Location


class Lecture(BaseModel):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    isPaid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    room = models.CharField(max_length=256,null=True)
