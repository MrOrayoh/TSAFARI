from django.urls import path
from .views import home, login, driver_dashboard, booking, trip_booking, register_driver, edit_account, mini_statements, choose_trip, toggle_availability

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('driver_dashboard/', driver_dashboard, name='driver_dashboard'),
    path('booking/', booking, name='booking'),
    path('trip_booking/', trip_booking, name='trip_booking'),
    path('choose_trip/<int:driver_id>/',choose_trip, name='choose_trip'),
    path('register/', register_driver, name='register_driver'),
    path('edit_account/', edit_account, name='edit_account'),
    path('mini_statements/', mini_statements, name='mini_statements'),
    path('toggle_availability/', toggle_availability, name='toggle_availability'),
]
