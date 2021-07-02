import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from slugify import slugify

from career.models import Category, Language, CategoryDescription
from career.serializers.GeneralSerializers import PageSerializer


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, )
    languageCode = serializers.CharField(write_only=True, required=False)
    uuid = serializers.UUIDField(read_only=True)
    isButton = serializers.BooleanField()

    def update(self, instance, validated_data):
        try:
            category_description = CategoryDescription.objects.get(category=instance, language=Language.objects.get(
                code=validated_data.get('languageCode')))

            category_description.name = validated_data.get('name')

            category_description.save()
            instance.isButton = validated_data.get('isButton')
            return category_description

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):

        try:
            with transaction.atomic():

                r = slugify(validated_data.get('name'))
                category = Category()
                category.type = 'Consultant'
                category.keyword = r
                category.isButton = validated_data.get('isButton')
                category.save()

                category_description = CategoryDescription()
                category_description.language = Language.objects.get(code='tr')
                category_description.category = category
                category_description.name = validated_data.get('name')
                category_description.save()

                languages = Language.objects.filter(~Q(code='tr'))

                for language in languages:
                    category_description = CategoryDescription()
                    category_description.language = language
                    category_description.category = category
                    category_description.name = ''
                    category_description.save()

                return category

        except Exception as e:
            traceback.print_exc()
            raise ValidationError("lütfen tekrar deneyiniz")


class CategoryPageableSerializer(PageSerializer):
    data = CategorySerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
