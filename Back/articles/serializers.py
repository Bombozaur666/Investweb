from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title',  'author', 'body', 'status', 'language']
        read_only_fields = ['slug', 'publish', 'created', 'updated']
