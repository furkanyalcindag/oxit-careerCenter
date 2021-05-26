from django.db import models

from career.models.BaseModel import BaseModel
from career.models.Language import Language
from career.models.MilitaryStatus import MilitaryStatus


class MilitaryStatusDescription(BaseModel):
    militaryStatus = models.ForeignKey(MilitaryStatus, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)