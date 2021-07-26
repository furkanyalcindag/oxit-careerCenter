import traceback

from rest_framework import serializers

from accounts.exceptions import PasswordConfirmException, PasswordValidationException
from accounts.models import GroupUrlMethod


class PasswordChangeSerializer(serializers.Serializer):
    confirmPassword = serializers.CharField()
    password = serializers.CharField()

    def update(self, instance, validated_data):
        try:
            password = validated_data.get('password')
            confirm = validated_data.get('confirmPassword')

            if password != confirm:
                raise PasswordConfirmException()

            if len(password) < 6:
                raise PasswordValidationException()

            instance.set_password(validated_data.get('password'))
            instance.save()
            return instance
        except PasswordConfirmException:
            traceback.print_exc()
            raise serializers.ValidationError("Şifreler eşleşmiyor")

        except PasswordValidationException:
            traceback.print_exc()
            raise serializers.ValidationError("En az 6 karakter olmalı")
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")

    def create(self, validated_data):
        pass


class PermissionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    groupId = serializers.IntegerField(write_only=True)
    moduleName = serializers.CharField()
    get = serializers.BooleanField()
    post = serializers.BooleanField()
    put = serializers.BooleanField()
    delete = serializers.BooleanField()














    def create(self, validated_data):
        pass
