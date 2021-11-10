from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import *
from .forms import *


# Create your views here.


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
        if request.user.is_anonymous:
            return HttpResponseRedirect('../login')
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
    return render(request, "index.html")


def homeRedirect(request):
    return redirect('home')


def account(request):
    return render(request, "account.html")


def bank(request):
    context = {}
    context['current_balance'] = request.user.balance / 100 if not request.user.is_anonymous else 0.00
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
        if request.user.is_anonymous:
            return HttpResponseRedirect('../login')
        drinkList = Drink.objects.all()
        addDrinkForm = addDrink()
        return render(request, 'drinkEdit.html', {'addDrinkForm': addDrinkForm, 'drinkList': drinkList})


def orderConfirmation(request):
    return render(request, 'orderConfirmation.html')


def createAccount(request):
    if request.method == "POST":
        for u in User.objects.all():
            if u.username == request.POST.get('username'):
                return HttpResponse("Error, There is already a User with this name")
        newUser = User()
        newUser.username = request.POST.get('username')
        newUser.first_name = request.POST.get('firstName')
        newUser.last_name = request.POST.get('lastName')
        newUser.email = request.POST.get('email')
        newUser.password = request.POST.get('password')
        newUser.phone_number = request.POST.get('phoneNumber')
        newUser.user_type = request.POST.get('userType')
        createUser = User.objects.create_user(newUser.username, newUser.email, newUser.password)
        createUser.first_name = newUser.first_name
        createUser.last_name = newUser.last_name
        createUser.phone_number = newUser.phone_number
        createUser.user_type = newUser.user_type
        createUser.save()

        if createUser.user_type == "1":
            newPlayer = Player()
            newPlayer.user = createUser
            newPlayer.hole = 0
            newPlayer.currentHole = 0
            newPlayer.save()

        if createUser.user_type == "2":
            newSponsor = Sponsor()
            newSponsor.user = createUser
            newSponsor.companyName = ""
            newSponsor.canSponsorTournament = False
            newSponsor.save()

        if createUser.user_type == "3":
            newDrinkmeister = Drinkmeister()
            newDrinkmeister.user = createUser
            newDrinkmeister.isAllowedToServeDrinks = False
            newDrinkmeister.save()

        if createUser.user_type == "4":
            newManger = Manager()
            newManger.user = createUser
            newManger.yearsWorked = 0
            newManger.mostMoneyHeld = 0
            newManger.drinksSold = 0
            newManger.totalTournamentsMade = 0
            newManger.save()

        return HttpResponseRedirect('login')


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
        return HttpResponse("Success for " + str(request.user.sponsor))
    else:
        if request.user.is_anonymous:
            return HttpResponseRedirect('../login')
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
        if request.user.is_anonymous:
            return HttpResponseRedirect('../login')
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
    context = {'sponsors_list': sponsors_list, 'drinkmeisters_list': drinkmeisters_list}
    return render(request, "verification.html", context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'


def handler404(request, exception):
    return render(request, '404.html', {})
