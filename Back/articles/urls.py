app_name = 'articles'
from .views import ArticleView, ArticlesListView, ArticleTypeView, FiltersView, ArticleTypeWithLangView
from .feeds import LatestArticles
from django.urls import path

urlpatterns = [
    path('', ArticlesListView.as_view()),
    path('<int:pk>/', ArticleView.as_view(), name='article'),
    path('feed/', LatestArticles(), name='articles_feed'),
    path('filters/', FiltersView.as_view(), name='filters_view'),
    path('<str:types>/', ArticleTypeView.as_view(), name='type_view'),
    path('<str:types>/<str:lang>/', ArticleTypeWithLangView.as_view(), name='type_view'),

]
