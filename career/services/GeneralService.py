import uuid
from datetime import timedelta
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from xhtml2pdf import pisa

from accounts.models import GroupUrlMethod, UrlMethod, UrlName


def get_translation_word(which_lg, keyword):
    with open('example.json', 'r') as myfile:
        data = myfile.read()


def is_integer(param):
    try:
        x = int(param)
        return True
    except:
        return False


from io import BytesIO  # A stream implementation using an in-memory bytes buffer
# It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template

# pisa is a html2pdf converter using the ReportLab Toolkit,
# the HTML5lib and pyPdf.

from xhtml2pdf import pisa


# difine render_to_pdf() function

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def show_urls_by_group(urllist, group, depth=0):
    for entry in urllist:
        if entry.name is not None and 'admin' in str(entry.name):
            url_name = None
            if len(UrlName.objects.filter(lookupString=entry.lookup_str)) > 0:
                url_name = UrlName.objects.get(lookupString=entry.lookup_str)
            else:
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

            print(str(entry.pattern))


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8", 'replace')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def send_order_email_confirmation(student):
    """
    Send email to customer with order details.
    """
    random_uuid = str(uuid.uuid4())
    activation_link = 'https://api-karmer.aybu.edu.tr:8080/career-service/karmer-activation/'
    activation_link = activation_link + random_uuid + '/' + str(student.uuid) + '/'
    message = get_template("activation-mail.html").render({
        'link': activation_link
    })

    html_message = render_to_string('activation-mail.html', {'link': activation_link})
    plain_message = strip_tags(html_message)
    mail = EmailMultiAlternatives(
        subject="AYBU Karmer Kullanıcı Aktivasyonu",
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[student.profile.user.email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.attach_alternative(html_message, 'text/html')
    mail.content_subtype = 'html'
    return mail.send()


def send_password_email_confirmation(user, password):
    """
    Send email to customer with order details.
    """
    random_uuid = str(uuid.uuid4())
    activation_link = 'https://karmer.aybu.edu.tr/portal/'

    message = get_template("password-mail.html").render({
        'link': activation_link,
        'password': password
    })

    html_message = render_to_string('password-mail.html', {'link': activation_link,
                                                           'email': user.email,
                                                           'password': password})
    plain_message = strip_tags(html_message)
    mail = EmailMultiAlternatives(
        subject="AYBU Karmer Kullanıcı Giriş Bilgileri",
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.attach_alternative(html_message, 'text/html')
    mail.content_subtype = 'html'
    return mail.send()



def send_forget_password(user, password):
    """
    Send email to customer with order details.
    """
    random_uuid = str(uuid.uuid4())
    activation_link = 'https://karmer.aybu.edu.tr/portal/'

    message = get_template("password-mail.html").render({
        'link': activation_link,
        'password': password
    })

    html_message = render_to_string('password-mail.html', {'link': activation_link,
                                                           'email': user.email,
                                                           'password': password})
    plain_message = strip_tags(html_message)
    mail = EmailMultiAlternatives(
        subject="AYBU Karmer Kullanıcı Giriş Bilgileri",
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.attach_alternative(html_message, 'text/html')
    mail.content_subtype = 'html'
    return mail.send()