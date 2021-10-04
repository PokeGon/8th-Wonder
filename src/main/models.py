from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    bank = models.OneToOneField('BankAccount', on_delete=models.CASCADE)

class User(models.Model):
    accountInfo = models.OneToOneField(Account, on_delete=models.CASCADE)

class BankAccount(models.Model):
    balance = models.IntegerField()

class Transaction(models.Model):
    date = models.DateField(auto_now=True)
    amount = models.IntegerField()
    account = models.ForeignKey(
        'BankAccount',
        models.SET_NULL,
        blank=True,
        null=True
    )

class Drink(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    instructions = models.CharField(max_length=300)

class Manager(models.Model):
    yearsWorked = models.IntegerField()
    mostMoneyHeld = models.IntegerField()
    drinksSold = models.IntegerField()
    totalTournamentsMade = models.IntegerField()

    def createTournament():
        pass

    def editTournament(tournament):
        pass

    def verifySponsor(sponsor):
        pass

    def verifyDrinkmeister(drinkmeister):
        pass

    def editDrink(drink):
        pass

    def addDrink():
        pass


class Player(models.Model):
    currentHole = models.IntegerField()
    currentTournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def getHole():
        pass

    def getScore():
        pass

    def setScore() :
        pass

    def setHole():
        pass

    def joinTournament(tournament):
        pass


class Sponsor(models.Model):
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField()

    def sponsorTournament():
        pass

class Order(models.Model):
    timeOrdered = models.TimeField(auto_now=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    served = models.BooleanField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class Drinkmeister(models.Model):
    employeeID = models.CharField(max_length=300)

    def makeAndDeliverOrder(order):
        pass

class Tournament(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateField()
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
    approved = models.BooleanField()
    completed = models.BooleanField()

    def newGame(name, date):
        pass

class Prize(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    amount = models.IntegerField()

class Score(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    amount = models.IntegerField()

