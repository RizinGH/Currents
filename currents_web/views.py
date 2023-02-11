from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "currents_web/base.html")

def home(request):
    return render(request, "currents_web/home.html")

def fy(request):
    return render(request, "currents_web/fy.html")


def profile(request):
    return render(request, "currents_web/profile.html")