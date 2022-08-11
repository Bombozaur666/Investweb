from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Article


class LatestArticles(Feed):
    title = 'Investweb'
    link = '/articles/'
    description = 'Welcome to Investweb!'

    def items(self):
        return Article.objects.published()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
