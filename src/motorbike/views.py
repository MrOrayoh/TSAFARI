from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'motorbike/home.html')

def login(request):
    return render(request, 'motorbike/login.html')

def register(request):
    return render(request, 'motorbike/register.html')

def driver_dashboard(request):
    return render(request, 'motorbike/driver_dashboard.html')

def booking(request):
    return render(request, 'motorbike/booking.html')