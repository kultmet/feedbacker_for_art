
from email.policy import default
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Genre(models.Model):
    """Модель для работы с жанрами"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Конвертер пути',
        help_text='Введите данные типа slug'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title


class Category(models.Model):
    """Модель для работы с категориями"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Конвертер пути',
        help_text='Введите данные типа slug'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    year = models.IntegerField(default=1)# если это поле требует год, то это дотжен быть DateField
    # если это int и это поле обязательное, значит нужно указать заначение по дефолту
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ForeignKey(
        Genre,
        # through='GenreToTitle',
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Модель связывающая произведение с жанром"""
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        default=5,# нужен дефолт если это обязательное поле
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Введите целое число от 1 до 10'),
            MaxValueValidator(10, 'Введите целое число от 1 до 10')
        ]
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['pub_date']
