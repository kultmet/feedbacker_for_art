from django.contrib import admin


from .models import Category, Genre, Title, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    search_fields = ('name', )
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
    list_display = ('pk', 'title', 'pub_date', 'text', 'author', ) #'score',
    search_fields = ('title', 'pub_date')   #'score',
    list_filter = ('title', 'pub_date') #'score',
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'pub_date', 'text', 'author', )
    search_fields = ('review', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
