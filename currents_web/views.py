from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login


def index(request):
    return render(request, "currents_web/base.html")

def home(request):
    return render(request, "currents_web/home.html")

def fy(request):
    return render(request, "currents_web/fy.html")

def profile(request):
    return render(request, "currents_web/profile.html")

def userLogin(request):
    return render(request, "currents_web/login.html")

def register(request):
    if request.method =="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request ,user)
            messages.success(request, "Sign-Up SuccessFull")
            return redirect("home")
        messages.error(request, "Sign-Up Failed")
    form = NewUserForm()
    return render(request = request, template_name="currents_web/register.html", context={"register_form":form})