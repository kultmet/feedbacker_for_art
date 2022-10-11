from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'score', 'pub_date', 'text', 'author',)
    search_fields = ('title', 'score', 'pub_date')
    list_filter = ('title', 'score', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'pub_date', 'text', 'author',)
    search_fields = ('review', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
