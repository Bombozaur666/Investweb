app_name = 'articles'
from .views import ArticleView, ArticlesListView, ArticleTypeView, FiltersView, ArticleTypeWithLangView, PolishArticlesView, EnglishArticlesView, GermanArticlesView
from .feeds import LatestArticles
from django.urls import path

urlpatterns = [
    path('', ArticlesListView.as_view()),
    path('<int:pk>/', ArticleView.as_view(), name='article'),
    path('pl/', PolishArticlesView.as_view(), name='polish-articles'),
    path('eng/', EnglishArticlesView.as_view(), name='english-articles'),
    path('de/', GermanArticlesView.as_view(), name='german-articles'),
    path('feed/', LatestArticles(), name='articles-feed'),
    path('filters/', FiltersView.as_view(), name='filters-view'),
    path('<str:types>/', ArticleTypeView.as_view(), name='type-view'),
    path('<str:types>/<str:lang>/', ArticleTypeWithLangView.as_view(), name='type-view'),

]
