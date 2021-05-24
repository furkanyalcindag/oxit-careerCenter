from django.db import models

from career.models import BaseModel, JobPost, Student


class ScholarshipApplication(BaseModel):
    scholarShip = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    isSuccessApplication = models.BooleanField(default=True)
