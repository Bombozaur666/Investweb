from django.contrib import admin
from .models import Article, Comment


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'tags', 'publish', 'updated', 'status')
    list_filter = ('status', 'created', 'publish', 'author', 'language')
    search_fields = ('title', 'body', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'body', 'created', 'updated', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'email', 'body')


"""
Depends of models
@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('articlePL', 'articleENG', 'articleDE')
    search_fields = ('articlePL', 'articleENG', 'articleDE')
"""
