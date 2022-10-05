from django.contrib import admin

from .models import (Review, Comment, Title)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    search_fields = ('name', )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'score', 'pub_date', 'text', 'author', )
    search_fields = ('title', 'score', 'pub_date')
    list_filter = ('score', 'title', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'pub_date', 'text', 'author', )
    search_fields = ('review', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'



