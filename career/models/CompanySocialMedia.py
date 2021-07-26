from django.db import models

from career.models import Company
from career.models.BaseModel import BaseModel
from career.models.Profile import Profile
from career.models.SocialMedia import SocialMedia


class CompanySocialMedia(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    socialMedia = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=256, null=True, blank=True)
