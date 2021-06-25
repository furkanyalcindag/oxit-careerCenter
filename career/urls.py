from django.conf.urls import url
from django.urls import path

from career.Views.AppointmentViews import AppointmentApi, AppointmentAdminApi, AppointmentStudentApi
from career.Views.BlogViews import BlogApi, BlogStudentApi
from career.Views.CategoryViews import ConsultantCategoryView
from career.Views.CompanyViews import CompanyApi, CompanyGeneralInformationApi, CompanyAboutInformationApi, \
    CompanyCommunicationInformationApi, CompanySelectApi, CompanyGeneralInformationStudentApi, CompanyListApi, \
    CompanyLogoApi
from career.Views.ConsultantViews import ConsultantApi, ConsultantStudentApi
from career.Views.DashboardViews import AdminDashboardApi, ConsultantDashboardApi, CompanyDashboardApi, \
    StudentDashboardApi
from career.Views.GeneralViews import LanguageApi, LocationSelectApi, CityDistrictSelectApi, JobTypeSelectApi, \
    UniversitySelectApi, FacultySelectApi, EducationTypeSelectApi, DeleteLog, MaritalStatusSelectApi, \
    MilitaryStatusSelectApi, NationalitySelectApi, GenderSelectApi, ForeignLanguageLevelSelectApi, \
    ForeignLanguageSelectApi, DriverLicenseSelectApi, BlogTypeSelectApi, UnitSelectApi, MenuApi, GroupSelectApi, \
    ConsultantCategorySelectApi, SocialMediaSelectApi
from career.Views.InitViews import InitDataApi, LocationDataApi, CityDistrictDataApi, UniversityDataApi, \
    EducationTypeDataApi, MaritalStatusDataApi, MilitaryStatusDataApi, NationalityDataApi, LanguageLevelDesc, \
    BlogTypeApi
from career.Views.InstructorViews import InstructorApi, InstructorSelectApi
from career.Views.JobApplicationViews import JopApplicantsApi, JopStudentApplicationsApi, \
    JobPostApplicationStudentCoverLetterApi
from career.Views.JobPostViews import JobPostApi, JobPostStudentApi, JobPostAdminApi
from career.Views.LectureViews import LectureApi, LectureInfoApi, LectureStudentApi, LectureStudentApplicants
from career.Views.PublicViews import AnnouncementPublicApi, UnitPublicApi
from career.Views.ScholarshipViews import ScholarshipApi, CompanyScholarshipApi, ScholarshipStudentApi, \
    ScholarshipApplicants
from career.Views.StudentViews import StudentApi, StudentEducationApi, StudentHighSchoolEducationApi, \
    StudentProfileImageApi, StudentGeneralInformationApi, StudentMilitaryStatusApi, StudentCommunicationApi, \
    StudentCertificateApi, StudentJobInfoApi, StudentReferenceApi, \
    StudentForeignLanguageApi, StudentQualificationApi, StudentExamApi, StudentDriverLicenseApi, StudentCVExportPDFApi, \
    StudentSelectApi
from career.Views.UnitViews import UnitApi, UnitStaffApi
from career.Views.UserViews import UserAPI, GroupAPI

app_name = 'career'

