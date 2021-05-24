import trace
import traceback

from rest_framework import serializers

from career.models import Scholarship, Company


class ScholarshipSerializer(serializers.Serializer):
    '''
    name = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    isApprove = models.BooleanField(default=False)
    '''

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    company = serializers.CharField(read_only=True)
    companyId = serializers.UUIDField(write_only=True, required=True)
    isApprove = serializers.BooleanField()

    def update(self, instance, validated_data):
        pass

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
