import traceback

from django.db.models import Q
from drf_api_logger.models import APILogsModel
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language, District, City, JobType, University, Faculty, EducationType, Department, \
    MaritalStatus, MilitaryStatusDescription, Nationality, Gender, ForeignLanguage, \
    ForeignLanguageLevel, ForeignLanguageLevelDescription, BlogType, Unit, MenuStudent, MenuCompany, MenuConsultant
from career.models.DriverLicenseEnum import DriverLicenseEnum
from career.models.ForeignLanguageDescription import ForeignLanguageDescription
from career.models.GenderDescription import GenderDescription
from career.models.Location import Location
from career.models.MaritalStatusDescription import MaritalStatusDescription
from career.models.Menu import Menu
from career.models.MilitaryStatus import MilitaryStatus
from career.models.SelectObject import SelectObject
from career.serializers.GeneralSerializers import LanguageSerializer, SelectSerializer, MenuSerializer


class LanguageApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        languages = Language.objects.all()

        serializer = LanguageSerializer(
            languages, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class LocationSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Location.objects.all()

        select_arr = []
        for location in data:
            select_object = SelectObject()
            select_object.value = location.uuid
            select_object.label = location.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class JobTypeSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = JobType.objects.all()

        select_arr = []
        for type in data:
            select_object = SelectObject()
            select_object.value = type.id
            select_object.label = type.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class CityDistrictSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            select_arr = []
            if request.GET.get('id') is not None:
                data = District.objects.filter(city=City.objects.get(id=request.GET.get('id')))

                for district in data:
                    select_object = SelectObject()
                    select_object.value = district.id
                    select_object.label = district.name
                    select_arr.append(select_object)

            else:
                data = City.objects.all()

                for city in data:
                    select_object = SelectObject()
                    select_object.value = city.id
                    select_object.label = city.name
                    select_arr.append(select_object)

            serializer = SelectSerializer(select_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:

            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class UniversitySelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = University.objects.all()

        select_arr = []
        for university in data:
            select_object = SelectObject()
            select_object.value = university.id
            select_object.label = university.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class FacultySelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Faculty.objects.all()

        select_arr = []
        for faculty in data:
            select_object = SelectObject()
            select_object.value = faculty.id
            select_object.label = faculty.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class DepartmentSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Department.objects.all()

        select_arr = []
        for department in data:
            select_object = SelectObject()
            select_object.value = department.id
            select_object.label = department.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class EducationTypeSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = EducationType.objects.filter(~Q(name='Lise'))

        select_arr = []
        for education_type in data:
            select_object = SelectObject()
            select_object.value = education_type.id
            select_object.label = education_type.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class MaritalStatusSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = Language.objects.get(code=lang_code)
        data = MaritalStatus.objects.filter()
        select_arr = []
        for marital_status in data:
            select_object = SelectObject()
            marital_status_description = MaritalStatusDescription.objects.get(maritalStatus=marital_status,
                                                                              language=lang)
            select_object.value = marital_status.uuid
            select_object.label = marital_status_description.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class MilitaryStatusSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = Language.objects.get(code=lang_code)
        data = MilitaryStatus.objects.filter()
        select_arr = []
        for military_status in data:
            select_object = SelectObject()
            military_status_description = MilitaryStatusDescription.objects.get(militaryStatus=military_status,
                                                                                language=lang)
            select_object.value = military_status.uuid
            select_object.label = military_status_description.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class DeleteLog(APIView):

    def delete(self, request, format=None):
        APILogsModel.objects.all().delete()

        Menu.objects.filter(~Q(parent=None)).delete()
        Menu.objects.all().delete()
        return Response("", status.HTTP_200_OK)


class NationalitySelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Nationality.objects.filter()

        select_arr = []
        for nationality in data:
            select_object = SelectObject()
            select_object.value = nationality.id
            select_object.label = nationality.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class GenderSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = Language.objects.get(code=lang_code)
        data = Gender.objects.filter()
        select_arr = []
        for gender in data:
            select_object = SelectObject()
            gender_description = GenderDescription.objects.get(gender=gender,
                                                               language=lang)
            select_object.value = gender.uuid
            select_object.label = gender_description.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class ForeignLanguageSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = Language.objects.get(code=lang_code)
        data = ForeignLanguage.objects.filter()
        select_arr = []
        for foreign_language in data:
            select_object = SelectObject()
            foreign_language_description = ForeignLanguageDescription.objects.get(foreignLanguage=foreign_language,
                                                                                  language=lang)
            select_object.value = foreign_language.id
            select_object.label = foreign_language_description.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class ForeignLanguageLevelSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = Language.objects.get(code=lang_code)
        data = ForeignLanguageLevel.objects.filter()
        select_arr = []
        for foreign_language_level in data:
            select_object = SelectObject()
            foreign_language_level_description = ForeignLanguageLevelDescription.objects.get(
                foreignLanguageLevel=foreign_language_level,
                language=lang)
            select_object.value = foreign_language_level.id
            select_object.label = foreign_language_level_description.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class DriverLicenseSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        select_arr = []
        for e in DriverLicenseEnum:
            select_object = SelectObject()
            select_object.value = e.value
            select_object.label = e.value
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class BlogTypeSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = BlogType.objects.filter()
        select_arr = []
        for type in data:
            select_object = SelectObject()
            select_object.value = type.uuid
            select_object.label = type.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class UnitSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = Unit.objects.filter(isDeleted=False)
        select_arr = []
        for type in data:
            select_object = SelectObject()
            select_object.value = type.uuid
            select_object.label = type.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)


class MenuApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            type = request.GET.get('type')
            menus = None

            if type == 'student':
                menus = MenuStudent.objects.filter(parent=None, isDeleted=False).order_by('order')
            elif type == 'company':
                menus = MenuCompany.objects.filter(parent=None, isDeleted=False).order_by('order')
            elif type == 'consultant':
                menus = MenuConsultant.objects.filter(parent=None, isDeleted=False).order_by('order')
            else:
                menus = Menu.objects.filter(parent=None, isDeleted=False).order_by('order')

            arr = []
            for q in menus:
                api_data = dict()

                api_data['uuid'] = q.uuid

                api_data['header'] = q.header
                api_data['title'] = q.title
                api_data['icon'] = q.icon
                if q.route is not None:
                    api_data['route'] = q.route

                children = None
                if type == 'student':
                    children = MenuStudent.objects.filter(parent=q, isDeleted=False).order_by('order')
                elif type == 'company':
                    children = MenuCompany.objects.filter(parent=q, isDeleted=False).order_by('order')
                elif type == 'consultant':
                    children = MenuConsultant.objects.filter(parent=q, isDeleted=False).order_by('order')
                else:
                    children = Menu.objects.filter(parent=q, isDeleted=False).order_by('order')

                x = []
                for child in children:
                    api_child = dict()
                    # api_child['uuid'] = child.uuid

                    api_child['header'] = child.header
                    api_child['title'] = child.title
                    api_child['icon'] = child.icon
                    api_child['route'] = child.route
                    # menu
                    x.append(api_child)

                if len(x) != 0:
                    api_data['children'] = x

                arr.append(api_data)

            serializer = MenuSerializer(arr, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)




        except Exception as e:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = MenuSerializer(data=request.data, context={'request': request})

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
            uuid = request.GET.get('id')
            menu = Menu.objects.get(uuid=uuid)
            menu.delete()

            return Response({"message": "menu is deleted"}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
