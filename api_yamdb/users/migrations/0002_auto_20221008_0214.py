# Generated by Django 2.2.16 on 2022-10-07 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[(1, 'user'), (2, 'moderator'), (3, 'admin')], default='user', max_length=20),
        ),
    ]
