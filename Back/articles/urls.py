app_name = 'articles'
from .feeds import LatestArticles
from django.urls import path, include
from .views import BasicArticle, BasicComment
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('basicarticle', BasicArticle)
router.register('basiccomment', BasicComment)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', LatestArticles(), name='articles_feed'),
]
