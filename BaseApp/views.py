from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.models import User

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

import markdown2


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

# USER-PROFILE PAGES
def userProfile(request):

    context = {'page':'index'}
    return render(request, 'BaseApp/user_index.html', context)

def userAbout(request):
    context = {'page':'about'}
    return render(request, 'BaseApp/user_about.html', context)

def userHistory(request):
    context = {'page':'history'}
    return render(request, 'BaseApp/user_history.html', context)

def userContact(request):
    context = {'page':'contact'}
    return render(request, 'BaseApp/user_contact.html', context)

def userChatbox(request):
    context = {'page':'chatbox'}
    return render(request, 'BaseApp/user_chatbox.html', context)

# SEARCH PAGE
def get_car_models(vehicle_type):
    suv_models = ['Fortuner', 'Sportage', 'BRV', 'Vitara', 'Prado', 'Land Cruiser']
    sedan_models = ['Axio', 'Grace', 'Premio', 'Civic', 'City', 'Corolla', 'Prius']
    roadster_models = ['S2000']  # Assuming S2000 is the intended roadster
    
    if vehicle_type.lower() == 'suv':
        return suv_models
    elif vehicle_type.lower() == 'sedan':
        return sedan_models
    elif vehicle_type.lower() == 'roadster':
        return roadster_models
    else:
        return "Invalid vehicle type"

def searchPage(request):
    if request.method == 'POST':
        search_input = request.POST.get('search-input')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        rate = request.POST.get('rate')
        postcode = request.POST.get('postcode')

        filter_conditions = Q(location__icontains=postcode)
        search_input_values = search_input.split()
        for value in search_input_values:
            filter_conditions &= Q(brand__icontains=value) | Q(model__icontains=value)
        if rate:
            filter_conditions &= Q(rental_rate_per_day__lt=rate)
        if start_date and end_date:
            filter_conditions &= ~Q(unavailable_dates__date__range=[start_date, end_date])

        cars = Car.objects.filter(filter_conditions)
        context = {'cars': cars}
        return render(request, "search.html", context)
    
    param_value = request.GET.get('cartype')
    if param_value:
        car_models = get_car_models(param_value)
        filter_conditions = Q()
        for car_model in car_models:
            filter_conditions |= Q(brand__icontains=car_model) | Q(model__icontains=car_model)
        cars = Car.objects.filter(filter_conditions)
    else:
        cars = Car.objects.all()
    context = {'page':'search','cars':cars}
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

def generate_pdf(request):
    # Replace 'path/to/your/markdown/file.md' with the actual path to your Markdown file
    markdown_file_path = './ContractTemplate.md'

    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="markdown_to_pdf.pdf"'

    # Create the PDF object
    pdf_buffer = HttpResponse(content_type='application/pdf')
    pdf_buffer['Content-Disposition'] = 'filename="markdown_to_pdf.pdf"'
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Create a style sheet
    styles = getSampleStyleSheet()

    # Create a Paragraph with the HTML content
    html_paragraph = Paragraph(html_content, styles["BodyText"])

    # Build the PDF document
    doc.build([html_paragraph])

    # Get the value of the BytesIO buffer and write it to the response
    pdf_value = pdf_buffer.getvalue()
    response.write(pdf_value)

    return response
