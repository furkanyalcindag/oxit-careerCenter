from django.contrib import admin

from career.models.Company import Company
from career.models.Student import Student

admin.site.register(Company)
admin.site.register(Student)