from django.urls import path
from . import views

urlpatterns = [
    path('searchBooks/', views.searchBooks, name="searchBooks"),
]
