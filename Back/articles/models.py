from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class ArticleManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status='published')

    def published_pl(self):
        return self.get_queryset().filter(status='published', language='PL')

    def published_eng(self):
        return self.get_queryset().filter(status='published', language='ENG')

    def published_de(self):
        return self.get_queryset().filter(status='published', language='DE')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    LANGUAGE_CHOICES = (
        ('PL', 'polish'),
        ('ENG', 'english'),
        ('DE', 'german')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique_for_date='publish')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='articles_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    language = models.CharField(max_length=15,
                                choices=LANGUAGE_CHOICES,
                                default='ENG')

    objects = ArticleManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


""" Maybe uncomment later. It will depend on requirements.
class Articles(models.Model):
    articlePL = models.ForeignKey(Article,
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  related_name='polish_article')
    articleENG = models.ForeignKey(Article,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='english_article')
    articleDE = models.ForeignKey(Article,
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  related_name='german_article')"""
