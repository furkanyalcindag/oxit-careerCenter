from django.contrib import auth, messages
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your Views here.
from accounts.serializers import PasswordChangeSerializer


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
