import traceback

from rest_framework import serializers

from career.models import Scholarship, Company
from career.serializers.GeneralSerializers import PageSerializer, SelectSerializer


class ScholarshipSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    uuid = serializers.UUIDField(read_only=True)
    description = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    company = SelectSerializer(read_only=True)
    companyLogo = serializers.CharField(read_only=True, required=False)
    companyId = serializers.UUIDField(write_only=True, required=True)
    isApprove = serializers.BooleanField()

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.description = validated_data.get('description')
            instance.company = Company.objects.get(uuid=validated_data.get('companyId'))
            instance.amount = validated_data.get('amount')
            instance.isApprove = validated_data.get('isApprove')
            instance.save()
            return instance
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            scholarship = Scholarship()
            scholarship.name = validated_data.get('name')
            scholarship.description = validated_data.get('description')
            scholarship.company = Company.objects.get(uuid=validated_data.get('companyId'))
            scholarship.amount = validated_data.get('amount')
            scholarship.isApprove = validated_data.get('isApprove')
            scholarship.save()
            return scholarship
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class ScholarshipPageableSerializer(PageSerializer):
    data = ScholarshipSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class CompanyScholarshipSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    uuid = serializers.UUIDField(read_only=True)
    description = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    company = SelectSerializer(read_only=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name')
            instance.description = validated_data.get('description')
            instance.amount = validated_data.get('amount')
            instance.isApprove = False
            instance.save()
            return instance
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:

            user = self.context['request'].user
            scholarship = Scholarship()
            scholarship.name = validated_data.get('name')
            scholarship.description = validated_data.get('description')
            scholarship.company = Company.objects.get(profile__user=user)
            scholarship.amount = validated_data.get('amount')
            scholarship.save()
            return scholarship
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
