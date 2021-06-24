import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Student, Company, Consultant, JobPost, Lecture, Appointment, Scholarship, LectureApplication
from career.models.JobApplication import JobApplication
from career.models.ScholarshipApplication import ScholarshipApplication


class AdminDashboardApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        api_data = dict()
        api_data['studentCount'] = Student.objects.filter(isDeleted=False, isGraduated=False).count()
        api_data['graduatedCount'] = Student.objects.filter(isDeleted=False, isGraduated=True).count()
        api_data['companyCount'] = Company.objects.filter(isDeleted=False).count()
        api_data['consultantCount'] = Consultant.objects.filter(isDeleted=False).count()
        api_data['jobPostCount'] = JobPost.objects.filter(isDeleted=False,
                                                          finishDate__lte=datetime.datetime.today().date()).count()
        api_data['lectureCount'] = Lecture.objects.filter(isDeleted=False).count()
        api_data['appointmentTotalCount'] = Appointment.objects.filter(isDeleted=False).count()
        api_data['appointmentDoneCount'] = Appointment.objects.filter(isDeleted=False, isCome=True).count()
        api_data['appointmentUnDoneCount'] = Appointment.objects.filter(isDeleted=False, isCome=False,
                                                                        date__lt=datetime.datetime.today().date()).count()

        return Response(api_data, status=status.HTTP_200_OK)


class ConsultantDashboardApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        api_data = dict()
        api_data['appointmentTotalCount'] = Appointment.objects.filter(consultant__profile__user=request.user,
                                                                       isDeleted=False).count()
        api_data['appointmentDoneCount'] = Appointment.objects.filter(consultant__profile__user=request.user,
                                                                      isDeleted=False, isCome=True).count()
        api_data['appointmentUnDoneCount'] = Appointment.objects.filter(consultant__profile__user=request.user,
                                                                        isDeleted=False, isCome=False,
                                                                        date__lt=datetime.datetime.today().date()).count()

        return Response(api_data, status=status.HTTP_200_OK)


class CompanyDashboardApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        api_data = dict()
        api_data['activeJobPostCount'] = JobPost.objects.filter(company__profile__user=request.user, isDeleted=False,).count()
        api_data['totalJobApplicantCount'] = JobApplication.objects.filter(jobPost__company__profile__user=request.user,
                                                                           isDeleted=False).count()

        api_data['totalScholarshipCount'] = Scholarship.objects.filter(company__profile__user=request.user,
                                                                       isDeleted=False).count()

        return Response(api_data, status=status.HTTP_200_OK)


class StudentDashboardApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        api_data = dict()
        api_data['totalLectureApplicationsCount'] = LectureApplication.objects.filter(
            student__profile__user=request.user, isDeleted=False).count()
        api_data['totalJobApplicationsCount'] = JobApplication.objects.filter(student__profile__user=request.user,
                                                                              isDeleted=False).count()

        api_data['totalScholarshipCount'] = ScholarshipApplication.objects.filter(student__profile__user=request.user,
                                                                                  isDeleted=False).count()

        return Response(api_data, status=status.HTTP_200_OK)
