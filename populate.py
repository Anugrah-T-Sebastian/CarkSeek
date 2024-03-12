# populate_cars.py
import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings  # Import Django settings module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarSeek.settings')
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from faker import Faker
from BaseApp.models import Car, UnavailableDate
from django.core.files import File
from pathlib import Path

fake = Faker('en_GB')  # Set the locale to en_GB for UK-specific data

def create_dummy_user():
    user_model = get_user_model()
    return user_model.objects.create(
        username=fake.user_name(),
        password="password123",
        user_type='dealer',
        drivers_license=fake.random_int(min=1000000000000000, max=9999999999999999)
    )

def create_dummy_car(posted_by, car_brand, car_model, car_image_path):
    car = Car.objects.create(
        brand=car_brand,
        posted_by=posted_by,
        model=car_model,
        rental_rate_per_day=fake.random.uniform(20, 100),
        location=fake.postcode(),
        image = car_image_path
    )

    return car

def get_all_files_in_folder(folder_path):
    file_list = []

    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # folder_name = os.path.basename(root)
            
            file_list.append(file)

    return file_list

def main():
    # Create 10 dummy users
    folder_path = "./media/car_images"
    file_names = os.listdir(folder_path)

    # Ensure there are enough files for the required number of users
    if len(file_names) < 10:
        print("Error: Not enough files in the specified folder.")
        return

    # Randomly select 10 unique file names
    # writed_files = []
    # for i in range(500):
    #     selected_file_names = fake.random.sample(file_names, 10)

    unique_cars = []
    for file_name in file_names:
        # if file_name in writed_files:
        #     continue
        substrings = file_name.split('_')
        brand = substrings[0].lower()
        model = substrings[1].lower()
        # user = create_dummy_user()
        # create_dummy_car(user, brand, model, 'car_images/' + file_name)
        # writed_files.append(file_name)
        car = brand + " " + model
        unique_cars.append(car.strip())
        
    unique_cars = list(set(unique_cars))
    for i in unique_cars:
        print(i)

if __name__ == '__main__':
    main()
