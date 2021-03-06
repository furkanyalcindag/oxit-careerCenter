import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from slugify import slugify

from career.models import Blog, BlogDescription, Language, Lecture, LectureDescription, Instructor, Company
from career.models.Location import Location
from career.serializers.GeneralSerializers import PageSerializer, SelectSerializer


class LectureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    languageCode = serializers.CharField(required=False)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    capacity = serializers.IntegerField()
    locationId = serializers.UUIDField(write_only=True)
    instructorId = serializers.UUIDField(write_only=True)
    location = SelectSerializer(read_only=True)
    instructor = SelectSerializer(read_only=True)
    isPaid = serializers.BooleanField(default=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    room = serializers.CharField()
    date = serializers.DateField(required=True, format="%DD-%MM-%YYYY")
    time = serializers.TimeField(required=True)
    companyId = serializers.UUIDField(write_only=True, required=False)
    company = SelectSerializer(read_only=True, required=False)

    def update(self, instance, validated_data):

        try:
            lecture = instance

            lecture_description = LectureDescription.objects.get(lecture=lecture, language=Language.objects.get(
                code=validated_data.get('languageCode')))

            lecture_description.name = validated_data.get('name')
            lecture_description.description = validated_data.get('description')
            lecture_description.image = validated_data.get('image')
            if validated_data.get('companyId') is not None:
                lecture.company = Company.objects.get(uuid=validated_data.get('companyId'))

            lecture_description.save()
            return lecture_description

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("l??tfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                lecture = Lecture()

                lecture.name = validated_data.get('name')
                lecture.isPaid = validated_data.get('isPaid')
                lecture.price = validated_data.get('price')
                lecture.capacity = validated_data.get('capacity')
                lecture.instructor = Instructor.objects.get(uuid=validated_data.get('instructorId'))
                lecture.location = Location.objects.get(uuid=validated_data.get('locationId'))
                lecture.room = validated_data.get('room')
                lecture.date = validated_data.get('date')
                lecture.time = validated_data.get('time')
                if validated_data.get('companyId') is not None:
                    lecture.company = Company.objects.get(uuid=validated_data.get('companyId'))
                lecture.save()

                lecture_tr = LectureDescription()
                lecture_tr.name = validated_data.get('name')
                lecture_tr.description = validated_data.get('description')
                lecture_tr.language = Language.objects.get(code='tr')
                lecture_tr.image = validated_data.get('image')

                lecture_tr.lecture = lecture
                lecture_tr.save()

                languages = Language.objects.filter(~Q(code='tr'))

                for lang in languages:
                    lecture_desc = LectureDescription()
                    lecture_desc.name = ''
                    lecture_desc.description = ''
                    lecture_desc.language = lang
                    lecture_desc.lecture = lecture
                    lecture_desc.image = None
                    lecture_desc.save()

                return lecture


        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("l??tfen tekrar deneyiniz")


class LecturePageableSerializer(PageSerializer):
    data = LectureSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LectureDescSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    languageCode = serializers.CharField(required=False)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        try:
            lecture = instance

            lecture_description = LectureDescription.objects.get(lecture=lecture, language=Language.objects.get(
                code=validated_data.get('languageCode')))

            lecture_description.name = validated_data.get('name')
            lecture_description.description = validated_data.get('description')
            lecture_description.image = validated_data.get('image')

            lecture_description.save()
            return lecture_description

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("l??tfen tekrar deneyiniz")


class LectureInformationSerializer(serializers.Serializer):
    capacity = serializers.IntegerField()
    isPaid = serializers.BooleanField(default=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    room = serializers.CharField()
    date = serializers.DateField(required=True, format="%DD-%MM-%YYYY")
    time = serializers.TimeField(required=True)
    locationId = serializers.UUIDField(write_only=True)
    instructorId = serializers.UUIDField(write_only=True)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time')
        instance.date = validated_data.get('date')
        instance.room = validated_data.get('room')
        instance.isPaid = validated_data.get('isPaid')
        instance.price = validated_data.get('price')
        instance.location = Location.objects.get(uuid=validated_data.get('locationId'))
        instance.instructor = Instructor.objects.get(uuid=validated_data.get('instructorId'))
        instance.save()
        return instance

    def create(self, validated_data):
        pass
