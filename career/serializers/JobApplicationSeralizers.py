import traceback

from rest_framework import serializers

from career.models import JobPost, Student
from career.models.JobApplication import JobApplication
from career.serializers.JobPostSerializer import JobPostSerializer
from career.serializers.StudentSerializer import StudentSerializer


class JobApplicationSerializer(serializers.Serializer):
    jobPost = JobPostSerializer()
    student = StudentSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class StudentJobApplicationSerializer(serializers.Serializer):
    jobPostId = serializers.UUIDField(required=True, write_only=True)
    coverLetter = serializers.CharField(required=False, allow_null=True)
    jobPost = JobPostSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    companyName = serializers.CharField(read_only=True)
    companyLogo = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:

            job_application = JobApplication()
            job_application.jobPost = JobPost.objects.get(uuid=validated_data.get('jobPostId'))
            job_application.student = Student.objects.get(profile__user=self.context['request'].user)
            job_application.coverLetter = validated_data.get('coverLetter')
            job_application.save()
            return job_application
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
