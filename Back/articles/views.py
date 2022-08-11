from django.shortcuts import render
from rest_framework import viewsets
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


# Create your views here.
class BasicArticle(viewsets.ModelViewSet):
    queryset = Article.objects.published()
    serializer_class = ArticleSerializer


class BasicComment(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
