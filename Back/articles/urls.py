app_name = 'articles'
from django.contrib import admin
from django.urls import path, include
from .views import ArticlesListView, ArticleView
from rest_framework.routers import DefaultRouter


"""router = DefaultRouter()
router.register('', )
router.register('', )"""

urlpatterns = [
    path('', ArticlesListView.as_view(), name='articles_list'),
    path('<int:pk>/', ArticleView.as_view(), name='article'),
]