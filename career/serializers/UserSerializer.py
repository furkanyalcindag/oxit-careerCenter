import traceback

from django.contrib.auth.models import Group, User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career import urls
from career.models import Profile, Student, UserContract, Contract
from career.services import GeneralService
from career.services.GeneralService import show_urls_by_group


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    groupId = serializers.CharField(write_only=True)
    groupName = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                group = Group.objects.get(id=int(validated_data.get('groupId')))

                user = User()
                user.first_name = validated_data.get('firstName')
                user.last_name = validated_data.get('lastName')
                user.email = validated_data.get('email')
                user.username = validated_data.get('email')
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()

                user.groups.add(group)
                user.save()

                profile = Profile()
                profile.user = user
                profile.save()

                GeneralService.send_password_email_confirmation(user, password)
                return profile

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class GroupSerializer(serializers.Serializer):
    groupName = serializers.CharField()
    id = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data('groupName')
            instance.save()
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz!")

    def create(self, validated_data):
        try:
            group = Group()
            group.name = validated_data.get('groupName')
            group.save()

            # show_urls_by_group(urls.urlpatterns, group, depth=0)
            return group
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz!")


class StudentRegisterSerializer(serializers.Serializer):
    # TODO: Student serializer
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    studentNumber = serializers.CharField(required=True)
    isGraduated = serializers.BooleanField(required=False)

    status = serializers.BooleanField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():

                if validated_data.get('status') and validated_data.get('password') == validated_data.get(
                        'confirmPassword'):
                    user = User.objects.create_user(username=validated_data.get('email'),
                                                    email=validated_data.get('email'))
                    user.first_name = validated_data.get("firstName")
                    user.last_name = validated_data.get("lastName")
                    user.set_password(validated_data.get('password'))
                    user.is_active = False
                    # user.set_password('oxit2016')
                    user.save()
                    group = Group.objects.get(name='Student')
                    user.groups.add(group)
                    user.save()
                    profile = Profile.objects.create(user=user)
                    profile.save()
                    student = Student(profile=profile)
                    student.studentNumber = validated_data.get("studentNumber")
                    student.isGraduated = validated_data.get('isGraduated')

                    student.save()
                    student_contract = UserContract()
                    student_contract.user = user
                    student_contract.contract = Contract.objects.get(name='KVKK_Student', isActive=True)
                    student_contract.save()

                    GeneralService.send_order_email_confirmation(student)
                    return student


        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
