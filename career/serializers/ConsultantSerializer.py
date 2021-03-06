import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from career.models import Profile, Consultant, Appointment, Category, ConsultantCategory
from career.serializers.GeneralSerializers import PageSerializer
from career.services import GeneralService
from oxiterp.serializers import UserSerializer


class ConsultantSerializer(serializers.Serializer):
    # TODO: Consultant serializer
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)
    speciality = serializers.CharField(required=True)

    isActive = serializers.BooleanField(read_only=True)

    categories = serializers.ListSerializer(write_only=True, child=serializers.UUIDField())
    categoryList = serializers.ListSerializer(read_only=True, required=False, child=serializers.CharField())

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=validated_data.get('email'),
                                                email=validated_data.get('email'))
                user.first_name = validated_data.get("firstName")
                user.last_name = validated_data.get("lastName")
                # user.set_password(validated_data.get('password'))
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()

                group = Group.objects.get(name='Consultant')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                consultant = Consultant(profile=profile)
                consultant.speciality = validated_data.get("speciality")
                consultant.save()

                for categoryUUID in validated_data.get('categories'):
                    category = Category.objects.get(uuid=categoryUUID)
                    consultant_category = ConsultantCategory()
                    consultant_category.consultant = consultant
                    consultant_category.category = category
                    consultant_category.save()

                GeneralService.send_password_email_confirmation(user, password)
                return consultant

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("l??tfen tekrar deneyiniz")


class ConsultantPageableSerializer(PageSerializer):
    data = ConsultantSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ConsultantStudentSerializer(serializers.Serializer):
    # TODO: Consultant student serializer
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField(read_only=True)
    lastName = serializers.CharField(read_only=True)
    speciality = serializers.CharField(read_only=True)
    profileImage = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ConsultantStudentPageableSerializer(PageSerializer):
    data = ConsultantStudentSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
