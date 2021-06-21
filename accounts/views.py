from django.contrib import auth, messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your Views here.
from accounts.models import UrlName, UrlMethod, GroupUrlMethod
from accounts.serializers import PasswordChangeSerializer, PermissionSerializer
from career import urls


def show_urls(urllist, depth=0):
    for entry in urllist:
        if entry.name is not None and len(UrlName.objects.filter(name=entry.name)) == 0 and 'admin' in str(entry.name):

            if len(UrlName.objects.filter(name=entry.name)) == 0:
                url_name = UrlName()
                url_name.name = entry.name
                url_name.lookupString = entry.lookup_str
                url_name.pattern = str(entry.pattern)
                url_name.save()

                arr = []
                url_method = UrlMethod()
                url_method.method_Name = 'GET'
                url_method.url = url_name
                url_method.save()

                url_method2 = UrlMethod()
                url_method2.method_Name = 'PUT'
                url_method2.url = url_name
                url_method2.save()

                url_method3 = UrlMethod()
                url_method3.method_Name = 'POST'
                url_method3.url = url_name
                url_method3.save()

                url_method4 = UrlMethod()
                url_method4.method_Name = 'DELETE'
                url_method4.url = url_name
                url_method4.save()

                arr.append(url_method)
                arr.append(url_method2)
                arr.append(url_method3)
                arr.append(url_method4)

                groups = Group.objects.exclude(name__in=['admin', 'consultant', 'student', 'company'])

                for group in groups:

                    for element in arr:
                        group_url = GroupUrlMethod()
                        group_url.group = group
                        group_url.urlMethod = element
                        group_url.isAccess = False
                        group_url.save()

            else:
                url_name = UrlName.objects.get(name=entry.name)

                if (len(UrlMethod.objects.filter(url_name=url_name)) == 0):
                    arr = []
                    url_method = UrlMethod()
                    url_method.method_Name = 'GET'
                    url_method.url = url_name
                    url_method.save()

                    url_method2 = UrlMethod()
                    url_method2.method_Name = 'PUT'
                    url_method2.url = url_name
                    url_method2.save()

                    url_method3 = UrlMethod()
                    url_method3.method_Name = 'POST'
                    url_method3.url = url_name
                    url_method3.save()

                    url_method4 = UrlMethod()
                    url_method4.method_Name = 'DELETE'
                    url_method4.url = url_name
                    url_method4.save()

                    arr.append(url_method)
                    arr.append(url_method2)
                    arr.append(url_method3)
                    arr.append(url_method4)

                    groups = Group.objects.exclude(name__in=['admin', 'consultant', 'student', 'company'])

                    for group in groups:

                        for element in arr:
                            group_url = GroupUrlMethod()
                            group_url.group = group
                            group_url.urlMethod = element
                            group_url.isAccess = False
                            group_url.save()


            print("  " * depth, entry.name)
            print(str(entry.pattern))
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


def show_urls_by_group(urllist, group, depth=0):
    for entry in urllist:
        if entry.name is not None and len(UrlName.objects.filter(name=entry.name)) == 0 and 'admin' in str(entry.name):
            url_name = UrlName()
            url_name.name = entry.name
            url_name.lookupString = entry.lookup_str
            url_name.pattern = str(entry.pattern)
            url_name.save()

            arr = []
            url_method = UrlMethod()
            url_method.method_Name = 'GET'
            url_method.url = url_name
            url_method.save()

            url_method2 = UrlMethod()
            url_method2.method_Name = 'PUT'
            url_method2.url = url_name
            url_method2.save()

            url_method3 = UrlMethod()
            url_method3.method_Name = 'POST'
            url_method3.url = url_name
            url_method3.save()

            url_method4 = UrlMethod()
            url_method4.method_Name = 'DELETE'
            url_method4.url = url_name
            url_method4.save()

            arr.append(url_method)
            arr.append(url_method2)
            arr.append(url_method3)
            arr.append(url_method4)

            groups = Group.objects.filter(name=group.name)

            for group in groups:

                for element in arr:
                    group_url = GroupUrlMethod()
                    group_url.group = group
                    group_url.urlMethod = element
                    group_url.isAccess = False
                    group_url.save()

            print("  " * depth, entry.name)
            print(str(entry.pattern))
        if hasattr(entry, 'url_patterns'):
            show_urls_by_group(entry.url_patterns, group, depth + 1)


# show_urls(career.urls.urlpatterns)


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.user.is_authenticated is True:
        return redirect('booqe:add-blog')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            # return render(request, 'patient/:patient/index', context={})
            return redirect('booqe:add-blog')

        else:
            messages.add_message(request, messages.SUCCESS, 'todo')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


class ChangePasswordApi(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        instance = request.user

        serializer = PasswordChangeSerializer(data=request.data, instance=instance, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "password is updated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionCreates(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        show_urls(urls.urlpatterns, 0)

        return Response({"message": "password is updated"}, status=status.HTTP_200_OK)


class PermissionApi(APIView):

    def get(self, request, format=None):
        group = Group.objects.get(name=request.GET.get('group'))

        urls = UrlName.objects.all()

        arr = []
        for url in urls:
            url_method_groups = GroupUrlMethod.objects.filter(group=group, urlMethod__url=url)

            api_data = dict()
            api_data['moduleName'] = url.name
            api_data['get'] = url_method_groups.get(urlMethod__method_Name='GET').isAccess
            api_data['post'] = url_method_groups.get(urlMethod__method_Name='POST').isAccess
            api_data['put'] = url_method_groups.get(urlMethod__method_Name='PUT').isAccess
            api_data['delete'] = url_method_groups.get(urlMethod__method_Name='DELETE').isAccess
            api_data['uuid'] = url.id

            arr.append(api_data)

        serializer = PermissionSerializer(arr, many=True, context={'request', request})

        return Response(serializer.data, status=status.HTTP_200_OK)
