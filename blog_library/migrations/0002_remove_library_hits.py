# Generated by Django 3.2.8 on 2022-01-10 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='hits',
        ),
    ]
