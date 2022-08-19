from .views import *
from .feeds import LatestArticles
from django.urls import path


app_name = 'articles'


urlpatterns = [
    path('feed/', LatestArticles(), name='articles-feed'),
    path('', ArticlesList.as_view()),
    path('create/', ArticleCreate.as_view()),
    path('<int:pk>/', ArticleDetail.as_view()),
    path('<int:pk>/update/', ArticleUpdate.as_view()),
    path('<int:pk>/create/', CreateComment.as_view()),
    path('<int:pk>/unpublish/', UnpublishArticle.as_view()),
    path('<int:pk>/deactivate/<int:commpk>/', DeactivateComment.as_view()),
    path('search/', Search.as_view()),
    path('similarposts/<int:pk>/', SimilarPostsByTags.as_view()),
]
