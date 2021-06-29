from django.db import models

from career.models.Language import Language
from career.models.Notification import Notification


class NotificationDescription(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    message = models.TextField()
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
