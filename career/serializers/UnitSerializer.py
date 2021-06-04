import traceback

from django.db import transaction
from rest_framework import serializers

from career.models import Unit, UnitStaff
from career.models.Person import Person
from career.serializers.GeneralSerializers import PageSerializer


class UnitSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    website = serializers.CharField(required=False)
    uuid = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        try:

            instance.name = validated_data.get('name')
            instance.website = validated_data.get('website')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            unit = Unit()
            unit.name = validated_data.get('name')
            unit.website = validated_data.get('website')
            unit.save()
            return unit
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class UnitPageableSerializer(PageSerializer):
    data = UnitSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UnitStaffSerializer(serializers.Serializer):
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    cv = serializers.CharField(required=True)
    unitId = serializers.UUIDField(required=True, write_only=True)
    unit = serializers.CharField(required=False, read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                person = Person()
                person.firstName = validated_data.get('firstName')
                person.lastName = validated_data.get('lastName')
                person.title = validated_data.get('title')
                person.cvLink = validated_data.get('cv')
                person.save()

                unit = Unit.objects.get(uuid=validated_data.get('unitId'))

                unit_staff = UnitStaff()
                unit_staff.unit = unit
                unit_staff.person = person
                unit_staff.save()

                return unit_staff
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class UnitStaffPageableSerializer(PageSerializer):
    data = UnitStaffSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
