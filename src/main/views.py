from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from src.main.models import Tournament


def index(request):
    return HttpResponse("Server is up and running.")


def tournament(request):
    # currentTournament = Tournament.objects.cantremember
    # context = {'currentTournament': currentTournament}
    context = {}
    return render(request, 'tournament', context)


def accountInformation(request):
    return render(request, 'Account Information')


def bank(request):
    return render(request, 'Bank')


def drinksEdit(request):
    return render(request, 'Drinks Edit')


def orderConfirmation(request):
    return render(request, 'Order Confirmation')


def sponsor(request):
    return render(request, 'Sponsor')
