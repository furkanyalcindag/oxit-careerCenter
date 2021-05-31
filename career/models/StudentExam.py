from django.db import models

from career.models import BaseModel, Student


class StudentExam(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    point = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    year = models.IntegerField()
