from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "currents_web/base.html")
