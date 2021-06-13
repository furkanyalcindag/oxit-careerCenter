import traceback

from django.db.models import Q
from rest_framework import serializers

from career.exceptions import AppointmentValidationException
from career.models import Consultant, Appointment, Student
from career.models.Location import Location
from career.serializers.GeneralSerializers import SelectSerializer


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
    location = SelectSerializer(read_only=True)
    studentId = serializers.UUIDField(required=False, allow_null=True)
    student = SelectSerializer(read_only=True, required=False)

    def update(self, instance, validated_data):
        try:
            user = self.context['request'].user
            consultant = Consultant.objects.get(profile__user=user)
            date = validated_data.get('date')
            start_time = validated_data.get('startTime')
            finish_time = validated_data.get('finishTime')

            appointments = Appointment.objects.filter(date=date, consultant=consultant, isDeleted=False,
                                                      startTime__lte=start_time,
                                                      finishTime__gt=start_time).filter(~Q(uuid=instance.uuid))
            if len(appointments) > 0:
                raise AppointmentValidationException()
            else:
                instance.consultant = consultant
                instance.isPaid = validated_data.get('isPaid')
                instance.price = validated_data.get('price')
                instance.date = date
                instance.startTime = start_time
                instance.finishTime = finish_time
                instance.room = validated_data.get('room')
                instance.location = Location.objects.get(uuid=validated_data.get('locationId'))
                if validated_data.get('studentId') is not None:
                    instance.student = Student.objects.get(uuid=validated_data.get('studentId'))
                    instance.isSuitable = False
                else:
                    instance.isSuitable = False
                instance.save()
                return instance
        except AppointmentValidationException:
            traceback.print_exc()
            raise serializers.ValidationError("Lütfen geçerli bir tarih ve zaman giriniz")

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            consultant = Consultant.objects.get(profile__user=user)
            date = validated_data.get('date')
            start_time = validated_data.get('startTime')
            finish_time = validated_data.get('finishTime')
            appointment = Appointment()

            appointments = Appointment.objects.filter(date=date, consultant=consultant, isDeleted=False,
                                                      startTime__lte=start_time,
                                                      finishTime__gt=start_time)
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


class AppointmentCalendarSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    start = serializers.CharField()
    end = serializers.CharField()
    title = serializers.CharField()
    id = serializers.CharField(read_only=False)

    def to_representation(self, obj):
        return {

            'uuid': obj['uuid'],
            'start': obj['start'],
            'end': obj['end'],
            'title': obj['title'],
            'class': obj['id'],

        }
