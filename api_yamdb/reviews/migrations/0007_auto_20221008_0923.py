# Generated by Django 2.2.16 on 2022-10-08 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_remove_title_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genretotitle',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='genretotitle',
            old_name='title_id',
            new_name='title',
        ),
    ]
