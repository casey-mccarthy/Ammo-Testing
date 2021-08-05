
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    weight = Trip.objects.get_vehicle_weight(trip=2)
    print(weight)

    quantities = Trip.objects.get_vehicle_quantity(trip=2)
    print(quantities)

    fuel = Trip.objects.get_vehicle_bingo_fuel(trip=2)
    print(fuel)

    vehicle_parts = Trip.objects.get_vehicle_parts_count(trip=2)
    print(vehicle_parts)

    context = {
        'weight' : weight,
        'quantities' : quantities,
        'fuel' : fuel,
        'vehicle_parts' : vehicle_parts,
    }

    return render(request, 'exercise/home.html', context=context)