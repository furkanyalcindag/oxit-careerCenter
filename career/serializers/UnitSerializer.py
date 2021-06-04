import traceback

from rest_framework import serializers

from career.models import Unit
from career.serializers.GeneralSerializers import PageSerializer


class UnitSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    website = serializers.CharField(required=False)
    uuid = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        try:

            instance.name = validated_data.get('name')
            instance.website = validated_data.get('website')
            instance.save()
            return instance
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        try:
            unit = Unit()
            unit.name = validated_data.get('name')
            unit.website = validated_data.get('website')
            unit.save()
            return unit
        except:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")


class UnitPageableSerializer(PageSerializer):
    data = UnitSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
