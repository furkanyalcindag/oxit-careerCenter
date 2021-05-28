import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Student, StudentEducationInfo, MaritalStatusDescription, MilitaryStatusDescription, \
    Certificate
from career.models.APIObject import APIObject
from career.models.GenderDescription import GenderDescription
from career.serializers.StudentSerializer import StudentSerializer, StudentPageableSerializer, \
    StudentUniversityEducationInformationSerializer, StudentHighSchoolEducationInformationSerializer, \
    StudentProfileImageSerializer, StudentGeneralInformationSerializer, StudentMilitaryStatusSerializer, \
    StudentCommunicationSerializer, StudentCertificateSerializer


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
        try:
            if request.GET.get('id') is not None:
                education_info = StudentEducationInfo.objects.get(uuid=request.GET.get('id'),
                                                                  student__profile__user=request.user, isDeleted=False)
                api_data = dict()
                api_data['isGraduated'] = education_info.isGraduated
                api_data['gpa'] = education_info.gpa
                api_data['startDate'] = education_info.startDate
                api_data['graduationDate'] = education_info.graduationDate
                api_data['uuid'] = education_info.uuid

                select_university = dict()
                if education_info.university is not None:

                    select_university['label'] = education_info.university.name
                    select_university['value'] = education_info.university.id
                else:
                    select_university['label'] = ''
                    select_university['value'] = ''

                select_faculty = dict()

                if education_info.faculty is not None:

                    select_faculty['label'] = education_info.faculty.name
                    select_faculty['value'] = education_info.faculty.id
                else:
                    select_faculty['label'] = ''
                    select_faculty['value'] = ''

                select_department = dict()
                if education_info.department is not None:
                    select_department['label'] = education_info.department.name
                    select_department['value'] = education_info.department.id
                else:
                    select_department['label'] = ''
                    select_department['value'] = ''

                select_education_type = dict()
                if education_info.educationType is not None:
                    select_education_type['label'] = education_info.educationType.name
                    select_education_type['value'] = education_info.educationType.id
                else:
                    select_education_type['label'] = ''
                    select_education_type['value'] = ''

                api_data['university'] = select_university
                api_data['faculty'] = select_faculty
                api_data['department'] = select_department
                api_data['educationType'] = select_education_type
                api_data['isQuaternarySystem'] = education_info.isQuaternarySystem

                serializer = StudentUniversityEducationInformationSerializer(api_data, context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                education_infos = StudentEducationInfo.objects.filter(student__profile__user=request.user,
                                                                      isDeleted=False)
                arr = []
                for education_info in education_infos:
                    api_data = dict()
                    api_data['isGraduated'] = education_info.isGraduated
                    api_data['gpa'] = education_info.gpa
                    api_data['startDate'] = education_info.startDate
                    api_data['graduationDate'] = education_info.graduationDate
                    api_data['uuid'] = education_info.uuid

                    select_university = dict()
                    if education_info.university is not None:

                        select_university['label'] = education_info.university.name
                        select_university['value'] = education_info.university.id
                    else:
                        select_university['label'] = ''
                        select_university['value'] = ''

                    select_faculty = dict()

                    if education_info.faculty is not None:

                        select_faculty['label'] = education_info.faculty.name
                        select_faculty['value'] = education_info.faculty.id
                    else:
                        select_faculty['label'] = ''
                        select_faculty['value'] = ''

                    select_department = dict()
                    if education_info.department is not None:
                        select_department['label'] = education_info.department.name
                        select_department['value'] = education_info.department.id
                    else:
                        select_department['label'] = ''
                        select_department['value'] = ''

                    select_education_type = dict()
                    if education_info.educationType is not None:
                        select_education_type['label'] = education_info.educationType.name
                        select_education_type['value'] = education_info.educationType.id
                    else:
                        select_education_type['label'] = ''
                        select_education_type['value'] = ''

                    api_data['university'] = select_university
                    api_data['faculty'] = select_faculty
                    api_data['department'] = select_department
                    api_data['educationType'] = select_education_type
                    api_data['isQuaternarySystem'] = education_info.isQuaternarySystem
                    arr.append(api_data)

                serializer = StudentUniversityEducationInformationSerializer(arr, many=True,
                                                                             context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    def put(self, request, format=None):
        try:
            instance = StudentEducationInfo.objects.get(uuid=request.GET.get('id'), student__profile__user=request.user)
            serializer = StudentUniversityEducationInformationSerializer(data=request.data, instance=instance,
                                                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "education info is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            student_education_info = StudentEducationInfo.objects.get(uuid=request.GET.get('id'),
                                                                      student__profile__user=request.user)
            student_education_info.isDeleted = True
            student_education_info.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentHighSchoolEducationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            education_info = StudentEducationInfo.objects.get(uuid=request.GET.get('id'),
                                                              student__profile__user=request.user, isDeleted=False)
            api_data = dict()
            api_data['isGraduated'] = education_info.isGraduated
            api_data['gpa'] = education_info.gpa
            api_data['startDate'] = education_info.startDate
            api_data['graduationDate'] = education_info.graduationDate
            api_data['uuid'] = education_info.uuid

            select_education_type = dict()
            select_education_type['label'] = education_info.educationType.name
            select_education_type['value'] = education_info.educationType.id

            api_data['highSchool'] = education_info.highSchool
            api_data['educationType'] = select_education_type
            api_data['isQuaternarySystem'] = education_info.isQuaternarySystem

            serializer = StudentHighSchoolEducationInformationSerializer(api_data, context={"request": request})
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            education_infos = StudentEducationInfo.objects.filter(student__profile__user=request.user, isDeleted=False)
            arr = []
            for education_info in education_infos:
                api_data = dict()
                api_data['isGraduated'] = education_info.isGraduated
                api_data['gpa'] = education_info.gpa
                api_data['startDate'] = education_info.startDate
                api_data['graduationDate'] = education_info.graduationDate
                api_data['uuid'] = education_info.uuid

                select_education_type = dict()
                select_education_type['label'] = education_info.educationType.name
                select_education_type['value'] = education_info.educationType.id

                api_data['highSchool'] = education_info.highSchool
                api_data['educationType'] = select_education_type
                api_data['isQuaternarySystem'] = education_info.isQuaternarySystem
                arr.append(api_data)

            serializer = StudentHighSchoolEducationInformationSerializer(arr, many=True, context={"request": request})
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = StudentHighSchoolEducationInformationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student education info is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = StudentEducationInfo.objects.get(uuid=request.GET.get('id'), student__profile__user=request.user)
            serializer = StudentHighSchoolEducationInformationSerializer(data=request.data, instance=instance,
                                                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "education info is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            student_education_info = StudentEducationInfo.objects.get(uuid=request.GET.get('id'),
                                                                      student__profile__user=request.user)
            student_education_info.isDeleted = True
            student_education_info.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentProfileImageApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            student = Student.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['profileImage'] = student.profile.profileImage

            serializer = StudentProfileImageSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Student.objects.get(profile__user=request.user)
            serializer = StudentProfileImageSerializer(data=request.data, instance=instance,
                                                       context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "profile image is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentGeneralInformationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            student = Student.objects.get(profile__user=request.user)
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            api_data = dict()
            api_data['firstName'] = student.profile.user.first_name
            api_data['lastName'] = student.profile.user.last_name
            api_data['birthDate'] = student.profile.birthDate
            api_data['email'] = student.profile.user.email
            api_data['studentNumber'] = student.studentNumber

            nationality_data = dict()
            if student.profile.nationality is not None:
                nationality_data['label'] = student.profile.nationality.name
                nationality_data['value'] = student.profile.nationality.id
            else:
                nationality_data['label'] = ''
                nationality_data['value'] = ''

            api_data['nationality'] = nationality_data

            gender_data = dict()
            if student.profile.gender is not None:
                gender_data['label'] = GenderDescription.objects.get(gender=student.profile.gender,
                                                                     language__code=lang_code).name
                gender_data['value'] = student.profile.gender.uuid
            else:
                gender_data['label'] = ''
                gender_data['value'] = ''

            api_data['gender'] = gender_data

            marital_data = dict()
            if student.profile.maritalStatus is not None:
                marital_data['label'] = MaritalStatusDescription.objects.get(
                    maritalStatus=student.profile.maritalStatus,
                    language__code=lang_code).name
                marital_data['value'] = student.profile.maritalStatus.uuid
            else:
                marital_data['label'] = ''
                marital_data['value'] = ''

            api_data['maritalStatus'] = marital_data

            serializer = StudentGeneralInformationSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Student.objects.get(profile__user=request.user)
            serializer = StudentGeneralInformationSerializer(data=request.data, instance=instance,
                                                             context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "student information is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentMilitaryStatusApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            student = Student.objects.get(profile__user=request.user)
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')

            api_data = dict()

            military_status_select = dict()
            if student.profile.militaryStatus is not None:
                military_status_select['label'] = MilitaryStatusDescription.objects.get(
                    militaryStatus=student.profile.militaryStatus, language__code=lang_code).name
                military_status_select['value'] = student.profile.militaryStatus.uuid
            else:
                military_status_select['label'] = ''
                military_status_select['value'] = ''

            api_data['militaryStatus'] = military_status_select
            api_data['delayedDate'] = student.profile.militaryDelayedDate

            serializer = StudentMilitaryStatusSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Student.objects.get(profile__user=request.user)
            serializer = StudentMilitaryStatusSerializer(data=request.data, instance=instance,
                                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "military status image is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentCommunicationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            student = Student.objects.get(profile__user=request.user)

            api_data = dict()

            api_data['mobilePhone'] = student.profile.mobilePhone
            api_data['address'] = student.profile.address

            serializer = StudentCommunicationSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Student.objects.get(profile__user=request.user)
            serializer = StudentCommunicationSerializer(data=request.data, instance=instance,
                                                        context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "communication is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentCertificateApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                certificate = Certificate.objects.get(uuid=request.GET.get('id'),
                                                      student__profile__user=request.user, isDeleted=False)
                api_data = dict()
                api_data['name'] = certificate.name
                api_data['institutionName'] = certificate.institutionName
                api_data['year'] = certificate.year
                api_data['certificateNo'] = certificate.certificateNo
                api_data['uuid'] = certificate.uuid
                api_data['description'] = certificate.description

                serializer = StudentCertificateSerializer(api_data, context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                certificates = Certificate.objects.filter(student__profile__user=request.user,
                                                          isDeleted=False)
                arr = []
                for certificate in certificates:
                    api_data = dict()
                    api_data['name'] = certificate.name
                    api_data['institutionName'] = certificate.institutionName
                    api_data['year'] = certificate.year
                    api_data['certificateNo'] = certificate.certificateNo
                    api_data['uuid'] = certificate.uuid
                    api_data['description'] = certificate.description
                    arr.append(api_data)

                serializer = StudentCertificateSerializer(arr, many=True,
                                                          context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Certificate.objects.get(student__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = StudentCertificateSerializer(data=request.data, instance=instance,
                                                      context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "communication is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentCertificateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student certificate is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            cert = Certificate.objects.get(uuid=request.GET.get('id'),
                                           student__profile__user=request.user)
            cert.isDeleted = True
            cert.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
