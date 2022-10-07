import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Genre, Title, Review, Comment


class Command(BaseCommand):
    """Команда для загрузки csv файлов в базу данных python:
     manage.py fill_database"""

    help = 'Загрузка информации из csv файлов в базу данных'

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'static/data/category.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], name=row[1], slug=row[2])

        with open(os.path.join(settings.BASE_DIR, 'static/data/comments.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], review_id=row[1],
                                          text=row[2], author=row[3],
                                          pub_date=row[4])

        with open(os.path.join(settings.BASE_DIR, 'static/data/genre.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], name=row[1], slug=row[2])

        with open(os.path.join(settings.BASE_DIR, 'static/data/genre_title.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], name=row[1], slug=row[2])

        with open(os.path.join(settings.BASE_DIR, 'static/data/review.csv'),
                  'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], title_id=row[1],
                                          text=row[2], author=row[3],
                                          score=row[4], pub_date=row[5])

        with open(os.path.join(settings.BASE_DIR, 'static/data/titles.csv'),
                  'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], name=row[1],
                                          year=row[2], category=row[3])

        with open(os.path.join(settings.BASE_DIR, 'static/data/users.csv'),
                  'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] != 'id':
                    Review.objects.create(id=row[0], username=row[1],
                                          email=row[2], role=row[3],
                                          bio=row[4], first_name=row[5],
                                          last_name=row[6])
