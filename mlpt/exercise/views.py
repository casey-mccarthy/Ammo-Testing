
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    trip = Trip.objects.get_vehicle_weight(trip=2)["total_weight"]
    print(trip)
    quantities = Trip.objects.get_vehicle_quantity(trip=2)
    print(quantities)
    context = {
        'trip' : trip
    }

    return render(request, 'exercise/home.html', context=context)