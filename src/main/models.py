from django.db import models

# Create your models here.

# NOTE: since we can't make variables private and still have Django work, we don't need to add getters and setters


class User(models.Model):
    accountInfo = models.OneToOneField('Account', on_delete=models.CASCADE)
    account = models.ForeignKey(
        'BankAccount',
        models.SET_NULL,
        blank=True,
        null=True
    )

    def orderDrink(self, name, qty, instructions):
        for i in range(qty):
            order = Order()
            order.timeOrdered = models.TimeField(auto_now=True)
            order.drink = name
            order.specificInstructions = instructions
            order.served = False
            order.user = self
            order.save()


class Account(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    bank = models.OneToOneField('BankAccount', on_delete=models.CASCADE)


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


class Manager(models.Model, User):
    yearsWorked = models.IntegerField()
    mostMoneyHeld = models.IntegerField()
    drinksSold = models.IntegerField()
    totalTournamentsMade = models.IntegerField()

    def createTournament(self, name, startTime, endTime, sponsor, approved, completed):
        tournament = Tournament(name, startTime, endTime, sponsor, approved, completed)
        tournament.save()

    def editTournament(self, tournament, name, startTime, endTime, sponsor, approved, completed):
        tournament.name = name
        tournament.startTime = startTime
        tournament.endTime = endTime
        tournament.sponsor = sponsor
        tournament.approved = approved
        tournament.completed = completed
        tournament.save()

    def verifySponsor(self, sponsor):
        sponsor.canSponsorTournament = True
        sponsor.save()

    def verifyDrinkmeister(self, drinkmeister):
        drinkmeister.isAllowedToServeDrinks = True
        drinkmeister.save()

    def editDrink(self, drink, name, price, instructions):
        drink.name = name
        drink.price = price
        drink.instructions = instructions
        drink.save()

    def addDrink(self, name, price, instructions):
        drink = Drink(name, price, instructions)
        drink.save()


class Player(models.Model, User):
    currentHole = models.IntegerField()
    score = models.IntegerField()
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


class Sponsor(models.Model, User):
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField()

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
    served = models.BooleanField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Drinkmeister(models.Model, User):
    employeeID = models.CharField(max_length=300)
    isAllowedToServeDrinks = models.BooleanField()

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
    players = models.ManyToManyField('Player', on_delete=models.CASCADE)
    sponsors = models.ManyToManyField('Sponsor', on_delete=models.CASCADE)
    approved = models.BooleanField()
    completed = models.BooleanField()

    def newGame(self, name, date, sponsor, approved, completed):
        tournament = Tournament(name, date, sponsor, approved, completed)
        tournament.save()


class Prize(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    amount = models.IntegerField()


class Score(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    amount = models.IntegerField()
