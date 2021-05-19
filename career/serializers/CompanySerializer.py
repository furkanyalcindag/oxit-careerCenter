import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Company, City, District
from career.serializers.GeneralSerializers import PageSerializer, SelectSerializer
from oxiterp.serializers import UserSerializer


class CompanySerializer(serializers.Serializer):
    # TODO: Company serializer
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)
    companyName = serializers.CharField(required=True)
    isInstitution = serializers.BooleanField(required=True)
    isActive = serializers.BooleanField(read_only=True)

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
                user.set_password('oxit2016')
                user.save()

                group = Group.objects.get(name='Company')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                company = Company(profile=profile)
                company.name = validated_data.get("companyName")
                company.isInstitution = bool(validated_data.get("isInstitution"))
                company.save()
                return company

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class CompanyPageableSerializer(PageSerializer):
    data = CompanySerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CompanyGeneralInformationSerializer(serializers.Serializer):
    # about = serializers.CharField()
    # city = SelectSerializer(read_only=True)
    # district = SelectSerializer(read_only=True)
    # cityId = serializers.CharField(write_only=True, required=True)
    # districtId = serializers.CharField(write_only=True)
    # address = serializers.CharField(required=True)
    name = serializers.CharField()
    logo = serializers.CharField(required=False, allow_null=True)
    staffCount = serializers.IntegerField(required=False, allow_null=True)
    website = serializers.CharField(required=False, allow_null=True)
    year = serializers.IntegerField(required=False, allow_null=True)

    # phone = serializers.CharField()
    # fax = serializers.CharField(required=False)
    # locationMap = serializers.CharField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.logo = validated_data.get('logo')
        instance.staffCount = validated_data.get('staffCount')
        instance.website = validated_data.get('website')
        instance.year = int(validated_data.get('year'))

        instance.save()
        return instance

    def create(self, validated_data):
        pass


class CompanyAboutInformationSerializer(serializers.Serializer):
    about = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.about = validated_data.get('about')
        instance.save()
        return instance

    def create(self, validated_data):
        pass


class CompanyCommunicationInformationSerializer(serializers.Serializer):
    city = SelectSerializer(read_only=True)
    district = SelectSerializer(read_only=True)
    cityId = serializers.CharField(write_only=True, required=False, allow_null=True)
    districtId = serializers.CharField(write_only=True,required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        if validated_data.get('cityId') is not None:
            instance.city = City.objects.get(id=int(validated_data.get('cityId')))
        if validated_data.get('districtId') is not None:
            instance.district = City.objects.get(id=int(validated_data.get('districtId')))
        instance.address = validated_data.get('address')
        instance.email = validated_data.get('email')
        instance.phone = validated_data.get('phone')
        instance.save()
        return instance

    def create(self, validated_data):
        pass
