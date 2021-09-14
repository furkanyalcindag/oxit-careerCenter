import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from slugify import slugify

from career.exceptions import LanguageCodeException
from career.models import Language
from career.models.APIObject import APIObject
from career.models.FAQ import FAQ
from career.models.FAQDescription import FAQDescription
from career.serializers.FAQSerializer import FAQSerializer, FAQPageableSerializer, FAQUpdateSerializer


class FAQApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        if request.GET.get('id') is not None:
            faq = FAQ.objects.get(uuid=request.GET.get('id'))

            lang = Language.objects.get(code=request.GET.get('langCode'))

            faq_translation = FAQDescription.objects.get(faq=faq, language=lang)

            api_data = dict()
            api_data['question'] = faq_translation.question
            api_data['answer'] = faq_translation.answer
            api_data['uuid'] = faq.uuid
            api_data['languageCode'] = lang.code

            serializer = FAQSerializer(
                api_data, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)


        else:
            active_page = 1
            count = 10

            title = ''

            lang_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if request.GET.get('page') is not None:
                active_page = int(request.GET.get('page'))

            if request.GET.get('question') is not None:
                title = slugify(request.GET.get('question'))

            if request.GET.get('count') is not None:
                count = int(request.GET.get('count'))

            lim_start = count * (int(active_page) - 1)
            lim_end = lim_start + int(count)

            data = FAQ.objects.filter(keyword__icontains=title, isDeleted=False).order_by(
                '-id')[
                   lim_start:lim_end]

            filtered_count = FAQ.objects.filter(keyword__icontains=title,
                                                isDeleted=False).count()
            arr = []
            for x in data:
                faq_translation = FAQDescription.objects.get(faq=x, language=Language.objects.get(code=lang_code))
                api_data = dict()
                api_data['question'] = faq_translation.question
                api_data['answer'] = faq_translation.answer
                api_data['uuid'] = x.uuid

                arr.append(api_data)

            api_object = APIObject()
            api_object.data = arr
            api_object.recordsFiltered = filtered_count
            api_object.recordsTotal = FAQ.objects.filter(isDeleted=False).count()
            api_object.activePage = 1

            serializer = FAQPageableSerializer(
                api_object, context={'request': request})

            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = FAQSerializer(data=request.data, context={'request': request})

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
            instance = FAQ.objects.get(uuid=request.GET.get('id'))
            serializer = FAQUpdateSerializer(data=request.data, instance=instance, context={'request': request})

            if request.data['languageCode'] is None:
                raise LanguageCodeException()

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "faq is updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        except LanguageCodeException:
            traceback.print_exc()
            return Response("Geçerli bir dil kodu gönderin", status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response("", status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        try:
            faq = FAQ.objects.get(uuid=request.GET.get('id'))
            faq.isDeleted = True
            faq.save()
            return Response('deleted', status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
