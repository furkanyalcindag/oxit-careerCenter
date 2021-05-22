from rest_framework import serializers

from career.serializers.JobPostSerializer import JobPostSerializer
from career.serializers.StudentSerializer import StudentSerializer


class JobApplicationSerializer(serializers.Serializer):
    jobPost = JobPostSerializer()
    student = StudentSerializer()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
    