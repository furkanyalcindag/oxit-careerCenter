from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Consultant import Consultant
from career.models.Location import Location
from career.models.Student import Student


class Appointment(BaseModel):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    startTime = models.TimeField(null=True)
    finishTime = models.TimeField(null=True)
    date = models.DateField()
    isCome = models.BooleanField(default=True)
    isSuitable = models.BooleanField(default=True)
    isPaid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    room = models.CharField(max_length=256, null=True)
