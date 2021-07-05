import traceback

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from career.models import JobPost, Student
from career.models.JobApplication import JobApplication
from career.serializers.GeneralSerializers import PageSerializer
from career.serializers.JobPostSerializer import JobPostSerializer
from career.serializers.StudentSerializer import StudentSerializer
from career.services.NotificationServices import create_notification


class JobApplicationSerializer(serializers.Serializer):
    jobPost = JobPostSerializer()
    student = StudentSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class StudentJobApplicationSerializer(serializers.Serializer):
    jobPostId = serializers.UUIDField(required=True)
    coverLetter = serializers.CharField(required=False,  allow_null=True)
    jobPost = JobPostSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    companyName = serializers.CharField(read_only=True)
    companyLogo = serializers.CharField(read_only=True)
    isApplied = serializers.BooleanField(read_only=True, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            job_post = JobPost.objects.get(uuid=validated_data.get('jobPostId'))
            job_application = JobApplication()
            job_application.jobPost = job_post
            job_application.student = Student.objects.get(profile__user=self.context['request'].user)
            job_application.coverLetter = validated_data.get('coverLetter')
            if len(JobApplication.objects.filter(jobPost=job_application.jobPost,
                                                 student=job_application.student)) == 0:
                job_application.save()
                create_notification(job_post.company.profile.user, 'company_student_apply_job_post')
                return job_application
            else:
                raise ValidationError("daha önce başvuruldu")
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class StudentJobApplicationPageableSerializer(PageSerializer):
    data = StudentJobApplicationSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
