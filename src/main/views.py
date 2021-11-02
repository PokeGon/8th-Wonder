from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import Sponsor, Order, Drinkmeister, Tournament, Manager
from .forms import addDrink, deleteDrink, editDrink

# Create your views here.


def index(request):
    return HttpResponse("Server is up and running.")


def main(request):
    return render(request, 'Main.html')


def tournament(request, tournamentName):
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
    return render(request, 'bank.html')


def drinksEdit(request):
    if request.method == 'POST':
        addDrinkForm = addDrink(request.POST)
        deleteDrinkForm = deleteDrink(request.POST)
        editDrinkForm = editDrink(request.POST)
        if addDrinkForm.is_valid() or deleteDrinkForm.is_valid() or editDrinkForm.is_valid():
            return HttpResponseRedirect('#')
    else:
        addDrinkForm = addDrink()
        deleteDrinkForm = deleteDrink()
        editDrinkForm = editDrink()
    return render(request, 'drinkEdit.html', {'addDrinkForm': addDrinkForm, 'deleteDrinkForm': deleteDrinkForm,
                                              'editDrinkForm': editDrinkForm})


def orderConfirmation(request):
    return render(request, 'orderConfirmation.html')


def sponsor(request):
    if request.method == "POST":
        if request.user.user_type != 2:
            return HttpResponse("Only sponsors can sponsor a tournament")
        for t in Tournament.objects.all():
            if str(t.date) == str(request.POST.get('date')):
                return HttpResponse("Error, there is already a tournament on this day!")
            if t.name == request.POST.get('tournamentName'):
                # Tournaments with almost identical names can still be created
                # including if the only difference is a space
                return HttpResponse("Error, there's already a Tournament by this name")
        newTournament = Tournament()
        newTournament.name = request.POST.get('tournamentName')
        newTournament.date = request.POST.get('date')
        newTournament.sponsor = request.user.sponsor
        newTournament.save()
        return HttpResponse("Success!")
    else:
        tournaments_list = Tournament.objects.all()
        context = {'tournaments_list': tournaments_list}
        return render(request, "sponsor.html", context)


def transfer(request):
    return render(request, 'transfer.html')


def drinkMeister(request):
    orderList = Order.objects.filter(served=False)
    return render(request, 'drinkMeister.html', {'orderList': orderList})


def events(request):
    tournaments_list = Tournament.objects.all()

    context = {'tournaments_list': tournaments_list}
    return render(request, "events.html", context)


def manager(request):
    return render(request, "manager.html")


def verification(request):
    sponsors_list = Sponsor.objects.all()
    drinkmeisters_list = Drinkmeister.objects.all()
    context = {'sponsors_list': sponsors_list, 'drinkmeisters_list':drinkmeisters_list}
    return render(request, "verification.html", context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'