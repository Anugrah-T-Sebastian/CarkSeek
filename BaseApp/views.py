from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from django.contrib.auth.models import User

from .models import Car
from .forms import CarSeekUserCreationForm, CarDetailsUploadForm


def layout(request):
    return render(request, "layout.html")

# HOME PAGE VIEWS
def home(request):
    print("Home test")
    context = {}
    return render(request, 'BaseApp/home.html', context)


# LOGIN/RGISTER PAGE VIEWS
def loginPage(request):
    page = 'login'
    print("Login test")
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method ==  'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            print("USER:",username)
            user = User.objects.get(username=username)
        except:
            # messages.error(request, 'User does not exist')
            print('User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # messages.error(request, 'Username OR password does not exist')
            print('Username OR password does not exist')

    context = {'page': page}
    return render(request, 'BaseApp/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    if request.method == 'POST':
        form = CarSeekUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home or any desired page after registration
    else:
        form = CarSeekUserCreationForm()
    context = {'form':form}
    return render(request, 'BaseApp/register.html', context)

# USER-PROFILE PAGE
def userProfile(request, pk):

    context = {'pk':pk}
    return render(request, 'BaseApp/profile.html', context)

# SEARCH PAGE
def searchPage(request):
    if request.method == 'POST':
        search_input = request.POST.get('search-input')
        start_date = request.POST.get('start-date')
        start_time = request.POST.get('start-time')
        end_date = request.POST.get('end-date')
        end_time = request.POST.get('end-time')

        filter_conditions = Q(brand__icontains=search_input) | Q(model__icontains=search_input)
        if start_date and end_date:
            filter_conditions &= ~Q(unavailable_dates__date__range=[start_date, end_date])

        cars = Car.objects.filter(filter_conditions)
        context = {'cars': cars}
        return render(request, "search.html", context)
        
    cars = Car.objects.all()
    context = {'cars':cars}
    return render(request, "search.html", context)

# CAR PAGES
def carDetailsPage(request, pk):
    car = Car.objects.get(id=pk)

    context = {'car':car}
    return render(request, 'BaseApp/car_details.html', context)


def uploadCarDetails(request):
    if request.method == 'POST':
        form = CarDetailsUploadForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.posted_by = request.user
            car.save()
            return redirect('home')  # Redirect to success page or another URL
    else:
        form = CarDetailsUploadForm()

    return render(request, 'car_create.html', {'form': form})