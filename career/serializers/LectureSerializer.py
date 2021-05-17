import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from slugify import slugify

from career.models import Blog, BlogDescription, Language, Lecture, LectureDescription, Instructor
from career.serializers.GeneralSerializers import PageSerializer


class LectureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    languageCode = serializers.CharField(required=False)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    capacity = serializers.IntegerField()
    locationId = serializers.UUIDField()
    instructorId = serializers.UUIDField()
    location = serializers.CharField(read_only=True)
    instructor = serializers.CharField(read_only=True)
    isPaid = serializers.BooleanField(default=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    room = serializers.CharField()

    def update(self, instance, validated_data):

        try:
            lecture = instance

            lecture_description = LectureDescription.objects.get(lecture=lecture, language=Language.objects.get(
                code=validated_data.get('languageCode')))

            lecture_description.title = validated_data.get('title')
            lecture_description.article = validated_data.get('article')
            lecture_description.image = validated_data.get('image')

            lecture_description.save()
            return lecture_description

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            with transaction.atomic():
                lecture = Lecture()

                lecture.name = validated_data.get('name')
                lecture.isPaid = validated_data.get('isPaid')
                lecture.price = validated_data.get('price')
                lecture.capacity = validated_data.get('capacity')
                lecture.instructor = Instructor.objects.get(uuid=validated_data.get('instructorId'))
                lecture.location = Instructor.objects.get(uuid=validated_data.get('locationId'))
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
                    lecture_desc.save()

                return lecture


        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class LecturePageableSerializer(PageSerializer):
    data = LectureSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
