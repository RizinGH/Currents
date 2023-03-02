from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('fy', views.fy, name='fy'),
    path('profile', views.profile, name='profile'),
    path('login', views.userLogin, name='userLogin'),
    path('register', views.register, name='register'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)