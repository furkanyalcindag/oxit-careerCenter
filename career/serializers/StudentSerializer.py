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
    universityId = serializers.CharField(write_only=True, required=True)
    educationType = SelectSerializer(read_only=True)
    departmentId = serializers.CharField(write_only=True, required=True)
    facultyId = serializers.CharField(write_only=True, required=True)
    educationTypeId = serializers.CharField(write_only=True, required=True)
    isGraduated = serializers.BooleanField(required=True)
    gpa = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    isQuaternarySystem = serializers.BooleanField(required=True)
    startDate = serializers.DateField(required=True)
    graduationDate = serializers.DateField(required=True)

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
            student_education_info.isGraduated = validated_data.get('isGraduated')
            student_education_info.student = student
            student_education_info.save()

            return student_education_info

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            if is_integer(validated_data.get('universityId')):
                instance.university = University.objects.get(id=int(validated_data.get('universityId')))
            else:
                instance.otherUniversityName = validated_data.get('universityId')

            if is_integer(validated_data.get('facultyId')):
                instance.faculty = Faculty.objects.get(id=int(validated_data.get('facultyId')))
            else:
                instance.otherFacultyName = validated_data.get('facultyId')

            if is_integer(validated_data.get('departmentId')):
                instance.department = Department.objects.get(id=int(validated_data.get('departmentId')))
            else:
                instance.otherDepartmentName = validated_data.get('departmentId')

            instance.educationType = EducationType.objects.get(id=validated_data.get('educationTypeId'))
            instance.startDate = validated_data.get('startDate')
            instance.graduationDate = validated_data.get('graduationDate')
            instance.gpa = validated_data.get('gpa')
            instance.isQuaternarySystem = validated_data.get('isQuaternarySystem')
            instance.isGraduated = validated_data.get('isGraduated')
            instance.save()
            return instance

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentHighSchoolEducationInformationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    educationType = SelectSerializer(read_only=True)
    isGraduated = serializers.BooleanField(required=True)
    gpa = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    isQuaternarySystem = serializers.BooleanField(required=True)
    startDate = serializers.DateField(required=True)
    graduationDate = serializers.DateField(required=True)
    highSchool = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            student_education_info = StudentEducationInfo()

            user = self.context['request'].user

            student = Student.objects.get(profile__user=user)

            student_education_info.highSchool = validated_data.get('highSchool')
            student_education_info.educationType = EducationType.objects.get(name='Lise')
            student_education_info.startDate = validated_data.get('startDate')
            student_education_info.graduationDate = validated_data.get('graduationDate')
            student_education_info.gpa = validated_data.get('gpa')
            student_education_info.isQuaternarySystem = validated_data.get('isQuaternarySystem')
            student_education_info.isGraduated = validated_data.get('isGraduated')
            student_education_info.student = student
            student_education_info.save()

            return student_education_info

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:

            instance.highSchool = validated_data.get('highSchool')
            instance.startDate = validated_data.get('startDate')
            instance.graduationDate = validated_data.get('graduationDate')
            instance.gpa = validated_data.get('gpa')
            instance.isQuaternarySystem = validated_data.get('isQuaternarySystem')
            instance.isGraduated = validated_data.get('isGraduated')
            instance.save()
            return instance

        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
