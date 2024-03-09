from django.urls import path
from . import views

urlpatterns = [
    path('loginUser/', views.loginUser, name="login"),
    path('registerUser/', views.registerUser, name="register"),
]
