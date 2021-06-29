import traceback

from django.contrib.auth.models import User

from career.models import NotificationUser, Notification


def create_notification(user, keyword):
    user_notification = NotificationUser()
    user_notification.notification = Notification.objects.get(keyword=keyword)
    user_notification.user = user
    user_notification.save()

    return user_notification


def create_notification_admin(keyword):
    try:
        users = User.objects.filter(groups__name__in=['Admin'])
        for user in users:
            user_notification = NotificationUser()
            user_notification.notification = Notification.objects.get(keyword=keyword)
            user_notification.user = user
            user_notification.save()

        return True
    except Exception as e:
        traceback.print_exc()
        return False
