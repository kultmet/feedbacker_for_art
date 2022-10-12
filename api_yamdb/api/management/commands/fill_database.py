import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Genre, GenreToTitle,
    Title, Review, Comment)
from users.models import User


class Command(BaseCommand):
    """Команда для загрузки csv файлов в базу данных:
     python manage.py fill_database """

    help = 'Загрузка информации из csv файлов в базу данных'

    def fill_user(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/users.csv'),
                  'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    )

    def fill_category(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/category.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Category.objects.get_or_create(
                        id=row[0], name=row[1], slug=row[2]
                    )

    def fill_genre(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/genre.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Genre.objects.get_or_create(
                        id=row[0], name=row[1], slug=row[2]
                    )

    def fill_titles(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/titles.csv'),
                  'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Title.objects.get_or_create(
                        id=row[0], name=row[1], year=row[2], category_id=row[3]
                    )

    def fill_genre_title(self):
        with open(
                os.path.join(settings.BASE_DIR, 'static/data/genre_title.csv'),
                'r',
                encoding='utf-8'
        ) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    GenreToTitle.objects.get_or_create(
                        id=row[0], title_id=row[1], genre_id=row[2]
                    )

    def fill_review(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/review.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.get_or_create(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        score=row[4],
                        pub_date=row[5]
                    )

    def fill_comments(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/comments.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Comment.objects.get_or_create(
                        id=row[0],
                        review_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        pub_date=row[4]
                    )

    def handle(self, *args, **options):
        self.fill_user()
        self.fill_category()
        self.fill_genre()
        self.fill_titles()
        self.fill_genre_title()
        self.fill_review()
        self.fill_comments()
