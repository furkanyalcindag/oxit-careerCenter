from django.contrib.auth.models import User
from django.db import models

from career.models import BaseModel, Notification


class NotificationUser(BaseModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isRead = models.BooleanField(default=False)
