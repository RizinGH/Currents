from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import *
from django.contrib import messages
from django.contrib.auth import login


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


def login(request):
    return render(request, "currents_web/login.html")

def register(request):
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).count():
            messages.error(request, "Account with email already exists!!")
            return render(request, "currents_web/register.html")
        else:
            user = User(email, password)
            user.save()
            UserDetails(email=user, username=username).save()
            messages.success(request, "Registered Successfully")
            return render(request, "currents_web/register.html")

    #     form = RegistrationForm(request.POST['email'], request.POST['password'])
    #     if form.is_valid():
    #         user = form.save()
    #         login(request ,user)
    #         messages.success(request, "Sign-Up SuccessFull")
    #         return redirect("home")
    #     messages.error(request, "Sign-Up Failed")
    # form = RegistrationForm()

    return render(request = request, template_name="currents_web/register.html", context={})

def about(request):
    pass

def weather(request):
    pass

def dashboard(request):
    return render(request, "currents_web/dashboard.html")