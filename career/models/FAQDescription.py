from django.db import models

from career.models import BaseModel, Language
from career.models.FAQ import FAQ


class FAQDescription(BaseModel):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    question = models.CharField(max_length=128)
    answer = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
