from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# NOTE: since we can't make variables private and still have Django work, we don't need to add getters and setters


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'player'),
        (2, 'sponsor'),
        (3, 'drinkMeister'),
        (4, 'manager'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.EmailField(max_length=80)
    bank = models.OneToOneField('BankAccount', on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    def orderDrink(self, name, qty, instructions):
        for i in range(qty):
            order = Order()
            order.timeOrdered = models.TimeField(auto_now=True)
            order.drink = name
            order.specificInstructions = instructions
            order.served = False
            order.user = self
            order.save()


class BankAccount(models.Model):
    balance = models.IntegerField()

    def addToBalance(self, amount):
        self.balance += amount
        self.save()


class Transaction(models.Model):
    date = models.DateField(auto_now=True)
    amount = models.IntegerField()
    account = models.ForeignKey(
        'BankAccount',
        models.SET_NULL,
        blank=True,
        null=True
    )


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    yearsWorked = models.IntegerField()
    mostMoneyHeld = models.IntegerField()
    drinksSold = models.IntegerField()
    totalTournamentsMade = models.IntegerField()

    @staticmethod
    def createTournament(name, startTime, endTime, sponsor, approved, completed):
        tournament = Tournament(name, startTime, endTime, sponsor, approved, completed)
        tournament.save()

    @staticmethod
    def editTournament(tournament, name, startTime, endTime, sponsor, approved, completed):
        tournament.name = name
        tournament.startTime = startTime
        tournament.endTime = endTime
        tournament.sponsor = sponsor
        tournament.approved = approved
        tournament.completed = completed
        tournament.save()

    @staticmethod
    def verifySponsor(sponsor):
        sponsor.canSponsorTournament = True
        sponsor.save()

    @staticmethod
    def verifyDrinkmeister(drinkmeister):
        drinkmeister.isAllowedToServeDrinks = True
        drinkmeister.save()

    @staticmethod
    def editDrink(drink, name, price, instructions):
        drink.name = name
        drink.price = price
        drink.instructions = instructions
        drink.save()

    @staticmethod
    def addDrink(name, price, instructions):
        drink = Drink(name, price, instructions)
        drink.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    currentHole = models.IntegerField()
    hole = models.IntegerField()
    currentTournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def joinTournament(self, tournament):
        self.currentTournament = tournament
        tournament.players.add(self)
        tournament.save()


class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField(default=False)

    def sponsorTournament(self, tournament):
        if self.canSponsorTournament:
            tournament.sponsors.add(self)
            tournament.save()
        else:
            return "You do not have authorization to sponsor tournaments"


class Drink(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    instructions = models.CharField(max_length=300)


class Order(models.Model):
    timeOrdered = models.TimeField(auto_now=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    specificInstructions = models.CharField(max_length=300)
    served = models.BooleanField(default=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class Drinkmeister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employeeID = models.CharField(max_length=300)
    isAllowedToServeDrinks = models.BooleanField(default=False)

    def makeAndDeliverOrder(self, order):
        if self.isAllowedToServeDrinks:
            order.served = True
            order.save()
        else:
            return "You do not have authorization to serve drinks."


class Tournament(models.Model):
    name = models.CharField(max_length=300)
    startTime = models.DateField()
    endTime = models.DateField()
    players = models.ManyToManyField('Player')
    sponsors = models.ManyToManyField('Sponsor')
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    @staticmethod
    def newGame(name, date, sponsor, approved, completed):
        tournament = Tournament(name, date, sponsor, approved, completed)
        tournament.save()


class Prize(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    amount = models.IntegerField()


class Score(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    amount = models.IntegerField()
