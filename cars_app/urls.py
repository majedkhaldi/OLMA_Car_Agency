from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('cars', views.cars_page),
    path('loginpage', views.login_page),
    path('login', views.login),
    path('registerpage', views.register_page),
    path('register', views.register),
    path('cars', views.cars_page),
