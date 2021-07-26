import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Instructor
from career.models.APIObject import APIObject
from career.models.SelectObject import SelectObject
from career.serializers.GeneralSerializers import SelectSerializer
from career.serializers.IntructorSerializer import InstructorPageableSerializer, InstructorSerializer


class InstructorApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        instructor_name = ''
        instructor_surname = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('instructorName') is not None:
            x = str(request.GET.get('instructorName')).split(' ')
            if len(x) > 1:
                instructor_name = x[0]
                instructor_surname = x[1]
            elif len(x) == 1:
                instructor_name = x[0]

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Instructor.objects.filter(person__firstName__icontains=instructor_name,
                                         person__lastName__icontains=instructor_surname, isDeleted=False).order_by(
            '-id')[
               lim_start:lim_end]

        filtered_count = Instructor.objects.filter(person__firstName__icontains=instructor_name,
                                                   person__lastName__icontains=instructor_surname,
                                                   isDeleted=False).count()
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.person.firstName
            api_data['lastName'] = x.person.lastName
            api_data['uuid'] = x.uuid
            api_data['title'] = x.title
            api_data['isDeleted'] = x.isDeleted
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
        api_object.recordsTotal = Instructor.objects.filter(isDeleted=False).count()
        api_object.activePage = 1

        serializer = InstructorPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = InstructorSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "instructor is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            instructor = Instructor.objects.get(uuid=request.GET.get('id'))
            person = instructor.person

            instructor.isDeleted = True

            person.isDeleted = True
            person.save()
            instructor.save()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class InstructorSelectApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        instructor_name = ''
        instructor_surname = ''

        if request.GET.get('instructorName') is not None:
            x = str(request.GET.get('instructorName')).split(' ')
            if len(x) > 1:
                instructor_name = x[0]
                instructor_surname = x[1]
            elif len(x) == 1:
                instructor_name = x[0]

        data = Instructor.objects.filter(person__firstName__icontains=instructor_name,
                                         person__lastName__icontains=instructor_surname, isDeleted=False).order_by(
            '-id')[:20]

        select_arr = []
        for instructor in data:
            select_object = SelectObject()
            select_object.value = instructor.uuid
            select_object.label = instructor.person.firstName + ' ' + instructor.person.lastName
            select_arr.append(select_object)

        serializer = SelectSerializer(select_arr, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)
