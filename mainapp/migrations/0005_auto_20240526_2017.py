# Generated by Django 3.2.21 on 2024-05-26 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_issuedbook_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listOfBook',
        ),
        migrations.RemoveField(
            model_name='user',
            name='numOfBook',
        ),
    ]
