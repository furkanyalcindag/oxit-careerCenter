import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Consultant, ConsultantCategory, CategoryDescription, Category
from career.models.APIObject import APIObject
from career.serializers.ConsultantSerializer import ConsultantPageableSerializer, ConsultantSerializer, \
    ConsultantStudentPageableSerializer, ConsultantStudentSerializer
from career.serializers.StudentSerializer import StudentProfileImageSerializer


class ConsultantApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        active_page = 1
        consultant_name = ''
        consultant_surname = ''
        consultant_speciality = ''
        lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if request.GET.get('page') is not None:
            active_page = int(request.GET.get('page'))

        if request.GET.get('consultantName') is not None:
            x = str(request.GET.get('consultantName')).split(' ')
            if len(x) > 1:
                consultant_name = x[0]
                consultant_surname = [1]
            elif len(x) == 1:
                consultant_name = x[0]

        if request.GET.get('specialityName') is not None:
            consultant_speciality = str(request.GET.get('specialityName'))

        lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
        lim_end = lim_start + int(request.GET.get('count'))

        data = Consultant.objects.filter(profile__user__first_name__icontains=consultant_name,
                                         profile__user__last_name__icontains=consultant_surname,
                                         speciality__icontains=consultant_speciality, isDeleted=False).order_by('-id')[
               lim_start:lim_end]

        filtered_count = Consultant.objects.filter(profile__user__first_name__icontains=consultant_name,
                                                   profile__user__last_name__icontains=consultant_surname,
                                                   speciality__icontains=consultant_speciality, isDeleted=False).count()
        arr = []
        for x in data:
            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['speciality'] = x.speciality
            api_data['email'] = x.profile.user.username
            api_data['isActive'] = x.profile.user.is_active
            arr_cat = []
            for consultant_category in ConsultantCategory.objects.filter(consultant=x):
                category = consultant_category.category
                category_desc = CategoryDescription.objects.get(category=category, language__code=lang_code)

                arr_cat.append(category_desc.name)

            api_data['categoryList'] = arr_cat
            arr.append(api_data)

        api_object = APIObject()
        api_object.data = arr
        api_object.recordsFiltered = filtered_count
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


class ConsultantStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is None:
            active_page = 1
            consultant_name = ''
            consultant_surname = ''
            consultant_speciality = ''
            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('consultantName') is not None:
                x = str(request.GET.get('consultantName')).split(' ')
                if len(x) > 1:
                    consultant_name = x[0]
                    consultant_surname = [1]
                elif len(x) == 1:
                    consultant_name = x[0]

            if request.GET.get('specialityName') is not None:
                consultant_speciality = str(request.GET.get('specialityName'))

            lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
            lim_end = lim_start + int(request.GET.get('count'))

            kwargs = dict()

            if request.GET.get('categoryId') is not None:
                category = Category.objects.get(uuid=request.GET.get('categoryId'))
                consultant_category = ConsultantCategory.objects.filter(category=category)
                arr = []
                for con_cat in consultant_category:
                    arr.append(con_cat.consultant.uuid)
                kwargs['uuid__in'] = arr

            kwargs['isDeleted'] = False
            kwargs['profile__user__first_name__icontains'] = consultant_name

            kwargs['speciality__icontains'] = consultant_speciality

            data = Consultant.objects.filter(**kwargs).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Consultant.objects.filter(**kwargs).count()
            arr = []
            for x in data:
                api_data = dict()
                api_data['firstName'] = x.profile.user.first_name
                api_data['lastName'] = x.profile.user.last_name
                api_data['uuid'] = x.uuid
                api_data['speciality'] = x.speciality
                api_data['profileImage'] = x.profile.profileImage
                api_data['email'] = x.profile.user.email
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Consultant.objects.count()
            api_object.activePage = 1

            serializer = ConsultantStudentPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        else:

            x = Consultant.objects.get(uuid=request.GET.get('id'))

            api_data = dict()
            api_data['firstName'] = x.profile.user.first_name
            api_data['lastName'] = x.profile.user.last_name
            api_data['uuid'] = x.uuid
            api_data['speciality'] = x.speciality
            api_data['profileImage'] = x.profile.profileImage
            api_data['email'] = x.profile.user.email

            serializer = ConsultantStudentSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


class ConsultantProfileImageApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            student = Consultant.objects.get(profile__user=request.user)
            api_data = dict()
            api_data['profileImage'] = student.profile.profileImage

            serializer = StudentProfileImageSerializer(api_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            instance = Consultant.objects.get(profile__user=request.user)
            serializer = StudentProfileImageSerializer(data=request.data, instance=instance,
                                                       context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "profile image is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
