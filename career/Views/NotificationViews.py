from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from career.models import Notification, NotificationUser, NotificationDescription


class NotificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is None:

            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            user = request.user

            notifications = NotificationUser.objects.filter(user=user, isRead=False)
            arr = []
            for notify in notifications:
                notification = notify.notification

                notification_description = NotificationDescription.objects.get(language__code=lang_code,
                                                                               notification=notification)
                api_dict = dict()
                api_dict['uuid'] = notify.uuid
                api_dict['message'] = notification_description.message
                arr.append(api_dict)

            return Response(arr, status=status)
        else:

            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            user = request.user

            notification_user = NotificationUser.objects.get(user=user, uuid=request.GET.get('id'))

            notification = notification_user.notification

            notification_description = NotificationDescription.objects.get(language__code=lang_code,
                                                                           notification=notification)
            api_dict = dict()

            api_dict['message'] = notification_description.message

            notification_user.isRead = True
            notification_user.save()

            return Response(api_dict, status=status.HTTP_200_OK)
