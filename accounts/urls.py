#import patterns as patterns
from django.urls import path, re_path

from accounts.forms import LoginForm
from . import views




urlpatterns = [
   #path('', views.index, name='index'),
   path('login/', views.login),
   path('permission-change/', views.PermissionCreates.as_view())

]

