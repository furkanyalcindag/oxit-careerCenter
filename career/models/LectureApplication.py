from django.db import models

from career.models import BaseModel
from career.models.Lecture import Lecture
from career.models.Student import Student


class LectureApplication(BaseModel):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    isSuccessApplication = models.BooleanField(default=True)
