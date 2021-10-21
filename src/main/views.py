from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.


def index(request):
    return HttpResponse("Server is up and running.")


def main(request):
    return render(request, 'Main.html')


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
    return render(request, "home.html")


def account(request):
    return render(request, "account.html")

def bank(request):
    return render(request, 'Bank.html')


def drinksEdit(request):
    return render(request, 'DrinkEdit.html')


def orderConfirmation(request):
    return render(request, 'OrderConfirmation.html')


def sponsor(request):
    return render(request, 'Sponsor.html')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'