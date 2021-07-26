from django.db import models

from career.models import BaseModel, Student


class StudentQualification(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    rating = models.IntegerField()
