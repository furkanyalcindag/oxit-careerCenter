from django.contrib.auth.models import User
from django.db import models

from career.models import BaseModel
from career.models.Contract import Contract


class UserContract(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
