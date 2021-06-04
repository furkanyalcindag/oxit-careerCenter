from django.db import models

from career.models.BaseModel import BaseModel
from career.models.BlogType import BlogType
from career.models.Category import Category
from career.models.Profile import Profile




class Blog(BaseModel):
    keyword = models.CharField(max_length=128, default=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    blogType = models.ForeignKey(BlogType, on_delete=models.CASCADE, default=None)
