from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def index(request):
    return render(request, "currents_web/index.html")

def home(request):
    return render(request, "currents_web/home.html")

def fy(request):
    return render(request, "currents_web/fy.html")

def profile(request):
    return render(request, "currents_web/profile.html")

def subscribe(request):
    return render(request, "currents_web/subscribe.html")


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
                return render(request, 'currents_web/login.html')
         
    return render(request, "currents_web/login.html")

def userLogout(request):
    logout(request)
    return redirect('login')
    
    
def register(request):
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])

        if User.objects.filter(email=email).count():
            messages.error(request, "Account with email already exists!!")
            return render(request, "currents_web/register.html")
        else:
            user = User(email, password)
            user.save()
            UserDetails(user=user, username=username).save()
            messages.success(request, "Registered Successfully")
            return render(request, "currents_web/register.html")

    return render(request = request, template_name="currents_web/register.html", context={})

def about(request):
    pass

def weather(request):
    pass

def dashboard(request):
    return render(request, "currents_web/dashboard.html")