from django.shortcuts import render

from career.models import Student


def activate_account(request, operation, activation):
    try:
        student = Student.objects.get(uuid=activation)
        user = student.profile.user
        user.is_active = True
        user.save()

        return render(request, 'activation.html', {'error': False})

    except:
        return render(request, 'activation.html', {'error': True})
