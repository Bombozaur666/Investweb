app_name = 'articles'
from .views import ArticleView, ArticlesListView
from .feeds import LatestArticles
from django.urls import path, include


urlpatterns = [
    path('', ArticlesListView.as_view(),
    path('<int:pk>/', ArticleView.as_view(), name='article'),
    path('feed/', LatestArticles(), name='articles_feed'),
]
