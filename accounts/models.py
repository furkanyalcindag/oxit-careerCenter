from django.contrib.auth.models import Group
from django.db import models


# Create your models here.
class UrlName(models.Model):
    name = models.CharField(max_length=256)
    lookupString = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)



class UrlMethod(models.Model):
    url = models.ForeignKey(UrlName, on_delete=models.ForeignKey)
    method_Name = models.CharField(max_length=255)


class GroupUrlMethod(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    urlMethod = models.ForeignKey(UrlMethod, on_delete=models.CASCADE)
    isAccess = models.BooleanField(default=False)






