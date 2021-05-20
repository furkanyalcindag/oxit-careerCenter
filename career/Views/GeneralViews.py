from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language, District, City, JobType
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
