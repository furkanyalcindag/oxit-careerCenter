from django.db import models

from career.models import BaseModel


class BlogType(BaseModel):
    name = models.CharField(max_length=128)
