from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from .forms import DriverRegistrationForm

def home(request):
    return render(request, 'motorbike/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # using email in place of "username" field
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
    return render(request, 'motorbike/driver_dashboard.html')

def booking(request):
    return render(request, 'motorbike/booking.html')

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
