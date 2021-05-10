from rest_framework import serializers


class PageSerializer(serializers.Serializer):
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
    activePage = serializers.IntegerField()


class LanguageSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    flag = serializers.CharField()
