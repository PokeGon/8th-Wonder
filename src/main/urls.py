from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournament', views.tournament, name='tournament'),
    path('error', views.error, name='error'),
    path('createAccount', views.accountCreation, name='accountCreation'),
    path('drinks', views.drinks, name='drinks'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('account', views.account, name='account'),
]
