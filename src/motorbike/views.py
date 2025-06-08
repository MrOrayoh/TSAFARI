from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import DriverRegistrationForm

def home(request):
    return render(request, 'motorbike/home.html')

def login(request):
    return render(request, 'motorbike/login.html')

def driver_dashboard(request):
    return render(request, 'motorbike/driver_dashboard.html')

def booking(request):
    return render(request, 'motorbike/booking.html')

def trip_booking(request):
    return render(request, 'motorbike/trip_booking.html')

# ✅ The ONLY register view you need:
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
