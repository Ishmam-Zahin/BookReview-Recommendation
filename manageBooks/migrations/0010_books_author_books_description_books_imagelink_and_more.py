# Generated by Django 5.0.3 on 2024-03-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageBooks', '0009_alter_books_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='author',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='imageLink',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='publishDate',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='publisher',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='title',
            field=models.TextField(null=True),
        ),
    ]