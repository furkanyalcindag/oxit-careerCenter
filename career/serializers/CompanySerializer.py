import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from career.models import Profile, Company, City, District, CompanySocialMedia, SocialMedia
from career.serializers.GeneralSerializers import PageSerializer, SelectSerializer
from career.services import GeneralService
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
                # user.set_password('oxit2016')
                password = User.objects.make_random_password()
                user.set_password(password)
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

                GeneralService.send_password_email_confirmation(user, password)
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


class CompanySocialMediaSerializer(serializers.Serializer):
    link = serializers.CharField(required=True)
    socialMediaId = serializers.IntegerField(write_only=True, required=True)
    socialMedia = SelectSerializer(read_only=True)
    uuid = serializers.UUIDField(read_only=True, required=False)

    def update(self, instance, validated_data):
        try:
            user = self.context['request'].user
            company = Company.objects.get(profile__user=user)
            instance.company = company
            instance.socialMedia = SocialMedia.objects.get(id=validated_data.get('socialMediaId'))
            instance.link = validated_data.get('link')
            instance.save()
            return instance

        except:
            traceback.print_exc()
            raise serializers.ValidationError('lütfen tekrar deneyiniz')

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            company = Company.objects.get(profile__user=user)

            social_media = CompanySocialMedia()
            social_media.company = company
            social_media.socialMedia = SocialMedia.objects.get(id=validated_data.get('socialMediaId'))
            social_media.link = validated_data.get('link')
            social_media.save()
            return social_media

        except:
            traceback.print_exc()
            raise serializers.ValidationError('Lütfen tekrar deneyiniz')


class CompanyGeneralInformationSerializer(serializers.Serializer):
    name = serializers.CharField()
    logo = serializers.CharField(required=False, allow_null=True)
    staffCount = serializers.IntegerField(required=False, allow_null=True)
    website = serializers.CharField(required=False, allow_null=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    address = serializers.CharField(read_only=True, required=False)
    phone = serializers.CharField(read_only=True, required=False)
    city = serializers.CharField(read_only=True, required=False)
    fax = serializers.CharField(read_only=True, required=False)
    about = serializers.CharField(read_only=True, required=False)
    socialMedias = CompanySocialMediaSerializer(many=True, read_only=True, required=False)
    email = serializers.CharField(read_only=True, required=False)

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
    city = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)
    cityId = serializers.CharField(write_only=True, required=False, allow_null=True)
    districtId = serializers.CharField(write_only=True, required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    fax = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        if validated_data.get('cityId') is not None:
            instance.city = City.objects.get(id=int(validated_data.get('cityId')))
        if validated_data.get('districtId') is not None:
            instance.district = District.objects.get(id=int(validated_data.get('districtId')))
        instance.address = validated_data.get('address')
        instance.email = validated_data.get('email')
        instance.phone = validated_data.get('phone')
        instance.fax = validated_data.get('fax')

        instance.save()
        return instance

    def create(self, validated_data):
        pass


class CompanyListSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    logo = serializers.CharField()
    name = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CompanyListPageableSerializer(PageSerializer):
    data = CompanyListSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CompanyLogoSerializer(serializers.Serializer):
    logo = serializers.CharField()

    def update(self, instance, validated_data):
        try:

            instance.logo = validated_data.get('logo')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError('lütfen tekrar deneyiniz')

    def create(self, validated_data):
        pass
