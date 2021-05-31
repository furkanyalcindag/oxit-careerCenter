from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Company
from career.models.APIObject import APIObject
from career.models.JobApplication import JobApplication
from career.serializers.JobApplicationSeralizers import StudentJobApplicationSerializer
from career.serializers.StudentSerializer import StudentPageableSerializer


class JopApplicantsApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        job_uuid = request.GET.get('id')

        company = Company.objects.get(profile__user=request.user)

        active_page = 1
        student_name = ''
        student_surname = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('studentName') is not None:
            x = str(request.GET.get('studentName')).split(' ')
            if len(x) > 1:
                student_name = x[0]
                student_surname = [1]
            elif len(x) == 1:
                student_name = x[0]

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = JobApplication.objects.filter(jobPost__uuid=job_uuid, jobPost__company=company,
                                             student__profile__user__first_name__icontains=student_name,
                                             student__profile__user__last_name__icontains=student_surname).order_by(
            '-id')[
               lim_start:lim_end]

        filtered_count = JobApplication.objects.filter(jobPost__uuid=job_uuid, jobPost__company=company,
                                                       student__profile__user__first_name__icontains=student_name,
                                                       student__profile__user__last_name__icontains=student_surname).count()
        arr = []

        for x in data:
            api_data = dict()
            api_data['firstName'] = x.student.profile.user.first_name
            api_data['lastName'] = x.student.profile.user.last_name
            api_data['uuid'] = x.student.uuid
            api_data['studentNumber'] = x.student.studentNumber
            api_data['email'] = x.student.profile.user.username
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = JobApplication.objects.filter(jobPost__uuid=job_uuid,
                                                                jobPost__company=company).count()
        api_object.activePage = active_page

        serializer = StudentPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class JopStudentApplicantsApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        job_uuid = request.GET.get('id')

        company = Company.objects.get(profile__user=request.user)

        active_page = 1
        student_name = ''
        student_surname = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('studentName') is not None:
            x = str(request.GET.get('studentName')).split(' ')
            if len(x) > 1:
                student_name = x[0]
                student_surname = [1]
            elif len(x) == 1:
                student_name = x[0]

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = JobApplication.objects.filter(jobPost__uuid=job_uuid, jobPost__company=company,
                                             student__profile__user__first_name__icontains=student_name,
                                             student__profile__user__last_name__icontains=student_surname).order_by(
            '-id')[
               lim_start:lim_end]

        filtered_count = JobApplication.objects.filter(jobPost__uuid=job_uuid, jobPost__company=company,
                                                       student__profile__user__first_name__icontains=student_name,
                                                       student__profile__user__last_name__icontains=student_surname).count()
        arr = []

        for x in data:
            api_data = dict()
            api_data['firstName'] = x.student.profile.user.first_name
            api_data['lastName'] = x.student.profile.user.last_name
            api_data['uuid'] = x.student.uuid
            api_data['studentNumber'] = x.student.studentNumber
            api_data['email'] = x.student.profile.user.username
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = JobApplication.objects.filter(jobPost__uuid=job_uuid,
                                                                jobPost__company=company).count()
        api_object.activePage = active_page

        serializer = StudentPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = StudentJobApplicationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "job application is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
