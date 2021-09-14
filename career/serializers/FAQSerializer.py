import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from slugify import slugify

from career.models import Language
from career.models.FAQ import FAQ
from career.models.FAQDescription import FAQDescription
from career.serializers.GeneralSerializers import PageSerializer


class FAQSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)
    languageCode = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                faq = FAQ()
                r = slugify(validated_data.get('question'))
                faq.keyword = r

                faq.save()

                faq_tr = FAQDescription()
                faq_tr.question = validated_data.get('question')
                faq_tr.faq = faq
                faq_tr.answer = validated_data.get('answer')
                faq_tr.language = Language.objects.get(code='tr')
                faq_tr.save()

                languages = Language.objects.filter(~Q(code='tr'))

                for lang in languages:
                    faq_desc = FAQDescription()
                    faq_desc.faq = faq
                    faq_desc.question = ''
                    faq_desc.answer = ''
                    faq_desc.language = lang
                    faq_desc.save()

                return faq


        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")



class FAQUpdateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)
    languageCode = serializers.CharField(required=False)


    def update(self, instance, validated_data):

        try:
            faq = instance

            faq_description = FAQDescription.objects.get(faq=faq, language=Language.objects.get(
                code=validated_data.get('languageCode')))

            faq_description.question = validated_data.get('question')
            faq_description.answer = validated_data.get('answer')


            faq_description.save()
            return faq_description

        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")



class FAQPageableSerializer(PageSerializer):
    data = FAQSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
