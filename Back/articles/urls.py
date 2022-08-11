app_name = 'articles'
from django.contrib import admin
from django.urls import path, include
from .views import BasicArticle, BasicComment
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('basicarticle', BasicArticle)
router.register('basiccomment', BasicComment)

urlpatterns = [
    path('', include(router.urls)),
]