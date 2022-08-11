from django.shortcuts import render
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
# Create your views here.


class BasicArticle(viewsets.ModelViewSet):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer

