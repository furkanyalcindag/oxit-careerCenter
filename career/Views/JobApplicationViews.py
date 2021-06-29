import traceback

import pdfkit
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Company, Student, MilitaryStatusDescription, MaritalStatusDescription, JobInfo, \
    StudentEducationInfo, StudentForeignLanguage, ForeignLanguageLevelDescription, StudentExam, StudentQualification, \
    Certificate
from career.models.APIObject import APIObject
from career.models.ForeignLanguageDescription import ForeignLanguageDescription
from career.models.GenderDescription import GenderDescription
from career.models.JobApplication import JobApplication
from career.models.Reference import Reference
from career.serializers.JobApplicationSeralizers import StudentJobApplicationSerializer, \
    StudentJobApplicationPageableSerializer
from career.serializers.StudentSerializer import StudentPageableSerializer
from career.services.NotificationServices import create_notification


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


class JopStudentApplicationsApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        job_uuid = request.GET.get('id')

        student = Student.objects.get(profile__user=request.user)

        active_page = 1
        count = 10

        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('count') is not None:
            count = int(request.GET.get('count'))

        lim_start = int(count) * (int(active_page) - 1)
        lim_end = lim_start + int(count)

        data = JobApplication.objects.filter(student=student).order_by('-id')[lim_start:lim_end]

        filtered_count = JobApplication.objects.filter(student=student).count()
        arr = []

        for x in data:
            api_data = dict()
            api_data['jobPostId'] = x.jobPost.uuid
            api_data['title'] = x.jobPost.title
            api_data['companyName'] = x.jobPost.company.name
            api_data['companyLogo'] = x.jobPost.company.logo
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = JobApplication.objects.filter(student=student).count()
        api_object.activePage = active_page

        serializer = StudentJobApplicationPageableSerializer(
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


class JobPostApplicationStudentCoverLetterApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            if request.GET.get('jobPostId'):
                uuid = request.GET.get('jobPostId')
                cover_letter = JobApplication.objects.get(student__profile__user=request.user,
                                                          jobPost__uuid=uuid).coverLetter
                return Response({'coverLetter': cover_letter}, status=status.HTTP_200_OK)
            else:
                raise Exception
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyApplicantCVExportPDFApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            api_dict = dict()
            student = Student.objects.get(uuid=request.GET.get('id'))

            api_dict['email'] = student.profile.user.email
            api_dict['firstName'] = student.profile.user.first_name
            api_dict['lastName'] = student.profile.user.last_name
            api_dict['telephoneNumber'] = student.profile.mobilePhone
            api_dict['birthDate'] = student.profile.birthDate
            api_dict['address'] = student.profile.address
            api_dict['profileImage'] = student.profile.profileImage
            api_dict['gender'] = GenderDescription.objects.filter(gender=student.profile.gender,
                                                                  language__code=lang_code)
            api_dict['nationality'] = student.profile.nationality
            api_dict['militaryStatus'] = MilitaryStatusDescription.objects.filter(
                militaryStatus=student.profile.militaryStatus, language__code=lang_code)
            api_dict['maritalStatus'] = MaritalStatusDescription.objects.filter(
                maritalStatus=student.profile.maritalStatus,
                language__code=lang_code)
            api_dict['experiments'] = JobInfo.objects.filter(student=student)
            api_dict['educations'] = StudentEducationInfo.objects.filter(student=student,
                                                                         educationType__name__in=['Lisans',
                                                                                                  'Yüksek Lisans',
                                                                                                  'Doktora',
                                                                                                  'Ön Lisans'])
            api_dict['educationHighSchools'] = StudentEducationInfo.objects.filter(student=student,
                                                                                   educationType__name='Lise')

            fls = StudentForeignLanguage.objects.filter(student=student)

            arr = []
            for fl in fls:
                fl_data = dict()

                fl_data['language'] = ForeignLanguageDescription.objects.get(language__code=lang_code,
                                                                             foreignLanguage=fl.foreignLanguage).name
                fl_data['reading'] = ForeignLanguageLevelDescription.objects.get(language__code=lang_code,
                                                                                 foreignLanguageLevel=fl.readingLevel).name
                fl_data['writing'] = ForeignLanguageLevelDescription.objects.get(language__code=lang_code,
                                                                                 foreignLanguageLevel=fl.writingLevel).name
                fl_data['listening'] = ForeignLanguageLevelDescription.objects.get(language__code=lang_code,
                                                                                   foreignLanguageLevel=fl.listeningLevel).name
                fl_data['speaking'] = ForeignLanguageLevelDescription.objects.get(language__code=lang_code,
                                                                                  foreignLanguageLevel=fl.speakingLevel).name
                arr.append(fl_data)

            api_dict['foreignLanguages'] = arr
            api_dict['exams'] = StudentExam.objects.filter(student=student)
            api_dict['qualifications'] = StudentQualification.objects.filter(student=student)
            api_dict['references'] = Reference.objects.filter(student=student)
            api_dict['certificates'] = Certificate.objects.filter(student=student)
            api_dict['range'] = range(1, 6)

            # Rendered
            # html_string = render_to_string('cv-print.html', {'data': api_dict})

            # html_string = html_string.encode('utf-8').strip()
            # html = HTML(string=html_string)
            # result = html.write_pdf('tmp/report.pdf')

            # pdf = render_to_pdf('resume.html', api_dict)

            html = loader.render_to_string('resume.html', {'data': api_dict})
            options = {
                "enable-local-file-access": None
            }
            output = pdfkit.from_string(html, output_path=False, options=options)
            response = HttpResponse(content_type="application/pdf")
            response.write(output)

            create_notification(student.profile.user, 'student_company_view_student_cv')

            return response
        except:
            traceback.print_exc()
