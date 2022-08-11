from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


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
    title = models.CharField(max_length=255,
                             null=False,
                             blank=False)
    slug = models.SlugField(max_length=255,
                            unique_for_date='publish')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='articles_posts',
                               null=False,
                               blank=False)

    body = models.TextField(null=False,
                            blank=False)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              null=False,
                              blank=False
                              )
    language = models.CharField(max_length=15,
                                choices=LANGUAGE_CHOICES,
                                default='ENG',
                                null=False,
                                blank=False)

    # tags by taggit
    tags = TaggableManager()
    # add new functions to custom manager
    objects = ArticleManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='commented_posts',
                                null=False,
                                blank=False)
    user = models.ForeignKey(User,
                             on_delete=models.SET('DELETED USER'),
                             related_name='user_comments',
                             null=False,
                             blank=False)
    body = models.TextField(null=False,
                            blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment added by {} for post {}.'.format(self.user, self.article)


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
