# Generated by Django 5.0.3 on 2024-03-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageBooks', '0006_recentlyviewedbooks_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]