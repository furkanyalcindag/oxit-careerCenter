from django.db import models

from career.models import BaseModel
from career.models.Consultant import Consultant
from career.models.Category import Category


class ConsultantCategory(BaseModel):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
