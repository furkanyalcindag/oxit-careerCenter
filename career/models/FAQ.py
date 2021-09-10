from django.db import models

from career.models import BaseModel


class FAQ(BaseModel):
    keyword = models.CharField(max_length=128)
