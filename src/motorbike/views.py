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

def booking(request):
    location_query = request.GET.get('location', '')
    available_drivers = []

    if location_query:
        available_drivers = Driver.objects.filter(
            Q(is_available=True),
            Q(stage__icontains=location_query) |
            Q(sacco__icontains=location_query)
        )
    else:
        available_drivers = Driver.objects.filter(is_available=True)

    return render(request, 'motorbike/booking.html', {
        'available_drivers': available_drivers
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

@csrf_exempt
def toggle_availability(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            body = json.loads(request.body)
            driver = request.user
            driver.is_available = not driver.is_available
            driver.save()
            return JsonResponse({'status': 'success', 'is_available': driver.is_available})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'unauthorized'}, status=401)
