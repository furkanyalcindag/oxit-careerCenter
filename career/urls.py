from django.conf.urls import url
from django.urls import path

from career.Views.AppointmentViews import AppointmentApi
from career.Views.BlogViews import BlogApi
from career.Views.CompanyViews import CompanyApi, CompanyGeneralInformationApi, CompanyAboutInformationApi, \
    CompanyCommunicationInformationApi, CompanySelectApi
from career.Views.ConsultantViews import ConsultantApi
from career.Views.GeneralViews import LanguageApi, LocationSelectApi, CityDistrictSelectApi, JobTypeSelectApi, \
    UniversitySelectApi, FacultySelectApi, EducationTypeSelectApi
from career.Views.InitViews import InitDataApi, LocationDataApi, CityDistrictDataApi, UniversityDataApi, \
    EducationTypeDataApi, MaritalStatusDataApi
from career.Views.InstructorViews import InstructorApi, InstructorSelectApi
from career.Views.JobApplicationViews import JopApplicantsApi
from career.Views.JobPostViews import JobPostApi
from career.Views.LectureViews import LectureApi, LectureInfoApi
from career.Views.ScholarshipViews import ScholarshipApi, CompanyScholarshipApi
from career.Views.StudentViews import StudentApi, StudentEducationApi, StudentHighSchoolEducationApi

app_name = 'career'

urlpatterns = [

    url(r'initial-data-api/$', InitDataApi.as_view()),
    url(r'initial-location-data-api/$', LocationDataApi.as_view()),
    url(r'initial-city-data-api/$', CityDistrictDataApi.as_view()),
    url(r'initial-uni-data-api/$', UniversityDataApi.as_view()),
    url(r'initial-education-type-api/$', EducationTypeDataApi.as_view()),
    url(r'initial-marital-status-api/$', MaritalStatusDataApi.as_view()),
    url(r'delete-logs-api/$', MaritalStatusDataApi.as_view()),

    # general
    url(r'location-select-api/$', LocationSelectApi.as_view()),
    url(r'city-district-select-api/$', CityDistrictSelectApi.as_view()),
    url(r'job-type-select-api/$', JobTypeSelectApi.as_view()),
    url(r'company-select-api/$', CompanySelectApi.as_view()),
    url(r'university-select-api/$', UniversitySelectApi.as_view()),
    url(r'faculty-select-api/$', FacultySelectApi.as_view()),
    url(r'department-select-api/$', FacultySelectApi.as_view()),
    url(r'education-type-select-api/$', EducationTypeSelectApi.as_view()),

    # ----------------admin api---------------------------
    # student
    url(r'student-api/$', StudentApi.as_view()),

    # company
    path('company-api/', CompanyApi.as_view()),

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

    # scholarship
    url(r'scholarship-api/$', ScholarshipApi.as_view()),

    # --------------------------------company api-------------------------------------------------------
    url(r'company/company-general-information-api/$', CompanyGeneralInformationApi.as_view()),
    url(r'company/company-about-information-api/$', CompanyAboutInformationApi.as_view()),
    url(r'company/company-communication-information-api/$', CompanyCommunicationInformationApi.as_view()),
    url(r'company/company-job-post-api/$', JobPostApi.as_view()),
    url(r'company/job-applicant-api/$', JopApplicantsApi.as_view()),
    path('company/scholarship-company-api/', CompanyScholarshipApi.as_view()),

    # -----------------------------consultant api----------------------------------------
    url(r'consultant/appointment-api/$', AppointmentApi.as_view()),

    # ------------------------------student api-----------------------------
    path('student/student-education-api/', StudentEducationApi.as_view()),
    path('student/student-high-school-education-api/', StudentHighSchoolEducationApi.as_view()),

]
