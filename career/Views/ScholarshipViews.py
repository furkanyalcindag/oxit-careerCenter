import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Scholarship
from career.models.APIObject import APIObject
from career.serializers.ScholarshipSerializer import ScholarshipSerializer, ScholarshipPageableSerializer


class ScholarshipApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            scholarship = Scholarship.objects.get(uuid=request.GET.get('id'))

            api_data = dict()
            api_data['name'] = scholarship.name
            api_data['description'] = scholarship.description
            api_data['uuid'] = scholarship.uuid
            api_data['amount'] = scholarship.amount
            api_data['isApprove'] = scholarship.isApprove

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
