import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from career.models import Profile, Student, StudentEducationInfo, University, Faculty, Department, EducationType, \
    MaritalStatus, Gender, Nationality, Certificate, JobInfo, JobType, StudentForeignLanguage, ForeignLanguage, \
    ForeignLanguageLevel, StudentQualification
from career.models.DriverLicenseEnum import DriverLicenseEnum
from career.models.MilitaryStatus import MilitaryStatus
from career.models.Reference import Reference
from career.models.StudentDriverLicense import StudentDriverLicense
from career.models.StudentExam import StudentExam
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
    isGraduated = serializers.BooleanField(required=True)
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
                student.isGraduated = validated_data.get('isGraduated')
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
    graduationDate = serializers.DateField(required=True, allow_null=True)

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
    graduationDate = serializers.DateField(required=True, allow_null=True)
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


class StudentGeneralInformationSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    birthDate = serializers.DateField()
    genderId = serializers.UUIDField(write_only=True)
    gender = SelectSerializer(read_only=True)
    maritalStatusId = serializers.UUIDField(write_only=True)
    maritalStatus = SelectSerializer(read_only=True)
    nationality = SelectSerializer(read_only=True)
    nationalityId = serializers.CharField(write_only=True)
    studentNumber = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        try:
            profile = instance.profile
            user = profile.user
            user.first_name = validated_data.get('firstName')
            user.last_name = validated_data.get('lastName')

            profile.birthDate = validated_data.get('birthDate')
            profile.maritalStatus = MaritalStatus.objects.get(uuid=validated_data.get('maritalStatusId'))
            profile.gender = Gender.objects.get(uuid=validated_data.get('genderId'))
            profile.nationality = Nationality.objects.get(id=int(validated_data.get('nationalityId')))
            user.save()
            profile.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class StudentProfileImageSerializer(serializers.Serializer):
    profileImage = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            profile = instance.profile
            profile.profileImage = validated_data.get('profileImage')
            profile.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError('lütfen tekrar deneyiniz')

    def create(self, validated_data):
        pass


class StudentMilitaryStatusSerializer(serializers.Serializer):
    militaryStatus = SelectSerializer(read_only=True)
    militaryStatusId = serializers.UUIDField(write_only=True)
    delayedDate = serializers.DateField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        try:
            profile = instance.profile
            military_status = MilitaryStatus.objects.get(uuid=validated_data.get('militaryStatusId'))
            profile.militaryStatus = military_status
            profile.militaryDelayedDate = validated_data.get('delayedDate')
            profile.profileImage = validated_data.get('profileImage')
            profile.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError('lütfen tekrar deneyiniz')

    def create(self, validated_data):
        pass


class StudentCommunicationSerializer(serializers.Serializer):
    mobilePhone = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        try:
            profile = instance.profile
            profile.mobilePhone = validated_data.get('mobilePhone')
            profile.address = validated_data.get('address')
            profile.save()
            return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError('lütfen tekrar deneyiniz')

    def create(self, validated_data):
        pass


class StudentCertificateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    institutionName = serializers.CharField(required=True)
    certificateNo = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True)
    year = serializers.IntegerField()

    def create(self, validated_data):
        try:
            certificate = Certificate()

            user = self.context['request'].user
            student = Student.objects.get(profile__user=user)
            certificate.student = student
            certificate.certificateNo = validated_data.get('certificateNo')
            certificate.name = validated_data.get('name')
            certificate.institutionName = validated_data.get('institutionName')
            certificate.description = validated_data.get('description')
            certificate.year = validated_data.get('year')
            certificate.save()

            return certificate

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            instance.certificateNo = validated_data.get('certificateNo')
            instance.name = validated_data.get('name')
            instance.institutionName = validated_data.get('institutionName')
            instance.description = validated_data.get('description')
            instance.year = validated_data.get('year')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentJobInformationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    company = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    startDate = serializers.DateField(required=True)
    isContinue = serializers.BooleanField(required=False, allow_null=True)
    finishDate = serializers.DateField(required=False, allow_null=True)
    description = serializers.CharField(required=False)
    jobType = SelectSerializer(read_only=True)
    jobTypeId = serializers.CharField(write_only=True)
    isApplied = serializers.BooleanField(read_only=True, required=False)

    def create(self, validated_data):
        try:
            job_information = JobInfo()

            user = self.context['request'].user
            student = Student.objects.get(profile__user=user)
            job_information.student = student
            job_information.company = validated_data.get('company')
            job_information.title = validated_data.get('title')
            job_information.startDate = validated_data.get('startDate')
            job_information.isContinue = validated_data.get('isContinue')
            job_information.finishDate = validated_data.get('finishDate')
            job_information.description = validated_data.get('description')
            job_information.jobType = JobType.objects.get(id=int(validated_data.get('jobTypeId')))
            job_information.save()

            return job_information

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            instance.company = validated_data.get('company')
            instance.title = validated_data.get('title')
            instance.startDate = validated_data.get('startDate')
            instance.isContinue = validated_data.get('isContinue')
            instance.finishDate = validated_data.get('finishDate')
            instance.description = validated_data.get('description')
            instance.jobType = JobType.objects.get(id=int(validated_data.get('jobTypeId')))
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentReferenceSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    telephoneNumber = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            reference = Reference()

            user = self.context['request'].user
            student = Student.objects.get(profile__user=user)
            reference.student = student
            reference.firstName = validated_data.get('firstName')
            reference.lastName = validated_data.get('lastName')
            reference.title = validated_data.get('title')
            reference.telephoneNumber = validated_data.get('telephoneNumber')

            reference.save()

            return reference

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def update(self, instance, validated_data):
        try:
            instance.firstName = validated_data.get('firstName')
            instance.lastName = validated_data.get('lastName')
            instance.title = validated_data.get('title')
            instance.telephoneNumber = validated_data.get('telephoneNumber')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentForeignLanguageSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    foreignLanguage = SelectSerializer(read_only=True)
    foreignLanguageId = serializers.CharField(write_only=True)

    readingLevel = SelectSerializer(read_only=True)
    readingLevelId = serializers.CharField(write_only=True)

    writingLevel = SelectSerializer(read_only=True)
    writingLevelId = serializers.CharField(write_only=True)

    speakingLevel = SelectSerializer(read_only=True)
    speakingLevelId = serializers.CharField(write_only=True)

    listeningLevel = SelectSerializer(read_only=True)
    listeningLevelId = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        try:
            instance.student = Student.objects.get(profile__user=self.context['request'].user)
            instance.foreignLanguage = ForeignLanguage.objects.get(
                id=int(validated_data.get('foreignLanguageId')))
            instance.readingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('readingLevelId')))
            instance.writingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('writingLevelId')))
            instance.speakingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('speakingLevelId')))
            instance.listeningLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('listeningLevelId')))

            instance.save()

            return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            student_foreign_language = StudentForeignLanguage()
            student_foreign_language.student = Student.objects.get(profile__user=self.context['request'].user)
            student_foreign_language.foreignLanguage = ForeignLanguage.objects.get(
                id=int(validated_data.get('foreignLanguageId')))
            student_foreign_language.readingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('readingLevelId')))
            student_foreign_language.writingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('writingLevelId')))
            student_foreign_language.speakingLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('speakingLevelId')))
            student_foreign_language.listeningLevel = ForeignLanguageLevel.objects.get(
                id=int(validated_data.get('listeningLevelId')))

            student_foreign_language.save()

            return student_foreign_language

        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentQualificationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    rating = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.rating = int(validated_data.get('rating'))

            instance.save()
            return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            student = Student.objects.get(profile__user=self.context['request'].user)

            qualification = StudentQualification()
            qualification.name = validated_data.get('name')
            qualification.rating = int(validated_data.get('rating'))
            qualification.student = student
            qualification.save()
            return qualification
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentExamSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    point = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    year = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.point = validated_data.get('point')
            instance.year = validated_data.get('year')
            instance.save()
            return instance
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            student = Student.objects.get(profile__user=self.context['request'].user)
            exam = StudentExam()
            exam.name = validated_data.get('name')
            exam.point = validated_data.get('point')
            exam.student = student
            exam.year = int(validated_data.get('year'))
            exam.save()
            return exam
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentDriverLicenseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    driverLicense = SelectSerializer(read_only=True)
    driverLicenseValue = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        try:
            valid_license = False
            for e in DriverLicenseEnum:
                if e.value == validated_data.get('driverLicenseValue'):
                    valid_license = True
                    break

            if valid_license:

                instance.driverLicense = validated_data.get('driverLicenseValue')
                instance.save()
                return instance
            else:
                raise Exception
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            student = Student.objects.get(profile__user=self.context['request'].user)
            driver_license = StudentDriverLicense()
            valid_license = False
            for e in DriverLicenseEnum:
                if e.value == validated_data.get('driverLicenseValue'):
                    valid_license = True
                    break

            if valid_license:
                driver_license.driverLicense = validated_data.get('driverLicenseValue')
                driver_license.student = student
                driver_license.save()

                return driver_license
            else:
                raise Exception
        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
