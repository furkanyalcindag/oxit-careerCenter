from django.db import models

from career.models import BaseModel, JobPost, Student


class JobApplication(BaseModel):
    jobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    coverLetter = models.TextField(null=True)
