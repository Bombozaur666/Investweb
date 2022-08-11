from rest_framework import serializers
from .models import Article
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'body', 'status', 'language', 'tags']
        read_only_fields = ['slug', 'publish', 'created', 'updated']
