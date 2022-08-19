from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer, BasicCommentSerializer
from rest_framework import generics, status
from django.contrib.postgres.search import SearchVector


# Create your views here.

class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.published().all()
    serializer_class = ArticleSerializer
    filterset_fields = ['language', 'type']


class ArticleUpdate(generics.UpdateAPIView):
    queryset = Article.objects.published().all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


class ArticleCreate(generics.CreateAPIView):
    queryset = Article.objects.published().all()
    serializer_class = ArticleSerializer


class ArticleDetail(generics.GenericAPIView):
    def get(self, request, pk):
        article = get_list_or_404(Article, status='published', pk=pk)
        article_serializer = ArticleSerializer(article, many=True)
        comments = Comment.objects.filter(article_id=pk, active=True)
        comments_serializer = CommentSerializer(comments, many=True)
        return JsonResponse({'article': article_serializer.data,
                             'comments': comments_serializer.data},
                            safe=False)


class UnpublishArticle(generics.GenericAPIView):
    def post(self, request, pk):
        try:
            article = Article.objects.published().get(pk=pk)
            article.status = 'draft'
            article.save()
        except Article.DoesNotExist:
            raise Http404
        return Response(status=status.HTTP_200_OK)


class DeactivateComment(generics.GenericAPIView):
    def get(self, request, pk, commpk):
        try:
            comm = Comment.objects.filter(pk=commpk).get()
            comm.active = False
            comm.save()
        except Comment.DoesNotExist:
            raise Http404
        return Response(status=status.HTTP_200_OK)


class CreateComment(generics.CreateAPIView):
    def put(self, request, pk):
        serializer = BasicCommentSerializer(data=request.data)
        if serializer.is_valid():
            comm = Comment(article_id=pk, body=serializer.validated_data['body'],
                           user=serializer.validated_data['user'])
            comm.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Search(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.annotate(search=SearchVector('title', 'body'),).filter(search=request.data['search'])
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarPostsByTags(APIView):
    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, status='published', pk=pk)
        article_tag_ids = []
        for tag in article.tags.all():
            article_tag_ids.append(str(tag.id))
        similar_articles = Article.objects.published().filter(tags__in=article_tag_ids).exclude(pk=article.pk)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        serializer = ArticleSerializer(similar_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
