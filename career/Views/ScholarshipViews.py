import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.exceptions import ScholarshipCompanyDeleteException
from career.models import Scholarship, Student
from career.models.APIObject import APIObject
from career.models.ScholarshipApplication import ScholarshipApplication
from career.serializers.ScholarshipSerializer import ScholarshipSerializer, ScholarshipPageableSerializer, \
    CompanyScholarshipSerializer


class ScholarshipApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'), isDeleted=False)

            api_data = dict()
            api_data['name'] = scholarship.name
            api_data['description'] = scholarship.description
            api_data['uuid'] = scholarship.uuid
            api_data['amount'] = scholarship.amount
            api_data['isApprove'] = scholarship.isApprove

            select_company = dict()
            select_company[
                'label'] = scholarship.company.name
            select_company['value'] = scholarship.company.uuid

            api_data['company'] = select_company

            serializer = ScholarshipSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            active_page = 1
            count = 10

            name = ''
            if request.GET.get('name') is not None:
                name = request.GET.get('name')

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Scholarship.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Scholarship.objects.filter(name__icontains=name, isDeleted=False).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['name'] = x.name
                api_data['description'] = x.description
                api_data['uuid'] = x.uuid
                api_data['amount'] = x.amount
                api_data['isApprove'] = x.isApprove
                select_company = dict()
                select_company[
                    'label'] = x.company.name
                select_company['value'] = x.company.uuid

                api_data['company'] = select_company
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Scholarship.objects.filter(isDeleted=False).count()
            api_object.activePage = active_page

            serializer = ScholarshipPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ScholarshipSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "scholar is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:
            instance = Scholarship.objects.get(uuid=request.GET.get('id'))
            serializer = ScholarshipSerializer(data=request.data, instance=instance,
                                               context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "scholarship is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'))
            scholarship.isDeleted = True
            scholarship.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyScholarshipApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'), company__profile__user=request.user,
                                                  isDeleted=False)

            api_data = dict()
            api_data['name'] = scholarship.name
            api_data['description'] = scholarship.description
            api_data['uuid'] = scholarship.uuid
            api_data['amount'] = scholarship.amount
            api_data['isApprove'] = scholarship.isApprove

            select_company = dict()
            select_company[
                'label'] = scholarship.company.name
            select_company['value'] = scholarship.company.uuid

            api_data['company'] = select_company

            serializer = ScholarshipSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            active_page = 1
            count = 10

            name = ''
            if request.GET.get('name') is not None:
                name = request.GET.get('name')

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Scholarship.objects.filter(name__icontains=name, company__profile__user=request.user,
                                              isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Scholarship.objects.filter(name__icontains=name, company__profile__user=request.user,
                                                        isDeleted=False).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['name'] = x.name
                api_data['description'] = x.description
                api_data['uuid'] = x.uuid
                api_data['amount'] = x.amount
                api_data['isApprove'] = x.isApprove
                select_company = dict()
                select_company[
                    'label'] = x.company.name
                select_company['value'] = x.company.uuid

                api_data['company'] = select_company
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Scholarship.objects.filter(isDeleted=False).count()
            api_object.activePage = active_page

            serializer = ScholarshipPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CompanyScholarshipSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "scholar is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:

            instance = Scholarship.objects.get(uuid=request.GET.get('id'), company__profile__user=request.user)
            serializer = CompanyScholarshipSerializer(data=request.data, instance=instance,
                                                      context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "scholarship is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:

            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'), company__profile__user=request.user)
            if scholarship.isApprove is False:
                scholarship.isDeleted = True
                scholarship.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise ScholarshipCompanyDeleteException

        except ScholarshipCompanyDeleteException as e:
            traceback.print_exc()
            return Response({"error": e.__str__()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ScholarshipStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'), isApprove=True, isDeleted=False)

            api_data = dict()
            api_data['name'] = scholarship.name
            api_data['description'] = scholarship.description
            api_data['uuid'] = scholarship.uuid
            api_data['amount'] = scholarship.amount
            api_data['isApprove'] = scholarship.isApprove

            if len(ScholarshipApplication.objects.filter(student__profile__user=request.user,
                                                         scholarShip=scholarship)) > 0:
                api_data['isApplied'] = True
            else:
                api_data['isApplied'] = False

            select_company = dict()
            select_company[
                'label'] = scholarship.company.name
            select_company['value'] = scholarship.company.uuid

            api_data['company'] = select_company
            api_data['companyLogo'] = scholarship.company.logo

            serializer = ScholarshipSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        else:
            active_page = 1
            count = 10

            name = ''
            if request.GET.get('name') is not None:
                name = request.GET.get('name')

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Scholarship.objects.filter(name__icontains=name, isApprove=True, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Scholarship.objects.filter(name__icontains=name, isApprove=True, isDeleted=False).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['uuid'] = x.uuid
                api_data['name'] = x.name
                api_data['description'] = x.description
                api_data['uuid'] = x.uuid
                api_data['amount'] = x.amount
                api_data['isApprove'] = x.isApprove
                select_company = dict()
                select_company[
                    'label'] = x.company.name
                select_company['value'] = x.company.uuid

                api_data['company'] = select_company
                api_data['companyLogo'] = x.company.logo

                if len(ScholarshipApplication.objects.filter(student__profile__user=request.user,
                                                             scholarShip=x)) > 0:
                    api_data['isApplied'] = True
                else:
                    api_data['isApplied'] = False

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Scholarship.objects.filter(isDeleted=False).count()
            api_object.activePage = active_page

            serializer = ScholarshipPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            scholarship_id = request.data['scholarshipId']
            student = Student.objects.get(profile__user=request.user)
            scholarship = Scholarship.objects.get(uuid=scholarship_id)
            applications = ScholarshipApplication.objects.filter(scholarShip=scholarship, student=student)
            if scholarship.isApprove and len(applications) == 0:
                scholarship_application = ScholarshipApplication()
                scholarship_application.student = student
                scholarship_application.scholarShip = scholarship
                scholarship_application.save()
                return Response("başarılı", status=status.HTTP_200_OK)
            else:
                return Response("Başvurulamaz", status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            traceback.print_exc()
            return Response("hatalı", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScholarshipApplicants(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        student = Student.objects.get(profile__user=request.user)

        active_page = 1
        count = 10

        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('count') is not None:
            count = int(request.GET.get('count'))

        lim_start = int(count) * (int(active_page) - 1)
        lim_end = lim_start + int(count)

        data = ScholarshipApplication.objects.filter(student=student).order_by('-id')[lim_start:lim_end]

        filtered_count = ScholarshipApplication.objects.filter(student=student).count()
        arr = []
        for x in data:
            api_data = dict()
            api_data['name'] = x.scholarShip.name
            api_data['description'] = x.scholarShip.description
            api_data['uuid'] = x.scholarShip.uuid
            api_data['amount'] = x.scholarShip.amount
            api_data['isApprove'] = x.scholarShip.isApprove
            select_company = dict()
            select_company[
                'label'] = x.scholarShip.company.name
            select_company['value'] = x.scholarShip.company.uuid

            api_data['company'] = select_company
            api_data['companyLogo'] = x.scholarShip.company.logo
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = ScholarshipApplication.objects.filter(student=student).count()
        api_object.activePage = active_page

        serializer = ScholarshipPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)
