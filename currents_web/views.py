from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def fy(request):
    return render(request, "fy.html")

def profile(request):
    return render(request, "profile.html")

def subscribe(request):
    return render(request, "subscribe.html")


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
    
def about(request):
    pass

def weather(request):
    pass

def dashboard(request):
    return render(request, "dashboard.html")