import traceback

from rest_framework import serializers

from career.exceptions import AppointmentValidationException
from career.models import Consultant, Appointment
from career.models.Location import Location


class AppointmentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    isPaid = serializers.BooleanField(default=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    room = serializers.CharField()
    date = serializers.DateField(required=True)
    startTime = serializers.TimeField(required=True)
    finishTime = serializers.TimeField(required=True)
    locationId = serializers.UUIDField(write_only=True)
    isSuitable = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            consultant = Consultant.objects.get(profile__user=user)
            date = validated_data.get('date')
            start_time = validated_data.get('startTime')
            finish_time = validated_data.get('finishTime')
            appointment = Appointment()

            appointments =Appointment.objects.filter(date=date, startTime__lte=start_time,finishTime__gt=start_time)
            if len(appointments) > 0:
                raise AppointmentValidationException()
            else:
                appointment.consultant = consultant
                appointment.isPaid = validated_data.get('isPaid')
                appointment.price = validated_data.get('price')
                appointment.date = date
                appointment.startTime = start_time
                appointment.finishTime = finish_time
                appointment.room = validated_data.get('room')
                appointment.location = Location.objects.get(uuid=validated_data.get('locationId'))
                appointment.save()
                return appointment
        except AppointmentValidationException:
            traceback.print_exc()
            raise serializers.ValidationError("Lütfen geçerli bir tarih ve zaman giriniz")

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
