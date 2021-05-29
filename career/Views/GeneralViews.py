from django.db.models import Q
from drf_api_logger.models import APILogsModel
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language, District, City, JobType, University, Faculty, EducationType, Department, \
    MaritalStatus, StudentEducationInfo, MilitaryStatusDescription, Nationality, Gender, ForeignLanguage, \
    ForeignLanguageLevel, ForeignLanguageLevelDescription
from career.models.ForeignLanguageDescription import ForeignLanguageDescription
from career.models.GenderDescription import GenderDescription
from career.models.Location import Location
from career.models.MaritalStatusDescription import MaritalStatusDescription
from career.models.MilitaryStatus import MilitaryStatus
from career.models.SelectObject import SelectObject
from career.serializers.GeneralSerializers import LanguageSerializer, SelectSerializer


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
        MaritalStatusDescription.objects.all().delete()
        MaritalStatus.objects.all().delete()

        MilitaryStatusDescription.objects.all().delete()
        MilitaryStatus.objects.all().delete()

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
