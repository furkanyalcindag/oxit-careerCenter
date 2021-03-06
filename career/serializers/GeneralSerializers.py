from rest_framework import serializers

from career.models.Menu import Menu
from career.models.MenuCompany import MenuCompany
from career.models.MenuConsultant import MenuConsultant
from career.models.MenuStudent import MenuStudent


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


class MenuChildrenSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    header = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    route = serializers.CharField(required=True)
    icon = serializers.CharField(required=True)


class MenuSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, read_only=True)
    type = serializers.CharField(write_only=True)
    header = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    route = serializers.CharField(required=False, allow_null=True)
    icon = serializers.CharField(required=True)
    parentId = serializers.UUIDField(write_only=True, allow_null=True)
    children = MenuChildrenSerializer(many=True, required=False, read_only=True)
    order = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):

        type = validated_data.get('type')

        menu = None
        if type == 'student':
            menu = MenuStudent()
        elif type == 'consultant':
            menu = MenuConsultant()
        elif type == 'company':
            menu = MenuCompany()
        else:
            menu = Menu()
        menu.title = validated_data.get('title')
        menu.header = validated_data.get('header')
        menu.icon = validated_data.get('icon')
        menu.route = validated_data.get('route')
        if validated_data.get('parentId') is not None:
            if type == 'student':
                menu.parent = MenuStudent.objects.get(uuid=validated_data.get('parentId'))
            elif type == 'consultant':
                menu.parent = MenuConsultant.objects.get(uuid=validated_data.get('parentId'))
            elif type == 'company':
                menu.parent = MenuCompany.objects.get(uuid=validated_data.get('parentId'))
            else:
                menu.parent = Menu.objects.get(uuid=validated_data.get('parentId'))

        menu.save()
        return menu
