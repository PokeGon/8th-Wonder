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
