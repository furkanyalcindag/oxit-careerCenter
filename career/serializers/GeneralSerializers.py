from rest_framework import serializers


class PageSerializer(serializers.Serializer):
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()


class LanguageSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    flag = serializers.CharField()


class SelectSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
