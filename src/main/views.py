from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


from .models import *
from .forms import *

# Create your views here.


def index(request):
    return HttpResponse("Server is up and running.")


def main(request):
    return render(request, 'Main.html')


def tournament(request, tournamentName):
    return render(request, 'tournament.html')


def drinks(request):
    if request.method == 'POST':
        newDrink = Drink.objects.get(name=request.POST.get('newDrink'))
        newOrder = Order()
        newOrder.user = request.user
        newOrder.drink = newDrink
        newOrder.location = request.POST.get('location')
        newOrder.specificInstructions = request.POST.get('instructions')
        newOrder.save()
        return render(request, 'orderConfirmation.html')

    else:
        orders = Order.objects.all()
        drinkList = Drink.objects.all()
        user = request.user.username
        return render(request, "drinks.html", {"orders": orders, "drinkList": drinkList, "user": user})


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
    context = {}
    context['current_balance'] = request.user.balance/100 if not request.user.is_anonymous else 0.00
    if not request.user.is_anonymous:
        context['transactions'] = Transaction.objects.filter(account=request.user)
    return render(request, 'bank.html', context)


def drinksEdit(request):
    if request.method == 'POST':
        if request.user.user_type != 4:
            return HttpResponse("Only managers can create or edit drinks.")

        addDrinkForm = addDrink(request.POST)
        if addDrinkForm.is_valid() and not request.POST.get('drink'):
            newDrink = Drink()
            newDrink.name = request.POST.get('name')
            newDrink.price = request.POST.get('price')
            newDrink.instructions = request.POST.get('instructions')
            newDrink.save()
        elif request.POST.get('deleteDrink'):
            drink = request.POST.get('deleteDrink')
            deleteDrink = Drink.objects.filter(name=drink)
            deleteDrink.delete()
        elif request.POST.get('drink') and request.POST.get('name') and request.POST.get('price') \
                and request.POST.get('instructions'):
            drink = request.POST.get('drink')
            editDrink = Drink.objects.filter(name=drink)
            editDrink.delete()
            newDrink = Drink()
            newDrink.name = request.POST.get('name')
            newDrink.price = request.POST.get('price')
            newDrink.instructions = request.POST.get('instructions')
            newDrink.save()
        return HttpResponseRedirect('#')

    else:
        drinkList = Drink.objects.all()
        addDrinkForm = addDrink()
    return render(request, 'drinkEdit.html', {'addDrinkForm': addDrinkForm, 'drinkList': drinkList})


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
    if request.method == "POST":
        if request.user.user_type != 3 and request.user.user_type != 4:
            return HttpResponse("Only Drink Meisters can deliver orders")
        order = Order.objects.get(id=request.POST.get('order'))
        order.delete()
        return HttpResponseRedirect('#')
    else:
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

def handler404(request, exception):
    return render(request, '404.html', {})
