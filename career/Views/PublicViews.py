import traceback

from django.urls import resolve
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.models import Blog, Language, BlogDescription, Unit, UnitStaff
from career.models.APIObject import APIObject
from career.serializers.BlogSerializer import BlogSerializer, BlogPageableSerializer
from career.serializers.UnitSerializer import UnitStaffPublicSerializer


class AnnouncementPublicApi(APIView):

    def get(self, request, format=None):
        try:

            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'), blogType__name='Duyuru')

                lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')

                lang = Language.objects.get(code=lang_code)


                blog_translation = BlogDescription.objects.get(blog=blog, language=lang)

                api_data = dict()
                api_data['title'] = blog_translation.title
                api_data['article'] = blog_translation.article
                api_data['uuid'] = blog.uuid
                api_data['languageCode'] = lang.code
                api_data['image'] = blog_translation.image
                api_data['creationDate'] = blog.creationDate.date()

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

                data = Blog.objects.filter(keyword__icontains=title, blogType__name='Duyuru', isDeleted=False).order_by(
                    '-id')[
                       lim_start:lim_end]

                filtered_count = Blog.objects.filter(keyword__icontains=title, blogType__name='Duyuru',
                                                     isDeleted=False).count()
                arr = []
                for x in data:
                    blog_translation = BlogDescription.objects.get(blog=x,
                                                                   language=Language.objects.get(code=lang_code))
                    api_data = dict()
                    api_data['title'] = blog_translation.title
                    api_data['article'] = blog_translation.article[0:70]
                    api_data['uuid'] = x.uuid
                    api_data['image'] = blog_translation.image
                    api_data['creationDate'] = x.creationDate.date()

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
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)




class BlogPublicApi(APIView):

    def get(self, request, format=None):
        try:

            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'), blogType__name='Blog')

                lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')

                lang = Language.objects.get(code=lang_code)


                blog_translation = BlogDescription.objects.get(blog=blog, language=lang)

                api_data = dict()
                api_data['title'] = blog_translation.title
                api_data['article'] = blog_translation.article
                api_data['uuid'] = blog.uuid
                api_data['languageCode'] = lang.code
                api_data['image'] = blog_translation.image
                api_data['creationDate'] = blog.creationDate.date()

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

                data = Blog.objects.filter(keyword__icontains=title, blogType__name='Blog', isDeleted=False).order_by(
                    '-id')[
                       lim_start:lim_end]

                filtered_count = Blog.objects.filter(keyword__icontains=title, blogType__name='Blog',
                                                     isDeleted=False).count()
                arr = []
                for x in data:
                    blog_translation = BlogDescription.objects.get(blog=x,
                                                                   language=Language.objects.get(code=lang_code))
                    api_data = dict()
                    api_data['title'] = blog_translation.title
                    api_data['article'] = blog_translation.article[0:70]
                    api_data['uuid'] = x.uuid
                    api_data['image'] = blog_translation.image
                    api_data['creationDate'] = x.creationDate.date()

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
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnitPublicApi(APIView):

    def get(self, request, format=None):
        try:



            data = Unit.objects.filter(isDeleted=False).order_by(
                'order')

            arr = []
            x = resolve(request.path_info).url_name
            for x in data:

                api_data = dict()
                api_data['unitName'] = x.name
                api_data['unitNameLink'] = x.website

                staffs = UnitStaff.objects.filter(unit=x, isDeleted=False)
                arr_staff = []
                for staff in staffs:
                    staff_data = dict()
                    staff_data['firstName'] = staff.person.firstName
                    staff_data['lastName'] = staff.person.lastName
                    staff_data['title'] = staff.person.title
                    staff_data['cvLink'] = staff.person.cvLink
                    arr_staff.append(staff_data)

                api_data['staffs'] = arr_staff

                arr.append(api_data)

            serializer = UnitStaffPublicSerializer(
                arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
