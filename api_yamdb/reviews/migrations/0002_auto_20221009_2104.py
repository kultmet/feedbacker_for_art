# Generated by Django 2.2.16 on 2022-10-09 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genretotitle',
            old_name='title',
            new_name='title1',
        ),
    ]