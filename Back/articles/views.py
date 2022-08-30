from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response


from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer, BasicCommentSerializer
from .mixins import MultipleFieldLookupMixin

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


class ArticleDetail(generics.RetrieveAPIView):
    def retrieve(self, request, pk):
        article = get_object_or_404(Article, status='published', pk=pk)
        article_serializer = ArticleSerializer(article)
        comments = Comment.objects.filter(article_id=pk, active=True)
        comments_serializer = CommentSerializer(comments, many=True)
        return Response({'article': article_serializer.data,
                        'comments': comments_serializer.data})


class UnpublishArticle(generics.GenericAPIView):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.status = 'draft'
        article.save()
        return Response(status=status.HTTP_200_OK)


class DeactivateComment(generics.GenericAPIView):
    def get(self, request, pk, commpk):
        comm = get_object_or_404(Comment, pk=commpk)
        comm.active = False
        comm.save()
        return Response(status=status.HTTP_200_OK)


class CreateComment(generics.CreateAPIView):
    def create(self, request, pk):
        serializer = BasicCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['article_id'] = pk
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Search(MultipleFieldLookupMixin, generics.ListAPIView):
    lookup_fields = ['language', 'type']

    def get_queryset(self):
        filter = {}
        queryset = Article.objects.published().annotate(search=SearchVector('title', 'body'), ).filter(
            search=self.request.data['search'])
        for field in self.lookup_fields:
            if self.request.query_params[field]:
                filter[field] = self.request.query_params[field]
        queryset = get_list_or_404(queryset, **filter)
        return queryset

    def list(self, request, *args, **kwargs):
        articles = self.get_queryset()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimilarPostsByTags(generics.ListAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def get_object(self):
        obj = get_object_or_404(Article, pk=self.kwargs['pk'])
        return obj

    def list(self, request, pk):
        obj = self.get_object()
        article_tag_ids = []
        for tag in obj.tags.all():
            article_tag_ids.append(str(tag.id))
        similar_articles = Article.objects.published().filter(tags__in=article_tag_ids).exclude(pk=obj.pk)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        serializer = ArticleSerializer(similar_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsList(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = Article.tags.all()

    def list(self, request):
        queryset = self.get_queryset()
        tags_name = []
        for tag in queryset:
            tags_name.append({'id': str(tag.id), 'name': str(tag.name)})
        return Response(tags_name, status.HTTP_200_OK)


class Tag(generics.ListAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'tags'

    def get_queryset(self, tag):
        return Article.objects.published().filter(tags=self.lookup_field)

    def list(self, request, tag):
        queryset = self.get_queryset(tag)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

