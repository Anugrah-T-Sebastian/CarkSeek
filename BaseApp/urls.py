from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('search/',views.searchPage, name='search'),
    path('layout/',views.layout),
    

    path('profile/<str:pk>', views.userProfile, name="user-profile"),

    path('car-details/<str:pk>', views.carDetailsPage, name="car-details"),
    path('car-details-upload', views.uploadCarDetails, name='car-details-upload'),
]