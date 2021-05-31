import datetime
import traceback

from rest_framework import serializers

from career.models import JobPost, JobType, City, District, Company
from career.serializers.GeneralSerializers import SelectSerializer, PageSerializer


class JobPostSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True)
    quality = serializers.CharField(required=True)
    jobDescription = serializers.CharField(required=True)
    typeId = serializers.IntegerField(write_only=True)
    type = SelectSerializer(read_only=True)
    experienceYear = serializers.IntegerField()
    viewCount = serializers.IntegerField(read_only=True)
    city = SelectSerializer(read_only=True)
    district = SelectSerializer(read_only=True)
    cityId = serializers.CharField(write_only=True, required=False, allow_null=True)
    districtId = serializers.CharField(write_only=True, required=False, allow_null=True)
    startDate = serializers.DateField(required=False)
    finishDate = serializers.DateField(read_only=True)
    logo = serializers.CharField(required=False, read_only=True)

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title')
            instance.quality = validated_data.get('quality')
            instance.jobDescription = validated_data.get('jobDescription')
            instance.type = JobType.objects.get(id=validated_data.get('typeId'))
            instance.experienceYear = validated_data.get('experienceYear')
            instance.company = Company.objects.get(profile__user=self.context['request'].user)
            instance.city = City.objects.get(id=int(validated_data.get('cityId')))
            instance.district = District.objects.get(id=int(validated_data.get('districtId')))
            instance.save()
            return instance

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):

        try:
            job_post = JobPost()
            job_post.title = validated_data.get('title')
            job_post.quality = validated_data.get('quality')
            job_post.jobDescription = validated_data.get('jobDescription')
            job_post.type = JobType.objects.get(id=validated_data.get('typeId'))
            job_post.experienceYear = validated_data.get('experienceYear')
            job_post.company = Company.objects.get(profile__user=self.context['request'].user)
            job_post.city = City.objects.get(id=int(validated_data.get('cityId')))
            job_post.district = District.objects.get(id=int(validated_data.get('districtId')))
            job_post.startDate = validated_data.get('startDate')
            job_post.finishDate = job_post.startDate + datetime.timedelta(days=30)
            job_post.viewCount = 0
            job_post.save()
            return job_post
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class JobPostPageableSerializer(PageSerializer):
    data = JobPostSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
