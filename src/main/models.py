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

    def createTournament(self, name, date, sponsor, approved, completed):
        tournament = Tournament(name, date, sponsor, approved, completed)
        tournament.save()  # Saves class instance to the database

    def editTournament(self, tournament, name, date, sponsor, approved, completed):
        # If we don't want a particular class variable to change, we can just pass in None when calling editTournament()
        if name:
            tournament.name = name
        if date:
            tournament.date = date
        if sponsor:
            tournament.sponsor = sponsor
        if approved:
            tournament.approved = approved
        if completed:
            tournament.completed = completed
        tournament.save()

    def verifySponsor(self, sponsor):
        pass

    def verifyDrinkmeister(self, drinkmeister):
        pass

    def editDrink(self, drink, name, price, instructions):
        # If we don't want a particular class variable to change, we can just pass in None when calling editDrink()
        if name:
            drink.name = name
        if price:
            drink.price = price
        if instructions:
            drink.instructions = instructions
        drink.save()

    def addDrink(self, name, price, instructions):
        drink = Drink(name, price, instructions)
        drink.save()


class Player(models.Model):
    currentHole = models.IntegerField()
    score = models.IntegerField()
    hole = models.IntegerField()
    currentTournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def getHole(self):
        return self.currentHole

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def setHole(self, hole):
        self.hole = hole

    def joinTournament(self, tournament):
        self.currentTournament = tournament


class Sponsor(models.Model):
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField()

    def sponsorTournament(self):
        pass

class Order(models.Model):
    timeOrdered = models.TimeField(auto_now=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    served = models.BooleanField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class Drinkmeister(models.Model):
    employeeID = models.CharField(max_length=300)

    def makeAndDeliverOrder(self, order):
        pass

class Tournament(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateField()
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
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

