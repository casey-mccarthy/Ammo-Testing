
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    trip = Trip.objects.first()
    car_weight = trip.get_vehicle_weight()
    car_fuel = trip.get_vehicle_fuel()
    
    context = {
        'trip' : trip
    }

    return render(request, 'exercise/home.html', context=context)