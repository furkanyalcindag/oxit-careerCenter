import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Student, Company, Consultant, JobPost, Lecture, Appointment


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
