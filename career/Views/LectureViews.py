import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.exceptions import LanguageCodeException
from career.models import Blog, BlogDescription, Language, Lecture, LectureDescription
from career.models.APIObject import APIObject
from career.serializers.BlogSerializer import BlogSerializer, BlogPageableSerializer
from career.serializers.LectureSerializer import LectureSerializer, LecturePageableSerializer, LectureDescSerializer


class LectureApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            lecture = Lecture.objects.get(uuid=request.GET.get('id'))

            lang = Language.objects.get(code=request.GET.get('langCode'))

            lecture_translation = LectureDescription.objects.get(lecture=lecture, language=lang)

            api_data = dict()
            api_data['name'] = lecture_translation.name
            api_data['description'] = lecture_translation.description
            api_data['uuid'] = lecture.uuid
            api_data['languageCode'] = lang.code
            api_data['image'] = lecture_translation.image
            api_data['room'] = lecture.room
            api_data['capacity'] = lecture.capacity
            api_data['instructor'] = lecture.instructor.person.firstName + ' ' + lecture.instructor.person.lastName
            api_data['location'] = lecture.location.name
            api_data['date'] = str(lecture.date)
            api_data['time'] = str(lecture.time)

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

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = Lecture.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                   lim_start:lim_end]

            filtered_count = Lecture.objects.filter(name__icontains=name).count()
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
                api_data['instructor'] = x.instructor.person.firstName + ' ' + x.instructor.person.lastName
                api_data['location'] = x.location.name
                api_data['date'] = str(x.date)
                api_data['time'] = str(x.time)
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = Lecture.objects.filter(isDeleted=False).count()
            api_object.activePage = 1

            serializer = LecturePageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LectureSerializer(data=request.data, context={'request': request})

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
            instance = Lecture.objects.get(uuid=request.GET.get('id'))
            serializer = LectureDescSerializer(data=request.data, instance=instance, context={'request': request})

            if request.data['languageCode'] is None:
                raise LanguageCodeException()

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "lecture is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except LanguageCodeException:
            traceback.print_exc()
            return Response("Geçerli bir dil kodu gönderin", status.HTTP_404_NOT_FOUND)

        except Exception:
            traceback.print_exc()
            return Response("", status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        try:
            lecture = Lecture.objects.get(uuid=request.GET.get('id'))
            lecture.isDeleted = True
            lecture.save()
            return Response('deleted', status.HTTP_200_OK)

        except Exception as e:

            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
