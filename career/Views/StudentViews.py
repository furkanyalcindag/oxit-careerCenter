import traceback

from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Student, MaritalStatusDescription, MilitaryStatusDescription, \
    Certificate, JobInfo, StudentForeignLanguage, ForeignLanguageLevelDescription, StudentQualification
from career.models.APIObject import APIObject
from career.models.ForeignLanguageDescription import ForeignLanguageDescription
from career.models.GenderDescription import GenderDescription
from career.models.Reference import Reference
from career.models.SelectObject import SelectObject
from career.models.StudentDriverLicense import StudentDriverLicense
from career.models.StudentEducationInfo import StudentEducationInfo
from career.models.StudentExam import StudentExam
from career.serializers.GeneralSerializers import SelectSerializer
from career.serializers.StudentSerializer import StudentSerializer, StudentPageableSerializer, \
    StudentUniversityEducationInformationSerializer, StudentHighSchoolEducationInformationSerializer, \
    StudentProfileImageSerializer, StudentGeneralInformationSerializer, StudentMilitaryStatusSerializer, \
    StudentCommunicationSerializer, StudentCertificateSerializer, StudentJobInformationSerializer, \
    StudentReferenceSerializer, StudentForeignLanguageSerializer, StudentQualificationSerializer, StudentExamSerializer, \
    StudentDriverLicenseSerializer
from career.services.GeneralService import render_to_pdf


class StudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        student_number = ''
        is_graduated = False

        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('type') is not None and request.GET.get('type') == 'graduated':
            is_graduated = True

        if request.GET.get('studentNumber') is not None:
            student_number = request.GET.get('studentNumber')

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Student.objects.filter(studentNumber__icontains=student_number, isGraduated=is_graduated).order_by(
            '-id')[lim_start:lim_end]
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['studentNumber'] = x.studentNumber
            api_data['email'] = x.profile.user.username
            api_data['isActive'] = x.profile.user.is_active
            api_data['isGraduated'] = x.isGraduated
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = Student.objects.filter(studentNumber__icontains=student_number,
                                                         isGraduated=is_graduated).count()
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
                education_infos = StudentEducationInfo.objects.exclude(educationType__name='Lise').filter(
                    student__profile__user=request.user,
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
                                                              student__profile__user=request.user,
                                                              educationType__name='Lise', isDeleted=False)
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
            education_infos = StudentEducationInfo.objects.filter(student__profile__user=request.user, isDeleted=False,
                                                                  educationType__name='Lise')
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


class StudentJobInfoApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                job_info = JobInfo.objects.get(uuid=request.GET.get('id'),
                                               student__profile__user=request.user, isDeleted=False)
                api_data = dict()
                api_data['uuid'] = job_info.uuid
                api_data['title'] = job_info.title
                api_data['company'] = job_info.company
                api_data['startDate'] = job_info.startDate
                api_data['isContinue'] = job_info.isContinue
                api_data['finishDate'] = job_info.finishDate
                api_data['description'] = job_info.description

                job_type_select = dict()
                if job_info.jobType is not None:
                    job_type_select['label'] = job_info.jobType.name
                    job_type_select['value'] = job_info.jobType.id
                else:
                    job_type_select['label'] = ''
                    job_type_select['value'] = ''

                api_data['jobType'] = job_type_select

                serializer = StudentJobInformationSerializer(api_data, context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                job_infos = JobInfo.objects.filter(student__profile__user=request.user,
                                                   isDeleted=False)
                arr = []
                for job_info in job_infos:
                    api_data = dict()
                    api_data['uuid'] = job_info.uuid
                    api_data['title'] = job_info.title
                    api_data['company'] = job_info.company
                    api_data['startDate'] = job_info.startDate
                    api_data['isContinue'] = job_info.isContinue
                    api_data['finishDate'] = job_info.finishDate
                    api_data['description'] = job_info.description

                    job_type_select = dict()
                    if job_info.jobType is not None:
                        job_type_select['label'] = job_info.jobType.name
                        job_type_select['value'] = job_info.jobType.id
                    else:
                        job_type_select['label'] = ''
                        job_type_select['value'] = ''

                    api_data['jobType'] = job_type_select

                    arr.append(api_data)

                serializer = StudentJobInformationSerializer(arr, many=True,
                                                             context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = JobInfo.objects.get(student__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = StudentJobInformationSerializer(data=request.data, instance=instance,
                                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "job info is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentJobInformationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "job info is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            job_info = JobInfo.objects.get(uuid=request.GET.get('id'),
                                           student__profile__user=request.user)
            job_info.isDeleted = True
            job_info.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentReferenceApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                reference = Reference.objects.get(uuid=request.GET.get('id'),
                                                  student__profile__user=request.user, isDeleted=False)
                api_data = dict()
                api_data['uuid'] = reference.uuid
                api_data['firstName'] = reference.firstName
                api_data['lastName'] = reference.lastName
                api_data['title'] = reference.title
                api_data['telephoneNumber'] = reference.telephoneNumber

                serializer = StudentReferenceSerializer(api_data, context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                references = Reference.objects.filter(student__profile__user=request.user,
                                                      isDeleted=False)
                arr = []
                for reference in references:
                    api_data = dict()
                    api_data['uuid'] = reference.uuid
                    api_data['firstName'] = reference.firstName
                    api_data['lastName'] = reference.lastName
                    api_data['title'] = reference.title
                    api_data['telephoneNumber'] = reference.telephoneNumber
                    arr.append(api_data)

                serializer = StudentReferenceSerializer(arr, many=True,
                                                        context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Reference.objects.get(student__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = StudentReferenceSerializer(data=request.data, instance=instance,
                                                    context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "reference is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentReferenceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student reference is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            reference = Reference.objects.get(uuid=request.GET.get('id'),
                                              student__profile__user=request.user)
            reference.isDeleted = True
            reference.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentForeignLanguageApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if request.GET.get('id') is not None:
                student_foreign_language = StudentForeignLanguage.objects.get(uuid=request.GET.get('id'),
                                                                              student__profile__user=request.user,
                                                                              isDeleted=False)
                api_data = dict()
                api_data['uuid'] = student_foreign_language.uuid

                foreign_language_select = dict()
                if student_foreign_language.foreignLanguage is not None:
                    foreign_language_select['label'] = ForeignLanguageDescription.objects.get(
                        foreignLanguage=student_foreign_language.foreignLanguage, language__code=lang_code).name
                    foreign_language_select['value'] = student_foreign_language.foreignLanguage.id
                else:
                    foreign_language_select['label'] = ''
                    foreign_language_select['value'] = ''

                api_data['foreignLanguage'] = foreign_language_select

                foreign_language_reading_level_select = dict()
                if student_foreign_language.readingLevel is not None:
                    foreign_language_reading_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                        foreignLanguageLevel=student_foreign_language.readingLevel, language__code=lang_code).name
                    foreign_language_reading_level_select['value'] = student_foreign_language.readingLevel.id
                else:
                    foreign_language_reading_level_select['label'] = ''
                    foreign_language_reading_level_select['value'] = ''

                api_data['readingLevel'] = foreign_language_reading_level_select

                foreign_language_writing_level_select = dict()
                if student_foreign_language.writingLevel is not None:
                    foreign_language_writing_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                        foreignLanguageLevel=student_foreign_language.writingLevel, language__code=lang_code).name
                    foreign_language_writing_level_select['value'] = student_foreign_language.writingLevel.id
                else:
                    foreign_language_writing_level_select['label'] = ''
                    foreign_language_writing_level_select['value'] = ''

                api_data['writingLevel'] = foreign_language_writing_level_select

                foreign_language_speaking_level_select = dict()
                if student_foreign_language.speakingLevel is not None:
                    foreign_language_speaking_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                        foreignLanguageLevel=student_foreign_language.speakingLevel, language__code=lang_code).name
                    foreign_language_speaking_level_select['value'] = student_foreign_language.speakingLevel.id
                else:
                    foreign_language_speaking_level_select['label'] = ''
                    foreign_language_speaking_level_select['value'] = ''

                api_data['speakingLevel'] = foreign_language_speaking_level_select

                foreign_language_listening_level_select = dict()
                if student_foreign_language.listeningLevel is not None:
                    foreign_language_listening_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                        foreignLanguageLevel=student_foreign_language.listeningLevel, language__code=lang_code).name
                    foreign_language_listening_level_select['value'] = student_foreign_language.listeningLevel.id
                else:
                    foreign_language_listening_level_select['label'] = ''
                    foreign_language_listening_level_select['value'] = ''

                api_data['listeningLevel'] = foreign_language_listening_level_select

                serializer = StudentForeignLanguageSerializer(api_data, context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                languages = StudentForeignLanguage.objects.filter(student__profile__user=request.user,
                                                                  isDeleted=False)
                arr = []
                for student_foreign_language in languages:
                    api_data = dict()
                    api_data['uuid'] = student_foreign_language.uuid

                    foreign_language_select = dict()
                    if student_foreign_language.foreignLanguage is not None:
                        foreign_language_select['label'] = ForeignLanguageDescription.objects.get(
                            foreignLanguage=student_foreign_language.foreignLanguage, language__code=lang_code).name
                        foreign_language_select['value'] = student_foreign_language.foreignLanguage.id
                    else:
                        foreign_language_select['label'] = ''
                        foreign_language_select['value'] = ''

                    api_data['foreignLanguage'] = foreign_language_select

                    foreign_language_reading_level_select = dict()
                    if student_foreign_language.readingLevel is not None:
                        foreign_language_reading_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                            foreignLanguageLevel=student_foreign_language.readingLevel, language__code=lang_code).name
                        foreign_language_reading_level_select['value'] = student_foreign_language.readingLevel.id
                    else:
                        foreign_language_reading_level_select['label'] = ''
                        foreign_language_reading_level_select['value'] = ''

                    api_data['readingLevel'] = foreign_language_reading_level_select

                    foreign_language_writing_level_select = dict()
                    if student_foreign_language.writingLevel is not None:
                        foreign_language_writing_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                            foreignLanguageLevel=student_foreign_language.writingLevel, language__code=lang_code).name
                        foreign_language_writing_level_select['value'] = student_foreign_language.writingLevel.id
                    else:
                        foreign_language_writing_level_select['label'] = ''
                        foreign_language_writing_level_select['value'] = ''

                    api_data['writingLevel'] = foreign_language_writing_level_select

                    foreign_language_speaking_level_select = dict()
                    if student_foreign_language.speakingLevel is not None:
                        foreign_language_speaking_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                            foreignLanguageLevel=student_foreign_language.speakingLevel, language__code=lang_code).name
                        foreign_language_speaking_level_select['value'] = student_foreign_language.speakingLevel.id
                    else:
                        foreign_language_speaking_level_select['label'] = ''
                        foreign_language_speaking_level_select['value'] = ''

                    api_data['speakingLevel'] = foreign_language_speaking_level_select

                    foreign_language_listening_level_select = dict()
                    if student_foreign_language.listeningLevel is not None:
                        foreign_language_listening_level_select['label'] = ForeignLanguageLevelDescription.objects.get(
                            foreignLanguageLevel=student_foreign_language.listeningLevel, language__code=lang_code).name
                        foreign_language_listening_level_select['value'] = student_foreign_language.listeningLevel.id
                    else:
                        foreign_language_listening_level_select['label'] = ''
                        foreign_language_listening_level_select['value'] = ''

                    api_data['listeningLevel'] = foreign_language_listening_level_select
                    arr.append(api_data)

                serializer = StudentForeignLanguageSerializer(arr, many=True,
                                                              context={"request": request})
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = StudentForeignLanguage.objects.get(student__profile__user=request.user,
                                                          uuid=request.GET.get('id'))
            serializer = StudentForeignLanguageSerializer(data=request.data, instance=instance,
                                                          context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "foreign language is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentForeignLanguageSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "foreign language is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            foreign_language = StudentForeignLanguage.objects.get(uuid=request.GET.get('id'),
                                                                  student__profile__user=request.user)
            foreign_language.isDeleted = True
            foreign_language.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentQualificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                qualification = StudentQualification.objects.get(student__profile__user=request.user,
                                                                 uuid=request.GET.get('id'))

                api_data = dict()

                api_data['uuid'] = qualification.uuid
                api_data['name'] = qualification.name
                api_data['rating'] = qualification.rating

                serializer = StudentQualificationSerializer(api_data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                qualifications = StudentQualification.objects.filter(student__profile__user=request.user,
                                                                     isDeleted=False)
                arr = []
                for q in qualifications:
                    api_data = dict()

                    api_data['uuid'] = q.uuid
                    api_data['name'] = q.name
                    api_data['rating'] = q.rating
                    arr.append(api_data)

                serializer = StudentQualificationSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = StudentQualification.objects.get(student__profile__user=request.user,
                                                        uuid=request.GET.get('id'))
            serializer = StudentQualificationSerializer(data=request.data, instance=instance,
                                                        context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "qualification is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentQualificationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "qualification is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            qualification = StudentQualification.objects.get(uuid=request.GET.get('id'),
                                                             student__profile__user=request.user)
            qualification.isDeleted = True
            qualification.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentExamApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                qualification = StudentExam.objects.get(student__profile__user=request.user,
                                                        uuid=request.GET.get('id'))

                api_data = dict()

                api_data['uuid'] = qualification.uuid
                api_data['name'] = qualification.name
                api_data['point'] = qualification.point
                api_data['year'] = qualification.year

                serializer = StudentExamSerializer(api_data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                qualifications = StudentExam.objects.filter(student__profile__user=request.user,
                                                            isDeleted=False)
                arr = []
                for q in qualifications:
                    api_data = dict()

                    api_data['uuid'] = q.uuid
                    api_data['name'] = q.name
                    api_data['point'] = q.point
                    api_data['year'] = q.year
                    arr.append(api_data)

                serializer = StudentExamSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = StudentExam.objects.get(student__profile__user=request.user,
                                               uuid=request.GET.get('id'))
            serializer = StudentExamSerializer(data=request.data, instance=instance,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "exam is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentExamSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "exam is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            exam = StudentExam.objects.get(uuid=request.GET.get('id'),
                                           student__profile__user=request.user)
            exam.isDeleted = True
            exam.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentDriverLicenseApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            if request.GET.get('id') is not None:
                driver_license = StudentDriverLicense.objects.get(student__profile__user=request.user,
                                                                  uuid=request.GET.get('id'))

                api_data = dict()

                api_data['uuid'] = driver_license.uuid

                api_licence_select = dict()
                api_licence_select['label'] = driver_license.driverLicense
                api_licence_select['value'] = driver_license.driverLicense

                api_data['driverLicense'] = api_licence_select

                serializer = StudentDriverLicenseSerializer(api_data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                licenses = StudentDriverLicense.objects.filter(student__profile__user=request.user,
                                                               isDeleted=False)
                arr = []
                for q in licenses:
                    api_data = dict()

                    api_data['uuid'] = q.uuid
                    api_licence_select = dict()
                    api_licence_select['label'] = q.driverLicense
                    api_licence_select['value'] = q.driverLicense

                    api_data['driverLicense'] = api_licence_select
                    arr.append(api_data)

                serializer = StudentDriverLicenseSerializer(arr, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = StudentDriverLicense.objects.get(student__profile__user=request.user,
                                                        uuid=request.GET.get('id'))
            serializer = StudentDriverLicenseSerializer(data=request.data, instance=instance,
                                                        context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "driver license is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = StudentDriverLicenseSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "driver license is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            license = StudentDriverLicense.objects.get(uuid=request.GET.get('id'),
                                                       student__profile__user=request.user)
            license.isDeleted = True
            license.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentCVExportPDFApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        api_dict = dict()
        '''student = Student.objects.get(profile__user=request.user)

       
        api_dict['email'] = student.profile.user.email
        api_dict['firstName'] = student.profile.user.first_name
        api_dict['lastName'] = student.profile.user.last_name
        api_dict['telephoneNumber'] = student.profile.mobilePhone
        api_dict['birthDate'] = student.profile.birthDate
        api_dict['address'] = student.profile.address
        api_dict['profileImage'] = student.profile.profileImage
        api_dict['gender'] = GenderDescription.objects.get(gender=student.profile.gender, language__code=lang_code).name
        api_dict['nationality'] = student.profile.nationality
        api_dict['militaryStatus'] = MilitaryStatusDescription.objects.get(
            militaryStatus=student.profile.militaryStatus, language__code=lang_code).name
        api_dict['maritalStatus'] = MaritalStatusDescription.objects.get(maritalStatus=student.profile.maritalStatus,
                                                                         language__code=lang_code).name
        api_dict['experiments'] = JobInfo.objects.filter(student=student)
        api_dict['educations'] = StudentEducationInfo.objects.filter(student=student)
        api_dict['foreignLanguages'] = StudentForeignLanguage.objects.filter(student=student)
        api_dict['exams'] = StudentExam.objects.filter(student=student)
        api_dict['qualifications'] = StudentQualification.objects.filter(student=student)
        api_dict['references'] = Reference.objects.filter(student=student)
        api_dict['certificate'] = Certificate.objects.filter(student=student)'''

        # Rendered
        # html_string = render_to_string('cv-print.html', {'data': api_dict})

        # html_string = html_string.encode('utf-8').strip()
        # html = HTML(string=html_string)
        # result = html.write_pdf('tmp/report.pdf')

        pdf = render_to_pdf('resume.html', api_dict)

        return FileResponse(pdf, status=status.HTTP_200_OK,
                            content_type='application/pdf')


class StudentSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        student_name = ''
        student_surname = ''

        if request.GET.get('studentName') is not None:
            x = str(request.GET.get('studentName')).split(' ')
            if len(x) > 1:
                student_name = x[0]
                student_surname = x[1]
            elif len(x) == 1:
                student_name = x[0]

        data = Student.objects.filter(profile__user__first_name__icontains=student_name,
                                      profile__user__last_name__icontains=student_surname, isDeleted=False).order_by(
            '-id')[:20]

        select_arr = []
        for student in data:
            select_object = SelectObject()
            select_object.value = student.uuid
            select_object.label = student.profile.user.first_name + ' ' + student.profile.user.last_name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)
