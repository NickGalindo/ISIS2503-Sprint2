from django.contrib import admin
from django.urls import path, include
from . import views

app_name="auth"
urlpatterns = [
    path('login', views.login, name='login'),
    path('test', views.test, name='test')
]
