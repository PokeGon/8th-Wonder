from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/', views.tournament, name='tournament'),
    path('error/', views.error, name='error'),
    path('createAccount/', views.accountCreation, name='accountCreation'),
    path('drinks/', views.drinks, name='drinks'),
    path('home/', views.home, name='home'),
    path('bank/', views.bank, name='bank'),
    path('editDrinks/', views.drinksEdit, name='editDrinks'),
    path('orderConfirmation/', views.orderConfirmation, name='orderConfirmation'),
    path('sponsor/', views.sponsor, name='sponsor'),
    path('transfer/', views.transfer, name='transfer'),
    path('account/', views.ProfileView.as_view(), name='account'),
    path('drinkMeister', views.drinkMeister, name='drinkMeister'),
    path('events', views.events, name='events'),
    path('manager', views.manager, name='manager'),

    # Django Auth
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
]
