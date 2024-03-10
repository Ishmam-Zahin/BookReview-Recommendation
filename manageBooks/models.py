from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Books(models.Model):
    bookId = models.CharField(max_length = 100)
    totalViews = models.IntegerField(default = 0)
    totalRatingCount = models.IntegerField(default = 0)
    rating = models.FloatField(default = 0)

class UserViewedBooks(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Books, on_delete = models.CASCADE)

class Reviews(models.Model):
    message = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Books, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now = True)

class RecentlyViewedBooks(models.Model):
    time = models.DateTimeField(auto_now = True)
    bookId = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

class Ratings(models.Model):
    rate = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Books, on_delete = models.CASCADE)