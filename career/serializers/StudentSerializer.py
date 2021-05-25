import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Student, StudentEducationInfo, University, Faculty, Department, EducationType
from career.serializers.GeneralSerializers import PageSerializer, SelectSerializer
from career.services.GeneralService import is_integer

from oxiterp.serializers import UserSerializer


class StudentSerializer(serializers.Serializer):
    # TODO: Student serializer
    uuid = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True)
    studentNumber = serializers.CharField(required=True)
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
                group = Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                student = Student(profile=profile)
                student.studentNumber = validated_data.get("studentNumber")
                student.isGraduated = False
                student.save()
                return student
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentPageableSerializer(PageSerializer):
    data = StudentSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class StudentUniversityEducationInformationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    university = SelectSerializer(read_only=True)
    faculty = SelectSerializer(read_only=True)
    department = SelectSerializer(read_only=True)
    universityId = serializers.CharField(write_only=True)
    educationType = SelectSerializer(read_only=True)
    departmentId = serializers.CharField(write_only=True)
    facultyId = serializers.CharField(write_only=True)
    educationTypeId = serializers.CharField(write_only=True)
    isGraduated = serializers.BooleanField()
    gpa = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    isQuaternarySystem = serializers.BooleanField()
    startDate = serializers.DateField(required=True)
    graduationDate = serializers.DateField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            student_education_info = StudentEducationInfo()

            user = self.context['request'].user

            student = Student.objects.get(profile__user=user)

            if is_integer(validated_data.get('universityId')):
                student_education_info.university = University.objects.get(id=int(validated_data.get('universityId')))
            else:
                student_education_info.otherUniversityName = validated_data.get('universityId')

            if is_integer(validated_data.get('facultyId')):
                student_education_info.faculty = Faculty.objects.get(id=int(validated_data.get('facultyId')))
            else:
                student_education_info.otherFacultyName = validated_data.get('facultyId')

            if is_integer(validated_data.get('departmentId')):
                student_education_info.department = Department.objects.get(id=int(validated_data.get('departmentId')))
            else:
                student_education_info.otherDepartmentName = validated_data.get('departmentId')

            student_education_info.educationType = EducationType.objects.get(id=validated_data.get('educationTypeId'))
            student_education_info.startDate = validated_data.get('startDate')
            student_education_info.graduationDate = validated_data.get('graduationDate')
            student_education_info.gpa = validated_data.get('gpa')
            student_education_info.isQuaternarySystem = validated_data.get('isQuaternarySystem')
            student_education_info.save()
            student_education_info.student = student
            return student_education_info

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
