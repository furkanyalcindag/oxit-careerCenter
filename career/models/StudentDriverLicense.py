from django.db import models

from career.models import BaseModel, Student


class StudentDriverLicense(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    driverLicense = models.CharField(max_length=12, null=True)
