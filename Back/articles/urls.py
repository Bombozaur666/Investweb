app_name = 'articles'

from django.urls import path
from .views import ArticlesListView, ArticleView

"""router = DefaultRouter()
router.register('', )
router.register('', )"""

urlpatterns = [
    path('', ArticlesListView.as_view(), name='articles_list'),
    path('<int:pk>/', ArticleView.as_view(), name='article'),
]
