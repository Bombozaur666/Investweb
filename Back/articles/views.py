from django.http import JsonResponse
from rest_framework import viewsets
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.views import APIView


# Create your views here.
class ArticleView(APIView):
    def get(self, request, pk):
        #return article with comments
        article = Article.objects.published().filter(pk=pk)
        article_serializer = ArticleSerializer(article, many=True)
        comments = Comment.objects.filter(article_id=pk)
        comments_serializer = CommentSerializer(comments, many=True)
        return JsonResponse([article_serializer.data, comments_serializer.data], safe=False)
    def post(self, request, pk):
        pass
        #add comment to specific article


class ArticlesListView(APIView):

    def get(self, request):
        #return all articles
        request.GET
        articles = Article.objects.published().all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        pass
