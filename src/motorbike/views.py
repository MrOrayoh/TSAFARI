from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
import json
from .forms import DriverRegistrationForm
from .models import Driver

def home(request):
    return render(request, 'motorbike/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # using email instead of "username"
        password = request.POST.get('password')

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            auth_login(request, user)
            return redirect('driver_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'motorbike/login.html')

def driver_dashboard(request):
    driver = request.user

    context = {
        'driver_name': getattr(driver, 'full_name', 'Not set'),
        'driver_phone': getattr(driver, 'phone', 'Not set'),
        'driver_sacco': getattr(driver, 'sacco', 'Not set'),
        'driver_stage': getattr(driver, 'stage', 'Not set'),
        'driver_rating': getattr(driver, 'rating', 'Not rated'),
        'is_available': driver.is_available,
        'rides_completed': 0,
        'earnings': 0.00,
        'pending_requests': 0,
    }

    return render(request, 'motorbike/driver_dashboard.html', context)

from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

def booking(request):
    location_query = request.GET.get('location', '')
    lat = request.GET.get('latitude')
    lng = request.GET.get('longitude')

    drivers = Driver.objects.filter(is_available=True, latitude__isnull=False, longitude__isnull=False)

    # Optional keyword filtering
    if location_query:
        drivers = drivers.filter(
            Q(stage__icontains=location_query) |
            Q(sacco__icontains=location_query)
        )

    # If GPS location provided, calculate distances
    if lat and lng:
        try:
            lat = float(lat)
            lng = float(lng)
            driver_list = []

            for driver in drivers:
                distance = haversine(lat, lng, driver.latitude, driver.longitude)
                driver_list.append((driver, round(distance, 2)))

            # Sort by nearest first
            driver_list.sort(key=lambda x: x[1])
            sorted_drivers = [{'driver': d, 'distance': dist} for d, dist in driver_list]
        except ValueError:
            sorted_drivers = [{'driver': d, 'distance': None} for d in drivers]
    else:
        sorted_drivers = [{'driver': d, 'distance': None} for d in drivers]

    return render(request, 'motorbike/booking.html', {
        'available_drivers': sorted_drivers
    })


def choose_trip(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    return render(request, 'motorbike/trip_booking.html', {
        'driver': driver
    })

def trip_booking(request):
    return render(request, 'motorbike/trip_booking.html')

def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            if hasattr(driver, 'set_password'):
                driver.set_password(form.cleaned_data['password'])
            else:
                driver.password = make_password(form.cleaned_data['password'])
            driver.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = DriverRegistrationForm()
    return render(request, 'motorbike/register.html', {'form': form})

def edit_account(request):
    return render(request, 'motorbike/edit_account.html')

def mini_statements(request):
    return render(request, 'motorbike/mini_statements.html')

# motorbike/views.py

@csrf_exempt
def toggle_availability(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            body = json.loads(request.body)
            driver = request.user

            new_status = body.get('is_available', not driver.is_available)
            latitude = body.get('latitude')
            longitude = body.get('longitude')

            driver.is_available = new_status
            if new_status and latitude and longitude:
                driver.latitude = latitude
                driver.longitude = longitude
            elif not new_status:
                driver.latitude = None
                driver.longitude = None

            driver.save()
            return JsonResponse({'status': 'success', 'is_available': driver.is_available})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'unauthorized'}, status=401)
