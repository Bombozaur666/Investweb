from rest_framework import serializers
from .models import Article, Comment
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


# addon to work properly you must find
# 'from django.utils.translation import ugettext_lazy as _'
# and replace it with
# 'from django.utils.translation import gettext_lazy as _'
# because django in 4.x version removed old functions and libraries didn't get update

class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    required = False

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'body', 'type', 'status', 'language', 'tags']
        read_only_fields = ['slug', 'publish', 'created', 'updated']


class BasicCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'body', 'created', 'updated', 'active']
