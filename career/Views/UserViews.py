import traceback

from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import GroupUrlMethod
from career.models import Profile
from career.serializers.StudentSerializer import StudentForgetPasswordSerializer
from career.serializers.UserSerializer import UserSerializer, GroupSerializer, StudentRegisterSerializer


class UserAPI(APIView):

    def get(self, request, format=None):

        if request.GET.get('id') is None:
            users = User.objects.exclude(groups__name__in=['Admin', 'Consultant', 'Company', 'Student'])
            arr = []
            for user in users:
                api_data = dict()
                api_data['firstName'] = user.first_name
                api_data['lastName'] = user.last_name
                api_data['email'] = user.email
                api_data['id'] = user.id

                api_data['groupName'] = Group.objects.get(user=user).name

                arr.append(api_data)

            serializers = UserSerializer(arr, many=True, context={'request': request})

            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(~Q(groups__name__in=['Admin', 'Consultant', 'Company', 'Student']),
                                    id=int(request.GET.get('id')))
            api_data = dict()
            api_data['firstName'] = user.first_name
            api_data['lastName'] = user.last_name
            api_data['email'] = user.email
            api_data['id'] = user.id

            api_data['groupName'] = Group.objects.get(user=user).name

            serializers = UserSerializer(api_data, context={'request': request})

            return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data, context={'request', request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "user is created"}, status=status.HTTP_200_OK)
            else:
                errors_dict = dict()
                for key, value in serializer.errors.items():
                    if key == 'studentNumber':
                        errors_dict['????renci Numaras??'] = value

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            id = request.GET.get('id')
            user = User.objects.get(id=int(id))
            profile = Profile.objects.get(user=user)
            profile.delete()

            user.delete()

            return Response({"message": "user is deleted"}, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupAPI(APIView):
    def get(self, request, format=None):

        if request.GET.get('id') is None:
            groups = Group.objects.exclude(name__in=['Admin', 'Consultant', 'Company', 'Student'])

            arr = []
            for group in groups:
                api_data = dict()
                api_data['id'] = group.id
                api_data['groupName'] = group.name
                arr.append(api_data)

            serializer = GroupSerializer(arr, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            group = Group.objects.get(~Q(name__in=['Admin', 'Consultant', 'Company', 'Student']),
                                      id=int(request.GET.get('id')))
            api_data = dict()
            api_data['id'] = group.id
            api_data['groupName'] = group.name

            serializer = GroupSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            serializer = GroupSerializer(data=request.data, context={'request', request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "group is created"}, status=status.HTTP_200_OK)
            else:
                errors_dict = dict()
                for key, value in serializer.errors.items():
                    if key == 'studentNumber':
                        errors_dict['????renci Numaras??'] = value

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            instance = Group.objects.get(id=request.GET.get('id'))
            serializer = GroupSerializer(data=request.data, instance=instance,
                                         context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "group is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            id = request.GET.get('id')
            group = Group.objects.get(id=int(id))
            users = User.objects.filter(groups__name__in=[group.name])
            if len(users) == 0:
                GroupUrlMethod.objects.filter(group=group).delete()
                group.delete()
                return Response({"message": "group is deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "group can not deleted"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentRegisterApi(APIView):

    def post(self, request, format=None):
        serializer = StudentRegisterSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['????renci Numaras??'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentForgetPasswordApi(APIView):

    def post(self, request, format=None):

        try:
            serializer = StudentForgetPasswordSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "password info sended"}, status=status.HTTP_200_OK)
            else:
                errors_dict = dict()
                for key, value in serializer.errors.items():
                    if key == 'studentNumber':
                        errors_dict['????renci Numaras??'] = value

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            traceback.print_exc()
            return Response("hata", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
