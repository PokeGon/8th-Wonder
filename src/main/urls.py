from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/tournament', views.tournament, name='tournament'),
    path('/accountInfo', views.accountInformation, name='Account Information'),
    path('/bank', views.bank, name='Bank'),
    path('/editDrinks', views.drinksEdit, name='Drinks Edit'),
    path('/orderConfirmation', views.orderConfirmation, name='Order Confirmation'),
    path('/sponsor', views.sponsor, name='Sponsor'),
]
