from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from career.models import Profile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['fullName'] = self.user.first_name + ' ' + self.user.last_name
        data['group'] = self.user.groups.values_list('name', flat=True)[0]
        if len(Profile.objects.filter(user=self.user)) > 0:
            data['avatar'] = Profile.objects.get(user=self.user).profileImage
        else:
            data['avatar'] = None
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
