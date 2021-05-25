import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Student, StudentEducationInfo
from career.models.APIObject import APIObject
from career.serializers.StudentSerializer import StudentSerializer, StudentPageableSerializer, \
    StudentUniversityEducationInformationSerializer


class StudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        student_number = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('studentNumber') is not None:
            student_number = request.GET.get('studentNumber')

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Student.objects.filter(studentNumber__icontains=student_number).order_by('-id')[lim_start:lim_end]
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['studentNumber'] = x.studentNumber
            api_data['email'] = x.profile.user.username
            api_data['isActive'] = x.profile.user.is_active
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = Student.objects.count()
        api_object.activePage = active_page

        serializer = StudentPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            student = Student.objects.get(uuid=request.GET.get('id'))
            profile = student.profile
            user = profile.user
            if request.GET.get('makeActive') == 'true':
                student.isDeleted = False
                user.is_active = True
                profile.isDeleted = False
                student.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)
            elif request.GET.get('makeActive') == 'false':
                student.isDeleted = True
                user.is_active = False
                profile.isDeleted = True
                student.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentEducationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            education_info = StudentEducationInfo.objects.get(uuid=request.GET.get('id'),
                                                              student__profile__user=request.user)
            api_data = dict()
            api_data['isGraduated'] = education_info.isGraduated
            api_data['gpa'] = education_info.gpa
            api_data['startDate'] = education_info.startDate
            api_data['graduationDate'] = education_info.graduationDate
            api_data['uuid'] = education_info.uuid

            select_university = dict()
            select_university['label'] = education_info.university.name
            select_university['value'] = education_info.university.id

            select_faculty = dict()
            select_faculty['label'] = education_info.faculty.name
            select_faculty['value'] = education_info.faculty.id

            select_department = dict()
            select_department['label'] = education_info.department.name
            select_department['value'] = education_info.department.id

            select_education_type = dict()
            select_education_type['label'] = education_info.educationType.name
            select_education_type['value'] = education_info.educationType.id

            api_data['university'] = select_university
            api_data['faculty'] = select_faculty
            api_data['department'] = select_department
            api_data['educationType'] = select_education_type
            api_data['isQuaternarySystem'] = education_info.isQuaternarySystem

            serializer = StudentUniversityEducationInformationSerializer(api_data, context={"request": request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            education_infos = StudentEducationInfo.objects.filter(student__profile__user=request.user)
            arr = []
            for education_info in education_infos:
                api_data = dict()
                api_data['isGraduated'] = education_info.isGraduated
                api_data['gpa'] = education_info.gpa
                api_data['startDate'] = education_info.startDate
                api_data['graduationDate'] = education_info.graduationDate
                api_data['uuid'] = education_info.uuid

                select_university = dict()
                select_university['label'] = education_info.university.name
                select_university['value'] = education_info.university.id

                select_faculty = dict()
                select_faculty['label'] = education_info.faculty.name
                select_faculty['value'] = education_info.faculty.id

                select_department = dict()
                select_department['label'] = education_info.department.name
                select_department['value'] = education_info.department.id

                select_education_type = dict()
                select_education_type['label'] = education_info.educationType.name
                select_education_type['value'] = education_info.educationType.id

                api_data['university'] = select_university
                api_data['faculty'] = select_faculty
                api_data['department'] = select_department
                api_data['educationType'] = select_education_type
                api_data['isQuaternarySystem'] = education_info.isQuaternarySystem
                arr.append(api_data)

            serializer = StudentUniversityEducationInformationSerializer(arr, many=True, context={"request": request})
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = StudentUniversityEducationInformationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student education info is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
