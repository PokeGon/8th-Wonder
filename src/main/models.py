from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
import datetime


# Create your models here.

# NOTE: since we can't make variables private and still have Django work, we don't need to add getters and setters


class TransactionManager(models.Manager):
    def create_transaction(self, amount, name):
        transaction = self.create(amount=amount, name=name)
        transaction.save()
        return transaction


class Transaction(models.Model):
    date = models.DateField(auto_now=True)
    name = models.TextField()
    amount = models.IntegerField()
    account = models.ForeignKey(
        'User',
        models.SET_NULL,
        blank=True,
        null=True
    )
    objects = TransactionManager()


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Player'),
        (2, 'Sponsor'),
        (3, 'Drinkmeister'),
        (4, 'Manager'),
    )

    user_type = models.PositiveSmallIntegerField(default=1, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    email = models.EmailField(max_length=80)
    date_joined = models.DateTimeField(auto_now_add=True)  # This only evaluates when User instance is first made!
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def addToBalance(self, amount, name):
        self.balance += amount
        Transaction.objects.create_transaction(amount, name)
        self.save()

    def orderDrink(self, name, qty, instructions):
        for i in range(qty):
            order = Order()
            order.timeOrdered = models.TimeField(auto_now=True)
            order.drink = name
            order.specificInstructions = instructions
            order.served = False
            order.user = self
            order.save()


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

    @staticmethod
    def newGame(name, date, sponsor, approved, completed):
        tournament = Tournament(name, date, sponsor, approved, completed)
        tournament.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    currentHole = models.IntegerField()
    hole = models.IntegerField()
    score = models.IntegerField(default=0)

    def joinTournament(self, tournament):
        tournament.players.add(self)
        tournament.save()


class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='sponsor')
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField(default=False)

    def sponsorTournament(self, tournament):
        if self.canSponsorTournament:
            tournament.sponsor.add(self)
            tournament.save()
        else:
            return "You do not have authorization to sponsor tournaments"


class Drink(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    price = models.IntegerField()
    instructions = models.CharField(max_length=300)


class Order(models.Model):
    timeOrdered = models.TimeField(auto_now=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    specificInstructions = models.CharField(max_length=300)
    served = models.BooleanField(default=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    location = models.IntegerField(default=0)


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
    name = models.CharField(max_length=300, primary_key=True, unique=True)
    date = models.DateField(unique=True)
    startTime = models.TimeField(default=datetime.time(7, 00))
    endTime = models.TimeField(default=datetime.time(16, 30))
    players = models.ManyToManyField('Player', blank=True)
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "Tournament: " + str(self.name) + " " + str(self.date)



class Prize(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    amount = models.IntegerField()

