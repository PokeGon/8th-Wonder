from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    return HttpResponse("Server is up and running.")


def tournament(request):
    return render(request, 'tournament.html')


def drinks(request):
    return render(request, "drinks.html")


def login(request):
    return render(request, "login.html")


def logout(request):
    return render(request, "logout.html")


def error(request):
    return render(request, "error.html")


def accountCreation(request):
    return render(request, "accountCreation.html")

def home(request):
    return render(request,"home.html")

def account(request):
    return render(request,"account.html")
