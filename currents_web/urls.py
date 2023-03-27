from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fy', views.fy, name='fy'),
    path('profile', views.profile, name='profile'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('weather', views.weather, name='weather'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('subscribe',views.subscribe,name='subscribe'),
    path('about',views.about,name='about'),

]
