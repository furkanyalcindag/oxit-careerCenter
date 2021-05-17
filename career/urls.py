from django.conf.urls import url

from career.Views.BlogViews import BlogApi
from career.Views.CompanyViews import CompanyApi
from career.Views.ConsultantViews import ConsultantApi
from career.Views.GeneralViews import LanguageApi, LocationSelectApi
from career.Views.InitViews import InitDataApi
from career.Views.InstructorViews import InstructorApi, InstructorSelectApi
from career.Views.StudentViews import StudentApi

app_name = 'career'

urlpatterns = [

    url(r'initial-data-api/$', InitDataApi.as_view()),
    url(r'location-select-api/$', LocationSelectApi.as_view()),

    # ----------------admin api---------------------------
    # student
    url(r'student-api/$', StudentApi.as_view()),

    # company
    url(r'company-api/$', CompanyApi.as_view()),

    # consultant
    url(r'consultant-api/$', ConsultantApi.as_view()),

    # instructor
    url(r'instructor-api/$', InstructorApi.as_view()),
    url(r'instructor-select-api/$', InstructorSelectApi.as_view()),

    # language
    url(r'language-api/$', LanguageApi.as_view()),

    # blog
    url(r'blog-api/$', BlogApi.as_view()),

]
