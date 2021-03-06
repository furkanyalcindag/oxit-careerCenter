import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import JobPost, Student
from career.models.APIObject import APIObject
from career.models.JobApplication import JobApplication
from career.serializers.JobPostSerializer import JobPostSerializer, JobPostPageableSerializer


class JobPostApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            user = request.user
            if request.GET.get('id') is None:

                active_page = 1
                title = ''
                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                if request.GET.get('title') is not None:
                    title = request.GET.get('title')

                lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
                lim_end = lim_start + int(request.GET.get('count'))

                data = JobPost.objects.filter(company__profile__user=user, title__icontains=title,
                                              company__isDeleted=False, isDeleted=False).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = JobPost.objects.filter(company__profile__user=user, title__icontains=title,
                                                        company__isDeleted=False, isDeleted=False).count()

                arr = []
                for x in data:
                    api_data = dict()
                    api_data['uuid'] = x.uuid
                    api_data['title'] = x.title
                    api_data['quality'] = x.quality
                    api_data['jobDescription'] = x.jobDescription

                    select_type = dict()
                    select_type['label'] = x.type.name
                    select_type['value'] = x.type.id

                    api_data['type'] = select_type
                    api_data['viewCount'] = x.viewCount
                    api_data['experienceYear'] = x.experienceYear

                    select_city = dict()

                    if x.city is not None:
                        select_city['label'] = x.city.name
                        select_city['value'] = x.city.id
                    else:
                        select_city = None

                    select_district = dict()
                    if x.district is not None:
                        select_district['label'] = x.district.name
                        select_district['value'] = x.district.id
                    else:
                        select_district = None

                    api_data['city'] = select_city
                    api_data['district'] = select_district
                    api_data['finishDate'] = x.finishDate
                    api_data['startDate'] = x.startDate
                    arr.append(api_data)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = JobPost.objects.filter(company__profile__user=user, isDeleted=False,
                                                                 company__isDeleted=False).count()
                api_object.activePage = active_page

                serializer = JobPostPageableSerializer(api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                uuid = request.GET.get('id')
                x = JobPost.objects.get(uuid=uuid)

                api_data = dict()
                api_data['uuid'] = x.uuid
                api_data['title'] = x.title
                api_data['quality'] = x.quality
                api_data['jobDescription'] = x.jobDescription

                select_type = dict()
                select_type['label'] = x.type.name
                select_type['value'] = x.type.id

                api_data['type'] = select_type
                api_data['viewCount'] = x.viewCount
                api_data['experienceYear'] = x.experienceYear

                select_city = dict()

                if x.city is not None:
                    select_city['label'] = x.city.name
                    select_city['value'] = x.city.id
                else:
                    select_city = None

                select_district = dict()
                if x.district is not None:
                    select_district['label'] = x.district.name
                    select_district['value'] = x.district.id
                else:
                    select_district = None

                api_data['city'] = select_city
                api_data['district'] = select_district
                api_data['finishDate'] = x.finishDate
                api_data['startDate'] = x.startDate

                serializer = JobPostSerializer(api_data, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = JobPostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "job post is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['????renci Numaras??'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:

            instance = JobPost.objects.get(company__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = JobPostSerializer(data=request.data, instance=instance,
                                           context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "job post is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobPostStudentApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            user = request.user
            if request.GET.get('id') is None:

                active_page = 1
                title = ''

                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                if request.GET.get('title') is not None:
                    title = request.GET.get('title')

                lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
                lim_end = lim_start + int(request.GET.get('count'))

                kwargs = dict()

                if request.GET.get('cityId') is not None:
                    kwargs['city__id'] = request.GET.get('cityId')

                if request.GET.get('jobType') is not None:
                    kwargs['type__id'] = request.GET.get('jobType')

                kwargs['title__icontains'] = title

                kwargs['isDeleted'] = False

                kwargs['company__isDeleted'] = False

                data = JobPost.objects.filter(**kwargs).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = JobPost.objects.filter(**kwargs).count()

                arr = []
                for x in data:
                    api_data = dict()
                    api_data['uuid'] = x.uuid
                    api_data['title'] = x.title
                    api_data['quality'] = x.quality
                    api_data['jobDescription'] = x.jobDescription
                    api_data['logo'] = x.company.logo
                    api_data['companyName'] = x.company.name
                    api_data['staffCount'] = x.company.staffCount

                    select_type = dict()
                    select_type['label'] = x.type.name
                    select_type['value'] = x.type.id

                    api_data['type'] = select_type
                    api_data['viewCount'] = x.viewCount
                    api_data['experienceYear'] = x.experienceYear

                    select_city = dict()

                    if x.city is not None:
                        select_city['label'] = x.city.name
                        select_city['value'] = x.city.id
                    else:
                        select_city = None

                    select_district = dict()
                    if x.district is not None:
                        select_district['label'] = x.district.name
                        select_district['value'] = x.district.id
                    else:
                        select_district = None

                    api_data['city'] = select_city
                    api_data['district'] = select_district
                    api_data['finishDate'] = x.finishDate
                    api_data['startDate'] = x.startDate
                    if len(JobApplication.objects.filter(student__profile__user=request.user, jobPost=x)) > 0:
                        api_data['isApplied'] = False
                    else:
                        api_data['isApplied'] = True
                    arr.append(api_data)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = JobPost.objects.filter(company__profile__user=user, isDeleted=False).count()
                api_object.activePage = active_page

                serializer = JobPostPageableSerializer(api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                uuid = request.GET.get('id')
                x = JobPost.objects.get(uuid=uuid)

                api_data = dict()
                api_data['uuid'] = x.uuid
                api_data['companyUUID'] = x.company.uuid
                api_data['title'] = x.title
                api_data['logo'] = x.company.logo
                api_data['quality'] = x.quality
                api_data['jobDescription'] = x.jobDescription
                api_data['companyName'] = x.company.name
                api_data['staffCount'] = x.company.staffCount

                select_type = dict()
                select_type['label'] = x.type.name
                select_type['value'] = x.type.id

                api_data['type'] = select_type
                api_data['viewCount'] = x.viewCount
                api_data['experienceYear'] = x.experienceYear

                select_city = dict()

                if x.city is not None:
                    select_city['label'] = x.city.name
                    select_city['value'] = x.city.id
                else:
                    select_city = None

                select_district = dict()
                if x.district is not None:
                    select_district['label'] = x.district.name
                    select_district['value'] = x.district.id
                else:
                    select_district = None
                api_data['city'] = select_city
                api_data['district'] = select_district
                api_data['finishDate'] = x.finishDate
                api_data['startDate'] = x.startDate

                if len(JobApplication.objects.filter(student__profile__user=request.user, jobPost=x)) > 0:
                    api_data['isApplied'] = False
                else:
                    api_data['isApplied'] = True

                x.viewCount = x.viewCount + 1
                x.save()
                serializer = JobPostSerializer(api_data, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = JobPostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "job post is created"}, status=status.HTTP_200_OK)
        else:
            errors_dict = dict()
            for key, value in serializer.errors.items():
                if key == 'studentNumber':
                    errors_dict['????renci Numaras??'] = value

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):

        try:

            instance = JobPost.objects.get(company__profile__user=request.user, uuid=request.GET.get('id'))
            serializer = JobPostSerializer(data=request.data, instance=instance,
                                           context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "job post is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobPostAdminApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            user = request.user
            if request.GET.get('id') is None:

                active_page = 1

                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
                lim_end = lim_start + int(request.GET.get('count'))

                kwargs = dict()

                if request.GET.get('companyId') is not None:
                    kwargs['company__uuid'] = request.GET.get('companyId')

                kwargs['isDeleted'] = False
                kwargs['company__isDeleted'] = False

                data = JobPost.objects.filter(**kwargs).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = JobPost.objects.filter(**kwargs).count()

                arr = []
                for x in data:
                    api_data = dict()
                    api_data['uuid'] = x.uuid
                    api_data['title'] = x.title
                    api_data['quality'] = x.quality
                    api_data['jobDescription'] = x.jobDescription
                    api_data['logo'] = x.company.logo
                    api_data['companyName'] = x.company.name
                    api_data['staffCount'] = x.company.staffCount

                    select_type = dict()
                    select_type['label'] = x.type.name
                    select_type['value'] = x.type.id

                    api_data['type'] = select_type
                    api_data['viewCount'] = x.viewCount
                    api_data['experienceYear'] = x.experienceYear

                    select_city = dict()

                    if x.city is not None:
                        select_city['label'] = x.city.name
                        select_city['value'] = x.city.id
                    else:
                        select_city = None

                    select_district = dict()
                    if x.district is not None:
                        select_district['label'] = x.district.name
                        select_district['value'] = x.district.id
                    else:
                        select_district = None

                    api_data['city'] = select_city
                    api_data['district'] = select_district
                    api_data['finishDate'] = x.finishDate
                    api_data['startDate'] = x.startDate
                    arr.append(api_data)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = JobPost.objects.filter(isDeleted=False).count()
                api_object.activePage = active_page

                serializer = JobPostPageableSerializer(api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                uuid = request.GET.get('id')
                x = JobPost.objects.get(uuid=uuid)

                api_data = dict()
                api_data['uuid'] = x.uuid
                api_data['title'] = x.title
                api_data['logo'] = x.company.logo
                api_data['quality'] = x.quality
                api_data['jobDescription'] = x.jobDescription
                api_data['companyName'] = x.company.name
                api_data['staffCount'] = x.company.staffCount

                select_type = dict()
                select_type['label'] = x.type.name
                select_type['value'] = x.type.id

                api_data['type'] = select_type
                api_data['viewCount'] = x.viewCount
                api_data['experienceYear'] = x.experienceYear

                select_city = dict()

                if x.city is not None:
                    select_city['label'] = x.city.name
                    select_city['value'] = x.city.id
                else:
                    select_city = None

                select_district = dict()
                if x.district is not None:
                    select_district['label'] = x.district.name
                    select_district['value'] = x.district.id
                else:
                    select_district = None
                api_data['city'] = select_city
                api_data['district'] = select_district
                api_data['finishDate'] = x.finishDate
                api_data['startDate'] = x.startDate

                if len(Student.objects.filter(profile__user=request.user)) > 0 and len(
                        JobApplication.objects.filter(student__profile__user=request.user, jobPost=x)) == 0:
                    api_data['isApplied'] = True
                else:
                    api_data['isApplied'] = False

                serializer = JobPostSerializer(api_data, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            job_post = JobPost.objects.get(uuid=request.GET.get('id'))
            job_post.isDeleted = True
            job_post.save()

            return Response(status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JobPostStudentCompanyApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:
            user = request.user
            if request.GET.get('id') is None:

                active_page = 1

                if request.GET.get('page') is not None:
                    active_page = int(request.GET.get('page'))

                lim_start = int(request.GET.get('count')) * (int(active_page) - 1)
                lim_end = lim_start + int(request.GET.get('count'))

                kwargs = dict()

                if request.GET.get('companyId') is not None:
                    kwargs['company__uuid'] = request.GET.get('companyId')

                kwargs['isDeleted'] = False

                kwargs['company__isDeleted'] = False

                data = JobPost.objects.filter(**kwargs).order_by('-id')[
                       lim_start:lim_end]

                filtered_count = JobPost.objects.filter(**kwargs).count()

                arr = []
                for x in data:
                    api_data = dict()
                    api_data['uuid'] = x.uuid
                    api_data['title'] = x.title
                    api_data['quality'] = x.quality
                    api_data['jobDescription'] = x.jobDescription
                    api_data['logo'] = x.company.logo
                    api_data['companyName'] = x.company.name
                    api_data['staffCount'] = x.company.staffCount

                    select_type = dict()
                    select_type['label'] = x.type.name
                    select_type['value'] = x.type.id

                    api_data['type'] = select_type
                    api_data['viewCount'] = x.viewCount
                    api_data['experienceYear'] = x.experienceYear

                    select_city = dict()

                    if x.city is not None:
                        select_city['label'] = x.city.name
                        select_city['value'] = x.city.id
                    else:
                        select_city = None

                    select_district = dict()
                    if x.district is not None:
                        select_district['label'] = x.district.name
                        select_district['value'] = x.district.id
                    else:
                        select_district = None

                    api_data['city'] = select_city
                    api_data['district'] = select_district
                    api_data['finishDate'] = x.finishDate
                    api_data['startDate'] = x.startDate

                    arr.append(api_data)

                api_object = APIObject()
                api_object.data = arr
                api_object.recordsFiltered = filtered_count
                api_object.recordsTotal = JobPost.objects.filter(isDeleted=False).count()
                api_object.activePage = active_page

                serializer = JobPostPageableSerializer(api_object, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobPostAdminDashboardApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        try:

            if request.GET.get('id') is None:

                data = JobPost.objects.filter(company__isDeleted=False, isDeleted=False).order_by('-id')[
                       1:10]

                arr = []
                for x in data:
                    api_data = dict()
                    api_data['uuid'] = x.uuid
                    api_data['title'] = x.title
                    api_data['quality'] = x.quality
                    api_data['jobDescription'] = x.jobDescription
                    api_data['logo'] = x.company.logo
                    api_data['companyName'] = x.company.name
                    api_data['staffCount'] = x.company.staffCount

                    select_type = dict()
                    select_type['label'] = x.type.name
                    select_type['value'] = x.type.id

                    api_data['type'] = select_type
                    api_data['viewCount'] = x.viewCount
                    api_data['experienceYear'] = x.experienceYear

                    select_city = dict()

                    if x.city is not None:
                        select_city['label'] = x.city.name
                        select_city['value'] = x.city.id
                    else:
                        select_city = None

                    select_district = dict()
                    if x.district is not None:
                        select_district['label'] = x.district.name
                        select_district['value'] = x.district.id
                    else:
                        select_district = None

                    api_data['city'] = select_city
                    api_data['district'] = select_district
                    api_data['finishDate'] = x.finishDate
                    api_data['startDate'] = x.startDate
                    arr.append(api_data)

                serializer = JobPostSerializer(arr, many=True, context={'request': request})

                return Response(serializer.data, status.HTTP_200_OK)

        except:
            traceback.print_exc()
            return Response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
