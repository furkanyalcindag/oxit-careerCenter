from django.db import models

from career.models import BaseModel, Student, Scholarship


class ScholarshipApplication(BaseModel):
    scholarShip = models.ForeignKey(Scholarship, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    isSuccessApplication = models.BooleanField(default=True)
