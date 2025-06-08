from django.urls import path
from .views import home, login, driver_dashboard, booking, trip_booking, register_driver

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('driver_dashboard/', driver_dashboard, name='driver_dashboard'),
    path('booking/', booking, name='booking'),
    path('trip_booking/', trip_booking, name='trip_booking'),
    path('register/', register_driver, name='register_driver'),
]
