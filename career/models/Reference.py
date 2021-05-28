from django.db import models

from career.models import BaseModel, Student


class Reference(BaseModel):
    firstName = models.CharField(max_length=128, null=True)
    lastName = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=128, null=True)
    telephoneNumber = models.CharField(max_length=128, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
