import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Unit, UnitStaff
from career.models.APIObject import APIObject
from career.models.Person import Person
from career.serializers.UnitSerializer import UnitSerializer, UnitPageableSerializer, UnitStaffSerializer, \
    UnitStaffPageableSerializer


class UnitApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            unit = Unit.objects.get(uuid=request.GET.get('id'), isDeleted=False)

            api_data = dict()
            api_data['name'] = unit.name
            api_data['website'] = unit.website
            api_data['uuid'] = unit.uuid

            serializer = UnitSerializer(
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

            data = Unit.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Unit.objects.filter(name__icontains=name, isDeleted=False).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['name'] = x.name
                api_data['website'] = x.website
                api_data['uuid'] = x.uuid

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Unit.objects.filter(isDeleted=False).count()
            api_object.activePage = active_page

            serializer = UnitPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "unit is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:
            instance = Unit.objects.get(uuid=request.GET.get('id'))
            serializer = UnitSerializer(data=request.data, instance=instance,
                                        context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "unit is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            scholarship = Unit.objects.get(uuid=request.GET.get('id'))
            scholarship.isDeleted = True
            scholarship.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UnitStaffApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:

            active_page = 1
            count = 10

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = UnitStaff.objects.filter(unit__uuid=request.GET.get('id'), isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = UnitStaff.objects.filter(unit__uuid=request.GET.get('id'), isDeleted=False).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['firstName'] = x.person.firstName
                api_data['lastName'] = x.person.lastName
                api_data['title'] = x.person.title
                api_data['cv'] = x.person.cvLink
                api_data['uuid'] = x.uuid

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = UnitStaff.objects.filter(isDeleted=False).count()
            api_object.activePage = active_page

            serializer = UnitStaffPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            raise Exception

    def post(self, request, format=None):
        serializer = UnitStaffSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "unit is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            unit_staff = UnitStaff.objects.get(uuid=request.GET.get('id'))
            unit_staff.isDeleted = True
            unit_staff.save()

            person = Person.objects.get(uuid=unit_staff.person.uuid)
            person.isDeleted = True
            person.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
