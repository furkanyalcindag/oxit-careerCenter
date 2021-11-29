import traceback

from django.urls import resolve
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.models import Blog, Language, BlogDescription, Unit, UnitStaff, Lecture, LectureDescription, Setting, \
    Company
from career.models.APIObject import APIObject
from career.serializers.BlogSerializer import BlogSerializer, BlogPageableSerializer
from career.serializers.CompanySerializer import CompanySerializer
from career.serializers.LectureSerializer import LectureSerializer
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


class EducationPublicApi(APIView):

    def get(self, request, format=None):
        try:

            if request.GET.get('id') is not None:
                blog = Blog.objects.get(uuid=request.GET.get('id'), blogType__name='Egitim')

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

                data = Blog.objects.filter(keyword__icontains=title, blogType__name='Egitim', isDeleted=False).order_by(
                    '-id')[
                       lim_start:lim_end]

                filtered_count = Blog.objects.filter(keyword__icontains=title, blogType__name='Egitim',
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


class LecturePublicApi(APIView):

    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                lecture = Lecture.objects.get(uuid=request.GET.get('id'))

                lang = request.META.get('HTTP_ACCEPT_LANGUAGE')

                lecture_translation = LectureDescription.objects.get(lecture=lecture, language__code=lang)

                api_data = dict()
                api_data['name'] = lecture_translation.name
                api_data['description'] = lecture_translation.description
                api_data['uuid'] = lecture.uuid
                api_data['languageCode'] = lang

                select_instructor = dict()
                select_instructor[
                    'label'] = lecture.instructor.person.firstName + ' ' + lecture.instructor.person.lastName
                select_instructor['value'] = lecture.instructor.uuid

                select_location = dict()
                select_location['label'] = lecture.location.name
                select_location['value'] = lecture.location.uuid

                api_data['image'] = lecture_translation.image
                api_data['room'] = lecture.room
                api_data['capacity'] = lecture.capacity
                api_data['instructor'] = select_instructor
                api_data['location'] = select_location
                api_data['date'] = str(lecture.date)
                api_data['time'] = str(lecture.time)
                api_data['isPaid'] = lecture.isPaid
                api_data['price'] = lecture.price

                serializer = LectureSerializer(
                    api_data, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)


            else:
                active_page = 1
                count = 10

                name = ''
                lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                if request.GET.get('name') is not None:
                    name = slugify(request.GET.get('name'))

                if request.GET.get('count') is not None:
                    count = int(request.GET.get('count'))

                data = Lecture.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')

                arr = []
                for x in data:
                    lecture_translation = LectureDescription.objects.get(lecture=x,
                                                                         language=Language.objects.get(code=lang_code))
                    api_data = dict()
                    api_data['name'] = lecture_translation.name
                    api_data['description'] = lecture_translation.description
                    api_data['uuid'] = x.uuid
                    api_data['image'] = lecture_translation.image
                    api_data['room'] = x.room
                    api_data['capacity'] = x.capacity

                    select_instructor = dict()
                    select_instructor[
                        'label'] = x.instructor.person.firstName + ' ' + x.instructor.person.lastName
                    select_instructor['value'] = x.instructor.uuid

                    select_location = dict()
                    select_location['label'] = x.location.name
                    select_location['value'] = x.location.uuid

                    api_data['instructor'] = select_instructor
                    api_data['location'] = select_location
                    api_data['date'] = str(x.date)
                    api_data['time'] = str(x.time)
                    api_data['isPaid'] = x.isPaid
                    api_data['price'] = x.price
                    arr.append(api_data)

                serializer = LectureSerializer(
                    arr, many=True, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class ContractPublicApi(APIView):

    def get(self, request, format=None):
        try:
            contract = Setting.objects.get(key='kvkk')

            return Response(contract, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyPublicApi(APIView):

    def get(self, request, format=None):
        try:

            data = Company.objects.filter(isDeleted=False).order_by(
                'name')
            arr = []
            for x in data:
                api_data = dict()
                api_data['companyName'] = x.name

                api_data['logo'] = x.logo
                api_data['firstName'] = "Anonymous"
                api_data['lastName'] = "Anonymous"
                api_data['email'] = "Anonymous"
                api_data['isInstitution'] = False
                api_data['uuid'] = x.uuid
                api_data['website'] = x.website
                api_data['city'] = x.city

                arr.append(api_data)

            serializer = CompanySerializer(
                arr, many=True, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
