
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
    context = {
        'weight' : weight,
        'quantities' : quantities,
        'fuel' : fuel,
    }

    return render(request, 'exercise/home.html', context=context)