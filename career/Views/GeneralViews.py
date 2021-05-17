from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Language
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
        data = Location.objects.all.order_by('-id')

        select_arr = []
        for location in data:
            select_object = SelectObject()
            select_object.value = location.uuid
            select_object.label = location.name
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)
