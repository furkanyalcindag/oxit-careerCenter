import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.models import Category, Language, CategoryDescription
from career.models.APIObject import APIObject
from career.serializers.CategorySerializer import CategorySerializer, CategoryPageableSerializer


class ConsultantCategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            category = Category.objects.get(uuid=request.GET.get('id'))

            lang = Language.objects.get(code=request.GET.get('langCode'))

            category_translation = CategoryDescription.objects.get(category=category, language=lang)

            api_data = dict()
            api_data['name'] = category_translation.name

            serializer = CategorySerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


        else:
            active_page = 1
            count = 10

            title = ''
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('name') is not None:
                title = slugify(request.GET.get('name'))

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Category.objects.filter(keyword__icontains=title, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Category.objects.filter(keyword__icontains=title).count()
            arr = []
            for x in data:
                blog_translation = CategoryDescription.objects.get(category=x, language=Language.objects.get(code=lang_code))
                api_data = dict()
                api_data['name'] = blog_translation.name

                api_data['uuid'] = x.uuid

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Category.objects.filter(isDeleted=False, type='Consultant').count()
            api_object.activePage = 1

            serializer = CategoryPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, format=None):

        serializer = CategorySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "consultant category is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:

            instance = Category.objects.get(uuid=request.GET.get('id'))

            serializer = CategorySerializer(data=request.data, instance=instance,
                                            context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "consultant category is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