urlpatterns = [
    url(r'initial-data-api/$', InitDataApi.as_view()),
    url(r'initial-location-data-api/$', LocationDataApi.as_view()),
    url(r'initial-city-data-api/$', CityDistrictDataApi.as_view()),
    url(r'initial-uni-data-api/$', UniversityDataApi.as_view()),
    url(r'initial-education-type-api/$', EducationTypeDataApi.as_view()),
    url(r'initial-marital-status-api/$', MaritalStatusDataApi.as_view()),
    url(r'initial-military-status-api/$', MilitaryStatusDataApi.as_view()),
    url(r'initial-nationality-data-api/$', NationalityDataApi.as_view()),
    url(r'initial-blog-type-data-api/$', BlogTypeApi.as_view()),
    url(r'initial-language-level-data-api/$', LanguageLevelDesc.as_view()),
    url(r'delete-logs-api/$', DeleteLog.as_view()),

    # general
    path('location-select-api/', LocationSelectApi.as_view(), name='location-select-api'),
    path('city-district-select-api/', CityDistrictSelectApi.as_view(), name='city-district-select-api'),
    path('job-type-select-api/', JobTypeSelectApi.as_view(), name='job-type-select-api'),
    path('company-select-api/', CompanySelectApi.as_view(), name='company-select-api'),
    path('university-select-api/', UniversitySelectApi.as_view(), name='university-select-api'),
    path('faculty-select-api/', FacultySelectApi.as_view(), name='faculty-select-api'),
    path('department-select-api/', FacultySelectApi.as_view(), name='department-select-api'),
    path('education-type-select-api/', EducationTypeSelectApi.as_view(), name='education-type-select-api'),
    path('marital-status-select-api/', MaritalStatusSelectApi.as_view(), name='marital-status-select-api'),
    path('military-status-select-api/', MilitaryStatusSelectApi.as_view(), name='military-status-select-api'),
    path('nationality-status-select-api/', NationalitySelectApi.as_view(), name='national-status-select-api'),
    path('gender-select-api/', GenderSelectApi.as_view(), name='gender-select-api'),
    path('group-select-api/', GroupSelectApi.as_view(), name='group-select-api'),
    path('foreign-language-level-select-api/', ForeignLanguageLevelSelectApi.as_view(),
         name='foreign-language-level-select-api'),
    path('foreign-language-select-api/', ForeignLanguageSelectApi.as_view(), name='foreign-language-select-api'),
    path('driver-license-select-api/', DriverLicenseSelectApi.as_view(), name='driver-licence-select-api'),
    path('blog-type-select-api/', BlogTypeSelectApi.as_view(), name='blog-type-select-api'),
    path('unit-select-api/', UnitSelectApi.as_view(), name='unit-select-api'),
    path('menu-create-api/', MenuApi.as_view(), name='menu-create-api'),
    path('student-select-api/', StudentSelectApi.as_view(), name='student-select-api'),
    path('instructor-select-api/', InstructorSelectApi.as_view(), name='instructor-select-api'),
    path('category-select-api/', ConsultantCategorySelectApi.as_view(), name='category-select-api'),
    path('social-media-select-api/', SocialMediaSelectApi.as_view(), name='social-media-select-api'),

    # -------------public api--------------------------------

    path('public/announcement-api/', AnnouncementPublicApi.as_view(), name='public-announcement-api'),
    path('public/unit-staff-api/', UnitPublicApi.as_view(), name="public-unit-staff-api"),

    # ----------------admin api---------------------------
    # student
    path('student-api/', StudentApi.as_view(), name='admin-student-api'),

    # dashboard
    path('admin-dashboard-api/', AdminDashboardApi.as_view(), name='admin-dashboard-api'),

    # company
    path('company-api/', CompanyApi.as_view(), name='admin-company-api'),
    path('company-job-post-api/', JobPostAdminApi.as_view(), name='admin-company-api'),
    path('company-general-information-api/', CompanyGeneralInformationStudentApi.as_view(),
         name='admin-company-general-information-api'),

    # consultant
    path('consultant-api/', ConsultantApi.as_view(), name='admin-consultant-api'),
    path('consultant-appointment-api/', AppointmentAdminApi.as_view(), name='admin-consultant-appointment-api'),
    path('consultant-category-api/', ConsultantCategoryView.as_view(), name='admin-consultant-category-api'),

    # instructor
    path('instructor-api/', InstructorApi.as_view(), name='admin-instructor-api'),

    # unit
    path('unit-api/', UnitApi.as_view(), name='admin-unit-api'),
    path('unit-staff-api/', UnitStaffApi.as_view(), name='admin-unit-staff-api'),

    # language
    path('language-api/', LanguageApi.as_view(), name='admin-language-api'),

    # blog
    path('blog-api/', BlogApi.as_view(), name='admin-blog-api'),

    # lecture
    path('lecture-api/', LectureApi.as_view(), name='admin-lecture-api'),
    path('lecture-info-api/', LectureInfoApi.as_view(), name='admin-lecture-info-api'),

    # scholarship
    path('scholarship-api/', ScholarshipApi.as_view(), name='admin-scholarship-api'),

    # user
    path('user-api/', UserAPI.as_view(), name='admin-user-api'),
    path('group-api/', GroupAPI.as_view(), name='admin-group-api'),

    # --------------------------------company api-------------------------------------------------------
    path('company/company-general-information-api/', CompanyGeneralInformationApi.as_view(),
         name='company-general-information-api'),
    path('company/company-about-information-api/', CompanyAboutInformationApi.as_view(),
         name='company-about-information-lecture-api'),
    path('company/company-logo-api/', CompanyLogoApi.as_view(),
         name='company-logo-api'),
    path('company/company-communication-information-api/', CompanyCommunicationInformationApi.as_view(),
         name='company-communication-information-api'),
    path('company/company-job-post-api/', JobPostApi.as_view(), name='company-job-post-api'),
    path('company/job-applicant-api/', JopApplicantsApi.as_view(), name='company-job-applicants-api'),
    path('company/scholarship-company-api/', CompanyScholarshipApi.as_view(), name='company-scholarship-api'),

    # -----------------------------dashboard api------------------------------------------------------
    path('company-dashboard-api/', CompanyDashboardApi.as_view(), name='company-dashboard-api'),

    # -----------------------------consultant api----------------------------------------
    path('consultant/appointment-api/', AppointmentApi.as_view(), name='consultant-appointment-api'),

    # -----------------------------dashboard api------------------------------------------------------
    path('consultant-dashboard-api/', ConsultantDashboardApi.as_view(), name='consultant-dashboard-api'),

    # ------------------------------student api-----------------------------
    path('student/student-education-api/', StudentEducationApi.as_view(), name='student-education-api'),
    path('student/student-high-school-education-api/', StudentHighSchoolEducationApi.as_view(),
         name='student-high-school-education-api'),
    path('student/student-profile-image-api/', StudentProfileImageApi.as_view(), name='student-profile-image-api'),
    path('student/student-general-information-api/', StudentGeneralInformationApi.as_view(),
         name='student-general-information-api'),
    path('student/student-military-status-api/', StudentMilitaryStatusApi.as_view(),
         name='student-military-status-api'),
    path('student/student-communication-api/', StudentCommunicationApi.as_view(), name='student-communication-api'),
    path('student/student-certificate-api/', StudentCertificateApi.as_view(), name='student-certificate-api'),
    path('student/student-job-info-api/', StudentJobInfoApi.as_view(), name='student-job-info-api'),
    path('student/student-reference-api/', StudentReferenceApi.as_view(), name='student-reference-api'),
    path('student/student-foreign-language-api/', StudentForeignLanguageApi.as_view(),
         name='student-foreign-language-api'),
    path('student/student-qualification-api/', StudentQualificationApi.as_view(), name='student-qualification-api'),
    path('student/student-exam-api/', StudentExamApi.as_view(), name='student-exam-api'),
    path('student/student-license-driver-api/', StudentDriverLicenseApi.as_view(), name='student-driver-license-api'),
    path('student/student-job-post-api/', JobPostStudentApi.as_view(), name='student-job-post-api'),
    path('student/student-job-application-api/', JopStudentApplicationsApi.as_view(),
         name='student-job-application-api'),
    path('student/student-job-application-cover-letter-api/', JobPostApplicationStudentCoverLetterApi.as_view(),
         name='student-job-application-cover-letter-api'),
    path('student/student-blog-api/', BlogStudentApi.as_view(), name='student-blog-api'),
    path('student/student-export-cv-api/', StudentCVExportPDFApi.as_view(), name='student-export-cv-api'),
    path('student/student-consultant-api/', ConsultantStudentApi.as_view(), name='student-consultant-api'),
    path('student/student-appointment-api/', AppointmentStudentApi.as_view(), name='student-appointment-api'),
    path('student/student-lecture-api/', LectureStudentApi.as_view(), name='student-lecture-api'),
    path('student/student-scholarship-api/', ScholarshipStudentApi.as_view(), name='student-scholar-api'),
    path('student/student-lecture-application-api/', LectureStudentApplicants.as_view(),
         name='student-lecture-application-api'),
    path('student/student-scholarship-application-api/', ScholarshipApplicants.as_view(),
         name='student-scholarship-application-api'),
    path('student/student-company-general-information-api/', CompanyGeneralInformationStudentApi.as_view(),
         name='student-company-general-information-api'),
    path('student/student-company-list-api/', CompanyListApi.as_view(),
         name='student-company-list-information-api'),
    path('student/student-dashboard-api/', StudentDashboardApi.as_view(),
         name='student-dashboard-api'),

    path('student/student-job-post-by-company-api/', JobPostStudentApi.as_view(),
         name='student-job-post-by-company-api'),

]
