import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.exceptions import LanguageCodeException
from career.models import Blog, BlogDescription, Language
from career.models.APIObject import APIObject
from career.serializers.BlogSerializer import BlogSerializer, BlogPageableSerializer, BlogUpdateSerializer


class BlogApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            blog = Blog.objects.get(uuid=request.GET.get('id'))

            lang = Language.objects.get(code=request.GET.get('langCode'))

            blog_translation = BlogDescription.objects.get(blog=blog, language=lang)

            api_data = dict()
            api_data['title'] = blog_translation.title
            api_data['article'] = blog_translation.article
            api_data['uuid'] = blog.uuid
            api_data['languageCode'] = lang.code
            api_data['image'] = blog_translation.image

            api_select_blog_type = dict()

            if blog.blogType is not None:
                api_select_blog_type['label'] = blog.blogType.name
                api_select_blog_type['value'] = blog.blogType.uuid
            else:
                api_select_blog_type = None

            api_data['type'] = api_select_blog_type

            serializer = BlogSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


        else:
            active_page = 1
            count = 10

            title = ''
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('title') is not None:
                title = slugify(request.GET.get('title'))

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Blog.objects.filter(keyword__icontains=title, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Blog.objects.filter(keyword__icontains=title).count()
            arr = []
            for x in data:
                blog_translation = BlogDescription.objects.get(blog=x, language=Language.objects.get(code=lang_code))
                api_data = dict()
                api_data['title'] = blog_translation.title
                api_data['article'] = blog_translation.article
                api_data['uuid'] = x.uuid
                api_data['image'] = blog_translation.image

                api_select_blog_type = dict()

                if x.blogType is not None:
                    api_select_blog_type['label'] = x.blogType.name
                    api_select_blog_type['value'] = x.blogType.uuid
                else:
                    api_select_blog_type = None

                api_data['type'] = api_select_blog_type

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Blog.objects.filter(isDeleted=False).count()
            api_object.activePage = 1

            serializer = BlogPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "blog is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['Öğrenci Numarası'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:
            instance = Blog.objects.get(uuid=request.GET.get('id'))
            serializer = BlogUpdateSerializer(data=request.data, instance=instance, context={'request': request})

            if request.data['languageCode'] is None:
                raise LanguageCodeException()

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "blog is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except LanguageCodeException:
            traceback.print_exc()
            return Response("Geçerli bir dil kodu gönderin", status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response("", status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        try:
            blog = Blog.objects.get(uuid=request.GET.get('id'))
            blog.isDeleted = True
            blog.save()
            return Response('deleted', status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BlogStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            blog = Blog.objects.get(uuid=request.GET.get('id'))

            lang = Language.objects.get(code=request.GET.get('langCode'))

            blog_translation = BlogDescription.objects.get(blog=blog, language=lang)

            api_data = dict()
            api_data['title'] = blog_translation.title
            api_data['article'] = blog_translation.article
            api_data['uuid'] = blog.uuid
            api_data['languageCode'] = lang.code
            api_data['image'] = blog_translation.image

            serializer = BlogSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


        else:
            active_page = 1
            count = 10

            title = ''
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('title') is not None:
                title = slugify(request.GET.get('title'))

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Blog.objects.filter(keyword__icontains=title, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Blog.objects.filter(keyword__icontains=title).count()
            arr = []
            for x in data:
                blog_translation = BlogDescription.objects.get(blog=x, language=Language.objects.get(code=lang_code))
                api_data = dict()
                api_data['title'] = blog_translation.title
                api_data['article'] = blog_translation.article[0:99]
                api_data['uuid'] = x.uuid
                api_data['image'] = blog_translation.image
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Blog.objects.filter(isDeleted=False).count()
            api_object.activePage = 1

            serializer = BlogPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)
