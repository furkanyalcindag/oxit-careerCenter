from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.models import Blog, BlogDescription, Language
from career.models.APIObject import APIObject
from career.serializers.BlogSerializer import BlogSerializer, BlogPageableSerializer


class BlogApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
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

        data = Blog.objects.filter(keyword__icontains=title).order_by('-id')[
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
