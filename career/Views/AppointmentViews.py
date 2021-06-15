import datetime
import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Appointment, Consultant, Student
from career.serializers.AppointmentSerializer import AppointmentSerializer, AppointmentCalendarSerializer
from career.services import GeneralService


class AppointmentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        date = request.GET.get('date')

        user = request.user

        consultant = Consultant.objects.get(profile__user=user)

        if request.GET.get('id') is None:

            date_start = request.GET.get('startDate').split(' ')[0]
            date_end = request.GET.get('endDate').split(' ')[0]
            appointments = Appointment.objects.filter(date__gte=date_start, date__lte=date_end, consultant=consultant,
                                                      isDeleted=False)

            appointment_arr = []
            for appointment in appointments:
                api_object = dict()
                api_object['uuid'] = appointment.uuid
                api_object[
                    'title'] = appointment.consultant.profile.user.first_name + ' ' + appointment.consultant.profile.user.last_name
                api_object['start'] = str(appointment.date) + ' ' + str(appointment.startTime)
                api_object['end'] = str(appointment.date) + ' ' + str(appointment.finishTime)
                if appointment.student is None:
                    api_object['id'] = 'done'
                else:
                    api_object['id'] = 'undone'

                appointment_arr.append(api_object)

            serializer = AppointmentCalendarSerializer(appointment_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        else:
            appointment = Appointment.objects.get(uuid=request.GET.get('id'))
            api_object = dict()
            api_object['uuid'] = appointment.uuid
            api_object['price'] = appointment.price
            api_object['isPaid'] = appointment.isPaid
            api_object['date'] = appointment.date
            api_object['startTime'] = appointment.startTime
            api_object['finishTime'] = appointment.finishTime
            api_object['isSuitable'] = appointment.isSuitable
            api_object['room'] = appointment.room
            select_location = dict()
            select_location['label'] = appointment.location.name
            select_location['value'] = appointment.location.uuid

            select_student = dict()

            if appointment.student is not None:
                select_student[
                    'label'] = appointment.student.profile.user.first_name + ' ' + appointment.student.profile.user.last_name
                select_student['value'] = appointment.student.uuid

            else:
                select_student = None

            api_object['student'] = select_student
            api_object['location'] = select_location
            serializer = AppointmentSerializer(api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "appointment is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):

        try:
            appointment = Appointment.objects.get(uuid=request.GET.get('id'))

            appointment.isDeleted = True
            appointment.save()
            return Response('deleted', status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:

            instance = Appointment.objects.get(consultant__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = AppointmentSerializer(data=request.data, instance=instance,
                                               context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Appointment is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentAdminApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        date = request.GET.get('date')

        user = request.user

        if request.GET.get('id') is None:

            date_start = request.GET.get('startDate').split(' ')[0]
            date_end = request.GET.get('endDate').split(' ')[0]
            appointments = Appointment.objects.filter(date__gte=date_start, date__lte=date_end,
                                                      isDeleted=False)

            appointment_arr = []
            for appointment in appointments:
                api_object = dict()
                api_object['uuid'] = appointment.uuid
                api_object[
                    'title'] = appointment.consultant.profile.user.first_name + ' ' + appointment.consultant.profile.user.last_name
                api_object['start'] = str(appointment.date) + ' ' + str(appointment.startTime)
                api_object['end'] = str(appointment.date) + ' ' + str(appointment.finishTime)

                if appointment.student is None:
                    api_object['id'] = 'done'
                    api_object['studentName'] = None
                else:
                    api_object[
                        'studentName'] = appointment.student.profile.user.first_name + ' ' + appointment.student.profile.user.last_name
                    api_object['id'] = 'undone'

                appointment_arr.append(api_object)

            serializer = AppointmentCalendarSerializer(appointment_arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        else:
            appointment = Appointment.objects.get(uuid=request.GET.get('id'))
            api_object = dict()
            api_object['uuid'] = appointment.uuid
            api_object['price'] = appointment.price
            api_object['isPaid'] = appointment.isPaid
            api_object['date'] = appointment.date
            api_object['startTime'] = appointment.startTime
            api_object['finishTime'] = appointment.finishTime
            api_object['isSuitable'] = appointment.isSuitable
            api_object['room'] = appointment.room
            select_location = dict()
            select_location['label'] = appointment.location.name
            select_location['value'] = appointment.location.uuid

            select_student = dict()

            if appointment.student is not None:
                select_student[
                    'label'] = appointment.student.profile.user.first_name + ' ' + appointment.student.profile.user.last_name
                select_student['value'] = appointment.student.uuid

            else:
                select_student = None

            api_object['student'] = select_student
            api_object['location'] = select_location
            serializer = AppointmentSerializer(api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


class AppointmentStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            if request.GET.get('startDate') is not None:
                consultant = Consultant.objects.get(uuid=request.GET.get('id'))

                date_start = datetime.datetime.strptime(request.GET.get('startDate'), '%Y-%m-%d')
                date_end = datetime.datetime.strptime(request.GET.get('endDate'), '%Y-%m-%d')

                days = GeneralService.date_range(date_start, date_end)
                hours_arr = []
                index = 0
                for day in days:
                    appointments = Appointment.objects.filter(date=day.date(),
                                                              consultant=consultant,
                                                              isDeleted=False).order_by('startTime')
                    if len(appointments) > 0:
                        api_parent = dict()

                        api_parent['date'] = day.date()
                        if index == 0:
                            api_parent['isVisible'] = True
                        else:
                            api_parent['isVisible'] = True
                        index = 0
                        appointment_arr = []

                        for appointment in appointments:
                            api_object = dict()
                            api_object['uuid'] = appointment.uuid
                            api_object['price'] = appointment.price
                            api_object['isPaid'] = appointment.isPaid
                            api_object['date'] = appointment.date
                            api_object['startTime'] = appointment.startTime
                            api_object['finishTime'] = appointment.finishTime
                            api_object['isSuitable'] = appointment.isSuitable

                            api_object['room'] = appointment.room
                            select_location = dict()
                            select_location['label'] = appointment.location.name
                            select_location['value'] = appointment.location.uuid

                            appointment_arr.append(api_object)

                        api_parent['hours'] = appointment_arr

                        hours_arr.append(api_parent)

                return Response(hours_arr, status.HTTP_200_OK)

            else:
                appointment = Appointment.objects.get(uuid=request.GET.get('id'))

                api_object = dict()
                api_object['uuid'] = appointment.uuid
                api_object['price'] = appointment.price
                api_object['isPaid'] = appointment.isPaid
                api_object['date'] = appointment.date
                api_object['startTime'] = appointment.startTime
                api_object['finishTime'] = appointment.finishTime
                api_object['isSuitable'] = appointment.isSuitable
                api_object[
                    'consultant'] = appointment.consultant.profile.user.first_name + ' ' + appointment.consultant.profile.user.last_name

                api_object['room'] = appointment.room
                select_location = dict()
                select_location['label'] = appointment.location.name
                select_location['value'] = appointment.location.uuid

                api_object['location'] = select_location

                return Response(api_object, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:


            appointment_id = request.data['appointmentId']
            student = Student.objects.get(profile__user=request.user)

            appointment = Appointment.objects.get(uuid=appointment_id)
            appointment.student = student
            appointment.isSuitable = False
            appointment.save()

            return Response("başarılı", status=status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("hatalı", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
