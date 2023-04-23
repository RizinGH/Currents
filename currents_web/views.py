import os
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from gnews import GNews
from datetime import date
import json
from decouple import config
import requests

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, "index.html")

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method =="POST":
            email = request.POST.get('email') 
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Email/Password')
                return render(request, 'login.html')
         
    return render(request, "login.html")

def userLogout(request):
    logout(request)
    return redirect('index')
    
    
def register(request):
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])

        if User.objects.filter(email=email).count():
            messages.error(request, "Account with email already exists!!")
            return render(request, "register.html")
        else:
            user = User(email, password)
            user.save()
            UserDetails(user=user, username=username).save()
            messages.success(request, "Registered Successfully")
            return render(request, "register.html")

    return render(request = request, template_name="register.html", context={})

@login_required(login_url='login')
def change_password(request):
    new_password = None
    confirm_password = 'x'
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
    if new_password != confirm_password:
        return render(request,'change_password.html')
    else:
        # user = User.objects.get(email=request.POST['email'])
        # user.password = new_password
        User.objects.filter(email=request.POST['email']).update(password=make_password(new_password))

        return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    news_file = f"{date.today()}_all_news.json"

    if not os.path.exists(news_file):
        google_news = GNews(language='en', country='IN', period='7d', max_results=5)

        news = {
            'top_news': google_news.get_top_news(),
            'world_news': google_news.get_news_by_topic("WORLD"),
            'business': google_news.get_news_by_topic("BUSINESS"),
            'technology': google_news.get_news_by_topic("TECHNOLOGY"),
            'entertainment': google_news.get_news_by_topic("ENTERTAINMENT"),
            'sports': google_news.get_news_by_topic("SPORTS"),
            'science': google_news.get_news_by_topic("SCIENCE"),
        }

        with open(news_file, 'w') as outfile:
            json.dump(news, outfile)
    else:
        with open(news_file, 'r') as infile:
            news = json.load(infile)

    return render(request, "dashboard.html", {"news": news})

def profile(request):
    
    if request.method == "POST":
        # email = request.POST['email']
        username = request.POST['username']
        preference = request.POST.getlist('preference')

        UserDetails.objects.filter(user=request.user).update(username=username, userPreferences=preference)
        
    user_details = UserDetails.objects.filter(user=request.user).first()
    
    return render(request, "profile.html", {'user_details': user_details})


def home(request):
    return render(request, "home.html")

def fy(request):
    # if already subscibed
    if Subscription.objects.filter(user=request.user).first():
        preferences = UserDetails.objects.get(user = request.user).userPreferences
        preferences = preferences.strip('][').replace("'", "").replace(" ", "").split(',')

        news_file = f"{date.today()}_{request.user}_all_news.json"

        if not os.path.exists(news_file):
            google_news = GNews(language='en', country='IN', period='7d', max_results=5)
            news = {
                'top_news': google_news.get_top_news(),
            }
            for category in preferences:
                news[category] = google_news.get_news_by_topic(category)
            
            with open(news_file, 'w') as outfile:
                json.dump(news, outfile)
        
        else:
            with open(news_file, 'r') as infile:
                news = json.load(infile)

        return render(request, "fy.html", {'news': news})

    return render(request, "fy.html")

def subscribe(request):
    # if already subscibed
    if Subscription.objects.filter(user=request.user).first():
        return redirect('fy')
    
    if request.method == 'POST':
        Subscription(user = request.user, date = date.today(), amount = 199, payment_mode='card').save()
        return render(request, "subscribe.html", {'msg': 'success'})
    return render(request, "subscribe.html")

def about(request):
    return render(request, "about.html")

def weather(request):
    lat = 12.9716
    lon = 77.5946
    ow_api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config('OW_API_KEY')}"

    print(ow_api)
    resp = requests.get(ow_api)
    print(resp.json())

    return render(request, 'weather.html')

