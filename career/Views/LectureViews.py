import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.exceptions import LanguageCodeException
from career.models import Language, Lecture, LectureDescription, Student, LectureApplication
from career.models.APIObject import APIObject
from career.serializers.LectureSerializer import LectureSerializer, LecturePageableSerializer, LectureDescSerializer, \
    LectureInformationSerializer


class LectureApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            if request.GET.get('id') is not None:
                lecture = Lecture.objects.get(uuid=request.GET.get('id'))

                lang = Language.objects.get(code=request.GET.get('langCode'))

                lecture_translation = LectureDescription.objects.get(lecture=lecture, language=lang)

                api_data = dict()
                api_data['name'] = lecture_translation.name
                api_data['description'] = lecture_translation.description
                api_data['uuid'] = lecture.uuid
                api_data['languageCode'] = lang.code
                select_company = dict()

                if lecture.company is not None:
                    select_company['label'] = lecture.company.name
                    select_company['value'] = lecture.company.uuid
                else:
                    select_company = None

                api_data['company'] = select_company

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

                lim_start = count * (int(active_page) - 1)
                lim_end = lim_start + int(count)

                data = Lecture.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = Lecture.objects.filter(name__icontains=name, isDeleted=False).count()
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
                    select_company = dict()
                    if x.company is not None:
                        select_company['label'] = x.company.name
                        select_company['value'] = x.company.uuid
                    else:
                        select_company = None

                    api_data['company'] = select_company

                    api_data['instructor'] = select_instructor
                    api_data['location'] = select_location
                    api_data['date'] = str(x.date)
                    api_data['time'] = str(x.time)
                    api_data['isPaid'] = x.isPaid
                    api_data['price'] = x.price
                    arr.append(api_data)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Lecture.objects.filter(isDeleted=False).count()
                api_object.activePage = active_page

                serializer = LecturePageableSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class LectureInfoApi(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):

        try:
            instance = Lecture.objects.get(uuid=request.GET.get('id'))
            serializer = LectureInformationSerializer(data=request.data, instance=instance,
                                                      context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "lecture is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)


class LectureStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

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

                lim_start = count * (int(active_page) - 1)
                lim_end = lim_start + int(count)

                data = Lecture.objects.filter(name__icontains=name, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = Lecture.objects.filter(name__icontains=name, isDeleted=False).count()
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

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = Lecture.objects.filter(isDeleted=False).count()
                api_object.activePage = active_page

                serializer = LecturePageableSerializer(
                    api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            scholarship_id = request.data['lectureId']
            student = Student.objects.get(profile__user=request.user)
            lecture = Lecture.objects.get(uuid=scholarship_id)
            applications = LectureApplication.objects.filter(lecture=lecture, student=student)
            if len(applications) == 0:
                lecture_application = LectureApplication()
                lecture_application.student = student
                lecture_application.lecture = lecture
                lecture_application.save()
                return Response("başarılı", status=status.HTTP_200_OK)
            else:
                return Response("Başvurulamaz", status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("hatalı", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LectureStudentApplicants(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            student = Student.objects.get(profile__user=request.user)

            active_page = 1
            count = 10

            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = int(count) * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = LectureApplication.objects.filter(student=student).order_by('-id')[lim_start:lim_end]

            filtered_count = LectureApplication.objects.filter(student=student).count()
            arr = []
            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            for x in data:
                lecture_translation = LectureDescription.objects.get(lecture=x.lecture,
                                                                     language=Language.objects.get(code=lang_code))
                api_data = dict()
                api_data['name'] = lecture_translation.name
                api_data['description'] = lecture_translation.description
                api_data['uuid'] = x.uuid
                api_data['image'] = lecture_translation.image
                api_data['room'] = x.lecture.room
                api_data['capacity'] = x.lecture.capacity

                select_instructor = dict()
                select_instructor[
                    'label'] = x.lecture.instructor.person.firstName + ' ' + x.lecture.instructor.person.lastName
                select_instructor['value'] = x.lecture.instructor.uuid

                select_location = dict()
                select_location['label'] = x.lecture.location.name
                select_location['value'] = x.lecture.location.uuid

                api_data['instructor'] = select_instructor
                api_data['location'] = select_location
                api_data['date'] = str(x.lecture.date)
                api_data['time'] = str(x.lecture.time)
                api_data['isPaid'] = x.lecture.isPaid
                api_data['price'] = x.lecture.price
                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = LectureApplication.objects.filter(student=student).count()
            api_object.activePage = active_page

            serializer = LecturePageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)
