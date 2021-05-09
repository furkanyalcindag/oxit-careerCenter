import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Company, Consultant
from career.models.APIObject import APIObject
from career.serializers.ConsultantSerializer import ConsultantPageableSerializer, ConsultantSerializer


class ConsultantApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        consultant_name = ''
        consultant_surname = ''
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('consultantName') is not None:
            x = str(request.GET.get('consultantName')).split(' ')
            if len(x) > 1:
                consultant_name = x[0]
                consultant_surname = [1]

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Consultant.objects.filter(profile__user__first_name__icontains=consultant_name,
                                         profile__user__last_name__icontains=consultant_surname).order_by('-id')[
               lim_start:lim_end]
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['speciality'] = x.speciality
            api_data['email'] = x.profile.user.username
            api_data['isActive'] = x.profile.user.is_active
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = data.count()
        api_object.recordsTotal = Consultant.objects.count()
        api_object.activePage = 1

        serializer = ConsultantPageableSerializer(
            api_object, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ConsultantSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "consultant is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            consultant = Consultant.objects.get(uuid=request.GET.get('id'))
            profile = consultant.profile
            user = profile.user
            if request.GET.get('makeActive') == 'true':
                consultant.isDeleted = False
                user.is_active = True
                profile.isDeleted = False
                consultant.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)
            elif request.GET.get('makeActive') == 'false':
                consultant.isDeleted = True
                user.is_active = False
                profile.isDeleted = True
                consultant.save()
                profile.save()
                user.save()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
