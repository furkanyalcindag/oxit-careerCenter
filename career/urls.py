from django.conf.urls import url

from career.Views.AppointmentViews import AppointmentApi
from career.Views.BlogViews import BlogApi
from career.Views.CompanyViews import CompanyApi, CompanyGeneralInformationApi, CompanyAboutInformationApi, \
    CompanyCommunicationInformationApi
from career.Views.ConsultantViews import ConsultantApi
from career.Views.GeneralViews import LanguageApi, LocationSelectApi, CityDistrictSelectApi
from career.Views.InitViews import InitDataApi, LocationDataApi, CityDistrictDataApi
from career.Views.InstructorViews import InstructorApi, InstructorSelectApi
from career.Views.LectureViews import LectureApi, LectureInfoApi
from career.Views.StudentViews import StudentApi

app_name = 'career'

urlpatterns = [

    url(r'initial-data-api/$', InitDataApi.as_view()),
    url(r'initial-location-data-api/$', LocationDataApi.as_view()),
    url(r'initial-city-data-api/$', CityDistrictDataApi.as_view()),

    # general
    url(r'location-select-api/$', LocationSelectApi.as_view()),
    url(r'city-district-select-api/$', CityDistrictSelectApi.as_view()),

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

    # lecture
    url(r'lecture-api/$', LectureApi.as_view()),
    url(r'lecture-info-api/$', LectureInfoApi.as_view()),

    # --------------------------------company api-------------------------------------------------------
    url(r'company/company-general-information-api/$', CompanyGeneralInformationApi.as_view()),
    url(r'company/company-about-information-api/$', CompanyAboutInformationApi.as_view()),
    url(r'company/company-communication-information-api/$', CompanyCommunicationInformationApi.as_view()),

    # -----------------------------consultant api----------------------------------------
    url(r'consultant/appointment-api/$', AppointmentApi.as_view()),

]
