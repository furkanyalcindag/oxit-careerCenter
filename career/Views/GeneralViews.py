from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language, District, City, JobType, University, Faculty, EducationType, Department
from career.models.Location import Location
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
