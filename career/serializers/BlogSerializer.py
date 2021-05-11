import traceback

from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from slugify import slugify

from career.models import Blog, BlogDescription, Language


class BlogSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    article = serializers.CharField(required=True)
    languageCode = serializers.CharField(write_only=True, required=False)
    image = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        try:
            with transaction.atomic():
                blog = Blog()

                r = slugify(validated_data.get('title'))
                blog.keyword = r
                blog.save()

                blog_tr = BlogDescription()
                blog_tr.title = validated_data.get('title')
                blog_tr.article = validated_data.get('article')
                blog_tr.language = Language.objects.get(code='tr')
                blog_tr.image = validated_data.get('image')
                blog_tr.blog = blog
                blog_tr.save()

                languages = Language.objects.filter(~Q(code='tr'))

                for lang in languages:
                    blog_desc = BlogDescription()
                    blog_desc.title = ''
                    blog_desc.article = ''
                    blog_desc.language = lang
                    blog_desc.blog = blog
                    blog_desc.save()

                return blog


        except Exception as e:
            traceback.print_exc()
            raise serializers.ValidationError("lütfen tekrar deneyiniz")
