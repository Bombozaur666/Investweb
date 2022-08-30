from .views import *
from .feeds import LatestArticles
from django.urls import path


app_name = 'articles'


urlpatterns = [
    path('feed/', LatestArticles(), name='articles-feed'),
    path('', ArticlesList.as_view(), name='articles-list'),
    path('create/', ArticleCreate.as_view(), name='create-article'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='update-article'),
    path('<int:pk>/create/', CreateComment.as_view(), name='create-comment'),
    path('<int:pk>/unpublish/', UnpublishArticle.as_view(), name='unpublish-article'),
    path('<int:pk>/deactivate/<int:commpk>/', DeactivateComment.as_view(), name='deactivate-comment'),
    path('search/', Search.as_view(), name='article-search'),
    path('tags/', TagsList.as_view(), name='tag-list'),
    path('tags/<int:tag>/', Tag.as_view(), name='tag'),
    path('similarposts/<int:pk>/', SimilarPostsByTags.as_view(), name='similar-posts'),
]
