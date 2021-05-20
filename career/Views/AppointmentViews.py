import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Appointment, Consultant
from career.serializers.AppointmentSerializer import AppointmentSerializer


class AppointmentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        date = request.GET.get('date')

        user = request.user

        consultant = Consultant.objects.get(profile__user=user)

        if request.GET.get('id') is None:

            appointments = Appointment.objects.filter(date=date, consultant=consultant, isDeleted=False)

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
                appointment_arr.append(api_object)

            serializer = AppointmentSerializer(appointment_arr, many=True, context={'request': request})

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
