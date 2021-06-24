import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Company
from career.models.APIObject import APIObject
from career.models.SelectObject import SelectObject
from career.serializers.CompanySerializer import CompanyPageableSerializer, CompanySerializer, \
    CompanyGeneralInformationSerializer, CompanyAboutInformationSerializer, CompanyCommunicationInformationSerializer, \
    CompanyListPageableSerializer, CompanyLogoSerializer
from career.serializers.GeneralSerializers import SelectSerializer


class CompanyApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        company_name = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('companyName') is not None:
            company_name = request.GET.get('companyName')

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Company.objects.filter(name__icontains=company_name).order_by('-id')[lim_start:lim_end]

        filtered_count = Company.objects.filter(name__icontains=company_name).order_by('-id').count()
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['companyName'] = x.name
            api_data['email'] = x.profile.user.username
            api_data['isInstitution'] = x.isInstitution
            api_data['isActive'] = x.profile.user.is_active
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = Company.objects.count()
        api_object.activePage = 1

        serializer = CompanyPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "company is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            company = Company.objects.get(uuid=request.GET.get('id'))
            profile = company.profile
            user = profile.user
            if request.GET.get('makeActive') == 'true':
                company.isDeleted = False
                user.is_active = True
                profile.isDeleted = False
                company.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)
            elif request.GET.get('makeActive') == 'false':
                company.isDeleted = True
                user.is_active = False
                profile.isDeleted = True
                company.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyGeneralInformationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            company = Company.objects.get(profile__user=user)
            api_object = dict()
            api_object['logo'] = company.logo
            '''select_city = dict()
            if company.city is not None:
                select_city['label'] = company.city.name
                select_city['value'] = company.city.id
            else:
                select_city = None
            api_object['city'] = select_city
            select_district = dict()
            if company.district is not None:
                select_district['label'] = company.district.name
                select_district['value'] = company.district.id
            else:
                select_district = None
            api_object['district'] = select_district
            api_object['address'] = company.address'''
            api_object['staffCount'] = company.staffCount
            api_object['website'] = company.website
            api_object['name'] = company.name
            api_object['year'] = company.year
            # api_object['locationMap'] = company.locationMap
            # api_object['phone'] = company.phone
            # api_object['fax'] = company.fax
            serializer = CompanyGeneralInformationSerializer(api_object, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):

        try:

            instance = Company.objects.get(profile__user=request.user)
            serializer = CompanyGeneralInformationSerializer(data=request.data, instance=instance,
                                                             context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "blog is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyAboutInformationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            company = Company.objects.get(profile__user=user)
            api_object = dict()
            api_object['about'] = company.about

            serializer = CompanyAboutInformationSerializer(api_object, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            instance = Company.objects.get(profile__user=request.user)
            serializer = CompanyAboutInformationSerializer(data=request.data, instance=instance,
                                                           context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "about is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyCommunicationInformationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = request.user
            company = Company.objects.get(profile__user=user)
            api_object = dict()
            api_object['address'] = company.address
            api_object['phone'] = company.phone
            api_object['fax'] = company.fax
            api_object['email'] = company.email

            select_city = dict()

            if company.city is not None:
                select_city['label'] = company.city.name
                select_city['value'] = company.city.id
            else:
                select_city = None

            select_district = dict()
            if company.district is not None:
                select_district['label'] = company.district.name
                select_district['value'] = company.district.id
            else:
                select_district = None

            api_object['city'] = select_city
            api_object['district'] = select_district

            serializer = CompanyCommunicationInformationSerializer(api_object, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:

            instance = Company.objects.get(profile__user=request.user)
            serializer = CompanyCommunicationInformationSerializer(data=request.data, instance=instance,
                                                                   context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "comm is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanySelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        company_name = ''

        if request.GET.get('companyName') is not None:
            company_name = str(request.GET.get('companyName'))

        data = Company.objects.filter(name__icontains=company_name, isDeleted=False).order_by('-id')[:20]
        select_arr = []
        for company in data:
            select_object = SelectObject()
            select_object.value = company.uuid
            select_object.label = company.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class CompanyGeneralInformationStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            company = Company.objects.get(uuid=request.GET.get('id'))
            api_object = dict()
            api_object['logo'] = company.logo
            select_city = dict()
            if company.city is not None:
                select_city['label'] = company.city.name
                select_city['value'] = company.city.id
            else:
                select_city = None
            api_object['city'] = select_city
            select_district = dict()
            if company.district is not None:
                select_district['label'] = company.district.name
                select_district['value'] = company.district.id
            else:
                select_district = None
            api_object['district'] = select_district
            api_object['address'] = company.address
            api_object['staffCount'] = company.staffCount
            api_object['website'] = company.website
            api_object['name'] = company.name
            api_object['year'] = company.year
            # api_object['locationMap'] = company.locationMap
            api_object['phone'] = company.phone
            api_object['about'] = company.about
            # api_object['fax'] = company.fax
            serializer = CompanyGeneralInformationSerializer(api_object, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyListApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        company_name = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('companyName') is not None:
            company_name = request.GET.get('companyName')

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Company.objects.filter(name__icontains=company_name).order_by('-id')[lim_start:lim_end]

        filtered_count = Company.objects.filter(name__icontains=company_name).order_by('-id').count()
        arr = []
        for x in data:
            api_data = dict()

            api_data['uuid'] = x.uuid
            api_data['name'] = x.name
            api_data['logo'] = x.logo

            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = Company.objects.count()
        api_object.activePage = 1

        serializer = CompanyListPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class CompanyLogoApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            company = Company.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['logo'] = company.logo

            serializer = CompanyLogoSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Company.objects.get(profile__user=request.user)
            serializer = CompanyLogoSerializer(data=request.data, instance=instance,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "logo is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
