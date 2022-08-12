from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.views import APIView


# Create your views here.
class ArticleView(APIView):
    def get(self, request, pk):
        # return article with comments
        article = Article.objects.published().filter(pk=pk)
        article_serializer = ArticleSerializer(article, many=True)
        comments = Comment.objects.filter(article_id=pk)
        comments_serializer = CommentSerializer(comments, many=True)
        return JsonResponse({'article': article_serializer.data,
                             'comments': comments_serializer.data},
                            safe=False)

    def put(self, request, pk):
        # add comment to specific article
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, request, pk):
        # update article
        if request.data['body']:
            article = Article.objects.get(pk=pk)
            article.body = request.data['body']
            article.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        # delete article and comments - CASCADE
        Article.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class ArticlesListView(APIView):

    def get(self, request):
        # return all articles
        articles = Article.objects.published().all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request):
        # create article
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
