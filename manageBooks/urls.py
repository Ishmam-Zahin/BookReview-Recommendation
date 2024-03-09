from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<id>/', views.showDetails, name="details"),
    path('getReviews/<id>/', views.getReviews, name="reviews"),
    path('postReview/<id>', views.postReview, name="postReview"),
]
