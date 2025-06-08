from django.urls import path
from .views import home, login, register, driver_dashboard, booking, trip_booking

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('driver_dashboard/', driver_dashboard, name='driver_dashboard'),
    path('booking/', booking, name='booking'),
    path('trip_booking/', trip_booking, name='trip_booking'),
]
