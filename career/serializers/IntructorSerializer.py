import traceback

from django.db import transaction
from rest_framework import serializers

from career.models import Instructor
from career.models.Person import Person
from career.serializers.GeneralSerializers import PageSerializer


class InstructorSerializer(serializers.Serializer):
    # TODO: Instructor serializer
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    isDeleted = serializers.BooleanField(write_only=True, required=False)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                person = instance.person
                person.firstName = validated_data.get('firstName')
                person.lastName = validated_data.get('lastName')
                person.save()

                instance.person = person
                instance.title = validated_data.get('title')

                instance.save()
                return instance


        except Exception:
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():

                person = Person()
                person.firstName = validated_data.get("firstName")
                person.lastName = validated_data.get("lastName")
                person.save()

                instructor = Instructor()
                instructor.person = person
                instructor.title = validated_data.get("title")
                instructor.save()
                return instructor

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class InstructorPageableSerializer(PageSerializer):
    data = InstructorSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
