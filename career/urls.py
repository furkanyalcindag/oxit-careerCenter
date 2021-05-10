from django.conf.urls import url

from career.Views.CompanyViews import CompanyApi
from career.Views.ConsultantViews import ConsultantApi
from career.Views.InitViews import InitDataApi
from career.Views.InstructorViews import InstructorApi
from career.Views.StudentViews import StudentApi

app_name = 'career'

urlpatterns = [

    url(r'student-api/$', StudentApi.as_view()),
    url(r'initial-data-api/$', InitDataApi.as_view()),

    # ----------------admin api---------------------------
    # student

    url(r'student-api/$', StudentApi.as_view()),

    # company
    url(r'company-api/$', CompanyApi.as_view()),

    # consultant
    url(r'consultant-api/$', ConsultantApi.as_view()),

    # consultant
    url(r'instructor-api/$', InstructorApi.as_view()),

]
