import os
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from gnews import GNews
from datetime import date, datetime
import json
from decouple import config
import requests
from django.conf import settings

SCRAPED_NEWS_DIR = f"{settings.BASE_DIR}{os.path.sep}scraped_news"

# create scraped news dir
if not os.path.exists(SCRAPED_NEWS_DIR):
    os.mkdir(SCRAPED_NEWS_DIR)

news_file = os.path.join(SCRAPED_NEWS_DIR, f"{date.today()}_all_news.json")
# scrape news if not already done
if not os.path.exists(news_file):
    google_news = GNews(language='en', country='IN', period='7d', max_results=10)

    news_today = {
        'top_news': google_news.get_top_news(),
        'world': google_news.get_news_by_topic("WORLD"),
        'business': google_news.get_news_by_topic("BUSINESS"),
        'technology': google_news.get_news_by_topic("TECHNOLOGY"),
        'entertainment': google_news.get_news_by_topic("ENTERTAINMENT"),
        'sports': google_news.get_news_by_topic("SPORTS"),
        'science': google_news.get_news_by_topic("SCIENCE"),
    }

    # save to file
    with open(news_file, 'w') as outfile:
        json.dump(news_today, outfile)

else:
    with open(news_file, 'r') as infile:
        news_today = json.load(infile)

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
    params = {
        'subscribed': False
    }
    
    # check if subscribed
    if Subscription.objects.filter(user=request.user).first():
        params['subscribed'] = True


    categories = list(news_today.keys())
    
    params['categories'] = categories

    return render(request, "dashboard.html", params)

def profile(request):
    params = {
        'subscribed': False
    }
    
    # check if subscribed
    if Subscription.objects.filter(user=request.user).first():
        params['subscribed'] = True
    
    if request.method == "POST":
        # email = request.POST['email']
        username = request.POST['username']
        preference = request.POST.getlist('preference')

        UserDetails.objects.filter(user=request.user).update(username=username, userPreferences=preference)
        
    user_details = UserDetails.objects.filter(user=request.user).first()

    params['user_details'] = user_details
    
    return render(request, "profile.html", params)


def home(request):
    return render(request, "home.html")

def fy(request):
    # check if subscribed
    if not Subscription.objects.filter(user=request.user).first():
        return redirect('subscription')

    # if already subscibed
    if Subscription.objects.filter(user=request.user).first():
        preferences = UserDetails.objects.get(user = request.user).userPreferences
        preferences = preferences.strip('][').replace("'", "").replace(" ", "").split(',')

        fy_news = {
            'top_news': news_today['top_news']
        }
        for pref in preferences:
            fy_news[pref] = news_today[pref]


    params = {
        'subscribed': True,
        'news': fy_news,
    }

    return render(request, "fy.html", params)

def subscription(request):
    # if already subscibed
    if Subscription.objects.filter(user=request.user).first():
        return redirect('fy')
    
    return render(request, 'subscription.html')

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
    # check if subscribed
    if not Subscription.objects.filter(user=request.user).first():
        return redirect('subscription')
    
    lat = 12.9762
    lon = 77.6033
    ow_api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config('OW_API_KEY')}"
    # print(ow_api)
    resp = requests.get(ow_api)
    # print(resp.json())

    params = {
        'subscribed': True,
        'wjson': resp.json(), 
        'today': date.today(),
        'day': datetime.now().strftime('%A'),
    }
    return render(request, 'weather.html', params)
    

def metal_rates(request):
    # check if subscribed
    if not Subscription.objects.filter(user=request.user).first():
        return redirect('subscription')
    
    params = {
        'subscribed': True,
    }

    return render(request,'metal_rates.html', params)
   # metal_price_api = f"https://api.metalpriceapi.com/v1/latest?api_key={config('METAL_PRICE_API_KEY')}&base=INR"

   # resp = requests.get(metal_price_api)
   # return JsonResponse(resp.json())

def set_favourite(request):
    title = request.POST['title']
    url = request.POST['url']

    Favourites(user=request.user, title=title, url=url).save()

    return HttpResponse("success")

def favourites(request):
    # check if subscribed
    if not Subscription.objects.filter(user=request.user).first():
        return redirect('subscription')
    
    params = {
        'subscribed': True,
        'favourites': Favourites.objects.filter(user=request.user)
    }
    
    return render(request, 'favourites.html', params)

def view_news(request, category):
    params = {
        'subscribed': False
    }
    
    # check if subscribed
    if Subscription.objects.filter(user=request.user).first():
        params['subscribed'] = True


    params['news'] = news_today[category]
    params['category'] = category

    # print(params['news'])

    # print(params)
    return render(request, "view_news.html", params)