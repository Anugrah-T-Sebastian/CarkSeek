from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('search/',views.searchPage, name='search'),
    path('layout/',views.layout),
   

    path('profile', views.userProfile, name="user-profile"),
    path('profile/about', views.userAbout, name="user-about"),
    path('profile/history', views.userHistory, name="user-history"),
    path('profile/damagereport', views.userContact, name="user-damage-report"),
    path('profile/chatbox', views.userChatbox, name="user-chatbox"),
    path('car-details/<str:pk>', views.carDetailsPage, name="car-details"),
    path('car-details-upload', views.uploadCarDetails, name='car-details-upload'),
    path('generate-pdf/<str:pk>', views.generate_pdf, name='generate_pdf'),
]